"""Editable finite envelopes, actual cell section, ray sampled headroom, UV evidence."""
import bpy,bmesh,json,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
OUT=Path(__file__).parent;P='SL_BLD_C01_MAIN_01_TRIAL_01';PRE=OUT/'Previews'
bpy.ops.wm.open_mainfile(filepath=str(OUT/(P+'.blend')))
scene=bpy.context.scene;whole=bpy.data.collections['WHOLE'];check=bpy.data.collections['CHECK_ONLY_NO_EXPORT'];check.hide_render=False;check.hide_viewport=False
def check_objects():
 def walk(c):return list(c.objects)+[o for child in list(c.children) for o in walk(child)]
 return [o for o in walk(check) if o is not None]
arch=[o for o in whole.all_objects if o is not None and o.type=='MESH'];existing=check_objects()
# Put thighs on top of seat, not through the seat surface; this is a CHECK proxy correction only.
for v in bpy.data.objects['POSE_PROXY_THIGHS'].data.vertices:
 if abs(v.co.z-4.40)<1e-4:v.co.z=4.43
 if abs(v.co.z-4.62)<1e-4:v.co.z=4.65
extra=bpy.data.collections.new('FINITE_ENVELOPES_AND_SHOE_SECTION');check.children.link(extra)
def move_to(ob):
 for c in list(ob.users_collection):c.objects.unlink(ob)
 extra.objects.link(ob)
def wire(ob,mat):
 ob.data.materials.clear();ob.data.materials.append(mat)
 m=ob.modifiers.new('FINITE_OUTLINE','WIREFRAME');m.thickness=.008;return ob
def capsule(name,pos):
 r=.34;h=1.92;seg=24;rings=[]
 for theta in [-math.pi/2+i*math.pi/16 for i in range(1,9)]:
  rings.append((r*math.cos(theta),r+r*math.sin(theta)))
 for theta in [i*math.pi/16 for i in range(8)]:
  rings.append((r*math.cos(theta),h-r+r*math.sin(theta)))
 verts=[(0,0,0)]+[(rr*math.cos(2*math.pi*i/seg),rr*math.sin(2*math.pi*i/seg),z) for rr,z in rings for i in range(seg)]+[(0,0,h)]
 faces=[]
 for i in range(seg):faces.append((0,1+(i+1)%seg,1+i))
 for j in range(len(rings)-1):
  for i in range(seg):a=1+j*seg+i;b=1+j*seg+(i+1)%seg;faces.append((a,b,b+seg,a+seg))
 top=len(verts)-1
 for i in range(seg):a=1+(len(rings)-1)*seg+i;b=1+(len(rings)-1)*seg+(i+1)%seg;faces.append((a,b,top))
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);ob=bpy.data.objects.new(name,me);extra.objects.link(ob);ob.location=pos
 ob['height']=h;ob['diameter']=.68;wire(ob,bpy.data.materials['CHECK_BLUE']);return ob
cap=capsule('CAPSULE_MAIN_NARROW',(45,16.5,4))
capdoor=capsule('CAPSULE_DOOR',(45,12.85,4))
capsule('CAPSULE_STAIR',(32.7,7.5,0))
def cube(name,b,mat,outline=False):
 x,y,z,X,Y,Z=b
 bpy.ops.mesh.primitive_cube_add(size=1,location=((x+X)/2,(y+Y)/2,(z+Z)/2));ob=bpy.context.object;ob.name=name;ob.dimensions=(X-x,Y-y,Z-z);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);move_to(ob);ob.data.materials.append(mat)
 if outline:wire(ob,mat)
 return ob
ops=[]
for n,b in [('ONE_FACE',[20.48,2.63,0,21.52,3.33,1.8]),('OPPOSITE_FAIL',[20.48,3.87,0,21.52,4.57,1.8])]:
 ops.append(cube('OPERATING_'+n,b,bpy.data.materials['CHECK_ORANGE'],True))
cross=[capsule('CROSS_ARRIVAL',(24.8,1.375,0)),capsule('CROSS_DEPARTURE',(25.2,1.375,0))]
# Real cabinetry clipped down to nominated open cell, no redrawn box substitute.
cell=[]
for n in ['LOCKER_MAIN_W1_CARCASS','LOCKER_MAIN_W1_FRONTS']:
 me=bpy.data.objects[n].data.copy();bm=bmesh.new();bm.from_mesh(me)
 for ax in range(3):
  for pos,sign in [([20.79,2.29,.59][ax],-1),([21.11,2.64,.91][ax],1)]:
   normal=[0,0,0];normal[ax]=sign;co=[0,0,0];co[ax]=pos
   bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=.000001,plane_co=co,plane_no=normal,clear_outer=True)
 bm.to_mesh(me);bm.free();ob=bpy.data.objects.new('CELL_SECTION_'+n,me);extra.objects.link(ob);cell.append(ob)
