"""Natural-light renders of the actual trial and explicitly separate editable check layers."""
import bpy,bmesh,math,json
from pathlib import Path
from mathutils import Vector
OUT=Path(__file__).parent;P='SL_BLD_C01_MAIN_01_TRIAL_01';PRE=OUT/'Previews';PRE.mkdir(exist_ok=True)
G=json.loads((OUT/'GEOMETRY.json').read_text(encoding='utf-8'))
bpy.ops.wm.open_mainfile(filepath=str(OUT/(P+'.blend')))
scene=bpy.context.scene;whole=bpy.data.collections['WHOLE'];context=bpy.data.collections['CONTEXT_NO_EXPORT']
check=bpy.data.collections['CHECK_ONLY_NO_EXPORT'];check.hide_render=False;check.hide_viewport=False
arch=[o for o in whole.all_objects if o.type=='MESH'];demo=[]
def col(n):
 c=bpy.data.collections.new(n);check.children.link(c);return c
classcol=col('CLASS_CUT_DEMO');shoecol=col('SHOE_CUT_DEMO');staircol=col('STAIR_CUT_DEMO');texcol=col('DENSITY_DEMO')
def solid(name,color):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(*color,1);return m
green=solid('CHECK_GREEN',(.12,.55,.34));orange=solid('CHECK_ORANGE',(.85,.34,.12));blue=solid('CHECK_BLUE',(.15,.42,.7))
def cube(name,b,m,c):
 x,y,z,X,Y,Z=b
 me=bpy.data.meshes.new(name);me.from_pydata([(x,y,z),(X,y,z),(X,Y,z),(x,Y,z),(x,y,Z),(X,y,Z),(X,Y,Z),(x,Y,Z)],[],[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]);me.materials.append(m)
 ob=bpy.data.objects.new(name,me);c.objects.link(ob);demo.append(ob);return ob
def clipped(ob,region,c):
 if not ob.data.vertices:return
 me=ob.data.copy();bm=bmesh.new();bm.from_mesh(me)
 for axis in range(3):
  for pos,sign in [(region[axis],-1),(region[axis+3],1)]:
   normal=[0,0,0];normal[axis]=sign;co=[0,0,0];co[axis]=pos
   bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=.00001,plane_co=co,plane_no=normal,clear_outer=True,clear_inner=False)
 bm.to_mesh(me);bm.free()
 if not len(me.polygons):bpy.data.meshes.remove(me);return
 dup=bpy.data.objects.new('CUT_'+ob.name,me);c.objects.link(dup);demo.append(dup);return dup
# Derived cuts use actual source wall/floor meshes. Display-only cut edges can be open.
for ob in arch:
 if ob.name=='SLAB_F02_ACTUAL':clipped(ob,[40.8,12.5,3.7,49.6,22,4.01],classcol)
 if ob.name.startswith('PARTITIONS_F02'):
  clipped(ob,[40.8,12.5,4,49.6,21.7,4.72],classcol)
  clipped(ob,[40.8,12.7,4.72,41,21.7,7.45],classcol)
 if ob.name.startswith('EXT_'):clipped(ob,[40.8,21.7,4,49.6,22,7.45],classcol)
 if ob.name=='SLAB_F01_ACTUAL':clipped(ob,[18.1,0,-.25,29.9,9.1,0],shoecol)
 if ob.name.startswith('PARTITIONS_F01'):clipped(ob,[18.1,0,0,29.9,9.1,.6],shoecol)
 if ob.name=='SLAB_F01_ACTUAL':clipped(ob,[30,0,-.25,38,9.1,0],staircol)
 if ob.name=='SLAB_F02_ACTUAL':clipped(ob,[30,0,3.75,38,9.1,4],staircol)
 if ob.name=='CEILING_F01':clipped(ob,[30,0,3.45,38,9.1,3.48],staircol)
# True, unchanged source PNG as an unlit check billboard. Full visible width retained.
im=bpy.data.images.load(G['character']['source'],check_existing=True);im.pack()
char=bpy.data.materials.new('CHECK_ORIGINAL_CHARACTER');char.use_nodes=True
ns=char.node_tree.nodes;ns.clear();out=ns.new('ShaderNodeOutputMaterial');em=ns.new('ShaderNodeEmission');tex=ns.new('ShaderNodeTexImage');tex.image=im;tex.interpolation='Closest'
tr=ns.new('ShaderNodeBsdfTransparent');mix=ns.new('ShaderNodeMixShader')
char.node_tree.links.new(tex.outputs['Color'],em.inputs['Color']);char.node_tree.links.new(tex.outputs['Alpha'],mix.inputs[0]);char.node_tree.links.new(tr.outputs[0],mix.inputs[1]);char.node_tree.links.new(em.outputs[0],mix.inputs[2]);char.node_tree.links.new(mix.outputs[0],out.inputs[0])
def figure(name,x,y,z,az,c):
 # Screen-right vector perpendicular to camera azimuth, original alpha canvas retained.
 h=1.8*128/116;bottom=z-8/116*1.8;a=math.radians(az);right=Vector((-math.sin(a),math.cos(a),0))*h/2
 v=[(x-right.x,y-right.y,bottom),(x+right.x,y+right.y,bottom),(x+right.x,y+right.y,bottom+h),(x-right.x,y-right.y,bottom+h)]
 me=bpy.data.meshes.new(name);me.from_pydata(v,[],[(0,1,2,3)]);me.materials.append(char);uv=me.uv_layers.new()
 for d,v in zip(uv.data,[(0,0),(1,0),(1,1),(0,1)]):d.uv=v
 ob=bpy.data.objects.new(name,me);c.objects.link(ob);demo.append(ob);ob['source_png_unchanged']=True;return ob
