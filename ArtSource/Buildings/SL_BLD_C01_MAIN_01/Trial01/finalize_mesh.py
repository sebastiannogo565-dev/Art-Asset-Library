"""Finish two concealed shaft corners, retain unchanged controls, re-export and update affected evidence."""
import bpy,bmesh,json,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
OUT=Path(__file__).parent;P='SL_BLD_C01_MAIN_01_TRIAL_01'
bpy.ops.wm.open_mainfile(filepath=str(OUT/(P+'.blend')))
scene=bpy.context.scene;whole=bpy.data.collections['WHOLE'];check=bpy.data.collections['CHECK_ONLY_NO_EXPORT']
arch=[o for o in whole.all_objects if o and o.type=='MESH']
def check_objects():
 def walk(c):return list(c.objects)+[o for child in list(c.children) for o in walk(child)]
 return [o for o in walk(check) if o is not None]
corrections=[]
for f in [1,2,3]:
 for suffix in ['DOOR_BAND','HEAD']:
  ob=bpy.data.objects[f'PARTITIONS_F{f:02}_{suffix}']
  z=min(v.co.z for v in ob.data.vertices);Z=max(v.co.z for v in ob.data.vertices)
  for a,b in [(79.8,80.001),(82.399,82.6)]:
   bpy.ops.mesh.primitive_cube_add(size=1,location=((a+b)/2,.7005,(z+Z)/2));cu=bpy.context.object;cu.dimensions=(b-a,.201,Z-z);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
   cu.data.materials.append(bpy.data.materials['WALL'])
   mod=ob.modifiers.new('SHAFT_CORNER_SOLID_UNION','BOOLEAN');mod.operation='UNION';mod.solver='EXACT';mod.object=cu;mod.use_self=True
   bpy.context.view_layer.objects.active=ob;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cu,do_unlink=True)
  bm=bmesh.new();bm.from_mesh(ob.data)
  bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.00001)
  bmesh.ops.dissolve_degenerate(bm,dist=.00001,edges=list(bm.edges))
  bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free();ob.data.update()
  uv=ob.data.uv_layers.active or ob.data.uv_layers.new(name='UV_METRIC_64')
  for poly in ob.data.polygons:
   normal=poly.normal;axis=max(range(3),key=lambda i:abs(normal[i]));u=Vector((0,1,0)) if axis==0 else Vector((1,0,0));u=(u-normal*u.dot(normal)).normalized();v=normal.cross(u)
   for li in poly.loop_indices:
    co=ob.data.vertices[ob.data.loops[li].vertex_index].co;uv.data[li].uv=(co.dot(u)/4,co.dot(v)/4)
  bm=bmesh.new();bm.from_mesh(ob.data);bad=sum(not e.is_manifold for e in bm.edges);bm.free()
  corrections.append(dict(mesh=ob.name,remaining_nonmanifold_edges=bad))
# Pose preserves dimensions, knee/shin translated60mm toward chair to clear the under-desk tray.
for name in ['POSE_PROXY_THIGHS','POSE_PROXY_SHINS']:
 ob=bpy.data.objects[name]
 if min(v.co.x for v in ob.data.vertices)<45.90:
  for v in ob.data.vertices:v.co.x+=.06
# Test pulled-chair surface intersection at1mm contact inset, then restore default rest.
for ob in arch:
 if ob.get('player_room_chair'):ob.location.x+=.25
bpy.context.view_layer.update();sv=[];sf=[]
for ob in arch:
 if ob.name.startswith('F2_W4_') and ('DESK_' in ob.name or 'CHAIR_' in ob.name):
  off=len(sv);sv.extend(tuple(ob.matrix_world@v.co) for v in ob.data.vertices);sf.extend(tuple(off+i for i in p.vertices) for p in ob.data.polygons)
tree=BVHTree.FromPolygons(sv,sf);results=[]
for ob in check_objects():
 if not ob.name.startswith('POSE_PROXY'):continue
 vs=[ob.matrix_world@v.co for v in ob.data.vertices];lo=[min(v[i] for v in vs)+.001 for i in range(3)];hi=[max(v[i] for v in vs)-.001 for i in range(3)];x,y,z=lo;X,Y,Z=hi
 vv=[(x,y,z),(X,y,z),(X,Y,z),(x,Y,z),(x,y,Z),(X,y,Z),(X,Y,Z),(x,Y,Z)]
 ff=[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]
 results.append(dict(proxy=ob.name,bounds=[lo,hi],triangle_surface_intersections=len(tree.overlap(BVHTree.FromPolygons(vv,ff)))))
for ob in arch:
 if ob.get('player_room_chair'):ob.location.x-=.25
