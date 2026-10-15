"""Load original trial read-only, update only validated high-frequency parts, save an independent revision."""
import bpy,bmesh,json,math,hashlib,array
from pathlib import Path
from mathutils import Vector
import numpy as np
OUT=Path(__file__).parent;BASE=OUT.parent;P='SL_BLD_C01_MAIN_01_TRIAL_01_REV_01'
L=json.loads((OUT/'LAYOUT.json').read_text(encoding='utf-8'));SH=json.loads((OUT/'SHOE_CHECKS.json').read_text(encoding='utf-8'))
assert all(s['passed'] for s in L['segments']),'No geometry update before player layout evidence'
assert SH['nominal']==900 and all(v['passed'] for v in SH['paths'] if v['id'] in ['MAIN_IN','MAIN_OUT','LINK_SINGLE_PERSON_LOOP'])
bpy.ops.wm.open_mainfile(filepath=str(BASE/'SL_BLD_C01_MAIN_01_TRIAL_01.blend'))
scene=bpy.context.scene;whole=bpy.data.collections['WHOLE'];root=next(o for o in whole.objects if o.type=='EMPTY')
def arch_objects():return [o for o in whole.all_objects if o and o.type=='MESH']
def meshhash(me):
 h=hashlib.sha256()
 def add(seq,prop,typ,n):
  a=array.array(typ,[0])*n;seq.foreach_get(prop,a);h.update(a.tobytes())
 add(me.vertices,'co','f',len(me.vertices)*3);add(me.loops,'vertex_index','i',len(me.loops))
 for uv in me.uv_layers:add(uv.data,'uv','f',len(uv.data)*2)
 h.update('|'.join(m.name for m in me.materials if m).encode());return h.hexdigest()
def fingerprints():
 cache={};r={}
 for o in arch_objects():
  if o.data not in cache:cache[o.data]=meshhash(o.data)
  r[o.name]=dict(mesh=cache[o.data],matrix=[float(x) for row in o.matrix_world for x in row],group=o.get('group'),materials=[m.name for m in o.data.materials])
 return r
before=fingerprints();groups={c.name:c for c in whole.children}
# New geometry uses inherited materials, metric UV and exact solid unions, no global rebuild or new textures.
MATS={n:bpy.data.materials[n] for n in ['METAL','ENTRY_FRAME','FRAME','CHAIR','BOARD']}
class Parts:
 def __init__(self):self.boxes=[]
 def add(self,b,m):self.boxes.append((b,m))
 def finish(self,name,group,location=(0,0,0)):
  axes=[sorted(set(round(b[i],7) for b,m in self.boxes)|set(round(b[i+3],7) for b,m in self.boxes)) for i in range(3)]
  indices=[{v:i for i,v in enumerate(a)} for a in axes];shape=tuple(len(a)-1 for a in axes)
  keys=list(MATS);grid=np.full(shape,-1,np.int16)
  for b,m in self.boxes:grid[tuple(slice(indices[i][round(b[i],7)],indices[i][round(b[i+3],7)]) for i in range(3))]=keys.index(m)
  vv=[];ff=[];mi=[];lookup={}
  dirs=[((-1,0,0),(0,4,7,3)),((1,0,0),(1,2,6,5)),((0,-1,0),(0,1,5,4)),((0,1,0),(3,7,6,2)),((0,0,-1),(0,3,2,1)),((0,0,1),(4,5,6,7))]
  for i,j,k in np.argwhere(grid>=0):
   x,X=axes[0][i:i+2];y,Y=axes[1][j:j+2];z,Z=axes[2][k:k+2]
   cs=[(x,y,z),(X,y,z),(X,Y,z),(x,Y,z),(x,y,Z),(X,y,Z),(X,Y,Z),(x,Y,Z)]
   for delta,face in dirs:
    a,b,c=i+delta[0],j+delta[1],k+delta[2]
    if 0<=a<shape[0] and 0<=b<shape[1] and 0<=c<shape[2] and grid[a,b,c]>=0:continue
    f=[]
    for q in face:
     v=cs[q]
     if v not in lookup:lookup[v]=len(vv);vv.append(v)
     f.append(lookup[v])
    ff.append(f);mi.append(int(grid[i,j,k]))
  me=bpy.data.meshes.new(name);me.from_pydata(vv,[],ff);me.update()
  used=sorted(set(mi))
  for i in used:me.materials.append(MATS[keys[i]])
  for poly,i in zip(me.polygons,mi):poly.material_index=used.index(i)
  bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();me.update()
  uv=me.uv_layers.new(name='UV_METRIC_64')
  for poly in me.polygons:
   normal=poly.normal;axis=max(range(3),key=lambda i:abs(normal[i]));u=Vector((0,1,0)) if axis==0 else Vector((1,0,0));u=(u-normal*u.dot(normal)).normalized();v=normal.cross(u)
   for li in poly.loop_indices:
    co=me.vertices[me.loops[li].vertex_index].co;uv.data[li].uv=(co.dot(u)/4,co.dot(v)/4)
  ob=bpy.data.objects.new(name,me);groups[group].objects.link(ob);ob.parent=root;ob.location=location;ob['group']=group;ob['purpose']='TRIAL_ARCHITECTURE'
  return ob