charclass=[figure('CHAR_DOOR',45,12.85,4,315,classcol),figure('CHAR_TURN',45,18.8,4,315,classcol),figure('CHAR_SEAT_SIDE',48.8,19.87,4,315,classcol)]
figure('CHAR_SHOE_ENTRY',25,.9,0,225,shoecol);figure('CHAR_SHOE_USER',21,3.00,0,225,shoecol)
figure('CHAR_STAIR',32.7,7.5,0,315,staircol);figure('CHAR_LANDING',35.2,7.6,4,315,staircol)
def route(points,z,width,m,c,prefix):
 for i,(a,b) in enumerate(zip(points,points[1:])):
  # Boxes aligned to cardinal route segments, green width refers to centreline indicator only.
  cube(prefix+str(i),[min(a[0],b[0])-width/2,min(a[1],b[1])-width/2,z,max(a[0],b[0])+width/2,max(a[1],b[1])+width/2,z+.008],m,c)
route(G['player_interface']['route_to_approach'],4.005,.055,green,classcol,'ROUTE_TO_')
route(G['player_interface']['route_return_via_teaching'],4.015,.035,blue,classcol,'RETURN_')
cube('BUSINESS_CLEAR_MARK',[44.94,19.44,4.008,45.06,19.56,4.02],orange,classcol)
cube('RECOVERY_CANDIDATE',[44.94,18.64,4.022,45.06,18.76,4.035],blue,classcol)
# A finite seated-pose candidate kept distinct from original character: side approach, no standing through back.
seatdemo=[]
for name,b in [('TORSO',[46.15,19.3501724,4.43,46.48,20.3898276,5.23]),('HEAD',[46.15,19.3501724,5.23,46.48,20.3898276,5.55]),('THIGHS',[45.87,19.62,4.43,46.3,20.12,4.65]),('SHINS',[45.87,19.62,4,46.02,20.12,4.44])]:
 seatdemo.append(cube('POSE_PROXY_'+name,b,blue,classcol))
for ob in seatdemo:
 if ob.name in ['POSE_PROXY_THIGHS','POSE_PROXY_SHINS']:
  for v in ob.data.vertices:v.co.x+=.06
# Operating strips are solid low markers; full-height directional cuboids show finite use envelopes separately.
active=cube('ACTIVE_USE',[20.48,2.63,.004,21.52,3.33,.018],green,shoecol)
opposite=cube('OPPOSITE_USE_FAIL',[20.48,3.87,.004,21.52,4.57,.018],orange,shoecol)
for x,y in [(22.9,6.2),(22.9,7.9)]:cube('QUEUE_FAIL',[x-.34,y-.34,.01,x+.34,y+.34,.04],orange,shoecol)
# 1m density panel and matching-camera comparison. Same actual material/UV, scale node switches1/.5.
for name,b in [('DENSITY_WALL',[0,0,0,1,.05,1]),('DENSITY_WOOD',[1.1,0,0,2.1,.05,1]),('DENSITY_FLOOR',[0,-1,0,2.1,0,.02])]:
 mat=bpy.data.materials['ENTRY_WOOD' if 'WOOD' in name else 'FLOOR' if 'FLOOR' in name else 'WALL']
 ob=cube(name,b,mat,texcol);uv=ob.data.uv_layers.new(name='UV_METRIC_64')
 for p in ob.data.polygons:
  n=p.normal;axis=max(range(3),key=lambda i:abs(n[i]));u=Vector((0,1,0)) if axis==0 else Vector((1,0,0));v=n.cross(u)
  for li in p.loop_indices:
   co=ob.data.vertices[ob.data.loops[li].vertex_index].co;uv.data[li].uv=(co.dot(u)/4,co.dot(v)/4)
