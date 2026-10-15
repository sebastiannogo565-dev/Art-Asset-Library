"""Render localized evidence from the revised source; check layers never enter FBX."""
import bpy,bmesh,math,json
from pathlib import Path
from mathutils import Vector
OUT=Path(__file__).parent;P='SL_BLD_C01_MAIN_01_TRIAL_01_REV_01';PRE=OUT/'Previews';PRE.mkdir(exist_ok=True)
L=json.loads((OUT/'LAYOUT.json').read_text(encoding='utf-8'));SH=json.loads((OUT/'SHOE_CHECKS.json').read_text(encoding='utf-8'))
bpy.ops.wm.open_mainfile(filepath=str(OUT/(P+'.blend')))
scene=bpy.context.scene;whole=bpy.data.collections['WHOLE'];check=bpy.data.collections['REVISION_CHECK_ONLY_NO_EXPORT'];check.hide_render=False;check.hide_viewport=False
arch=[o for o in whole.all_objects if o.type=='MESH'];demo=[]
def col(n):
 c=bpy.data.collections.new(n);check.children.link(c);return c
cc=col('REV_CLASS_CUT');mc=col('REV_MAIN_CUT');lc=col('REV_LINK_CUT');posecol=col('REV_POSE_ASSUMPTION');charcol=col('REV_ORIGINAL_STANDING_ONLY')
def mat(n,c):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(*c,1);return m
green=mat('REV_CHECK_GREEN',(.08,.42,.24));blue=mat('REV_CHECK_BLUE',(.07,.28,.65));orange=mat('REV_CHECK_AMBER',(.85,.37,.06));red=mat('REV_CHECK_FAIL',(.75,.05,.04))
def cube(n,b,m,c):
 x,y,z,X,Y,Z=b;me=bpy.data.meshes.new(n);me.from_pydata([(x,y,z),(X,y,z),(X,Y,z),(x,Y,z),(x,y,Z),(X,y,Z),(X,Y,Z),(x,Y,Z)],[],[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]);me.materials.append(m)
 o=bpy.data.objects.new(n,me);c.objects.link(o);demo.append(o);return o
def outline(n,b,m,c):
 x,y,z,X,Y,Z=b;t=.012
 for k,(a,A) in enumerate([(x,X),(y,Y),(z,Z)]):
  for u in [0,1]:
   for v in [0,1]:
    q=[x,y,z];Q=[x+t,y+t,z+t];other=[i for i in range(3) if i!=k]
    for j,bit in zip(other,[u,v]):q[j]=[x,y,z][j] if not bit else [X,Y,Z][j]-t;Q[j]=q[j]+t
    q[k]=a;Q[k]=A;cube(n+f'_{k}_{u}{v}',q+Q,m,c)
def clipped(o,b,c):
 me=o.data.copy();bm=bmesh.new();bm.from_mesh(me)
 for axis in range(3):
  for pos,sign in [(b[axis],-1),(b[axis+3],1)]:
   no=[0,0,0];no[axis]=sign;co=[0,0,0];co[axis]=pos;bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=.00001,plane_co=co,plane_no=no,clear_outer=True)
 bm.to_mesh(me);bm.free()
 if not me.polygons:bpy.data.meshes.remove(me);return
 d=bpy.data.objects.new('REV_CUT_'+o.name,me);c.objects.link(d);demo.append(d)
for o in arch:
 if o.name=='SLAB_F02_ACTUAL':clipped(o,[40.8,12.5,3.7,49.6,22,4.01],cc)
 if o.name.startswith('PARTITIONS_F02'):
  clipped(o,[40.8,12.5,4,49.6,21.7,4.72],cc);clipped(o,[40.8,12.7,4.72,41,21.7,7.45],cc)
 if o.name.startswith('EXT_'):clipped(o,[40.8,21.7,4,49.6,22,7.45],cc)
 for c,b in [(mc,[18.1,0,-.25,29.9,9.1,0]),(lc,[52.1,12.8,-.25,63.9,22,0])]:
  if o.name=='SLAB_F01_ACTUAL':clipped(o,b,c)
  if o.name.startswith('PARTITIONS_F01'):clipped(o,[b[0],b[1],0,b[3],b[4],.6],c)
