"""Independent factory Blender process. Never saves host, design or SchoolLife.
Assembly SVG/PNG must already exist. One editable 11-component plaque source set.
"""
from pathlib import Path
import bpy,bmesh,json,math,hashlib,time,traceback
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parent.parent
LIB=ROOT.parents[3];CACHE=LIB/'.cache/sign-plate-trial01'
DATA=json.loads((ROOT/'Source/SL_GE_SIGN_PLATE_01_TRIAL_GEOMETRY_UV.json').read_text(encoding='utf-8'))
def progress(stage,**kw):(CACHE/'build_progress.json').write_text(json.dumps({'stage':stage,'time':time.time(),**kw}),encoding='utf-8')
def stats(o):
 bpy.context.view_layer.update();v=[o.matrix_world@q.co for q in o.data.vertices]
 bm=bmesh.new();bm.from_mesh(o.data)
 d={'name':o.name,'bounds_m':{'min':[min(p[k] for p in v) for k in range(3)],'max':[max(p[k] for p in v) for k in range(3)]},
    'origin_m':list(o.location),'scale':list(o.scale),'vertices':len(o.data.vertices),'edges':len(o.data.edges),
    'polygons':len(o.data.polygons),'triangles':sum(len(p.vertices)-2 for p in o.data.polygons),
    'non_manifold_edges':sum(not e.is_manifold for e in bm.edges),'zero_area_faces':sum(f.calc_area()<1e-13 for f in bm.faces),
    'signed_volume_m3':bm.calc_volume(signed=True),'material_slots':len(o.data.materials)}
 bm.free();return d
def bounds(objs):
 ss=[stats(o) for o in objs]
 return {'min':[min(s['bounds_m']['min'][k] for s in ss) for k in range(3)],'max':[max(s['bounds_m']['max'][k] for s in ss) for k in range(3)]}
def material(name,color,roughness=.85):
 m=bpy.data.materials.new(name);m.use_nodes=True;m.diffuse_color=(*color,1)
 bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=roughness
 return m
def collection(scene,name):
 c=bpy.data.collections.new(name);scene.collection.children.link(c);return c
def camera(scene,col,name,pos,target,scale):
 d=bpy.data.cameras.new(name);d.type='ORTHO';d.ortho_scale=scale;d.clip_start=.01;d.clip_end=200
 o=bpy.data.objects.new(name,d);col.objects.link(o);o.location=pos;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();return o
def daylight(scene):
 scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1;scene.unit_settings.length_unit='METERS'
 scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=48;scene.cycles.use_denoising=True
 scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB';scene.render.film_transparent=False
 scene.view_settings.view_transform='Standard';scene.view_settings.exposure=0;scene.view_settings.gamma=1
 w=bpy.data.worlds.new(scene.name+'_WORLD');w.use_nodes=True;w.node_tree.nodes['Background'].inputs['Color'].default_value=(.65,.68,.72,1);w.node_tree.nodes['Background'].inputs['Strength'].default_value=.45;scene.world=w
 c=collection(scene,scene.name+'_LIGHTS_CAMERAS');d=bpy.data.lights.new(scene.name+'_SUN','SUN');d.energy=1.8;d.angle=math.radians(5)
 o=bpy.data.objects.new(d.name,d);c.objects.link(o);o.rotation_euler=Vector((.5,.6,-1)).to_track_quat('-Z','Y').to_euler();return c
def floor(scene,z):
 c=collection(scene,scene.name+'_REFERENCE_FLOOR');m=bpy.data.meshes.new(c.name)
 m.from_pydata([(-50,-50,z),(50,-50,z),(50,50,z),(-50,50,z)],[],[(0,1,2,3)]);m.update()
 o=bpy.data.objects.new(c.name,m);c.objects.link(o);m.materials.append(material(c.name,(.64,.66,.63),.92));o['preview_only']=True;return c
