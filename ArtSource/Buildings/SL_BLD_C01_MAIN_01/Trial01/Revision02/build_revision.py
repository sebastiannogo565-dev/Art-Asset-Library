"""Actual local Blender modification of Revision01, never write its files."""
import bpy,bmesh,json,math,hashlib,array,ast
import numpy as np
from pathlib import Path
from mathutils import Vector
O=Path(__file__).parent;B=O.parent/'Revision01';P='SL_BLD_C01_MAIN_01_TRIAL_01_REV_02'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def write(n,v):(O/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
L=read(O/'LAYOUT.json');assert all(p['passed'] for p in L['paths']) and L['bench_transition']['passed'] and L['shoe_change']['passed']
bpy.ops.wm.open_mainfile(filepath=str(B/'SL_BLD_C01_MAIN_01_TRIAL_01_REV_01.blend'))
scene=bpy.context.scene;whole=bpy.data.collections['WHOLE'];root=next(o for o in whole.objects if o and o.type=='EMPTY');groups={c.name:c for c in whole.children}
MATS={n:bpy.data.materials[n] for n in ['FRAME','GLASS','CHAIR','WALL']}
tree=ast.parse((B/'update_model.py').read_text(encoding='utf-8'));nodes=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in ['Parts','meshhash','fingerprints','arch_objects']]
exec(compile(ast.Module(body=nodes,type_ignores=[]),'Revision01 definitions only','exec'),globals())
before=fingerprints()
# Open the actual low partition union, retain head and all other walls/rooms.
wall=bpy.data.objects['PARTITIONS_F01_DOOR_BAND'];wall.data=wall.data.copy();originalwall=wall.data.copy()
pa=Parts();pa.add([56.8,12.65,-.1,59.2,13.15,2.6],'WALL');cut=pa.finish('REV02_TEMP_CUT','PARTITIONS_F01')
bpy.ops.object.select_all(action='DESELECT');wall.select_set(True);bpy.context.view_layer.objects.active=wall
mod=wall.modifiers.new('REV02_ONLY_WESTLINK_WIDEN','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cut
bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
# New cut faces receive the same face-planar metric UV as the original source.
def metric_uv(me):
 me.update();uv=me.uv_layers.active or me.uv_layers.new(name='UV_METRIC_64')
 for p in me.polygons:
  n=p.normal;axis=max(range(3),key=lambda i:abs(n[i]));u=Vector((0,1,0)) if axis==0 else Vector((1,0,0));u=(u-n*u.dot(n)).normalized();v=n.cross(u)
  for li in p.loop_indices:
   co=me.vertices[me.loops[li].vertex_index].co;uv.data[li].uv=(co.dot(u)/4,co.dot(v)/4)
metric_uv(wall.data)
# Final reveal frame at room north faceY13; actual wall midline stays12.9. Leaves park clear on hall side.
old=bpy.data.objects['OPEN_F1_LW_D'];bpy.data.objects.remove(old,do_unlink=True);pa=Parts()
for x,X in [(56.745,56.8),(59.2,59.255)]:pa.add([x,12.8,0,X,13,2.655],'FRAME')
pa.add([56.8,12.8,2.6,59.2,13,2.655],'FRAME')
for x,X in L['door']['leaf_x']:
 pa.add([x,12.72,.025,X,12.74,2.575],'GLASS')
 for a,A in [(x,x+.035),(X-.035,X)]:pa.add([a,12.71,0,A,12.75,2.6],'FRAME')
 for z,Z in [(0,.05),(2.55,2.6)]:pa.add([x,12.71,z,X,12.75,Z],'FRAME')
door=pa.finish('OPEN_F1_LW_D','INTERIOR_F01');door['opening_id']='F1_LW_D';door['clear_width']=2.4;door['clear_height']=2.6
door['interface_center_m']=[58.,13.,0.];door['leaves_parked_y_m']=[12.71,12.75]
pa=Parts();pa.add([52.8,13.15,.395,55.2,13.6,.43],'CHAIR')
for x in [52.95,54.,55.05]:
 for y in [13.23,13.52]:pa.add([x-.025,y-.025,0,x+.025,y+.025,.395],'FRAME')
bench=pa.finish('REV02_CHANGE_BENCH','INTERIOR_F01');bench['use']='two-person north-facing shoe-changing bench candidate';bench['seat_height_m']=.43
bpy.context.view_layer.update();after=fingerprints();allowed={'PARTITIONS_F01_DOOR_BAND','OPEN_F1_LW_D'}
unexpected=[n for n in before if n not in allowed and after.get(n)!=before[n]];assert not unexpected,unexpected
unaffected={n:v for n,v in before.items() if n not in allowed};assert len(unaffected)==2212
write('CHANGE_SCOPE.json',dict(base_blend_sha256=hashlib.sha256((B/'SL_BLD_C01_MAIN_01_TRIAL_01_REV_01.blend').read_bytes()).hexdigest(),
 changed=[n for n in before if n in after and before[n]!=after[n]],added=sorted(set(after)-set(before)),unexpected=unexpected,
 unchanged_architecture_objects=len(unaffected),unaffected_fingerprints=unaffected,
 classroom='All30 desk/chair transforms/data/UV/materials unchanged;5_5 study preserved, no final player binding',
 cabinets='All9 banks exact fingerprints unchanged;900 actual cavities and previous UV retained',
 opening='1.4→2.4 at same room interface58/13, reveal/frame/parked leaves and actual wall cut updated',
 original_wall_triangle_count=sum(len(p.vertices)-2 for p in originalwall.polygons),revised_wall_triangle_count=sum(len(p.vertices)-2 for p in wall.data.polygons)))
check=bpy.data.collections.new('REV02_CHECK_ONLY_NO_EXPORT');scene.collection.children.link(check);check.hide_render=True;check.hide_viewport=True
for im in bpy.data.images:
 if im.source=='FILE' and not im.packed_file:im.pack()
arch=arch_objects();meshes=set(o.data for o in arch)
stats=dict(mesh_objects=len(arch),unique_mesh_sources=len(meshes),linked_placements=len(arch)-len(meshes),source_vertices=sum(len(m.vertices) for m in meshes),
 placed_triangles=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in arch),materials=len(set(m for o in arch for m in o.data.materials)),nominal_cells=900,new_texture_files=0,bench_users=2)
