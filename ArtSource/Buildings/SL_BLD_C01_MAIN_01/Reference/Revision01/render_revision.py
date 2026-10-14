"""Load reproducible parent rendering setup read-only; never save the parent .blend."""
from pathlib import Path
import bpy,json,copy,hashlib,math
OUT=Path(__file__).parent;BASE=OUT.parent
OLD='SL_BLD_C01_MAIN_01_REFERENCE_01';PREFIX=OLD+'_REV_01'
setup=(BASE/'render_reference.py').read_text(encoding='utf-8').split("source_only='--source-only'")[0]
setup=setup.replace("PREFIX='SL_BLD_C01_MAIN_01_REFERENCE_01'","PREFIX='SL_BLD_C01_MAIN_01_REFERENCE_01_REV_01'")
ownership={'clipped_faces':0,'input_faces':0,'position_changes':0}
def owned_assemble(name,parts):
 """Give overlapping coplanar OUTER surfaces one material owner, preserve solid union.
 No primitive bounds, silhouette, opening, light or shadow-visibility changes.
 """
 from mathutils import Vector
 faces=[];planes={};buckets={}
 rank={'ENTRY_WOOD':100,'ENTRY_FRAME':90,'FRAME':80,'BAND_REV':70,'WOOD':50,'GLASS':20,'WALL':0}
 for p in parts:
  key=(p['group'],p['material']);buckets.setdefault(key,[[],[],[]])[2].append(p['id'])
  if p['type']=='mesh':
   faces.extend((p['group'],p['material'],[p['vertices'][i] for i in f]) for f in p['faces']);continue
  verts,ff=cubegeo(p['bounds'])
  for f in ff:
   pts=[verts[i] for i in f]
   axis=next(i for i in range(3) if max(v[i] for v in pts)-min(v[i] for v in pts)<1e-8)
   n=(Vector(pts[1])-Vector(pts[0])).cross(Vector(pts[2])-Vector(pts[0]))[axis]
   n=1 if n>0 else -1;uv=[i for i in range(3) if i!=axis]
   rect=[min(v[uv[0]] for v in pts),min(v[uv[1]] for v in pts),max(v[uv[0]] for v in pts),max(v[uv[1]] for v in pts)]
   planes.setdefault((axis,round(pts[0][axis],8),n),[]).append((rank.get(p['material'],40),p['group'],p['material'],rect))
 def subtract(a,b):
  x0=max(a[0],b[0]);y0=max(a[1],b[1]);x1=min(a[2],b[2]);y1=min(a[3],b[3])
  if x1-x0<1e-8 or y1-y0<1e-8:return [a]
  out=[]
  for q in [[a[0],a[1],x0,a[3]],[x1,a[1],a[2],a[3]],[x0,a[1],x1,y0],[x0,y1,x1,a[3]]]:
   if q[2]-q[0]>1e-8 and q[3]-q[1]>1e-8:out.append(q)
  ownership['clipped_faces']+=1;return out
 for (axis,coord,n),items in planes.items():
  owned=[];uv=[i for i in range(3) if i!=axis]
  for priority,group,mat,r in sorted(items,key=lambda q:q[0],reverse=True):
   ownership['input_faces']+=1;pieces=[r]
   for prev in owned:
    pieces=[q for piece in pieces for q in subtract(piece,prev)]
    if not pieces:break
   owned+=pieces
   for q in pieces:
    pts=[]
    for u,v in [(q[0],q[1]),(q[2],q[1]),(q[2],q[3]),(q[0],q[3])]:
     p=[0,0,0];p[axis]=coord;p[uv[0]]=u;p[uv[1]]=v;pts.append(p)
    cross=(Vector(pts[1])-Vector(pts[0])).cross(Vector(pts[2])-Vector(pts[0]))[axis]
    if cross*n<0:pts.reverse()
    faces.append((group,mat,pts))
 for group,mat,pts in faces:
  vv,ff,ids=buckets[(group,mat)];off=len(vv);vv.extend(pts);ff.append(list(range(off,off+len(pts))))
 result=[]
 for (group,mat),(v,f,ids) in buckets.items():
  me=bpy.data.meshes.new(name+'_'+group+'_'+mat);me.from_pydata(v,[],f);me.update()
  ob=bpy.data.objects.new(me.name,me);collection(name+'__'+group).objects.link(ob);ob.data.materials.append(M[mat])
  ob['source_ids']=json.dumps(ids);ob['scope']='REFERENCE ONLY; coplanar material ownership; unchanged primitive bounds'
  result.append(ob)
 return result
