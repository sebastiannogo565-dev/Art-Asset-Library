from pathlib import Path
import json,math
OUT=Path(__file__).parent
L=json.loads((OUT/'LAYOUT.json').read_text(encoding='utf-8'));S=L['shoe'];W=L['proxy']['standing_visible'][0]
R=math.hypot(W/2,.17)
def point_dist(p,r):return math.hypot(max(r[0]-p[0],0,p[0]-r[2]),max(r[1]-p[1],0,p[1]-r[3]))
def sd(a,b,r):
 dx,dy=b[0]-a[0],b[1]-a[1];ll=dx*dx+dy*dy
 def dp(q):
  t=max(0,min(1,((q[0]-a[0])*dx+(q[1]-a[1])*dy)/ll)) if ll else 0
  return math.hypot(q[0]-a[0]-t*dx,q[1]-a[1]-t*dy)
 lo,hi=0.,1.
 for aa,dd,mn,mx in [(a[0],dx,r[0],r[2]),(a[1],dy,r[1],r[3])]:
  if abs(dd)<1e-12:
   if not mn<=aa<=mx:lo=2;break
  else:
   q0,q1=sorted([(mn-aa)/dd,(mx-aa)/dd]);lo=max(lo,q0);hi=min(hi,q1)
 if lo<=hi and hi>=0 and lo<=1:return 0.
 return min(point_dist(a,r),point_dist(b,r),*(dp(q) for q in [(r[0],r[1]),(r[2],r[1]),(r[2],r[3]),(r[0],r[3])]))
operators=[];solid=[]
for b in S['banks']:
 x,y,z,X,Y,Z=b['bounds'];solid.append(dict(id=b['id'],rect=[x,y,X,Y],room=b['room']))
 length=X-x if b['axis']=='X' else Y-y
 count=2 if b['id'].startswith('REV_MAIN_W') else 1 if b['id'].startswith('REV_MAIN_E') else 3
 positions=[(x+X)/2 if b['axis']=='X' else (y+Y)/2] if count==1 else [(x if b['axis']=='X' else y)+W/2+i*(length-W)/(count-1) for i in range(count)]
 for face in ([-1,1] if b['faces']==2 else [1]):
  for k,u in enumerate(positions):
   if b['axis']=='X':
    v=y if face<0 else Y;rect=[u-W/2,v-.7 if face<0 else v,u+W/2,v if face<0 else v+.7]
   else:
    v=x if face<0 else X;rect=[v-.7 if face<0 else v,u-W/2,v if face<0 else v+.7,u+W/2]
   operators.append(dict(id=b['id']+f'_OP{face}_{k}',room=b['room'],rect=rect))
def pathcheck(name,path,room,door_width=None):
 obs=[v for v in solid+operators if v['room']==room]+[dict(id='QUEUE',rect=q['bounds']) for q in S['queues'] if q['room']==room]
 margins=[(sd(a,b,o['rect'])-R,o['id']) for a,b in zip(path,path[1:]) for o in obs]
 if room=='F1_LW' and door_width:
  # Door jambs with specified centre; real width1.4 and candidate2.4 are checked separately.
  for a,b in zip(path,path[1:]):
   for r in [[52.3,12.8,58-door_width/2,13],[58+door_width/2,12.8,63.7,13]]:margins.append((sd(a,b,r)-R,'LW_DOOR_JAMB'))
 m,ob=min(margins)
 return dict(id=name,path=path,min_clearance=m,closest=ob,passed=m>=-1e-5,room=room)
checks=[pathcheck('MAIN_IN',S['main_in_path'],'F1_WL'),pathcheck('MAIN_OUT',S['main_out_path'],'F1_WL'),
 pathcheck('LINK_SINGLE_PERSON_LOOP',S['link_in_path'],'F1_LW',1.4),
 pathcheck('LINK_PROPOSED_IN_REAL_DOOR',S['link_proposed_in'],'F1_LW',1.4),
 pathcheck('LINK_PROPOSED_OUT_REAL_DOOR',S['link_proposed_out'],'F1_LW',1.4),
 pathcheck('LINK_PROPOSED_IN_2_4_CANDIDATE',S['link_proposed_in'],'F1_LW',2.4),
 pathcheck('LINK_PROPOSED_OUT_2_4_CANDIDATE',S['link_proposed_out'],'F1_LW',2.4)]
def pairgap(p,q):
 # Exact segment distance, treating the second route as thin rectangles plus endpoints.
 return min(sd(a,b,[min(c[0],d[0]),min(c[1],d[1]),max(c[0],d[0]),max(c[1],d[1])])-2*R
  for a,b in zip(p,p[1:]) for c,d in zip(q,q[1:]))
pair=dict(main_pair_margin=pairgap(S['main_in_path'],S['main_out_path']),
 proposed_link_pair_margin=pairgap(S['link_proposed_in'],S['link_proposed_out']))
result=dict(nominal=S['nominal'],main=S['main'],link=S['link'],banks=S['banks'],operators=operators,
 method='whole visible1.039655m x .34m footprint circumscribed circle, all line/corner sweeps exact distance to actual operating rectangles/queue/carcasses',
 radius=R,net_aisle=2.52-.7-.7,paths=checks,pair=pair,queue_count=6,
 scope='finite named simultaneous users; not all possible counterflow/NPC or900-person peak operation',
 upper_use=dict(open_height=.276,shoe_plus_hand_height=.15,margin=.126,arm_length=.8,shoulder_z=1.,hand_z=1.60,offset=.37,normal_distance=.30,
 reach=math.sqrt(.6**2+.37**2+.30**2),status='static dimensional hypothesis only, no real hand/force validation'))
(OUT/'SHOE_CHECKS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('SHOES',[(p['id'],p['passed'],round(p['min_clearance'],5)) for p in checks],pair)