cam=scene.camera
def camera(t,az,el,scale):
 a=math.radians(az);e=math.radians(el);v=Vector(t);cam.location=v+Vector((math.cos(a)*math.cos(e),math.sin(a)*math.cos(e),math.sin(e)))*200
 cam.rotation_euler=(v-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale
def reset():
 for c in whole.children:c.hide_render=False
 for o in arch:o.hide_render=False
 for o in demo:o.hide_render=True
 for m in bpy.data.materials:
  if m.use_nodes and m.node_tree.nodes.get('DENSITY_64_OR_32'):m.node_tree.nodes['DENSITY_64_OR_32'].inputs[3].default_value=1
 for o in arch:
  if o.get('player_room_chair'):o.location.x=float(o.location.x) # pull restored explicitly in render routine
def showdemo(c):
 for o in demo:
  if o.name in c.objects:o.hide_render=False
log=[]
def render(n,target,az,el,scale,w=2560,h=1440):
 camera(target,az,el,scale);scene.render.resolution_x=w;scene.render.resolution_y=h;scene.render.resolution_percentage=100;scene.cycles.samples=24
 scene.render.filepath=str(PRE/(P+'_'+n+'.png'));bpy.ops.render.render(write_still=True)
 log.append(dict(file=Path(scene.render.filepath).name,target=target,azimuth=az,elevation=el,ortho_scale=scale,size=[w,h],sun='same early summer sun/world/AgX',display_only_cut=n not in ['A','B','ENTRY','ROOF']))
 (OUT/'CAMERAS.json').write_text(json.dumps(log,indent=2)+'\n',encoding='utf-8',newline='\n');print('RENDER_DONE',n,flush=True)
reset();render('A',[75,14,5.5],225,30,150)
reset();render('B',[75,14,5.5],45,30,150)
reset();render('ENTRY',[25,3,2],240,30,20)
reset();render('ROOF',[80,16,5],225,75,156)
reset()
for c in whole.children:
 if c.name in ['ROOF','EXTERIOR'] or c.name.startswith('CEILING') or c.name.startswith('PARTITIONS'):c.hide_render=True
render('LAYERS',[75,14,4],225,40,152)
# Floor2 isolation, retain all independent stair supports as requested.
reset()
for c in whole.children:
 if c.name in ['ROOF','EXTERIOR'] or c.name.startswith('CEILING') or c.name.endswith('F01') or c.name.endswith('F03'):c.hide_render=True
render('F02',[75,14,4.5],225,40,150)
reset()
for ob in arch:ob.hide_render=True
showdemo(classcol)
for ob in arch:
 if ob.name.startswith('F2_W4_') or ob.name.startswith('OPEN_F2_W4_N'):ob.hide_render=False
for ob in seatdemo:ob.hide_render=True
render('CLASS_REST',[45.2,17.3,4.8],315,30,13.5)
for ob in arch:
 if ob.get('player_room_chair'):ob.location.x+=.25
for ob in seatdemo:ob.hide_render=False
render('CLASS_PULLED',[45.2,17.3,4.8],315,30,13.5)
for ob in arch:
 if ob.get('player_room_chair'):ob.location.x-=.25
# Same camera narrow/door scale evidence is included in class pair. Side pose gives explicit proxy/art distinction.
reset()
for ob in arch:ob.hide_render=True
showdemo(shoecol);opposite.hide_render=True
for ob in arch:
 if ob.name.startswith('LOCKER_MAIN') or ob.name.startswith('P1_') or ob.name=='OPEN_F1_WL_D_REV':ob.hide_render=False
render('SHOES_ONE_SIDE',[24,4.5,.7],225,30,15)
opposite.hide_render=False
render('SHOES_TWO_SIDE_FAIL',[24,4.5,.7],225,30,15)
reset()
for ob in arch:ob.hide_render=True
showdemo(staircol)
for ob in arch:
 if ob.get('group')=='STAIR_CORE_S1':ob.hide_render=False
render('STAIR',[34,4.6,3.8],315,30,13.5)
# Court and terrace source geometry with top and near walls removed, no substitute geometry.
reset()
for c in whole.children:
 if c.name=='ROOF' or c.name.startswith('CEILING'):c.hide_render=True
for ob in arch:
 if ob.name.startswith('EXT_') or ob.name.startswith('PARTITIONS_'):ob.hide_render=True
render('COURT_TERRACE',[79,14,4.7],225,30,41)
reset()
for ob in arch:ob.hide_render=True
showdemo(texcol)
render('DENSITY_64',[1.05,-.05,.45],270,30,3.2,1600,1200)
for m in bpy.data.materials:
 if m.use_nodes and m.node_tree.nodes.get('DENSITY_64_OR_32'):m.node_tree.nodes['DENSITY_64_OR_32'].inputs[3].default_value=.5
render('DENSITY_32',[1.05,-.05,.45],270,30,3.2,1600,1200)
reset();camera((75,14,5.5),225,30,150)
for o in demo:o.hide_render=False;o.hide_viewport=False
check.hide_render=True;check.hide_viewport=True
scene.render.resolution_x=2560;scene.render.resolution_y=1440
# Source contains editable check layers, hidden by default; export remains only WHOLE.
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/(P+'.blend')),compress=True)
print('ALL_PREVIEWS_DONE',flush=True)