setup=setup.replace('full=assemble(','full=owned_assemble(').replace('details[name]=assemble(','details[name]=owned_assemble(')
exec(compile(setup,str(BASE/'render_reference.py'),'exec'),globals())
original=json.loads((BASE/(OLD+'_GEOMETRY.json')).read_text(encoding='utf-8'))
changes={v['id']:v['new'] for v in G['material_changes']}
control_parts=copy.deepcopy(original['primitives'])
for p in control_parts:p['material']=changes.get(p['id'],p['material'])
control=owned_assemble('ENTRY_COLOR_CONTROL_ORIGINAL_GEOMETRY',control_parts)
gate=owned_assemble('CUT_SHOES_GATE',[p for p in G['primitives'] if p['id'].startswith('F1_WL_N_REV')])
details['SHOES']+=gate
r=[41,12.7,4,49.4,21.7,7.4]
pulled=[copy.deepcopy(p) for p in G['primitives'] if roi(p,r) and not 'CEILING' in p['group']
        and not p['group'].startswith(('ROOF','SLAB')) and not p['group'].endswith('_WALLS')]
for p in pulled:
 if p['id'].startswith('C30_') and '_CHAIR' in p['id']:p['bounds'][0]+=.25;p['bounds'][3]+=.25
pulled+=[dict(id='CLASS_PULL_FLOOR',type='box',bounds=[41,12.7,3.8,49.4,21.7,4],material='FLOOR',group='CUTAWAY'),
 dict(id='CLASS_PULL_W',type='box',bounds=[40.8,12.7,4,41,21.7,6.9],material='WALL',group='CUTAWAY')]
details['CLASS_PULLED']=owned_assemble('CUT_CLASS_PULLED',pulled)
def show(obs):
 for ob in full+grounds+control+sum(details.values(),[]):ob.hide_render=ob not in obs
def render(name,target,az,el,scale,obs):
 show(obs);camera(target,az,el,scale)
 scene.render.filepath=str(OUT/(PREFIX+'_'+name+'.png'));bpy.ops.render.render(write_still=True)
 print('REV_RENDER_DONE',name,flush=True)
render('ENTRY_AFTER',[25,3,2],240,18,22,control+grounds)
render('ENTRY_CURRENT',[25,3,2],240,18,22,full+grounds)
render('CLASS',[45.2,17.2,4.8],45,50,13,details['CLASS'])
render('CLASS_PULLED',[45.2,17.2,4.8],45,50,13,details['CLASS_PULLED'])
render('SHOES',[24,4.5,.7],270,55,16,details['SHOES'])
render('A',[75,14,5.5],225,30,149,full+grounds)
render('B',[75,14,5.5],45,30,149,full+grounds)
show(full+grounds);camera([75,14,5.5],225,30,149)
for ob in full+grounds+control+sum(details.values(),[]):ob.hide_viewport=ob not in full+grounds
scene['geometry_sha256']=hashlib.sha256((OUT/(PREFIX+'_GEOMETRY.json')).read_bytes()).hexdigest()
scene['scope']='REFERENCE_REV01 only, no formal asset/UV/UE; control original geometry used for material-only comparison'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/(PREFIX+'_REFERENCE_ONLY.blend')))
maxz=max((max(v[2] for v in p['vertices']) if p['type']=='mesh' else p['bounds'][5]) for p in G['primitives'])
report={'date':'2026-10-15','blender':bpy.app.version_string,'geometry_sha256':scene['geometry_sha256'],
 'source_primitives':len(G['primitives']),'native_previews':[2304,1296],'rendered':['ENTRY_AFTER','ENTRY_CURRENT','CLASS','CLASS_PULLED','SHOES','A','B'],
 'highest_actual':maxz,'entry_original_before':{'path':str(BASE/'Preview_ENTRY.png'),'sha256':hashlib.sha256((BASE/'Preview_ENTRY.png').read_bytes()).hexdigest()},
 'entry_control_geometry_unchanged':all(all(p[k]==q[k] for k in p if k!='material') for p,q in zip(control_parts,original['primitives'])),
 'entry_camera':{'target':[25,3,2],'azimuth':240,'elevation':18,'ortho_scale':22},
 'lighting':{'sun_energy':2.5,'sun_angle_degrees':5,'sun_rotation_degrees':[30,-20,-35],'world_strength':.6,
  'exposure':scene.view_settings.exposure,'gamma':scene.view_settings.gamma,'view_transform':scene.view_settings.view_transform,'look':scene.view_settings.look},
 'material_render_policy':'color IDs + one-owner coplanar surface clipping, unchanged solid-union boundary/primitive positions. No emission, no shadow-ray visibility change.',
 'coplanar_surface_ownership':ownership,
 'saved_view':'WHOLE+CONTEXT only; all cutaway/control duplicates hidden',
 'formal_asset':False,'UV':False,'UE':False}
(OUT/'BLENDER_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