for x in [20.82,20.95]:
 cell.append(cube('SHOE_ENVELOPE_290_105_115',[x,2.316,.615,x+.105,2.606,.730],bpy.data.materials['CHECK_BLUE']))
# Native mesh UV sample dump used by the reading board; actual loop coordinates.
samples=[]
for n in ['EXT_WHOLE_UNION','F2_W4_DESK_1_1','LOCKER_MAIN_W1_CARCASS','S1_L0_UP1','ROOF_GABLE_0_3.4']:
 me=bpy.data.objects[n].data;uv=me.uv_layers.active
 samples.append(dict(object=n,vertices=len(me.vertices),polygons=len(me.polygons),
  uv_faces=[dict(material=me.materials[p.material_index].name,uv=[list(uv.data[i].uv) for i in p.loop_indices]) for p in list(me.polygons)[:140]]))
(OUT/'UV_SAMPLES.json').write_text(json.dumps(samples,indent=2)+'\n',encoding='utf-8',newline='\n')
# Actual upwards-ray headroom samples; bound broadphase, all WHOLE meshes participate.
bounds={}
for ob in arch:
 co=[ob.matrix_world@Vector(v) for v in ob.bound_box]
 bounds[ob]=([min(v[i] for v in co) for i in range(3)],[max(v[i] for v in co) for i in range(3)])
def headroom(x,y,z):
 hits=[]
 for ob,(lo,hi) in bounds.items():
  if lo[0]-.001<=x<=hi[0]+.001 and lo[1]-.001<=y<=hi[1]+.001 and hi[2]>z+.02:
   origin=ob.matrix_world.inverted()@Vector((x,y,z+.015))
   direction=(ob.matrix_world.inverted().to_3x3()@Vector((0,0,1))).normalized()
   hit,loc,n,idx=ob.ray_cast(origin,direction,distance=20)
   if hit:
    zz=(ob.matrix_world@loc).z
    if zz>z+.02:hits.append((zz-z,ob.name))
 return min(hits) if hits else (None,None)
head=[]
for x in [32.7,88.7,144.7]:
 for base in [0,4]:
  for i in range(11):
   y=6.4-(i+.5)*.3;z=base+(i+1)*4/24
   d,n=headroom(x,y,z);head.append(dict(x=x,y=y,floor=z,clear=d,hit=n))
  for i in range(11):
   y=3.1+(i+.5)*.3;z=base+2+(i+1)*4/24
   d,n=headroom(x+2.5,y,z);head.append(dict(x=x+2.5,y=y,floor=z,clear=d,hit=n))
  for y in [1.4,2.4]:
   d,n=headroom(x,y,base+2);head.append(dict(x=x,y=y,floor=base+2,clear=d,hit=n))
headresult=dict(method='vertical native mesh rays .015m above actual tread; all exported geometry participates',
 samples=head,min_clear=min(x['clear'] for x in head if x['clear'] is not None),
 below_capsule=[x for x in head if x['clear'] is not None and x['clear']<1.92],code_compliance='not assessed')
(OUT/'STAIR_HEADROOM.json').write_text(json.dumps(headresult,indent=2)+'\n',encoding='utf-8',newline='\n')
G=json.loads((OUT/'GEOMETRY.json').read_text(encoding='utf-8'))
for st in G['stairs']:
 st['headroom_status']='native vertical-ray samples; see STAIR_HEADROOM.json'
 st['headroom_measured_min']=headresult['min_clear']
 st['headroom_parallel_flight']=None
