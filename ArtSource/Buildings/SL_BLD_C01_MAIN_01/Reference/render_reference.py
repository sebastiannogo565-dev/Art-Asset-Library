"""Fresh Blender background only: editable reference blockout, no UV/exports/UE."""
import bpy,json,math,sys,hashlib
from pathlib import Path
from mathutils import Vector
OUT=Path(__file__).parent;PREFIX='SL_BLD_C01_MAIN_01_REFERENCE_01'
G=json.loads((OUT/(PREFIX+'_GEOMETRY.json')).read_text(encoding='utf-8'))
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene
scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene.render.engine='CYCLES';scene.cycles.samples=24
scene.cycles.use_denoising=True
scene.render.resolution_x=2304;scene.render.resolution_y=1296;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB'
scene.view_settings.view_transform='AgX'
scene.world=bpy.data.worlds.new('REFERENCE_DAYLIGHT');scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.72,.82,1,1)
scene.world.node_tree.nodes['Background'].inputs[1].default_value=.6
M={}
for name,h in G['materials'].items():
 col=tuple(int(h[i:i+2],16)/255 for i in (1,3,5))
 # convert hex sRGB to linear; shaders reflect natural illumination only
 col=tuple(x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in col)
 m=bpy.data.materials.new('REF_'+name);m.diffuse_color=(*col,1);m.use_nodes=True
 node=m.node_tree.nodes.get('Principled BSDF');node.inputs['Base Color'].default_value=(*col,1)
 node.inputs['Roughness'].default_value=.75 if name not in ('GLASS','SKYLIGHT') else .22
 if name in ('GLASS','SKYLIGHT'):
  node.inputs['Transmission Weight'].default_value=.65;node.inputs['IOR'].default_value=1.45
 # Flat design colours only. Pixel-density studies are independent SVG samples.
 M[name]=m
def cubegeo(b):
 a,c,e,d,f,h=b
 return [[a,c,e],[d,c,e],[d,f,e],[a,f,e],[a,c,h],[d,c,h],[d,f,h],[a,f,h]],[[0,3,2,1],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7],[4,5,6,7]]
collections={}
def collection(name):
 if name not in collections:
  co=bpy.data.collections.new(name);scene.collection.children.link(co);collections[name]=co
 return collections[name]
def assemble(name,parts):
 buckets={}
 for p in parts:
  key=(p['group'],p['material']);buckets.setdefault(key,[[],[],[]])
  verts,faces=cubegeo(p['bounds']) if p['type']=='box' else (p['vertices'],p['faces'])
  v,ff,ids=buckets[key];offset=len(v);v.extend(verts);ff.extend([[i+offset for i in f] for f in faces]);ids.append(p['id'])
 result=[]
 for (group,mat),(v,f,ids) in buckets.items():
  me=bpy.data.meshes.new(name+'_'+group+'_'+mat);me.from_pydata(v,[],f);me.update()
  ob=bpy.data.objects.new(me.name,me);collection(name+'__'+group).objects.link(ob);ob.data.materials.append(M[mat])
  ob['scope']='REFERENCE ONLY; no final UV, refined model or UE';ob['source_ids']=json.dumps(ids);ob['shared_origin']='SW0,0,0'
  result.append(ob)
 return result
full=assemble('WHOLE',G['primitives'])
# Optional context represented only as a simple neutral ground / paving, no campus assets added.
grounds=assemble('CONTEXT',[{'id':'GROUND','type':'box','bounds':[-24,-28,-.30,174,53,-.02],'material':'GROUND','group':'CONTEXT'},
 {'id':'FRONT_PAVE','type':'box','bounds':[0,-6,-.20,150,0,0],'material':'PAVE','group':'CONTEXT'}])
def roi(p,r):
 b=p['bounds'] if p['type']=='box' else [min(v[i] for v in p['vertices']) for i in range(3)]+[max(v[i] for v in p['vertices']) for i in range(3)]
 return all(b[i]>=r[i]-.31 and b[i+3]<=r[i+3]+.31 for i in range(3))