playerdesk=bpy.data.objects['F2_W4_DESK_5_5'];playerdesk.location.x=47.715
oldchair=bpy.data.objects['F2_W4_CHAIR_5_5'];bpy.data.objects.remove(oldchair,do_unlink=True)
pa=Parts()
pa.add([-.225,-.225,.395,.225,.225,.43],'CHAIR');pa.add([.16,-.225,.43,.22,.225,.84],'CHAIR')
for x in [-.18,.18]:
 for y in [-.18,.18]:pa.add([x-.015,y-.015,0,x+.015,y+.015,.395],'FRAME')
pa.add([.21,-.10,.83,.30,.10,.88],'FRAME') # 10mm solid overlap into back; no edge-only contact
for y in [-.08,.06]:pa.add([.18,y,.80,.26,y+.02,.86],'FRAME')
playerchair=pa.finish('F2_W4_CHAIR_5_5','INTERIOR_F02',(48.275,19.87,4));playerchair['revision_player']=True
removed=[]
for ob in list(arch_objects()):
 if ob.name.startswith('LOCKER_') or ob.name in ['P1_CHANGE_W','P1_WAIT','LINK_CHANGE']:
  removed.append(ob.name);bpy.data.objects.remove(ob,do_unlink=True)
for bank in L['shoe']['banks']:
 pa=Parts();x,y,z,X,Y,Z=bank['bounds'];axis=bank['axis'];length=X-x if axis=='X' else Y-y;D=bank['depth'];N=bank['columns'];H=bank['rows']*.3
 def add(b,mat):
  u,v,w,U,V,W=b
  world=[x+u,y+v,w,x+U,y+V,W] if axis=='X' else [x+v,y+u,w,x+V,y+U,W]
  pa.add(world,mat)
 # Actual carcass, six shelves and real cavities; open fronts are the revision candidate.
 if bank['faces']==2:add([0,D/2-.006,0,length,D/2+.006,H],'METAL')
 else:add([0,0,0,length,.012,H],'METAL')
 for i in range(N+1):
  u=i*.3;add([max(0,u-.006),0,0,min(length,u+.006),D,H],'METAL')
 for j in range(bank['rows']+1):
  h=j*.3;add([0,0,max(0,h-.006),length,D,min(H,h+.006)],'METAL')
 for j in range(bank['rows']):
  if bank['faces']==2:add([0,0,j*.3+.282,length,.004,j*.3+.294],'ENTRY_FRAME')
  add([0,D-.004,j*.3+.282,length,D,j*.3+.294],'ENTRY_FRAME')
 ob=pa.finish('LOCKER_'+bank['id'],'INTERIOR_F01');ob['nominal_cells']=bank['nominal'];ob['candidate']='six-row open cubbies; no final hardware'
# Move the existing notice off the newly restored main east-end bypass, preserving its mesh/material/UV.
notice=bpy.data.objects['P1_PHOTOS'];notice.location=(34,19.65,0)
bpy.context.view_layer.update();after=fingerprints()
allowed=set(removed)|{'F2_W4_DESK_5_5','F2_W4_CHAIR_5_5','P1_PHOTOS'}
changed=[n for n in before if n in after and before[n]!=after[n]]
unexpected=[n for n in changed if n not in allowed]
assert not unexpected,unexpected
unaffected={n:v for n,v in before.items() if n not in allowed}
assert all(after.get(n)==v for n,v in unaffected.items())
# Drop stale demonstration geometry in the COPY, keep original Trial files and all architectural groups.
check=bpy.data.collections.get('CHECK_ONLY_NO_EXPORT')
def children(c):
 return [c]+[q for child in list(c.children) for q in children(child)]
if check:
 for c in children(check)[::-1]:
  for ob in list(c.objects):bpy.data.objects.remove(ob,do_unlink=True)
  bpy.data.collections.remove(c)
check=bpy.data.collections.new('REVISION_CHECK_ONLY_NO_EXPORT');scene.collection.children.link(check);check.hide_render=True;check.hide_viewport=True
for im in bpy.data.images:
 if im.source=='FILE' and not im.packed_file:im.pack()