(OUT/'GEOMETRY.json').write_text(json.dumps(G,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
# Static finite-capsule samples on three actual indoor high-frequency route sets.
# Stair motion itself is not inferred from these horizontal samples.
vv=[];ff=[]
for ob in arch:
 offset=len(vv);vv.extend(tuple(ob.matrix_world@v.co) for v in ob.data.vertices)
 ff.extend(tuple(offset+i for i in poly.vertices) for poly in ob.data.polygons)
bvh=BVHTree.FromPolygons(vv,ff,all_triangles=False)
route_sets=[
 ('DAILY_01',0,[[25,0],[25,8.8],[25,10.9],[34,10.9],[34,7.5],[32.7,7.5],[32.7,6.8]]),
 ('DAILY_01',4,[[35.2,6.8],[35.2,7.5],[34,7.5],[34,10.9],[45,10.9],[45,12.7],[45,18.8],[46.425,18.8]]),
 ('DAILY_02',4,[[45,12.7],[45,10.9],[90,10.9],[90,7.5],[91.2,7.5],[91.2,6.8]]),
 ('DAILY_02',0,[[88.7,6.8],[88.7,7.5],[90,7.5],[90,10.9],[90,13],[90,28]]),
 ('DAILY_03',4,[[45,12.7],[45,10.9],[146,10.9],[146,7.5],[147.2,7.5],[147.2,6.8]]),
 ('DAILY_03',0,[[144.7,6.8],[144.7,7.5],[146,7.5],[146,14],[150,14]])]
route_report=[]
for rid,z,pts in route_sets:
 blocked=[];count=0
 for a,b in zip(pts,pts[1:]):
  n=max(1,math.ceil(math.dist(a,b)/.20))
  for k in range(n+1):
   t=k/n;x=a[0]+(b[0]-a[0])*t;y=a[1]+(b[1]-a[1])*t;count+=1;hit=False
   for hz in [.10,.34,.96,1.58,1.82]:
    rr=.34 if .34<=hz<=1.58 else math.sqrt(.34**2-(.34-hz if hz<.34 else hz-1.58)**2)
    for j in range(16):
     aa=2*math.pi*j/16
     loc,normal,index,d=bvh.ray_cast(Vector((x,y,z+hz)),Vector((math.cos(aa),math.sin(aa),0)),rr)
     if loc is not None:hit=True;break
    if hit:break
   if hit:blocked.append([x,y,z])
 route_report.append(dict(id=rid,floor=z,points=pts,stations=count,blocked_stations=blocked,sampled_capsule_clear=not blocked))
(OUT/'MAIN_ROUTES.json').write_text(json.dumps(dict(method='0.20m stations / 16 radial directions / 5 heights of .68x1.92 capsule; actual WHOLE mesh BVH',
 scope='indoor horizontal sections and landings only; actual stair headroom separate; no continuous sweep/nav/crowds/outer map claim',routes=route_report),indent=2)+'\n',encoding='utf-8',newline='\n')
# Actual pulled-chair static seated envelope test. Contact surfaces have 1mm test inset.
for ob in arch:
 if ob.get('player_room_chair'):ob.location.x+=.25
bpy.context.view_layer.update()
sv=[];sf=[]
for ob in arch:
 if ob.name.startswith('F2_W4_') and ('DESK_' in ob.name or 'CHAIR_' in ob.name):
  off=len(sv);sv.extend(tuple(ob.matrix_world@v.co) for v in ob.data.vertices);sf.extend(tuple(off+i for i in p.vertices) for p in ob.data.polygons)
seatedbvh=BVHTree.FromPolygons(sv,sf)
seatresults=[]
for ob in check_objects():
 if not ob.name.startswith('POSE_PROXY'):continue
 vs=[ob.matrix_world@v.co for v in ob.data.vertices];lo=[min(v[i] for v in vs)+.001 for i in range(3)];hi=[max(v[i] for v in vs)-.001 for i in range(3)]
 x,y,z=lo;X,Y,Z=hi
 vv=[(x,y,z),(X,y,z),(X,Y,z),(x,Y,z),(x,y,Z),(X,y,Z),(X,Y,Z),(x,Y,Z)]
 ff=[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]
 overlaps=seatedbvh.overlap(BVHTree.FromPolygons(vv,ff))
 seatresults.append(dict(proxy=ob.name,bounds=[lo,hi],triangle_surface_intersections=len(overlaps)))
(OUT/'SEATED_STATIC_CHECK.json').write_text(json.dumps(dict(chair_state='all player chairs pulled.25m',contact_inset_m=.001,results=seatresults,
 scope='static proxy surface intersection only; no approved seated character/continuous transition/full occupancy certification'),indent=2)+'\n',encoding='utf-8',newline='\n')
for ob in arch:
 if ob.get('player_room_chair'):ob.location.x-=.25
bpy.context.view_layer.update()
def reset():
 for ob in arch:ob.hide_render=True
 for ob in check_objects():ob.hide_render=True
def camera(target,az,el,scale):
 cam=scene.camera;t=Vector(target);a=math.radians(az);e=math.radians(el)
 cam.location=t+Vector((math.cos(a)*math.cos(e),math.sin(a)*math.cos(e),math.sin(e)))*200
 cam.rotation_euler=(t-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale
log=json.loads((OUT/'CAMERAS.json').read_text())
def render(n,t,az,el,scale,w=2560,h=1440):
 camera(t,az,el,scale);scene.render.resolution_x=w;scene.render.resolution_y=h;scene.cycles.samples=24
 scene.render.filepath=str(PRE/(P+'_'+n+'.png'));bpy.ops.render.render(write_still=True)
 log.append(dict(file=Path(scene.render.filepath).name,target=t,azimuth=az,elevation=el,ortho_scale=scale,size=[w,h],display_only_cut=True,sun='same early summer sun/world/AgX'))
 (OUT/'CAMERAS.json').write_text(json.dumps(log,indent=2)+'\n',encoding='utf-8',newline='\n');print('ENVELOPE_RENDER',n,flush=True)
reset()
for ob in bpy.data.collections['CLASS_CUT_DEMO'].objects:ob.hide_render=False
for ob in arch:
 if ob.name.startswith('F2_W4_') or ob.name.startswith('OPEN_F2_W4_N'):ob.hide_render=False
for ob in [cap,capdoor]:ob.hide_render=False
for ob in check_objects():
 if ob.name.startswith('POSE_PROXY'):ob.hide_render=True
render('FINITE_CLASS',[45.2,17.3,4.8],315,30,13.5)
# Refresh pulled-pose evidence after the seat-contact correction. Same camera/daylight.
for ob in [cap,capdoor]:ob.hide_render=True
for ob in check_objects():
 if ob.name.startswith('POSE_PROXY'):ob.hide_render=False
for ob in arch:
 if ob.get('player_room_chair'):ob.location.x+=.25
bpy.context.view_layer.update()
log=[x for x in log if x['file']!=P+'_CLASS_PULLED.png']
render('CLASS_PULLED',[45.2,17.3,4.8],315,30,13.5)
for ob in arch:
 if ob.get('player_room_chair'):ob.location.x-=.25
bpy.context.view_layer.update()
reset()
for ob in bpy.data.collections['SHOE_CUT_DEMO'].objects:ob.hide_render=False
for ob in arch:
 if ob.name.startswith('LOCKER_MAIN') or ob.name.startswith('P1_') or ob.name=='OPEN_F1_WL_D_REV':ob.hide_render=False
for ob in ops+cross:ob.hide_render=False
render('FINITE_SHOE_FAIL',[24,4.5,.7],225,30,15)
reset()
for ob in cell:ob.hide_render=False
render('SHOE_CELL',[20.95,2.48,.73],60,30,.58,1600,1200)
# Density is compared on the same UV / 4m motif scale, using actual directly drawn128px variants.
# This avoids changing plank/tile physical dimensions along with texel density.
reset()
for ob in bpy.data.collections['DENSITY_DEMO'].objects:ob.hide_render=False
original_nodes=[]
for name in ['WALL','ENTRY_WOOD','FLOOR']:
 mat=bpy.data.materials[name];mat.node_tree.nodes['DENSITY_64_OR_32'].inputs[3].default_value=1
 for node in mat.node_tree.nodes:
  if node.type=='TEX_IMAGE':original_nodes.append((name,node,node.image))
log=[x for x in log if x['file'] not in [P+'_DENSITY_32.png',P+'_DENSITY_64.png']]
render('DENSITY_64',[1.05,-.05,.45],270,30,3.2,1600,1200)
for name,node,im in original_nodes:
 suffix='_R' if im.name.startswith(name+'_R') else '_BC'
 node.image=bpy.data.images.load(str(OUT/'Textures'/(name+'_32'+suffix+'.png')),check_existing=True)
 node.image.colorspace_settings.name='Non-Color' if suffix=='_R' else 'sRGB';node.image.pack();node.image.use_fake_user=True
render('DENSITY_32',[1.05,-.05,.45],270,30,3.2,1600,1200)
for name,node,im in original_nodes:node.image=im
stats=json.loads((OUT/'STATISTICS.json').read_text())
stats['texture_pngs']=len(list((OUT/'Textures').glob('*.png')))
(OUT/'STATISTICS.json').write_text(json.dumps(stats,indent=2)+'\n',encoding='utf-8',newline='\n')
G['stats']=stats;G['uv']['comparison32']='same4m UV; direct128px BC/R variants of wall, entry wood and floor'
(OUT/'GEOMETRY.json').write_text(json.dumps(G,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
reset()
for ob in arch:ob.hide_render=False
for ob in check_objects():ob.hide_render=False;ob.hide_viewport=False
check.hide_render=True;check.hide_viewport=True
camera([75,14,5.5],225,30,150);scene.render.resolution_x=2560;scene.render.resolution_y=1440
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/(P+'.blend')),compress=True)
print('ENHANCED_DONE headroom',headresult['min_clear'],'below capsule',len(headresult['below_capsule']),flush=True)
