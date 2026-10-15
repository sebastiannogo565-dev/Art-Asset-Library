"""Native reopen, invariant mesh fingerprints, new cavities, and true FBX reimport."""
import bpy,bmesh,json,hashlib,array,math
from pathlib import Path
from mathutils import Vector
O=Path(__file__).parent;P='SL_BLD_C01_MAIN_01_TRIAL_01_REV_01'
def read(n):return json.loads((O/n).read_text(encoding='utf-8'))
def write(n,v):(O/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
L=read('LAYOUT.json');scope=read('CHANGE_SCOPE.json');G=read('GEOMETRY.json')
bpy.ops.wm.open_mainfile(filepath=str(O/(P+'.blend')))
obs=[o for o in bpy.data.collections['WHOLE'].all_objects if o.type=='MESH']
def bbox(obs):
 co=[o.matrix_world@Vector(v) for o in obs for v in o.bound_box];return [[min(v[i] for v in co) for i in range(3)],[max(v[i] for v in co) for i in range(3)]]
def meshhash(me):
 h=hashlib.sha256()
 def add(seq,prop,typ,n):
  a=array.array(typ,[0])*n;seq.foreach_get(prop,a);h.update(a.tobytes())
 add(me.vertices,'co','f',len(me.vertices)*3);add(me.loops,'vertex_index','i',len(me.loops))
 for uv in me.uv_layers:add(uv.data,'uv','f',len(uv.data)*2)
 h.update('|'.join(m.name for m in me.materials if m).encode());return h.hexdigest()
cache={};bad=[]
for n,expected in scope['unaffected_fingerprints'].items():
 o=bpy.data.objects[n]
 if o.data not in cache:cache[o.data]=meshhash(o.data)
 actual=dict(mesh=cache[o.data],matrix=[float(x) for row in o.matrix_world for x in row],group=o.get('group'),materials=[m.name for m in o.data.materials])
 if expected!=actual:bad.append(n)
assert not bad,bad
top=[];density=[];missing=[]
for me in set(o.data for o in obs):
 bm=bmesh.new();bm.from_mesh(me);top.append(dict(mesh=me.name,zero_area=sum(f.calc_area()<1e-10 for f in bm.faces),nonmanifold=sum(not e.is_manifold for e in bm.edges)));bm.free()
 uv=me.uv_layers.active
 if not uv or len(uv.data)!=len(me.loops):missing.append(me.name);continue
 for p in me.polygons:
  if p.area<.0001:continue
  pts=[uv.data[i].uv for i in p.loop_indices];area=abs(sum(pts[i].x*pts[(i+1)%len(pts)].y-pts[(i+1)%len(pts)].x*pts[i].y for i in range(len(pts)))/2)
  density.append(256*math.sqrt(area/p.area))
print('TOPOLOGY_DIAGNOSTIC',missing,[x for x in top if x['zero_area'] or x['nonmanifold']],flush=True)
assert not missing and not sum(x['zero_area']+x['nonmanifold'] for x in top)
# Native rays into each of 900 actual cells; no drawer/slider can occlude the front.
cells=[]
for b in L['shoe']['banks']:
 o=bpy.data.objects['LOCKER_'+b['id']];x,y,z,X,Y,Z=b['bounds'];axis=b['axis'];faces=[-1,1] if b['faces']==2 else [1]
 for face in faces:
  for col in range(b['columns']):
   for row in range(b['rows']):
    u=.3*(col+.5);h=.3*row+.14
    if axis=='X':a=Vector((x+u,y-.02 if face<0 else Y+.02,h));d=Vector((0,-face,0))
    else:a=Vector((x-.02 if face<0 else X+.02,y+u,h));d=Vector((-face,0,0))
    hit,loc,no,idx=o.ray_cast(a,d,distance=b['depth']+.1)
    depth=(loc-a).length-.02 if hit else -1
    assert hit and depth>=b['cavity'][1]-.00001,(b['id'],col,row,face,depth)
    cells.append(dict(bank=b['id'],column=col+1,row=row+1,face=face,ray_cavity_depth=depth))
assert len(cells)==900
def areas(objects):
 r={}
 for o in objects:
  for p in o.data.polygons:
   n=o.data.materials[p.material_index].name;r[n]=r.get(n,0)+p.area
 return r
sa=areas(obs);sb=bbox(obs);names=set(o.name for o in obs);groups={o.name:o.get('group') for o in obs}
charsha=hashlib.sha256(Path(G['character']['source']).read_bytes()).hexdigest()
images=[dict(name=im.name,sha256=hashlib.sha256(im.packed_file.data).hexdigest(),packed=True) for im in bpy.data.images if im.packed_file]
assert any(im['sha256']==charsha for im in images)
source=dict(sha256=hashlib.sha256((O/(P+'.blend')).read_bytes()).hexdigest(),objects=len(obs),unique_meshes=len(set(o.data for o in obs)),bbox=sb,
 unchanged_objects_checked=len(scope['unaffected_fingerprints']),unexpected_changes=bad,missing_uv=missing,zero_area=sum(x['zero_area'] for x in top),nonmanifold=sum(x['nonmanifold'] for x in top),
 density_m2_threshold=.0001,density_px_per_m=[min(density),max(density)],new_mesh_topology=[x for x in top if x['mesh'].startswith('LOCKER_REV_') or x['mesh'].startswith('F2_W4_CHAIR_5_5')],
 real_cavity_rays=len(cells),cells=cells,packed_images=images,character_sha256=charsha,default_check_hidden=bpy.data.collections['REVISION_CHECK_ONLY_NO_EXPORT'].hide_render,
 actual_westlink_door='OPEN_F1_LW_D geometry/UV/material/matrix fingerprint identical to original; net1.4m;2.4 is check-only',
 material_areas=sa,triangles=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in obs))
write('SOURCE_CHECK.json',source)
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.fbx(filepath=str(O/(P+'.fbx')))
imp=[o for o in bpy.context.scene.objects if o.type=='MESH'];ib=bbox(imp);ia=areas(imp)
missing_names=sorted(names-set(o.name for o in imp));extra_names=sorted(set(o.name for o in imp)-names)
uvbad=[o.name for o in imp if not o.data.uv_layers.active or len(o.data.uv_layers.active.data)!=len(o.data.loops)]
groupbad=[o.name for o in imp if o.get('group')!=groups.get(o.name)]
bounderr=max(abs(sb[i][j]-ib[i][j]) for i in range(2) for j in range(3));areaerr=max(abs(v-ia.get(k,0)) for k,v in sa.items())
imagepaths=[dict(name=im.name,path=im.filepath,exists=Path(bpy.path.abspath(im.filepath)).exists()) for im in bpy.data.images if im.source=='FILE']
result=dict(fbx_sha256=hashlib.sha256((O/(P+'.fbx')).read_bytes()).hexdigest(),source_blend_sha256=source['sha256'],objects=len(imp),bbox=ib,missing_names=missing_names,extra_names=extra_names,missing_uv=uvbad,group_mismatch=groupbad,bbox_error_m=bounderr,material_area_max_error_m2=areaerr,imagepaths=imagepaths,
 no_check_geometry=not extra_names,scope='real FBX import in empty Blender, not UE import, collisions/navigation/gameplay unverified')
assert len(imp)==len(names) and not(missing_names or extra_names or uvbad or groupbad) and bounderr<.0001 and areaerr<.1,result
assert all(x['exists'] for x in imagepaths),imagepaths
write('FBX_CHECK.json',result);print('SOURCE_AND_FBX_CHECKED',source['objects'],len(cells),source['density_px_per_m'],bounderr,areaerr,flush=True)
