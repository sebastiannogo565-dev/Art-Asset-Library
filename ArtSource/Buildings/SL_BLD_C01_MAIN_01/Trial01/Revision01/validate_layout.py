"""Trial revision01: low-detail, same-coordinate conservative interval envelopes BEFORE mesh changes."""
from pathlib import Path
import json,math,hashlib,csv,collections
ROOT=Path('D:/Art Asset Library');OUT=Path(__file__).parent;BASE=OUT.parent
P='SL_BLD_C01_MAIN_01_TRIAL_01_REV_01'
G=json.loads((BASE/'GEOMETRY.json').read_text(encoding='utf-8'))
W=1.039655172413793;FLOOR=4.;ROOM=[41,12.7,49.4,21.7]
def write(n,o):(OUT/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
if not (OUT/'protected_inputs.json').exists():
 paths={Path(v['path']) for v in json.loads((BASE/'protected_inputs.json').read_text())}
 paths.update(p for p in BASE.rglob('*') if p.is_file() and OUT not in p.parents and p.suffix!='.blend1')
 paths.update(ROOT/('Docs/AssetPlanning/BuildingProduction/'+s) for s in ['TaskCards/SL_BLD_C01_MAIN_01_TRIAL_01.md','review-C01-trial-01.md','C01/trial-01-planning-audit.json'])
 write('protected_inputs.json',[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(paths) if p.exists()])
def box(name,b):return dict(id=name,bounds=b)
def desk_boxes(x,y,prefix):
 b=[box(prefix+'_TOP',[x-.225,y-.325,.69,x+.225,y+.325,.72]),box(prefix+'_TRAY',[x-.14,y-.24,.54,x+.14,y+.24,.56])]
 for a in [-.18,.18]:
  for c in [-.29,.29]:b.append(box(prefix+'_LEG',[x+a-.018,y+c-.018,0,x+a+.018,y+c+.018,.69]))
 return b
def chair_boxes(x,y,prefix,handle=False):
 b=[box(prefix+'_SEAT',[x-.225,y-.225,.395,x+.225,y+.225,.43]),box(prefix+'_BACK',[x+.16,y-.225,.43,x+.22,y+.225,.84])]
 for a in [-.18,.18]:
  for c in [-.18,.18]:b.append(box(prefix+'_LEG',[x+a-.015,y+c-.015,0,x+a+.015,y+c+.015,.395]))
 if handle:b.append(box(prefix+'_HANDLE',[x+.16,y-.10,.80,x+.30,y+.10,.88]))
 return b
desks=[];chairs=[];obstacles=[]
for i,x in enumerate(G['player_layout']['desk_x'],1):
 for j,y in enumerate(G['player_layout']['desk_y'],1):
  sid=f'F2_W4_DESK_{i}_{j}';player=sid=='F2_W4_DESK_5_5'
  dx=x+.04 if player else x;cx=48.275 if player else x+.4
  desks.append(dict(id=sid,x=dx,y=y,floor=4,changed=player))
  chairs.append(dict(id=sid.replace('DESK','CHAIR'),x=cx,y=y,player=player))
  obstacles+=desk_boxes(dx,y,sid)+chair_boxes(cx,y,sid.replace('DESK','CHAIR'),player)
# Same wall/teacher interfaces as original, no new opening.
obstacles+=desk_boxes(41.75,17,'TEACHER')[:0]
obstacles += [box('TEACHER_TOP',[41.45,16.4,.72,42.05,17.6,.75])]
for x in [41.5,42.0]:
 for y in [16.45,17.55]:obstacles.append(box('TEACHER_LEG',[x,y,0,x+.035,y+.035,.72]))
obstacles += [box('WALL_W',[40.8,12.7,0,41,21.7,3.45]),box('WALL_E',[49.4,12.7,0,49.6,21.7,3.45]),
 box('WALL_N',[41,21.7,0,49.4,22,3.45]),box('DOOR_W',[41,12.5,0,44.2,12.7,3.45]),
 box('DOOR_E',[45.8,12.5,0,49.4,12.7,3.45]),box('DOOR_HEAD',[44.2,12.5,2.6,45.8,12.7,3.45])]
# Positive separation means disjoint; zero allows real surface contact, never a1mm body inset.
def separation(a,b):
 return max(b[0]-a[3],a[0]-b[3],b[1]-a[4],a[1]-b[4],b[2]-a[5],a[2]-b[5])
def hull(a,b):return [min(a[i],b[i]) for i in range(3)]+[max(a[i],b[i]) for i in range(3,6)]
def cover_obb(cx,cy,cz,dx,dy,dz,yaw):
 c,s=abs(math.cos(yaw)),abs(math.sin(yaw));hx=(c*dx+s*dy)/2;hy=(s*dx+c*dy)/2
 return [cx-hx,cy-hy,cz-dz/2,cx+hx,cy+hy,cz+dz/2]
def standing(x,y,yaw):
 # Full unchanged PNG width is preserved in .30..1.80m; lower .64m covers actual PNG feet span .6362.
 return [('VISIBLE_LOW',cover_obb(x,y,.15,.28,.64,.30,yaw)),
 ('VISIBLE_MID',cover_obb(x,y,.685,.34,W,.77,yaw)),
 ('VISIBLE_UPPER',cover_obb(x,y,1.365,.34,W,.87,yaw)),
 ('CAPSULE_BOUND',[x-.34,y-.34,0,x+.34,y+.34,1.92])]
def static_near(parts,obs):
 best=(999,None,None)
 for name,a in parts:
  for o in obs:
   s=separation(a,o['bounds'])
   if s<best[0]:best=(s,name,o['id'])
 return best
def swept_standing(a,b,yaw0,yaw1,obs):
 # Translation intervals are exact; rotation covered by max sin/cos inside each <=.25degree interval.
 n=max(1,math.ceil(math.dist(a,b)/.01),math.ceil(abs(yaw1-yaw0)/math.radians(.25)));worst=(999,None,None);bad=[]
 for k in range(n):
  t0,t1=k/n,(k+1)/n
  def pose(t):return standing(a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t,yaw0+(yaw1-yaw0)*t)
  pa,pb=pose(t0),pose(t1)
  for (name,A),(_,B) in zip(pa,pb):
   C=hull(A,B)
   # Bounding-box support function curvature: radius*delta_angle^2/8.
   if yaw0!=yaw1:
    pad=.6*((yaw1-yaw0)/n)**2/8
    for q in [0,1]:C[q]-=pad;C[q+3]+=pad
   r=static_near([(name,C)],obs)
   if r[0]<worst[0]:worst=r
   if r[0]<-1e-5:bad.append(dict(interval=[t0,t1],part=name,obstacle=r[2],penetration=-r[0]))
 return dict(intervals=n,min_separation=worst[0],closest_part=worst[1],closest_obstacle=worst[2],blocked=bad[:12],passed=not bad)
playerprefix='F2_W4_CHAIR_5_5';rest=48.275;pulled=48.90
static=[o for o in obstacles if not o['id'].startswith(playerprefix)]
restobs=static+chair_boxes(rest,19.87,playerprefix,True);pullobs=static+chair_boxes(pulled,19.87,playerprefix,True)
segments=[]
def standseg(name,a,b,ya,yb,obs):
 r=swept_standing(a,b,ya,yb,obs);segments.append(dict(id=name,start=a,end=b,yaw_start=ya,yaw_end=yb,**r))
# Side-stepping is a spatial candidate, not a game locomotion rule; explicit turns at generous cross aisle.
standseg('01_DOOR_TO_CROSS',[45,12.7],[45,18.8],0,0,restobs)
standseg('02_CROSS_TO_OPERATOR',[45,18.8],[48.80,18.8],0,0,restobs)
standseg('03_TURN_NORTH',[48.80,18.8],[48.80,18.8],0,-math.pi/2,restobs)
standseg('04_OPERATOR_APPROACH',[48.80,18.8],[48.80,19.08],-math.pi/2,-math.pi/2,restobs)
standseg('05_OPERATOR_TURN_WEST',[48.80,19.08],[48.80,19.08],-math.pi/2,0,restobs)
# Chair travel retains seat/back/legs/handle, and operator remains present.
chair_sweep=[];operator=standing(48.8,19.08,0)
for A,B in zip(chair_boxes(rest,19.87,playerprefix,True),chair_boxes(pulled,19.87,playerprefix,True)):
 C=hull(A['bounds'],B['bounds']);r=static_near([(A['id'],C)],static+[box('OPERATOR_'+n,b) for n,b in operator])
 chair_sweep.append(dict(part=A['id'],swept=C,min_separation=r[0],obstacle=r[2]))
arm_region=[48.40,19.34,.885,49.25,20.03,1.75]
arm_clear=static_near([('ARM_REACH_VOLUME',arm_region)],static+chair_boxes(rest,19.87,playerprefix,True)+chair_boxes(pulled,19.87,playerprefix,True))
hand_max=max(math.dist([48.8,19.38,1.30],[x+.27,19.8,.91]) for x in [rest,pulled])
segments.append(dict(id='06_CHAIR_PULL',start=[rest,19.87],end=[pulled,19.87],operator=[48.8,19.08],travel=pulled-rest,
 passed=all(v['min_separation']>=-1e-5 for v in chair_sweep) and arm_clear[0]>=-1e-5 and hand_max<=.8,parts=chair_sweep,
 hand=dict(arm_links=[.4,.4],max_endpoint_distance=hand_max,enclosing_arm_volume=arm_region,min_clearance=arm_clear[0],
 finger_contact='radius.03 sphere centred at handleX+.27,Y19.8,Z.91; bottom .88 touches handle top, no volume inset',
 status='continuous geometric reach/contact hypothesis only; real grasp/force not verified')))
standseg('07_RETURN_SIDE',[48.80,19.08],[48.80,18.8],0,0,pullobs)
standseg('08_CHAIR_FRONT',[48.80,18.8],[48.29,18.8],0,0,pullobs)
standseg('09_ENTER_FRONT',[48.29,18.8],[48.29,19.87],0,0,pullobs)
# Constant-size articulated envelope. Standing union covers original PNG alpha height bands.
# Hinged lower-visible band (.77x1.039655x.34) is a conservative garment/arms proxy, NOT anatomy inferred from PNG.
def ik(s):
 hx=48.29+.585*math.sin(math.pi*s/2);hz=.93-.41*s*s;ax,az=48.29,.07
 dx,dz=hx-ax,hz-az;D=math.hypot(dx,dz)
 if D>.88000001:raise ValueError(('unreachable leg',s,D))
 q=math.sqrt(max(0,.44**2-D*D/4))/D
 return hx,hz,ax+.5*dx-dz*q,az+.5*dz+dx*q
def seated_parts(s):
 hx,hz,kx,kz=ik(s);th=math.pi*s/2;parts=[]
 parts += [('FEET',[48.09,19.55,0,48.37,20.19,.30]),
 ('PELVIS',[hx-.12,19.60,hz-.09,hx+.12,20.14,hz+.09]),
 ('UPPER',[hx-.17,19.87-W/2,hz,hx+.17,19.87+W/2,hz+.87])]
 for j in range(24):
  u=(j+.5)*.77/24;L=.77/24
  cx=hx-u*math.sin(th);cz=hz+.14-u*math.cos(th)
  ex=abs(math.sin(th))*L/2+abs(math.cos(th))*.17;ez=abs(math.cos(th))*L/2+abs(math.sin(th))*.17
  parts.append((f'VISIBLE_HINGE_{j}',[cx-ex,19.87-W/2,cz-ez,cx+ex,19.87+W/2,cz+ez]))
 for sy in [19.64,20.10]:
  for n,a,b in [('THIGH',(hx,hz),(kx,kz)),('SHIN',(kx,kz),(48.29,.07))]:
   for j in range(12):
    u,v=j/12,(j+1)/12
    A=[a[q]*(1-u)+b[q]*u for q in [0,1]];B=[a[q]*(1-v)+b[q]*v for q in [0,1]]
    parts.append((n+f'_{j}',[min(A[0],B[0])-.06,sy-.06,min(A[1],B[1])-.06,max(A[0],B[0])+.06,sy+.06,max(A[1],B[1])+.06]))
 return parts
def transition():
 bad=[];best=(999,None,None);poses=[];N=1000
 for k in range(N):
  a,b=k/N,(k+1)/N;pa,pb=seated_parts(a),seated_parts(b)
  # Interval bounds for hip monotone and sin/cos; hull+rigorous component support bounds.
  hxa,hza,kxa,kza=ik(a);hxb,hzb,kxb,kzb=ik(b)
  sin0,sin1=math.sin(math.pi*a/2),math.sin(math.pi*b/2);cos0,cos1=math.cos(math.pi*a/2),math.cos(math.pi*b/2)
  dx0,dx1=hxa-48.29,hxb-48.29;dz0,dz1=hzb-.07,hza-.07
  dl=math.sqrt(dx0*dx0+dz0*dz0);du=min(.88,math.sqrt(dx1*dx1+dz1*dz1))
  ql=math.sqrt(max(0,.44**2-du*du/4))/du;qu=math.sqrt(max(0,.44**2-dl*dl/4))/dl
  kxl,kxu=48.29+.5*dx0-dz1*qu,48.29+.5*dx1-dz0*ql
  kzl,kzu=.07+.5*dz0+dx0*ql,.07+.5*dz1+dx1*qu
  for (name,A),(_,B) in zip(pa,pb):
   C=hull(A,B)
   if name.startswith('VISIBLE_HINGE'):
    j=int(name.split('_')[-1]);u0=j*.77/24;u1=(j+1)*.77/24
    C=[hxa-u1*sin1-.17*cos0,19.87-W/2,hzb+.14-u1*cos0-.17*sin1,
       hxb-u0*sin0+.17*cos0,19.87+W/2,hza+.14-u0*cos1+.17*sin1]
   elif name.startswith(('THIGH_','SHIN_')):
    j=int(name.split('_')[-1]);u,v=j/12,(j+1)/12
    if name.startswith('THIGH'):
     xl=[hxa*(1-t)+kxl*t for t in [u,v]];xu=[hxb*(1-t)+kxu*t for t in [u,v]]
     zl=[hzb*(1-t)+kzl*t for t in [u,v]];zu=[hza*(1-t)+kzu*t for t in [u,v]]
    else:
     xl=[kxl*(1-t)+48.29*t for t in [u,v]];xu=[kxu*(1-t)+48.29*t for t in [u,v]]
     zl=[kzl*(1-t)+.07*t for t in [u,v]];zu=[kzu*(1-t)+.07*t for t in [u,v]]
    C=[min(xl)-.06,A[1],min(zl)-.06,max(xu)+.06,A[4],max(zu)+.06]
   r=static_near([(name,C)],pullobs)
   if r[0]<best[0]:best=r
   if r[0]<-1e-5:bad.append(dict(interval=[a,b],part=name,obstacle=r[2],penetration=-r[0]))
  if k%50==0:poses.append(dict(t=a,hip=[hxa,19.87,hza+4],knee=[kxa,19.87,kza+4],parts=[dict(name=n,bounds=[v+4 if i in [2,5] else v for i,v in enumerate(bb)]) for n,bb in pa]))
 poses.append(dict(t=1,parts=[dict(name=n,bounds=[v+4 if i in [2,5] else v for i,v in enumerate(bb)]) for n,bb in seated_parts(1)]))
 return dict(intervals=N,passed=not bad,min_separation=best[0],closest_part=best[1],closest_obstacle=best[2],blocked=bad[:30],poses=poses,
 method='interval arithmetic of monotone hip, sin/cos and two-link IK; all chair components retained; no body inset; surface contact allowed only, tolerance10um')
motion=transition();segments.append(dict(id='10_SIT',**{k:v for k,v in motion.items() if k!='poses'}))
segments.append(dict(id='11_RISE',reverse_of='10_SIT',passed=motion['passed'],min_separation=motion['min_separation']))
standseg('12_EXIT_FRONT',[48.29,19.87],[48.29,18.8],0,0,pullobs)
standseg('13_LEAVE_OPERATOR',[48.29,18.8],[48.8,18.8],0,0,pullobs)
standseg('14_OPERATOR_RETURN',[48.8,18.8],[48.8,19.08],0,0,pullobs)
segments.append(dict(id='15_CHAIR_RETURN',reverse_of='06_CHAIR_PULL',passed=segments[5]['passed']))
standseg('16_RETURN_CROSS',[48.8,19.08],[48.8,18.8],0,0,restobs)
standseg('17_FRONT_TEACHING',[48.8,18.8],[41.7,18.8],0,0,restobs)
standseg('18_ORIGINAL_DOOR',[41.7,18.8],[45,18.8],0,0,restobs)
standseg('19_EXIT_DOOR',[45,18.8],[45,12.7],0,0,restobs)
# Reach table: actual standing silhouette rectangle, fixed west orientation; each own chair movement tested.
def reach(target,obs):
 step=.05;xs=[41.2+i*step for i in range(161)];ys=[13.25+i*step for i in range(159)]
 inflated=[(o['bounds'][0]-.34,o['bounds'][1]-W/2,o['bounds'][3]+.34,o['bounds'][4]+W/2) for o in obs if o['bounds'][2]<1.92 and o['bounds'][5]>0]
 def free(i,j):
  x,y=xs[i],ys[j]
  return all(not (a+1e-5<x<c-1e-5 and b+1e-5<y<d-1e-5) for a,b,c,d in inflated)
 start=(min(range(len(xs)),key=lambda i:abs(xs[i]-45)),0)
 end=(min(range(len(xs)),key=lambda i:abs(xs[i]-target[0])),min(range(len(ys)),key=lambda j:abs(ys[j]-target[1])))
 if not free(*end):return None,'站位包络受阻'
 q=collections.deque([start]);prev={start:None}
 while q:
  k=q.popleft()
  if k==end:
   path=[]
   while k is not None:path.append([xs[k[0]],ys[k[1]]]);k=prev[k]
   return path[::-1],'站立到达（固定朝西、网格保守矩形；动作未外推）'
  for di,dj in [(1,0),(-1,0),(0,1),(0,-1)]:
   t=k[0]+di,k[1]+dj
   if 0<=t[0]<len(xs) and 0<=t[1]<len(ys) and t not in prev and free(*t):prev[t]=k;q.append(t)
 return None,'当前候选站位与主通路断开（保守矩形）'
seats=[]
for d,ch in zip(desks,chairs):
 player=ch['player'];cx=pulled if player else d['x']+1.25
 others=[o for o in obstacles if not o['id'].startswith(ch['id'])]
 oldb=chair_boxes(ch['x'],ch['y'],ch['id'],player);newb=chair_boxes(cx,ch['y'],ch['id'],player)
 cm=min(static_near([(aa['id'],hull(aa['bounds'],bb['bounds']))],others)[0] for aa,bb in zip(oldb,newb))
 target=[48.29 if player else d['x']+.575,d['y']]
 path,reason=reach(target,others+newb)
 state='可达（站立）' if path and cm>=-1e-5 else '受阻'
 if player:state='该尺寸假设下连续空间通过' if motion['passed'] and all(s.get('passed',False) for s in segments) else '受阻或未解决'
 seats.append(dict(id=d['id'],desk=[d['x'],d['y'],4],chair_rest=[ch['x'],ch['y'],4.43],chair_candidate=[cx,ch['y'],4.43],
 approach=target+[4],state=state,chair_travel_clearance=cm,standing_path=path,reason=reason,
 transition='该尺寸假设下连续进入/坐定/起身/退出检查' if player else '未验证（不外推玩家席结果）'))
# Locker redistribution. Door and accepted shell remain untouched.
banks=[]
for j,y in enumerate([1.05,4.21,7.37],1):
 for side,x,length,cols in [('W',19.42,3.,10),('E',27.60,.9,3)]:
  banks.append(dict(id=f'REV_MAIN_{side}{j}',room='F1_WL',axis='X',bounds=[x,y,0,x+length,y+.64,1.8],columns=cols,rows=6,faces=2,depth=.64,
   cavity=[.288,.304,.276],front='open cubby candidate; .004m recessed lip, no sliding panel/handle sweep',nominal=cols*12))
for name,x,depth,cols,faces in [('SINGLE',52.3,.35,16,1),('MID',56.04,.7,14,2),('EAST',59.26,.7,14,2)]:
 banks.append(dict(id='REV_LINK_'+name,room='F1_LW',axis='Y',bounds=[x,15.4,0,x+depth,15.4+cols*.3,1.8],columns=cols,rows=6,faces=faces,depth=depth,
  cavity=[.288,.328 if faces==1 else .334,.276],front='open cubby; single bank faces east with west back against wall',nominal=cols*6*faces))
queues=[dict(room='F1_LW',center=[62.9,y],bounds=[62.9-W/2,y-.34,62.9+W/2,y+.34]) for y in [14.55,15.65,16.75,17.85,18.95,20.05]]
shoe=dict(banks=banks,nominal=sum(b['nominal'] for b in banks),main=468,link=432,net_face_gap=2.52,operating_depth=.70,public_width=1.12,
 main_end_bypass=1.12,link_end_space=2.40,main_spine=[23.60,.35,26.40,8.72],queues=queues,
 main_in_path=[[24.15,0],[24.15,2.95],[18.86,2.95],[18.86,6.11],[24.15,6.11],[24.15,8.8]],
 main_out_path=[[25.85,8.8],[25.85,6.11],[29.135,6.11],[29.135,2.95],[25.85,2.95],[25.85,0]],
 link_in_path=[[58,13],[58,21.1],[61.6,21.1],[61.6,13.6],[58,13.6],[58,13]],
 link_proposed_in=[[57.4,13],[57.4,14.7],[58,15.1],[58,21.1]],
 link_proposed_out=[[61.6,21.1],[61.6,13.6],[58.6,13.6],[58.6,13]],
 face_hardware_projection=0,standing_operation_assumption=[1.039655172413793,.70,1.8],
 original_door_conflict=dict(id='F1_LW_D',center=[58,13],width=1.4,two_visible_width=2*W,deficit=2*W-1.4,
  result='受阻：原1.4m内门不能让两个原人物正面包络同时通过；未改该门，不用错时通过',
  single_recommended_trade='请规划将同中心西连接内部廊口净宽1.4→2.4m；不减900/扩房/移外门。本轮保留原门，暂停该接口精作。'),
 upper_use=dict(shoe=[.29,.105,.115],pair_width=.235,hand_assumption=[.08,.18,.025],open_height=.276,rows=6,top_row_bottom=1.5,
  static_combined_height=.15,scope='single shoe with hand envelope; no real grasp/force/high-peak certification'),
 correction=dict(old_main_length=18,old_depth=.60,trial_depth=.66,old_main_area=10.8,trial_main_area=11.88,added_area=1.08,wrong_old_report=.54),
 new_area=dict(main=11.7*.64,link=4.8*.35+8.4*.70,total=11.7*.64+4.8*.35+8.4*.70,old_trial_total=18*.66+9*.7,delta_from_old_trial=11.7*.64+4.8*.35+8.4*.70-(18*.66+9*.7)))
layout=dict(asset=P,date='2026-10-16',base_git='8c1ddb206b654f002577f09607fd6c0f525205f8',units='m',room=ROOM,business=[45,19.5,4],recovery_candidate=[45,18.7,4],
 player=dict(id='F2_W4_DESK_5_5',old_id=G['player_interface']['designated_seat_id'],desk=[47.715,19.87,4.72],chair_rest=[48.275,19.87,4.43],
 chair_pulled=[48.9,19.87,4.43],approach=[48.29,19.87,4],operator=[48.8,19.08,4]),
 desks=desks,chairs=chairs,obstacles=obstacles,segments=segments,seated_motion=motion,seats=seats,shoe=shoe,
 proxy=dict(standing_visible=[W,1.8],capsule=[.68,1.92],feet=[.28,.64,.30],hip_stand=.93,hip_sit=.52,leg_links=[.44,.44],leg_radius=.06,
  visible_hinge=[.34,W,.77],hinge_count=24,upper=[.34,W,.87],arm_links=[.4,.4],tolerance=.00001,
  scope='conservative full-width visible band retained at constant size and hinged continuously; not anatomy inferred from PNG or approved seated character. Original silhouette standing coverage checked separately.'),
 unaffected='Other23 classrooms, all accepted shell/roof/layers/materials/UV unchanged; no RT01 access or UE')
write('LAYOUT.json',layout)
with (OUT/'SEATS.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f,lineterminator='\n');w.writerow(['ID','状态','椅活动净距m','接近站位','入座退出覆盖','说明'])
 for s in seats:w.writerow([s['id'],s['state'],s['chair_travel_clearance'],s['approach'],s['transition'],s['reason']])
print('MOTION',motion['passed'],motion['min_separation'],motion['blocked'][:2])
print('SEGMENTS',[(s['id'],s['passed'],s.get('min_separation')) for s in segments])
print('SEATS',collections.Counter(s['state'] for s in seats),'SHOES',shoe['nominal'],shoe['new_area'])