def line(n,pts,z,m,c):
 for i,(a,b) in enumerate(zip(pts,pts[1:])):
  # True diagonal line segment, not its bounding rectangle.
  a=Vector((a[0],a[1],z));b=Vector((b[0],b[1],z));d=b-a;mid=(a+b)/2
  o=cube(n+str(i),[-.025,-d.length/2,-.004,.025,d.length/2,.004],m,c);o.location=mid;o.rotation_euler=d.to_track_quat('Y','Z').to_euler()
for k in ['main_in_path','main_out_path']:line(k,L['shoe'][k],.025,green if 'in' in k else blue,mc)
for k in ['link_proposed_in','link_proposed_out']:line('CANDIDATE_'+k,L['shoe'][k],.025,green if 'in' in k else blue,lc)
for op in SH['operators']:
 a,b,A,B=op['rect'];c=mc if op['room']=='F1_WL' else lc
 cube(op['id']+'_ZONE',[a,b,.006,A,B,.018],green,c);outline(op['id']+'_PERSON',[a,b,.02,A,B,1.8],green,c)
for i,q in enumerate(L['shoe']['queues']):
 a,b,A,B=q['bounds'];outline('WAIT_'+str(i),[a,b,.02,A,B,1.8],orange,lc)
outline('REAL_DOOR_1_4',[57.3,12.94,0,58.7,13.02,2.6],red,lc)
outline('CANDIDATE_ONLY_2_4',[56.8,12.90,0,59.2,12.94,2.6],blue,lc)
# Original PNG is never edited. Its complete canvas preserves the alpha scale.
G=json.loads((OUT/'GEOMETRY.json').read_text(encoding='utf-8'));im=bpy.data.images.load(G['character']['source'],check_existing=True);im.pack()
cm=bpy.data.materials.new('REV_ORIGINAL_PNG');cm.use_nodes=True;ns=cm.node_tree.nodes;ns.clear();out=ns.new('ShaderNodeOutputMaterial');em=ns.new('ShaderNodeEmission');tx=ns.new('ShaderNodeTexImage');tx.image=im;tx.interpolation='Closest';tr=ns.new('ShaderNodeBsdfTransparent');mix=ns.new('ShaderNodeMixShader')
for a,b in [(tx.outputs['Color'],em.inputs['Color']),(tx.outputs['Alpha'],mix.inputs[0]),(tr.outputs[0],mix.inputs[1]),(em.outputs[0],mix.inputs[2]),(mix.outputs[0],out.inputs[0])]:cm.node_tree.links.new(a,b)
def figure(n,x,y,z,az,c):
 h=1.8*128/116;bottom=z-8/116*1.8;a=math.radians(az);right=Vector((-math.sin(a),math.cos(a),0))*h/2
 me=bpy.data.meshes.new(n);me.from_pydata([(x-right.x,y-right.y,bottom),(x+right.x,y+right.y,bottom),(x+right.x,y+right.y,bottom+h),(x-right.x,y-right.y,bottom+h)],[],[(0,1,2,3)]);me.materials.append(cm);uv=me.uv_layers.new()
 for d,v in zip(uv.data,[(0,0),(1,0),(1,1),(0,1)]):d.uv=v
 o=bpy.data.objects.new(n,me);c.objects.link(o);demo.append(o);o['visible_height']=1.8;o['capsule_height']=1.92;return o