details={}
for name,r in [('CLASS',[41,12.7,4,49.4,21.7,7.4]),('SHOES',[18.3,0,0,29.7,8.8,3.4]),
 ('COURT',[74,15,0,86,24,12.2]),('LINK',[52.3,13,4,63.7,21.7,7.4])]:
 parts=[p for p in G['primitives'] if roi(p,r) and not 'CEILING' in p['group'] and
        not p['group'].startswith(('ROOF','SLAB')) and not p['group'].endswith('_WALLS')]
 # Dedicated floor and rear walls for isolated cutaway only: clearly not another building design.
 a,b,z,c,d,h=r
 parts.append({'id':name+'_CUT_FLOOR','type':'box','bounds':[a,b,z-.2,c,d,z],'material':'FLOOR','group':'CUTAWAY'})
 if name=='CLASS':
  parts.append({'id':name+'_CUT_W','type':'box','bounds':[a-.2,b,z,a,d,z+2.9],'material':'WALL','group':'CUTAWAY'})
 details[name]=assemble('CUT_'+name,parts)
sun_data=bpy.data.lights.new('SUN_REFERENCE','SUN');sun_data.energy=2.5;sun_data.angle=math.radians(5)
sun=bpy.data.objects.new('SUN_REFERENCE',sun_data);scene.collection.objects.link(sun)
sun.rotation_euler=(math.radians(30),math.radians(-20),math.radians(-35))
cam_data=bpy.data.cameras.new('REFERENCE_CAMERA');cam=bpy.data.objects.new('REFERENCE_CAMERA',cam_data);scene.collection.objects.link(cam);scene.camera=cam
cam_data.type='ORTHO'
def camera(target,az,el,scale):
 a=math.radians(az);e=math.radians(el);t=Vector(target)
 cam.location=t+Vector((math.cos(a)*math.cos(e),math.sin(a)*math.cos(e),math.sin(e)))*180
 cam.rotation_euler=(t-cam.location).to_track_quat('-Z','Y').to_euler();cam_data.ortho_scale=scale
def show(obs):
 for ob in full+grounds+sum(details.values(),[]):ob.hide_render=ob not in obs
def render(name,target,az,el,scale,obs):
 show(obs);camera(target,az,el,scale)
 scene.render.filepath=str(OUT/('Preview_'+name+'.png'));bpy.ops.render.render(write_still=True)
 print('C01_RENDER_DONE',name,flush=True)
source_only='--source-only' in sys.argv
if not source_only:
 render('A',[75,14,5.5],225,30,149,full+grounds)
 render('B',[75,14,5.5],45,30,149,full+grounds)
 render('ENTRY',[25,3,2],240,18,22,full+grounds)
 for name,target,az,el,scale in [('CLASS',[45.2,17.2,4.8],45,50,13),
  ('SHOES',[24,4.5,.7],270,55,16),('COURT',[80,19.5,4],240,35,22),('LINK',[58,17.5,4.8],230,45,16)]:
  render(name,target,az,el,scale,details[name])
show(full+grounds);camera([75,14,5.5],225,30,149)
scene['geometry_source']=PREFIX+'_GEOMETRY.json'
scene['geometry_sha256']=hashlib.sha256((OUT/(PREFIX+'_GEOMETRY.json')).read_bytes()).hexdigest()
scene['scope']='One unified editable building reference blockout only. Formal Trial, UV, textures, export, UE not started.'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/(PREFIX+'_REFERENCE_ONLY.blend')))
(OUT/'BLENDER_REPORT.json').write_text(json.dumps({'blender_version':bpy.app.version_string,'render_engine':'Cycles CPU',
 'samples':24,'preview_native':[2304,1296],'geometry_sha256':scene['geometry_sha256'],'rendered':['A','B','ENTRY','CLASS','SHOES','COURT','LINK'],
 'source_primitives':len(G['primitives']),'source_openings':len(G['openings']),'formal_model':False,'final_UV':False,'UE':False,
 'source_only_rebuild':source_only,'source_only_reason':'LF serialization normalization only; prior7renders identical geometry' if source_only else None},indent=2),encoding='utf-8',newline='\n')