bpy.context.view_layer.update()
def write(n,v):(OUT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
write('SEATED_STATIC_CHECK.json',dict(chair_state='all player chairs pulled.25m',contact_inset_m=.001,
 adjustment='thigh/shin dimensions unchanged; translated+X.06m toward chair after tray intersection',results=results,
 scope='static surface intersection, not continuous transition, approved seated art or all seats'))
write('MESH_FINALIZATION.json',dict(shaft_corner_union=corrections,reason='two edge-only contacts at lift shaft south corners per floor; net2.4x2.4 unchanged',
 unchanged_visible_exterior=True,preview_updates=['CLASS_PULLED','LAYERS','F02','COURT_TERRACE']))
S=json.loads((OUT/'STATISTICS.json').read_text());meshes=set(o.data for o in arch)
S.update(source_vertices=sum(len(m.vertices) for m in meshes),source_triangles=sum(len(p.vertices)-2 for m in meshes for p in m.polygons),
 placed_vertices=sum(len(o.data.vertices) for o in arch),placed_triangles=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in arch))
write('STATISTICS.json',S);G=json.loads((OUT/'GEOMETRY.json').read_text(encoding='utf-8'));G['stats']=S;G['authorized_internal_adjustments'].append('Lift shaft south wall corner caps extended into corner thickness; net shaft dimensions unchanged');write('GEOMETRY.json',G)
# Export ONLY architecture; export meshes expanded, source linked data remains editable.
bpy.ops.object.select_all(action='DESELECT')
for ob in arch:ob.select_set(True)
bpy.context.view_layer.objects.active=arch[0];original={o:o.data for o in arch}
for ob in arch:
 if ob.data.users>1:ob.data=ob.data.copy()
bpy.context.view_layer.update()
bpy.ops.export_scene.fbx(filepath=str(OUT/(P+'.fbx')),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,
 axis_forward='-Y',axis_up='Z',add_leaf_bones=False,mesh_smooth_type='FACE',path_mode='RELATIVE',use_mesh_modifiers=True,use_custom_props=True)
for ob,me in original.items():ob.data=me
log=json.loads((OUT/'CAMERAS.json').read_text());check.hide_render=False;check.hide_viewport=False
def reset():
 for c in whole.children:c.hide_render=False
 for ob in arch:ob.hide_render=False
 for ob in check_objects():ob.hide_render=True
def render(n,t,az,el,scale):
 cam=scene.camera;t=Vector(t);a=math.radians(az);e=math.radians(el);cam.location=t+Vector((math.cos(a)*math.cos(e),math.sin(a)*math.cos(e),math.sin(e)))*200
 cam.rotation_euler=(t-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale
 scene.render.resolution_x=2560;scene.render.resolution_y=1440;scene.cycles.samples=24;scene.render.filepath=str(OUT/'Previews'/(P+'_'+n+'.png'));bpy.ops.render.render(write_still=True)
 global log;log=[x for x in log if x['file']!=P+'_'+n+'.png'];log.append(dict(file=P+'_'+n+'.png',target=list(t),azimuth=az,elevation=el,ortho_scale=scale,size=[2560,1440],display_only_cut=True,sun='same early summer sun/world/AgX',update='final shaft corner/pose verification'))
 print('FINAL_RENDER',n,flush=True)
reset()
for ob in arch:ob.hide_render=True
for ob in bpy.data.collections['CLASS_CUT_DEMO'].objects:ob.hide_render=False
for ob in arch:
 if ob.name.startswith('F2_W4_') or ob.name.startswith('OPEN_F2_W4_N'):ob.hide_render=False
for ob in arch:
 if ob.get('player_room_chair'):ob.location.x+=.25
render('CLASS_PULLED',[45.2,17.3,4.8],315,30,13.5)
for ob in arch:
 if ob.get('player_room_chair'):ob.location.x-=.25
reset()
for c in whole.children:
 if c.name in ['ROOF','EXTERIOR'] or c.name.startswith('CEILING') or c.name.startswith('PARTITIONS'):c.hide_render=True
render('LAYERS',[75,14,4],225,40,152)
reset()
for c in whole.children:
 if c.name in ['ROOF','EXTERIOR'] or c.name.startswith('CEILING') or c.name.endswith('F01') or c.name.endswith('F03'):c.hide_render=True
render('F02',[75,14,4.5],225,40,150)
reset()
for c in whole.children:
 if c.name=='ROOF' or c.name.startswith('CEILING'):c.hide_render=True
for ob in arch:
 if ob.name.startswith('EXT_') or ob.name.startswith('PARTITIONS_'):ob.hide_render=True
render('COURT_TERRACE',[79,14,4.7],225,30,41)
reset()
for ob in check_objects():ob.hide_render=False;ob.hide_viewport=False
check.hide_render=True;check.hide_viewport=True
write('CAMERAS.json',log)
cam=scene.camera;t=Vector((75,14,5.5));a=math.radians(225);e=math.radians(30);cam.location=t+Vector((math.cos(a)*math.cos(e),math.sin(a)*math.cos(e),math.sin(e)))*200;cam.rotation_euler=(t-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=150
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/(P+'.blend')),compress=True)
print('FINAL_MESH',corrections,'POSE',results,flush=True)