doorchar=figure('REV_CHAR_DOOR',45,12.85,4,315,charcol)
movingchar=figure('REV_CHAR_OPERATOR',48.8,19.08,4,315,charcol)
outline('CAPSULE_STANDING_BOUND_068_192',[48.46,18.74,4,49.14,19.42,5.92],orange,charcol)
line('ARRIVE',[[45,12.7],[45,18.8],[48.8,18.8],[48.8,19.08]],4.02,green,cc)
line('EXIT_VIA_TEACHING',[[48.29,19.87],[48.29,18.8],[41.7,18.8],[45,18.8],[45,12.7]],4.03,blue,cc)
for n,x,y,m in [('BUSINESS',45,19.5,orange),('RECOVERY_CANDIDATE',45,18.7,blue)]:cube(n,[x-.06,y-.06,4.04,x+.06,y+.06,4.06],m,cc)
poses={}
for t in [0,.5,1]:
 c=col('REV_ASSUMPTION_POSE_'+str(t));poses[t]=c
 p=next(p for p in L['seated_motion']['poses'] if abs(p['t']-t)<1e-8)
 for item in p['parts']:
  # All interval proof boxes are real editable geometry; subdivisions are constant size bounds.
  cube('ASSUMPTION_'+str(t)+'_'+item['name'],item['bounds'],blue,c)
cam=scene.camera
def camera(target,az,el,scale):
 a=math.radians(az);e=math.radians(el);v=Vector(target);cam.location=v+Vector((math.cos(a)*math.cos(e),math.sin(a)*math.cos(e),math.sin(e)))*200;cam.rotation_euler=(v-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale
def reset():
 for c in whole.children:c.hide_render=False
 for o in arch:o.hide_render=True
 for o in demo:o.hide_render=True
def show(c):
 for o in c.all_objects:o.hide_render=False
def classview(t=None,pulled=False,standing=True):
 reset();show(cc);doorchar.hide_render=False
 for o in arch:
  if o.name.startswith('F2_W4_') or o.name.startswith('OPEN_F2_W4_N'):o.hide_render=False
 chair=bpy.data.objects['F2_W4_CHAIR_5_5'];chair.location.x=48.9 if pulled else 48.275
 if standing:movingchar.hide_render=False
 if t is not None:show(poses[t])
log=[]
def render(n,target,az,scale):
 camera(target,az,30,scale);scene.render.resolution_x=2560;scene.render.resolution_y=1440;scene.render.resolution_percentage=100;scene.cycles.samples=24
 scene.render.filepath=str(PRE/(P+'_'+n+'.png'));bpy.ops.render.render(write_still=True)
 log.append(dict(file=Path(scene.render.filepath).name,target=target,azimuth=az,elevation=30,ortho_scale=scale,size=[2560,1440],sun='unchanged original Sun/world/AgX',kind='actual local revised geometry with separate check layers; not game output'))
 (OUT/'CAMERAS.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');print('RENDER_DONE',n,flush=True)
classview(pulled=False);render('CLASS_REST_OPERATOR',[45.2,17.3,4.8],315,13.5)
classview(t=0,pulled=True,standing=False);render('CLASS_PULLED_APPROACH',[45.2,17.3,4.8],315,13.5)
classview(t=.5,pulled=True,standing=False);render('CLASS_TRANSITION_HALF',[45.2,17.3,4.8],315,13.5)
classview(t=1,pulled=True,standing=False);render('CLASS_SEATED_ASSUMPTION',[45.2,17.3,4.8],315,13.5)
classview(pulled=False,standing=False);render('CLASS_RESTORED',[45.2,17.3,4.8],315,13.5)
reset();show(mc)
for o in arch:
 if o.name.startswith('LOCKER_REV_MAIN_') or o.name in ['OPEN_F1_WL_D_REV','OPEN_C01_MAIN']:o.hide_render=False
render('SHOES_MAIN_SIMULTANEOUS',[24,4.5,.7],225,15)
reset();show(lc)
for o in arch:
 if o.name.startswith('LOCKER_REV_LINK_') or o.name in ['OPEN_F1_LW_D','P1_PHOTOS']:o.hide_render=False
render('SHOES_LINK_DOOR_CONFLICT',[58,17.3,.7],315,15)
for o in arch:o.hide_render=False
for o in demo:o.hide_render=False
bpy.data.objects['F2_W4_CHAIR_5_5'].location.x=48.275
check.hide_render=True;check.hide_viewport=True;camera((75,14,5.5),225,30,150)
scene.render.filepath='';bpy.ops.wm.save_as_mainfile(filepath=str(OUT/(P+'.blend')),compress=True)
print('REVISION_LOCAL_PREVIEWS_COMPLETE',flush=True)