def render(scene,cam,name,width,height):
 bpy.context.window.scene=scene;scene.camera=cam;scene.render.resolution_x=width;scene.render.resolution_y=height
 scene.render.filepath=str(ROOT/'Previews/Renders'/name);progress('render_'+name);bpy.ops.render.render(write_still=True)
def workbench(scene):
 scene.render.engine='BLENDER_WORKBENCH';scene.display.shading.light='STUDIO';scene.display.shading.color_type='MATERIAL'
 scene.display.shading.show_shadows=True;scene.display.shading.show_cavity=True;scene.display.shading.background_type='WORLD';scene.world.color=(.93,.94,.92)
def density(o):
 values=[];uv=o.data.uv_layers.active.data
 for f in o.data.polygons:
  li=list(f.loop_indices);vv=[o.data.vertices[o.data.loops[i].vertex_index].co for i in li];pp=[uv[i].uv*256 for i in li]
  for k in range(1,len(li)-1):
   a=.5*(vv[k]-vv[0]).cross(vv[k+1]-vv[0]).length
   b=pp[k]-pp[0];c=pp[k+1]-pp[0];t=.5*abs(b.x*c.y-b.y*c.x)
   # Ngons can include collinear edge subdivisions; Blender tessellation is authoritative below.
   if a>1e-12 and t>1e-10:values.append(math.sqrt(t/a))
 return values
