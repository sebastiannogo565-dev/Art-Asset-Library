"""Four necessary actual localized previews; same inherited daylight, editable check layers."""
import bpy,bmesh,json,ast,math
from pathlib import Path
from mathutils import Vector
O=Path(__file__).parent;B=O.parent/'Revision01';P='SL_BLD_C01_MAIN_01_TRIAL_01_REV_02';PRE=O/'Previews';PRE.mkdir(exist_ok=True)
L=json.loads((O/'LAYOUT.json').read_text(encoding='utf-8'));A=json.loads((O/'ACTIVITY_DISTANCE.json').read_text(encoding='utf-8'))
bpy.ops.wm.open_mainfile(filepath=str(O/(P+'.blend')));scene=bpy.context.scene;cam=scene.camera;whole=bpy.data.collections['WHOLE'];check=bpy.data.collections['REV02_CHECK_ONLY_NO_EXPORT'];check.hide_render=False;check.hide_viewport=False
arch=[o for o in list(whole.all_objects) if o and o.type=='MESH'];demo=[]
tree=ast.parse((B/'render_revision.py').read_text(encoding='utf-8'));exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['mat','cube','outline','clipped','line','figure','camera']],type_ignores=[]),'inherited render helpers','exec'),globals())
def col(n):c=bpy.data.collections.new(n);check.children.link(c);return c
lc=col('REV02_WESTLINK_CUT');dc=col('REV02_DOOR_HALL_CUT');cc=col('REV02_CLASS_OPERATION_CUT');pc=col('REV02_BENCH_POSE_ASSUMPTION')
green=mat('REV02_CHECK_GREEN',(.08,.42,.24));blue=mat('REV02_CHECK_BLUE',(.07,.28,.65));amber=mat('REV02_CHECK_AMBER',(.85,.37,.06))
for o in arch:
 if o.name=='SLAB_F01_ACTUAL':
  clipped(o,[52.1,10.4,-.25,63.9,22,0],lc);clipped(o,[52.1,10.4,-.25,63.9,17,0],dc)
 if o.name.startswith('PARTITIONS_F01'):
  clipped(o,[52.1,12.8,0,63.9,22,.6],lc)
  clipped(o,[52.1,12.8,0,63.9,13,3.45],dc)
 if o.name=='SLAB_F02_ACTUAL':clipped(o,[40.8,12.5,3.7,49.6,22,4.01],cc)
 if o.name.startswith('PARTITIONS_F02'):
  clipped(o,[40.8,12.5,4,49.6,21.7,4.72],cc);clipped(o,[40.8,12.7,4.72,41,21.7,7.45],cc)
 if o.name.startswith('EXT_'):clipped(o,[40.8,21.7,4,49.6,22,7.45],cc)
for op in L['operators']:
 if op['room']!='F1_LW':continue
 a,b,X,Y=op['rect'];cube(op['id']+'_ZONE',[a,b,.005,X,Y,.015],green,lc);outline(op['id'],[a,b,.015,X,Y,1.8],green,lc)
for i,q in enumerate(L['queues']):a,b,X,Y=q['bounds'];outline('REV02_WAIT_'+str(i),[a,b,.015,X,Y,1.8],amber,lc)
for q in L['paths']:
 if q['id'] in ['DOOR_IN_SIMULTANEOUS','DOOR_OUT_SIMULTANEOUS']:line(q['id'],q['points'],.025,green if 'IN_' in q['id'] else blue,lc)
for q in L['paths']:
 if q['id'] in ['DOOR_TO_TAKE','BENCH_APPROACH','RISE_TO_PUBLIC','WAIT_TO_EXIT']:line('LOOP_'+q['id'],q['points'],.035,amber,lc)
# Actual same-size proxies, not edited character art. Keep fixed feet/pelvis/legs and full-width lower envelope.
pose=next(p for p in L['bench_poses'] if p['t']==1)
for shift,lean in [(-1.2,False),(0,True)]:
 for q in pose['parts']:
  if lean and q['name']=='UPPER':continue
  b=q['bounds'][:];b[0]+=shift;b[3]+=shift
  if q['name'] in ['UPPER','PELVIS','FEET']:cube('REV02_BODY_'+str(shift)+q['name'],b,blue,pc)
  else:outline('REV02_BOUND_'+str(shift)+q['name'],b,blue,pc)
 if lean:
  W=1.039655172413793;o=cube('REV02_CONSTANT_SIZE_UPPER_BEND',[-W/2,-.34,0,W/2,0,.87],blue,pc);o.location=(54.6,13.635,.52);o.rotation_euler.x=math.radians(-65)
  cube('REV02_SHOES_FLOOR',L['shoe_change']['floor_shoe'],amber,pc)
  for i,(a,b) in enumerate(zip([L['shoe_change']['shoulder'],L['shoe_change']['elbow']],[L['shoe_change']['elbow'],L['shoe_change']['hand']])):
   a=Vector(a);b=Vector(b);d=b-a;o=cube('REV02_ARM_LINK_'+str(i),[-.025,-d.length/2,-.025,.025,d.length/2,.025],amber,pc);o.location=(a+b)/2;o.rotation_euler=d.to_track_quat('Y','Z').to_euler()