scene['revision']='TRIAL_01_REV_01';scene['revision_scope']='player desk/chair, nine locker banks, main local bench removal and notice relocation only'
def write(n,v):(OUT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
write('CHANGE_SCOPE.json',dict(base_blend_sha256=hashlib.sha256((BASE/'SL_BLD_C01_MAIN_01_TRIAL_01.blend').read_bytes()).hexdigest(),
 changed=changed,removed=removed,added=sorted(set(after)-set(before)),unexpected=unexpected,
 unchanged_architecture_objects=len(unaffected),unaffected_fingerprints=unaffected,
 other23_classrooms='all object transforms, source mesh data, UV and material fingerprints unchanged',
 original_LW_door='F1_LW_D1.4m preserved;2.4m proposal exists only in CHECK/drawing, not exported',
 notice='P1_PHOTOS moved +X34,+Y19.65 to west-link east wall; same data/UV/materials'))
def export():
 arch=arch_objects();bpy.ops.object.select_all(action='DESELECT')
 for ob in arch:ob.select_set(True)
 bpy.context.view_layer.objects.active=arch[0];original={o:o.data for o in arch}
 for ob in arch:
  if ob.data.users>1:ob.data=ob.data.copy()
 bpy.context.view_layer.update()
 bpy.ops.export_scene.fbx(filepath=str(OUT/(P+'.fbx')),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,
  axis_forward='-Y',axis_up='Z',use_custom_props=True,add_leaf_bones=False,mesh_smooth_type='FACE',path_mode='RELATIVE')
 for ob,me in original.items():ob.data=me
export();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/(P+'.blend')),compress=True)
arch=arch_objects();meshes=set(o.data for o in arch)
stats=dict(mesh_objects=len(arch),unique_mesh_sources=len(meshes),linked_placements=len(arch)-len(meshes),source_vertices=sum(len(m.vertices) for m in meshes),
 placed_triangles=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in arch),materials=len(set(m for o in arch for m in o.data.materials)),
 new_texture_files=0,inherited_textures='../Textures (48 original files, packed)',nominal_cells=sum(b['nominal'] for b in L['shoe']['banks']))
write('STATISTICS.json',stats)
GG=json.loads((BASE/'GEOMETRY.json').read_text(encoding='utf-8'));GG.update(asset=P,revision_layout='LAYOUT.json',lockers=L['shoe']['banks'],stats=stats)
GG['player_interface'].update(designated_seat_id=L['player']['id'],seat_rest=L['player']['chair_rest'],seat_pulled=L['player']['chair_pulled'],
 standing_approach=L['player']['approach'],continuous_certificate='LAYOUT.json segments; assumed proxy only, not approved character motion')
GG['player_interface'].update(route_to_approach=[[45,12.7],[45,18.8],[48.8,18.8],[48.8,19.08]],
 route_operator_to_front=[[48.8,19.08],[48.8,18.8],[48.29,18.8],[48.29,19.87]],
 seat_transfer='LAYOUT.json seated_motion;19 ordered segments; own chair X48.900 while transferring',
 route_return_via_teaching=[[48.29,19.87],[48.29,18.8],[48.8,18.8],[48.8,19.08],[48.8,18.8],[41.7,18.8],[45,18.8],[45,12.7]],
 seat_transfer_status='conditional continuous spatial check under explicit full-size proxy hypothesis, not approved character action')
GG['base_trial_internal_adjustments_historical']=GG.pop('authorized_internal_adjustments')
GG['authorized_internal_adjustments']=['Only F2_W4 desk5_5 X+0.04 and unique chair5_5 X+0.20 with local handle; other23 rooms unchanged',
 'Nine six-row open-front candidate banks main468/link432; original benches P1_CHANGE_W/P1_WAIT/LINK_CHANGE removed',
 'P1_PHOTOS unchanged mesh moved +34,+19.65; actual westlink1.4m door unchanged;2.4m check-only proposal']
GG['player_layout'].update(scope='desk_x/desk_y are inherited base grid; use explicit placement table for this room, not Cartesian product',
 explicit_desks=L['desks'],explicit_chairs=L['chairs'],seat_status='SEATS.csv',all_seats_validated=False)
GG['shoe_layout']=L['shoe'];GG['texture_root']='../Textures';GG['revision_dependencies']='VIEW_DEPENDENCIES.json'
GG['source_geometry']='Original Trial01 build_trial.py, then this independent update_model.py; local changes only'
write('GEOMETRY.json',GG)
print('MODEL_UPDATED',stats,'UNCHANGED',len(unaffected),'CHANGED',changed,flush=True)
