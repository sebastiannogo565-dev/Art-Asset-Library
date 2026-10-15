"""Revision02 low-detail layout, read-only code evidence, separate 3D coordinate cases."""
from pathlib import Path
import json,hashlib,math,ast,csv
O=Path(__file__).parent;B=O.parent/'Revision01';R=Path('D:/Art Asset Library');P='SL_BLD_C01_MAIN_01_TRIAL_01_REV_02'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def write(n,v):(O/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
L=read(B/'LAYOUT.json');G=read(B/'GEOMETRY.json');S=L['shoe'];ev=read(R/'Docs/AssetPlanning/BuildingProduction/C01/activity-distance-code-evidence.json')
sources=[]
for q in ev['sources']:
 a=Path(q['path']);s=sha(a);sources.append(dict(path=str(a),sha256=s,planning_evidence_sha=q['sha256'],matches=s==q['sha256']))
assert all(q['matches'] for q in sources),'Read-only code changed; inspect before adopting interface assumptions'
write('CODE_EVIDENCE.json',dict(sources=sources,logic=ev['verified_logic'],runtime_anchor_read=False,
 current_runtime_actor_transform_read=False,scope='Read source files and historical recipe only; no PIE/map transform readback, no UE writes'))
if not (O/'protected_inputs.json').exists():
 paths={Path(v['path']) for v in read(B/'protected_inputs.json')};paths.update(p for p in B.rglob('*') if p.is_file() and p.suffix not in ['.blend1','.pyc'] and '__pycache__' not in p.parts)
 paths.update(R/('Docs/AssetPlanning/BuildingProduction/'+n) for n in ['TaskCards/SL_BLD_C01_MAIN_01_TRIAL_01.md','review-C01-trial-revision-01.md','C01/trial-revision-01-planning-audit.json','C01/activity-distance-code-evidence.json'])
 paths.update(Path(q['path']) for q in sources);write('protected_inputs.json',[dict(path=str(p),sha256=sha(p)) for p in sorted(paths) if p.exists()])
# Reuse definitions only. Never run the original module: it writes Revision01 files.
tree=ast.parse((B/'validate_layout.py').read_text(encoding='utf-8'));defs=[n for n in tree.body if isinstance(n,ast.FunctionDef)]
ns=dict(math=math,W=1.039655172413793)
exec(compile(ast.Module(body=defs,type_ignores=[]),'Revision01/validate_layout.py definitions only','exec'),ns)
W=ns['W'];sep=ns['separation'];hull=ns['hull'];standing=ns['standing'];sweep=ns['swept_standing']
# Keep the original 19-stage study immutable, with explicit source hashes and unchanged classroom fingerprint.
write('INHERITED_STUDY.json',dict(source='../Revision01/LAYOUT.json',sha256=sha(B/'LAYOUT.json'),stage_ids=[s['id'] for s in L['segments']],
 stages=19,retested_stages=[],inherited_stages=19,reason='No classroom furniture/room/door changes; necessary standing branch from stage01 cross-aisle to activity operation, not an extra seating stage/prerequisite',
 study_seat='F2_W4_DESK_5_5',final_seat_bound=False,pose_assumption=L['proxy'],seat_status_source='../Revision01/SEATS.csv',other29_pose='unverified'))
bench=dict(id='REV02_CHANGE_BENCH',bounds=[52.8,13.15,0,55.2,13.60,.43],seat_height=.43,seat_depth=.45,length=2.4,
 centers=[[53.4,13.465,.43],[54.6,13.465,.43]],standing_fronts=[[53.4,14.05,0],[54.6,14.05,0]],faces='north',nominal_users=2,
 usage_bounds=[[53.4-W/2,13.15,53.4+W/2,14.45],[54.6-W/2,13.15,54.6+W/2,14.45]],
 type='two-person flat wood bench, six legs, no back; conditional full-width bend/feet envelope, not approved character pose')
door=dict(id='F1_LW_D',interface_center=[58,13,0],wall_midline_y=12.9,clear_width=2.4,clear_height=2.6,
 lo=56.8,hi=59.2,wall_thickness_y=[12.8,13.0],frame_y=[12.8,13.0],parked_leaf_y=[12.71,12.75],
 leaf_x=[[55.53,56.73],[59.27,60.47]],old_width=1.4,additional_opening_face_m2=2.6,new_ground_area_m2=0)
ops=read(B/'SHOE_CHECKS.json')['operators'];queues=S['queues'];obs=[]
def ob(n,b):return dict(id=n,bounds=b)
for b in S['banks']:obs.append(ob(b['id'],b['bounds']))
for q in ops:
 a,b,A,Bb=q['rect'];obs.append(ob(q['id'],[a,b,0,A,Bb,1.8]))
for i,q in enumerate(queues):
 a,b,A,Bb=q['bounds'];obs.append(ob('WAIT_'+str(i),[a,b,0,A,Bb,1.8]))
obs+= [ob('WALL_W',[52.1,13,0,52.3,22,3.45]),ob('WALL_E',[63.7,13,0,63.9,22,3.45]),ob('WALL_N',[52.3,21.7,0,63.7,22,3.45]),
 ob('WALL_S_L',[52.3,12.8,0,56.8,13,3.45]),ob('WALL_S_R',[59.2,12.8,0,63.7,13,3.45]),ob('HEADER',[56.8,12.8,2.6,59.2,13,3.45])]
for i,(a,b) in enumerate(door['leaf_x']):obs.append(ob('PARKED_LEAF_'+str(i),[a,12.71,0,b,12.75,2.6]))
def benchparts():
 r=[ob('BENCH_SEAT',[52.8,13.15,.395,55.2,13.6,.43])]
 for x in [52.95,54.0,55.05]:
  for y in [13.23,13.52]:r.append(ob('BENCH_LEG',[x-.025,y-.025,0,x+.025,y+.025,.395]))
 return r
obs+=benchparts()
# Transform inherited west-facing body exactly (rotation -90deg) into north-facing bench coordinates.
def toworld(b,cx=54.6):
 x,y,z,X,Y,Z=b;return [cx+y-19.87,14.05-(X-48.29),z,cx+Y-19.87,14.05-(x-48.29),Z]
def toold(b,cx=54.6):
 x,y,z,X,Y,Z=b;return [48.29+14.05-Y,19.87+x-cx,z,48.29+14.05-y,19.87+X-cx,Z]
other_user=ob('OTHER_BENCH_USER_LEFT',[53.4-W/2,13.15,0,53.4+W/2,14.45,1.8])
# Other user remains present; bench and own seated pelvis contact are retained.
transition_obs=obs+[other_user]
ns['pullobs']=[ob(o['id'],toold(o['bounds'])) for o in transition_obs]
motion=ns['transition']();assert motion['passed'],motion['blocked'][:5]
poses=[]
for p in motion['poses']:
 poses.append(dict(t=p['t'],parts=[dict(name=q['name'],bounds=toworld([v-4 if i in [2,5] else v for i,v in enumerate(q['bounds'])])) for q in p['parts']]))
motion['method']='Inherited analytic1000-interval body bounds rotated90deg into bench frame; actual bench seat/6legs and other bench user retained; no body inset, contact only,10um tolerance'
# Bend the same full-size upper box about its front lower edge; pelvis/legs/feet remain.
# No inset or dimension reduction. 65deg bend permits a .8m two-link reach to shoe at z.16.
angle=math.radians(65);pivot=(13.465+.17,.52);bend=[];worst=(99,None,None);bad=[]
def bendbox(a,b):
 # Rotation YZ support for upper [-.34,0] alongY, [0,.87] above pivot.
 cs=[math.cos(a),math.cos(b)];ss=[math.sin(a),math.sin(b)]
 return [54.6-W/2,pivot[0]-.34*max(cs),pivot[1],54.6+W/2,pivot[0]+.87*max(ss),pivot[1]+.34*max(ss)+.87*max(cs)]
for k in range(260):
 a=angle*k/260;b=angle*(k+1)/260;bb=bendbox(a,b);r=ns['static_near']([('FULL_SIZE_UPPER_BEND',bb)],transition_obs)
 if r[0]<worst[0]:worst=r
 if r[0]<-1e-5:bad.append([k,r])
 if k in [0,130,259]:bend.append(dict(angle_deg=math.degrees(b),bounds=bendbox(b,b)))
assert not bad,bad[:3]
shoulder=[54.6,pivot[0]-.17*math.cos(angle)+.6*math.sin(angle),pivot[1]+.17*math.sin(angle)+.6*math.cos(angle)]
hand=[54.6,14.15,.16];reach=math.dist(shoulder,hand);assert reach<=.8
dy,dz=hand[1]-shoulder[1],hand[2]-shoulder[2];q=math.sqrt(.4**2-(reach/2)**2)/reach
elbow=[54.6,(hand[1]+shoulder[1])/2-dz*q,(hand[2]+shoulder[2])/2+dy*q]
shoe_change=dict(bend_angle=65,upper_dimensions_unchanged=[.34,W,.87],bend_intervals=260,min_clearance=worst[0],passed=not bad,
 pivot_front_lower_yz=list(pivot),poses=bend,shoulder=shoulder,elbow=elbow,hand=hand,hand_distance=reach,arm_length=.8,
 hand_scope='two-link geometric reach only; real grasp, balance and character pose not certified',
 floor_shoe=[54.4825,14.10,.015,54.7175,14.39,.13],hands_feet_use_zone=[54.08,13.15,0,55.12,14.45,1.8])
# Check only changed local flow, not extra classroom stages. East-facing before turn; north-facing bench approach.
useobs=[o for o in obs if o['id'] not in ['REV_LINK_MID_OP-1_0','WAIT_0']]+[other_user]
paths=[]
def path(n,pts,yaw,obstacles=useobs):
 vals=[sweep(a,b,yaw,yaw,obstacles) for a,b in zip(pts,pts[1:])]
 paths.append(dict(id=n,points=pts,yaw=yaw,passed=all(v['passed'] for v in vals),min_clearance=min(v['min_separation'] for v in vals),details=vals))
path('DOOR_TO_TAKE',[[57.4,11.6],[57.4,14.7],[55.64,14.7],[55.64,15.85]],math.pi)
path('TAKE_TO_TURN',[[55.64,15.85],[55.64,14.7],[55.8,14.7]],math.pi)
turn=sweep([55.8,14.7],[55.8,14.7],math.pi,math.pi*1.5,useobs);assert turn['passed'],turn
path('BENCH_APPROACH',[[55.8,14.7],[55.8,14.05],[54.6,14.05]],-math.pi/2)
path('RISE_TO_PUBLIC',[[54.6,14.05],[55.8,14.05],[55.8,14.7],[58,14.7],[58,21.1],[61.6,21.1],[61.6,14.55]],-math.pi/2)
path('PUBLIC_TO_WAIT',[[61.6,14.55],[62.9,14.55]],0)
path('WAIT_TO_EXIT',[[62.9,14.55],[61.6,14.55],[61.6,13.6],[58.6,13.6],[58.6,11.6]],0)
# Recheck the approved two-way door approaches with every locker operator and six queues present.
doorobs=obs+[other_user,ob('RIGHT_BENCH_USE',[54.6-W/2,13.15,0,54.6+W/2,14.45,1.8])]
path('DOOR_IN_SIMULTANEOUS',[[57.4,11.6],[57.4,14.7],[58,15.1],[58,21.1]],-math.pi/2,doorobs)
path('DOOR_OUT_SIMULTANEOUS',[[61.6,21.1],[61.6,13.6],[58.6,13.6],[58.6,11.6]],-math.pi/2,doorobs)
for q in paths:assert q['passed'],(q['id'],[(x['closest_obstacle'],x['min_separation']) for x in q['details'] if not x['passed']])
carry=[]
def carrybox(p,yaw):
 return ns['cover_obb'](p[0]-.20*math.cos(yaw),p[1]-.20*math.sin(yaw),.705,.29,.235,.15,yaw)
for q in paths[:3]:
 best=(99,None,None)
 for a,b in zip(q['points'],q['points'][1:]):
  r=ns['static_near']([('CARRIED_SHOE_PAIR',hull(carrybox(a,q['yaw']),carrybox(b,q['yaw'])))],useobs)
  if r[0]<best[0]:best=r
 carry.append(dict(path=q['id'],passed=best[0]>=-1e-5,min_clearance=best[0],closest=best[2]))
for k in range(360):
 a=math.pi+math.pi/2*k/360;b=math.pi+math.pi/2*(k+1)/360;bb=hull(carrybox([55.8,14.7],a),carrybox([55.8,14.7],b));pad=.6*((b-a)**2)/8
 for j in [0,1]:bb[j]-=pad;bb[j+3]+=pad
 assert ns['static_near']([('CARRIED_SHOE_TURN',bb)],useobs)[0]>=-1e-5
assert all(q['passed'] for q in carry)
lowering_box=[54.4825,14.10,.015,54.7175,14.40,.78];lowering=ns['static_near']([('SHOE_LOWERING',lowering_box)],useobs);assert lowering[0]>=-1e-5
st=ast.parse((B/'check_shoes.py').read_text(encoding='utf-8'));pn=dict(math=math,R=math.hypot(W/2,.17))
exec(compile(ast.Module(body=[n for n in st.body if isinstance(n,ast.FunctionDef) and n.name in ['point_dist','sd','pairgap']],type_ignores=[]),'existing exact path distance functions','exec'),pn)
pp={q['id']:q['points'] for q in paths};pair_margin=pn['pairgap'](pp['DOOR_IN_SIMULTANEOUS'],pp['DOOR_OUT_SIMULTANEOUS']);assert pair_margin>=0
# Static carry/shoe extraction and upper-row evidence remain explicit dimensional hypotheses.
take=dict(bank='REV_LINK_MID',face='west',column=2,row=3,standing=[55.64,15.85,0],shoe=[.29,.235,.115],
 shoe_start=[56.06,15.7325,.63,56.35,15.9675,.745],hand_envelope=[55.92,15.76,.73,56.10,15.94,.78],
 shoe_end=[55.40,15.7325,.63,55.69,15.9675,.745],available_cavity=[.288,.334,.276],
 cavity_bounds=[56.04,15.706,.606,56.384,15.994,.882],clearance_width=.288-.235,clearance_depth=.334-.29,
 status='straight pull through real open cubby; hand at open front, no sliding-panel obstruction; .8m reach hypothesis, not grasp/force certification')
assert take['shoe_start'][3]<take['cavity_bounds'][3] and take['shoe_start'][1]>take['cavity_bounds'][1] and take['hand_envelope'][5]<take['cavity_bounds'][5]
# Activity interface: no new chair moves, operation on old stage01; no automatic movement to seat.
classobs=L['obstacles'];r0=ns['swept_standing']([45,12.7],[45,18.8],0,0,classobs);r1=ns['swept_standing']([45,18.8],[45,19.5],0,0,classobs)
route=dict(passed=r0['passed'] and r1['passed'],min_separation=min(r0['min_separation'],r1['min_separation']),parts=[r0,r1]);assert route['passed']
cases=[]
for name,A,scope in [('HISTORICAL_RECIPE_Z800',[4500,7050,800],'historical file, NOT live map'),('FORMAL_PLANNING_Z1200',[4500,7050,1200],'conditional formal C01 mapping, NOT current anchor evidence')]:
 for off,why in [(.96,'constructor half-height96cm, scale1/contact assumed'),(.98,'landing-helper96+2cm illustrative only, not universal live offset')]:
  Gcm=[4500,7050,1200];actor=[4500,7050,1200+off*100]
  for mode in ['PREVIEW_P','ENTER_E']:
   d=math.dist(actor,A);cases.append(dict(candidate_id='OP_C30_01',seat_relation='F2_W4_DESK_3_5 tentative, not final bound',mode=mode,anchor_case=name,
    anchor_source=scope,A_cm=A,G_local_m=[45,19.5,4],G_engineering_cm=Gcm,actor_offset_m=off,offset_evidence=why,
    actor_local_m=[45,19.5,4+off],actor_world_cm=actor,world_basis='engineering UE candidate mapping; live C01 actor/world transform unverified',
    distance_squared_cm2=sum((a-b)**2 for a,b in zip(actor,A)),distance_cm=d,margin_cm=230-d,within230=d<=230,
    route_passed=route['passed'],current_engineering_compatibility='UNVERIFIED; historical case fails',eligibility_game='UNVERIFIED'))
write('ACTIVITY_DISTANCE.json',dict(fixed_radius_cm=230,P_equals_E=True,cases=cases,route=dict(points=[[45,12.7,4],[45,18.8,4],[45,19.5,4]],**route),
 candidate=dict(id='OP_C30_01',seat_id='F2_W4_DESK_3_5',chair=[46.175,19.87,4.43],chair_approach_original=[46.35,19.87,4],
 operation_ground=[45,19.5,4],relation='standing preview/Enter reachable from cross-aisle, not a sitting prerequisite or automatic seat transfer',
 seat_sit_exit='Revision01 standing/pull candidate blocked; full conversion unverified, do not bind final player seat',
 old_study='5_5 retained unchanged, not final player seat',old_study_chair=[48.275,19.87,4.43],old_study_approach=[48.29,19.87,4]),
 conflict=dict(min_vertical_cm=496,vertical_shortfall_cm=266,at_operation_history_distance=math.dist([4500,7050,1296],[4500,7050,800]),
  recommendation='Keep original anchor/radius/floor; pause final seat binding, request planning/development read-only live Actor/Anchor transform evidence before deciding interface alignment. No source/map edits in this task.'),
 scope='Only P/E proximity, not all19 phases. No teleport, radius/anchor change or new sitting start condition. Live map/scaled capsule/nearest eligible place not verified.'))
with (O/'ACTIVITY_DISTANCE.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f,lineterminator='\n');w.writerow(['candidate','P_or_E','anchor_source_case','A_cm','G_local_m','G_UE_candidate_cm','offset_m','Actor_local_m','Actor_UE_candidate_cm','d_cm','230_minus_d_cm','condition_within230','runtime_verified'])
 for q in cases:w.writerow([q['candidate_id'],q['mode'],q['anchor_case'],q['A_cm'],q['G_local_m'],q['G_engineering_cm'],q['actor_offset_m'],q['actor_local_m'],q['actor_world_cm'],q['distance_cm'],q['margin_cm'],q['within230'],False])
write('LAYOUT.json',dict(asset=P,units='m',base='../Revision01',door=door,bench=bench,shoe_banks=S['banks'],queues=queues,operators=ops,
 shoe_change=shoe_change,take=take,door_two_travellers=dict(passed=True,enclosing_radius=pn['R'],pair_clearance=pair_margin,scope='two independent complete door lines, circle hull; not all arbitrary merging traffic'),carried_shoes=dict(checks=carry,turn_intervals=360,passed=True,
  lowering_box=lowering_box,lowering_min_clearance=lowering[0],scope='shoe translation/turn/lowering in free front use-zone; own feet contact allowed, real grasp unverified'),bench_transition={k:v for k,v in motion.items() if k!='poses'},bench_poses=poses,
 paths=paths,turn=turn,simultaneous_other_user=other_user,obstacles=obs,
 areas=dict(cabinets_main=7.488,cabinets_link=7.56,cabinets_total=15.048,bench_projection=2.4*.45,
  bench_use_two_people=2*W*1.30,stand_rise_two_people=2*W*.68,queue_six_people=6*W*.68,
  full_face_operating_main=11.7*2*.7,full_face_operating_link=(4.8+4.2*4)*.7,
  public_clear_main_spine=2.8*8.37,public_net_face_lane=1.12,
  notes='areas separated, usage can overlap own seat; not added as building floor area. Original deepen correction1.08 is unrelated to new bench1.08.'),
 inherited_classroom='INHERITED_STUDY.json; no changed classroom geometry or added19-stage requirements',
 limitations=['finite two bench users and named routes, not900-person peak','real seated/bending/hand/shoe animation unapproved','live activity Actor/Anchor Z unverified; historicalZ8 conflicts with formal floorZ12']))
print('LOW_LAYOUT_READY',[(q['id'],q['passed'],round(q['min_clearance'],6)) for q in paths], 'BENCH',motion['passed'],shoe_change['hand_distance'],'DIST',[(q['anchor_case'],q['distance_cm']) for q in cases[::2]],flush=True)