write('STATISTICS.json',stats)
GG=read(B/'GEOMETRY.json');GG['asset']=P;GG['revision_layout']='LAYOUT.json';GG['source_geometry']='Revision01 actual source + build_revision.py local wall/door/bench changes';GG['stats']=stats;GG['texture_root']='../Textures'
for r in GG['rooms']:
 if r['id']=='F1_LW':r['door_width']=2.4;r['door_height']=2.6
for q in GG['openings']:
 if q['id']=='F1_LW_D':q.update(lo=56.8,hi=59.2,line=12.9,frame_y=[12.8,13.0],leaves_y=[12.71,12.75],interface_center=[58,13,0])
GG['inherited_5_5_study']=GG.pop('player_interface');GG['player_interface']=dict(business_semantic_xy=[45,19.5],floor_local=4,
 historical_anchor_engineering_cm=[4500,7050,800],formal_anchor_candidate_cm=[4500,7050,1200],actual_runtime_anchor_verified=False,
 designated_seat_id=None,research_candidate_seat_id='F2_W4_DESK_3_5',actual_operation_ground_local_m=[45,19.5,4],P_equals_E=True,
 candidate_recovery=[45,18.7,4],radius_cm=230,distance_table='ACTIVITY_DISTANCE.json',continuous_study='INHERITED_STUDY.json;5_5 unchanged,not final binding',
 scope='Original actor anchor/radius/map not changed; formal mapping distance condition only, historicalZ8 conflict retained')
GG['shoe_layout']=dict(banks=L['shoe_banks'],bench=L['bench'],operation_and_use='LAYOUT.json',nominal=900,main=468,link=432,
 actual_link_door_width=2.4,cabinet_area_m2=15.048,bench_area_m2=1.08)
GG['authorized_internal_adjustments']=['Local westlink actual wall opening/reveal/frame/leaves2.4x2.6 at same58/13 interface',
 'Add north-facing2.4x.45x.43m bench, two conditional users;900 banks unchanged',
 'Class geometry unchanged; candidate3_5 relation and reachable standing P=E45/19.5 only; no final player binding/anchor or radius change']
write('GEOMETRY.json',GG)
bpy.ops.object.select_all(action='DESELECT')
for o in arch:o.select_set(True)
bpy.context.view_layer.objects.active=arch[0];original={o:o.data for o in arch}
for o in arch:
 if o.data.users>1:o.data=o.data.copy()
bpy.context.view_layer.update();bpy.ops.export_scene.fbx(filepath=str(O/(P+'.fbx')),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,
 axis_forward='-Y',axis_up='Z',use_custom_props=True,add_leaf_bones=False,mesh_smooth_type='FACE',path_mode='RELATIVE')
for o,me in original.items():o.data=me
scene['revision']='TRIAL_01_REV_02';scene['revision_scope']='local internal door wall/frame/leaves, two-person bench;classroom unchanged and interface uncertainty retained'
bpy.ops.wm.save_as_mainfile(filepath=str(O/(P+'.blend')),compress=True)
print('REV02_ACTUAL_SOURCE_BUILT',stats,'UNCHANGED',len(unaffected),flush=True)
