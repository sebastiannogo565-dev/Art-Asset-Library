"""Targeted new-wall/door/bench checks, exact unchanged fingerprints, necessary real FBX reimport."""
import bpy,bmesh,ast,json,hashlib,array,math
from pathlib import Path
from mathutils import Vector
O=Path(__file__).parent;B=O.parent/'Revision01';P='SL_BLD_C01_MAIN_01_TRIAL_01_REV_02'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def write(n,v):(O/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
tree=ast.parse((B/'verify_revision.py').read_text(encoding='utf-8'));exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['meshhash','bbox','areas']],type_ignores=[]),'inherited fingerprint functions','exec'),globals())
scope=read(O/'CHANGE_SCOPE.json');L=read(O/'LAYOUT.json');bpy.ops.wm.open_mainfile(filepath=str(O/(P+'.blend')))
obs=[o for o in list(bpy.data.collections['WHOLE'].all_objects) if o and o.type=='MESH'];cache={};bad=[]
for n,e in scope['unaffected_fingerprints'].items():
 o=bpy.data.objects[n]
 if o.data not in cache:cache[o.data]=meshhash(o.data)
 v=dict(mesh=cache[o.data],matrix=[float(x) for row in o.matrix_world for x in row],group=o.get('group'),materials=[m.name for m in o.data.materials])
 if v!=e:bad.append(n)
assert not bad,bad
changed=[bpy.data.objects[n] for n in scope['changed']+scope['added']];top=[];density=[]
for o in changed:
 me=o.data;bm=bmesh.new();bm.from_mesh(me);q=dict(object=o.name,zero_area=sum(f.calc_area()<1e-10 for f in bm.faces),nonmanifold=sum(not e.is_manifold for e in bm.edges));bm.free();top.append(q)
 uv=me.uv_layers.active;assert uv and len(uv.data)==len(me.loops),o.name
 for poly in me.polygons:
  if poly.area<.0001:continue
  pts=[uv.data[i].uv for i in poly.loop_indices];a=abs(sum(pts[i].x*pts[(i+1)%len(pts)].y-pts[(i+1)%len(pts)].x*pts[i].y for i in range(len(pts)))/2);density.append(256*math.sqrt(a/poly.area))
print('LOCAL_TOPOLOGY',top,flush=True);assert not sum(q['zero_area']+q['nonmanifold'] for q in top),top
doorobjs=[bpy.data.objects[n] for n in ['PARTITIONS_F01_DOOR_BAND','PARTITIONS_F01_HEAD','OPEN_F1_LW_D']]
def hitdist(pos,d):
 a=Vector(pos);direction=Vector(d);dist=[]
 for o in doorobjs:
  inv=o.matrix_world.inverted();ok,p,n,i=o.ray_cast(inv@a,inv.to_3x3()@direction,distance=20)
  if ok:dist.append(((o.matrix_world@p)-a).length)
 return min(dist) if dist else 99
rays=[]
for y in [12.72,12.74,12.82,12.90,12.99]:
 for z in [.1,1.,1.92,2.59]:
  width=hitdist((58,y,z),(-1,0,0))+hitdist((58,y,z),(1,0,0));height=hitdist((58,y,.001),(0,0,1))+.001
  rays.append(dict(y=y,z=z,width_m=width,height_m=height))
minwidth=min(r['width_m'] for r in rays);minheight=min(r['height_m'] for r in rays)
assert minwidth>=2.4-1e-5 and minheight>=2.6-1e-5,(minwidth,minheight)
benchbox=bbox([bpy.data.objects['REV02_CHANGE_BENCH']]);assert abs(benchbox[1][2]-.43)<1e-6
G=read(O/'GEOMETRY.json');charsha=hashlib.sha256(Path(G['character']['source']).read_bytes()).hexdigest()
assert any(im.packed_file and hashlib.sha256(im.packed_file.data).hexdigest()==charsha for im in bpy.data.images)
sa=areas(obs);sb=bbox(obs);names={o.name for o in obs};groups={o.name:o.get('group') for o in obs}
old=read(B/'SOURCE_CHECK.json')
source=dict(blend_sha256=hashlib.sha256((O/(P+'.blend')).read_bytes()).hexdigest(),objects=len(obs),bbox=sb,material_areas=sa,
 local_topology=top,local_uv_density_m2_threshold=.0001,local_density_px_per_m=[min(density),max(density)],
 unchanged_objects_checked=len(scope['unaffected_fingerprints']),unexpected_changes=bad,all30_classroom_furniture_unchanged=True,
 nine_cabinet_banks_unchanged=True,cavity_check_inherited=dict(file='../Revision01/SOURCE_CHECK.json',sha256=hashlib.sha256((B/'SOURCE_CHECK.json').read_bytes()).hexdigest(),rays=900,retested_rays=0,reason='all9 bank mesh/UV/matrix fingerprints unchanged'),
 native_door=dict(interface_center=[58,13,0],rays=rays,min_width_m=minwidth,min_height_m=minheight,numeric_tolerance_m=.00001,
  parked_leaves_y=[12.71,12.75],wall_south_y=12.8,parked_leaf_wall_gap_m=.05,extra_opening_face_m2=2.6,extra_ground_area_m2=0),
 bench_bbox=benchbox,character_sha256=charsha,default_new_check_hidden=bpy.data.collections['REV02_CHECK_ONLY_NO_EXPORT'].hide_render,
 proof_scope='Only three changed/new architectural meshes topologically retested;2212 others exact fingerprints. Original whole checks inherited, not a new whole-building final acceptance')
write('SOURCE_CHECK.json',source)
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.fbx(filepath=str(O/(P+'.fbx')))
imp=[o for o in bpy.context.scene.objects if o.type=='MESH'];ib=bbox(imp);ia=areas(imp)
missing=sorted(names-set(o.name for o in imp));extra=sorted(set(o.name for o in imp)-names);uvbad=[o.name for o in imp if not o.data.uv_layers.active or len(o.data.uv_layers.active.data)!=len(o.data.loops)]
groupbad=[o.name for o in imp if o.get('group')!=groups[o.name]];berr=max(abs(sb[i][j]-ib[i][j]) for i in range(2) for j in range(3));aerr=max(abs(v-ia.get(k,0)) for k,v in sa.items())
paths=[dict(path=im.filepath,exists=Path(bpy.path.abspath(im.filepath)).exists()) for im in bpy.data.images if im.source=='FILE']
assert len(imp)==len(names) and not(missing or extra or uvbad or groupbad) and berr<.0001 and aerr<.1
assert all(q['exists'] for q in paths)
write('FBX_CHECK.json',dict(fbx_sha256=hashlib.sha256((O/(P+'.fbx')).read_bytes()).hexdigest(),source_blend_sha256=source['blend_sha256'],objects=len(imp),
 bbox=ib,bbox_max_error_m=berr,material_area_max_error_m2=aerr,missing_names=missing,extra_names=extra,missing_uv=uvbad,group_mismatch=groupbad,imagepaths=paths,
 no_checks_in_export=not extra,scope='real empty-scene Blender reimport; not UE/game'))
print('REV02_NATIVE_AND_REIMPORT_PASS',len(obs),'door',minwidth,minheight,'uv',source['local_density_px_per_m'],flush=True)