try:
 progress('starting');assert not bpy.data.filepath
 assert (ROOT/'Source/SL_GE_SIGN_PLATE_01_TRIAL_ASSEMBLY.png').exists(),'Assembly first'
 for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
 source=bpy.context.scene;source.name='SOURCE_PLAQUE_TRIAL01'
 asset=collection(source,'ASSET_SOURCE_ONLY_ONE_SET');rig=daylight(source);ground=floor(source,-.42)
 mat=material('M_SL_SIGN_TRIAL_COATED_METAL',(96/255,118/255,122/255));bs=mat.node_tree.nodes.get('Principled BSDF')
 bs.inputs['Metallic'].default_value=0;bs.inputs['IOR'].default_value=1.45
 images=[]
 for name,color,socket in [('BaseColor','sRGB','Base Color'),('Roughness','Non-Color','Roughness')]:
  im=bpy.data.images.load(str(ROOT/f'Textures/SL_GE_SIGN_PLATE_01_TRIAL_{name}.png'));im.name='SIGN_TRIAL_'+name;im.colorspace_settings.name=color
  n=mat.node_tree.nodes.new('ShaderNodeTexImage');n.image=im;n.interpolation='Closest';n.extension='EXTEND';mat.node_tree.links.new(n.outputs['Color'],bs.inputs[socket]);im.pack();im.filepath='//../Textures/'+Path(im.filepath).name;images.append(im)
 objs=[]
 for p in DATA['parts']:
  m=bpy.data.meshes.new(p['name']+'_MESH');m.from_pydata(p['vertices'],[],p['faces']);m.update();assert not m.validate(verbose=False,clean_customdata=False)
  uv=m.uv_layers.new(name='UVMap_64px_per_m')
  for f,coords in zip(m.polygons,p['face_uvs']):
   for li,q in zip(f.loop_indices,coords):uv.data[li].uv=q
  # Blender recalculates actual outward winding; custom UV data remains attached to the corners.
  bm=bmesh.new();bm.from_mesh(m);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(m);bm.free();m.update();m.materials.append(mat)
  o=bpy.data.objects.new(p['name'],m);asset.objects.link(o);o['asset_id']='SL_GE_SIGN_PLATE_01';o['part_role']=p['role'];o['shared_pivot']='rear_contact_datum_center';o['stage']='TRIAL_01_NOT_FINAL';objs.append(o)
 bpy.context.view_layer.update()
 measured=[stats(o) for o in objs]
 for s in measured:assert s['non_manifold_edges']==0 and s['zero_area_faces']==0 and s['signed_volume_m3']>0,s
 allbounds=bounds(objs)
 for k in range(3):
  assert abs(allbounds['min'][k]-DATA['overall_bounds_m']['min'][k])<1e-7
  assert abs(allbounds['max'][k]-DATA['overall_bounds_m']['max'][k])<1e-7
 dens=[d for o in objs for d in density(o)];assert max(abs(d-64) for d in dens)<.05
 # Independent assembly motion scene, fixed and moving pieces are visibly distinguishable.
 exploded=bpy.data.scenes.new('INSPECTION_ONLY_EXPLODED_NOT_INSTALL_VISIBILITY');er=daylight(exploded);ec=collection(exploded,'INSPECTION_COPIES_NO_EXPORT')
 for o in objs:
  q=bpy.data.objects.new('EXPLODED_'+o.name,o.data);ec.objects.link(q);q.location=(.20 if o.name in DATA['assembly']['fixed_parts'] else -.20,0,0)
 explodedcam=camera(exploded,er,'EXPLODED_REAR',(.9,3,1.0),(0,0,0),1.05)
 # Load one accepted native host mesh and its packed materials, READ ONLY.
 installed=bpy.data.scenes.new('INSTALLED_OPAQUE_HOST_DAYLIGHT');ir=daylight(installed);floor(installed,8)
 refs=collection(installed,'READONLY_HOST_ORIGINAL_REFERENCE');instances=collection(installed,'PLAQUE_ONE_INSTALLED_SET')
 hostpath=LIB/'ArtSource/SchoolGate/SL_GE_GATE_PIER_01/Trial01/Source/SL_GE_GATE_PIER_01_TRIAL_01.blend'
 with bpy.data.libraries.load(str(hostpath),link=False) as (src,dst):dst.objects=['SM_SL_GE_GATE_PIER_01']
 host=dst.objects[0];refs.objects.link(host);host.name='READONLY_ACCEPTED_PIER_LEFT';host.location=(-3.3,0,8);host['read_only_copy']=str(hostpath)
 inst=[]
 for o in objs:
  q=bpy.data.objects.new('INSTALLED_'+o.name,o.data);q.location=(-3.3,-.27,9.4);instances.objects.link(q);inst.append(q)
 charpath=Path('D:/UE project/SchoolLife/ArtSource/Characters/StudentChibi/FrontIdle/StudentChibi_Front_Idle.png')
 ci=bpy.data.images.load(str(charpath));ci.name='REFERENCE_ORIGINAL_128_RGBA_SIGN';ci.pack()
 assert hashlib.sha256(bytes(ci.packed_file.data)).hexdigest()=='082ceb410d904f0037dfe09dd3502e50195351691ab4047cc5dbbb639147b8cd'
 cm=bpy.data.materials.new('SCALE_REFERENCE_ONLY_ORIGINAL_IMAGE');cm.use_nodes=True;n=cm.node_tree.nodes;n.clear();l=cm.node_tree.links
 output=n.new('ShaderNodeOutputMaterial');mix=n.new('ShaderNodeMixShader');transparent=n.new('ShaderNodeBsdfTransparent');emission=n.new('ShaderNodeEmission');emission.inputs['Strength'].default_value=1
 texture=n.new('ShaderNodeTexImage');texture.image=ci;texture.interpolation='Closest';texture.extension='CLIP'
 l.new(texture.outputs['Color'],emission.inputs['Color']);l.new(texture.outputs['Alpha'],mix.inputs[0]);l.new(transparent.outputs[0],mix.inputs[1]);l.new(emission.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],output.inputs['Surface'])
 cmesh=bpy.data.meshes.new('REFERENCE_ORIGINAL_CHARACTER_BOARD');cmesh.from_pydata([(0,0,0)]*4,[],[(0,1,2,3)]);cmesh.update();cu=cmesh.uv_layers.new(name='ORIGINAL_UV')
 for i,q in enumerate([(0,0),(1,0),(1,1),(0,1)]):cu.data[i].uv=q
 cmesh.materials.append(cm);co=bpy.data.objects.new('REFERENCE_ONLY_CHARACTER_VISIBLE_180_CAPSULE_192',cmesh);refs.objects.link(co)
 co.visible_shadow=False;co.visible_diffuse=False;co.visible_glossy=False
 def character(az):
  a=math.radians(az);r=Vector((-math.sin(a),math.cos(a),0));anchor=Vector((-4.9,0,8));h=1.8*128/116
  for v,(u,z) in zip(cmesh.vertices,[(-64.5/128*h,-8/128*h),(63.5/128*h,-8/128*h),(63.5/128*h,120/128*h),(-64.5/128*h,120/128*h)]):v.co=anchor+r*u+Vector((0,0,z))
  cmesh.update()
 bpy.context.window.scene=installed;bpy.context.view_layer.update()
 ib=bounds(inst);hs=stats(host)
 assert all(abs(a-b)<3e-6 for a,b in zip(ib['min'],[-3.42,-.29,8.98]));assert all(abs(a-b)<3e-6 for a,b in zip(ib['max'],[-3.18,-.27,9.82]))
 pads=[stats(o) for o in inst if '_PAD_' in o.name]
 assert all(abs(s['bounds_m']['max'][1]+.27)<1e-6 for s in pads)
 # Engineering placement check: second host/platform only, never rendered or exported.
 check=collection(installed,'PLACEMENT_CHECK_ONLY_NOT_RENDERED');check.hide_render=True
 right=bpy.data.objects.new('CHECK_RIGHT_ACCEPTED_HOST',host.data);right.location=(3.3,0,8);check.objects.link(right)
 bpy.context.view_layer.update();rightstats=stats(right);clear=rightstats['bounds_m']['min'][0]-hs['bounds_m']['max'][0];assert abs(clear-6)<1e-6
 views={};target=Vector((-3.85,0,9.18));cams={}
 for key,az in [('A',225),('B',45)]:
  a=math.radians(az);e=math.radians(30);pos=target+7*Vector((math.cos(e)*math.cos(a),math.cos(e)*math.sin(a),math.sin(e)))
  cam=camera(installed,ir,'INSTALL_'+key,pos,target,4.6);cams[key]=cam
  character(az);bpy.context.view_layer.update();installed.camera=cam
  installed.render.resolution_x=1600;installed.render.resolution_y=1400
  pts={}
  for h in [0,1.8,1.92]:
   q=world_to_camera_view(installed,cam,Vector((-4.9,0,8+h)));pts[str(h)]=[q.x*1600,(1-q.y)*1400]
  views[key]={'azimuth_deg':az,'elevation_deg':30,'host_opaque':True,'native_px':[1600,1400],'ortho_scale_m':4.6,'camera_m':list(cam.location),'target_m':list(target),'character_reference_points_px':pts,'same_source_meshes':True}
  # Actual ray visibility to source front patch through the opaque host.
  dg=bpy.context.evaluated_depsgraph_get();hits=[]
  for x in [-.10,0,.10]:
   for z in [-.38,0,.38]:
    p=Vector((-3.3+x,-.29001,9.4+z));direction=(p-cam.location).normalized();hit,loc,n,idx,ob,m=installed.ray_cast(dg,cam.location,direction,distance=(p-cam.location).length+.001)
    hits.append({'front_sample_m':list(p),'first_hit':ob.name if hit else None})
  views[key]['front_patch_ray_first_hits']=hits
  render(installed,cam,f'SL_GE_SIGN_PLATE_01_TRIAL_INSTALL_{key}_RENDER.png',1600,1400)
 bpy.context.window.scene=source;bpy.context.view_layer.update()
 closecam=camera(source,rig,'SINGLE_PLAQUE_DAYLIGHT_FRONT',(0,-3,.3),(0,0,0),.98)
 render(source,closecam,'SL_GE_SIGN_PLATE_01_TRIAL_COATING_RENDER.png',700,1100)
 # Actual orthogonal geometry checks, never redraw geometry into differing views.
 ground.hide_render=True;workbench(source)
 for key,direction,w,h,scale in [('FRONT',(0,-1,0),480,800,.96),('REAR',(0,1,0),480,800,.96),('EAST',(1,0,0),360,800,.96),('TOP',(0,0,1),600,240,.32)]:
  cam=camera(source,rig,'CHECK_'+key,Vector(direction)*3,(0,0,0),scale);render(source,cam,'CHECK_'+key+'.png',w,h)
 workbench(exploded);render(exploded,explodedcam,'CHECK_EXPLODED_REAR.png',850,1050)
 # Save source scene with all components selected and installed preview scene retained separately.
 bpy.context.window.scene=source;source.render.engine='CYCLES';ground.hide_render=False;source.camera=closecam;source.render.resolution_x=700;source.render.resolution_y=1100
 for o in source.objects:o.select_set(False)
 for o in objs:o.select_set(True)
 bpy.context.view_layer.objects.active=objs[0]
 character(225);installed.camera=cams['A']
 # Refresh actual serialized corners after outward normal correction.
 for p,o in zip(DATA['parts'],objs):
  p['vertices']=[list(v.co) for v in o.data.vertices];p['faces']=[list(f.vertices) for f in o.data.polygons];uv=o.data.uv_layers.active.data
  p['face_uvs']=[[list(uv[li].uv) for li in f.loop_indices] for f in o.data.polygons];p['actual_measurements']=stats(o)
 DATA['actual_source_bounds_m']=allbounds;DATA['actual_source_component_count']=len(objs);DATA['actual_uv_density_px_per_m']={'min':min(dens),'max':max(dens),'mean':sum(dens)/len(dens)}
 (ROOT/'Source/SL_GE_SIGN_PLATE_01_TRIAL_GEOMETRY_UV.json').write_text(json.dumps(DATA,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
 blend=ROOT/'Source/SL_GE_SIGN_PLATE_01_TRIAL_01.blend';bpy.ops.wm.save_as_mainfile(filepath=str(blend))
 opts={'use_selection':True,'object_types':{'MESH'},'global_scale':1.0,'apply_unit_scale':True,'apply_scale_options':'FBX_SCALE_UNITS','axis_forward':'-Y','axis_up':'Z','bake_space_transform':False,'use_mesh_modifiers':True,'mesh_smooth_type':'OFF','use_triangles':True,'bake_anim':False,'path_mode':'RELATIVE','embed_textures':False,'use_custom_props':True}
 bpy.ops.export_scene.fbx(filepath=str(ROOT/'Exports/SL_GE_SIGN_PLATE_01_TRIAL_01.fbx'),**opts)
 report={'blender_version':bpy.app.version_string,'source_count':1,'component_count':len(objs),'parts':measured,'source_bounds_m':allbounds,
  'total_vertices':sum(s['vertices'] for s in measured),'total_polygons':sum(s['polygons'] for s in measured),'total_triangles':sum(s['triangles'] for s in measured),
  'installed':{'one_target_set':True,'pivot_engineering_m':[-3.3,-.27,9.4],'bounds_m':ib,'contact_pads':pads,'host':hs,'right_host':rightstats,'minimum_opening_m':clear,'road_width_reference_m':5,'platform_top_reference_m':8},
  'views':views,'original_character_packed_sha256':hashlib.sha256(bytes(ci.packed_file.data)).hexdigest(),
  'daylight':{'engine':'CYCLES_CPU','samples':48,'sun_energy':1.8,'sun_angle_deg':5,'incoming_sun_direction':[.5,.6,-1],'world_strength':.45,'world_color':[.65,.68,.72],'view_transform':'Standard','film_transparent':False},
  'export':{k:sorted(v) if isinstance(v,set) else v for k,v in opts.items()},'assembly_supplement_existed_before_mesh':True,'UE_imports':0}
 (ROOT/'Source/blender_measurements.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
 progress('complete',vertices=report['total_vertices'],triangles=report['total_triangles'])
except Exception:
 progress('failed',error=traceback.format_exc());raise