# Original unedited standing PNG billboard, separate actor-centre marker.
G=json.loads((O/'GEOMETRY.json').read_text(encoding='utf-8'));im=bpy.data.images.load(G['character']['source'],check_existing=True);im.pack()
cm=bpy.data.materials.new('REV02_ORIGINAL_PNG');cm.use_nodes=True;ns=cm.node_tree.nodes;ns.clear();out=ns.new('ShaderNodeOutputMaterial');em=ns.new('ShaderNodeEmission');tx=ns.new('ShaderNodeTexImage');tx.image=im;tx.interpolation='Closest';tr=ns.new('ShaderNodeBsdfTransparent');mix=ns.new('ShaderNodeMixShader')
for a,b in [(tx.outputs['Color'],em.inputs['Color']),(tx.outputs['Alpha'],mix.inputs[0]),(tr.outputs[0],mix.inputs[1]),(em.outputs[0],mix.inputs[2]),(mix.outputs[0],out.inputs[0])]:cm.node_tree.links.new(a,b)
figure('REV02_CHAR_OPERATION',45,19.5,4,315,cc);figure('REV02_CHAR_DOOR',45,12.85,4,315,cc)
line('REV02_CLASS_REACH',[[45,12.7],[45,18.8],[45,19.5]],4.025,green,cc)
cube('REV02_G_OPERATION',[44.94,19.44,4.03,45.06,19.56,4.045],green,cc)
cube('REV02_ACTOR_P_EQUALS_E_096',[44.96,19.46,4.92,45.04,19.54,5.0],amber,cc)
outline('REV02_SEAT_3_5_CANDIDATE',[45.55,19.50,4,46.45,20.25,4.90],amber,cc)
outline('REV02_OLD5_5_STUDY_ONLY',[47.49,19.50,4,48.58,20.25,4.9],blue,cc)
log=[]
def reset():
 for c in whole.children:c.hide_render=False
 for o in arch:o.hide_render=True
 for o in demo:o.hide_render=True
def show(c):
 for o in list(c.all_objects):
  if o:o.hide_render=False
def showlink():
 for o in arch:
  if o.name.startswith('LOCKER_REV_LINK_') or o.name in ['REV02_CHANGE_BENCH','OPEN_F1_LW_D','P1_PHOTOS']:o.hide_render=False
def render(n,t,az,scale):
 camera(t,az,30,scale);scene.render.resolution_x=2560;scene.render.resolution_y=1440;scene.render.resolution_percentage=100;scene.cycles.samples=24
 scene.render.filepath=str(PRE/(P+'_'+n+'.png'));bpy.ops.render.render(write_still=True)
 log.append(dict(file=Path(scene.render.filepath).name,target=t,azimuth=az,elevation=30,ortho_scale=scale,size=[2560,1440],sun='unchanged original Sun/world/AgX',scope='actual revised mesh plus editable cuts/proxies;not game/approved character pose'))
 (O/'CAMERAS.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');print('RENDER_DONE',n,flush=True)
reset();show(lc);show(pc);showlink();render('WESTLINK_CHANGE_LOOP',[58,17,.8],315,15)
reset();show(lc);show(pc);showlink();render('CHANGE_SEAT_CLOSE',[54.7,14.15,.70],90,5.8)
reset();show(dc);showlink();render('DOOR_HALL_APPROACH',[58,13.8,1.1],270,8)
reset();show(cc)
for o in arch:
 if o.name.startswith('F2_W4_') or o.name.startswith('OPEN_F2_W4_N'):o.hide_render=False
render('CLASS_OPERATION_P_EQUALS_E',[45.2,17.3,4.8],315,13.5)
for o in arch:o.hide_render=False
for o in demo:o.hide_render=False
check.hide_render=True;check.hide_viewport=True;camera((75,14,5.5),225,30,150);scene.render.filepath=''
bpy.ops.wm.save_as_mainfile(filepath=str(O/(P+'.blend')),compress=True);print('REV02_PREVIEWS_COMPLETE',flush=True)
