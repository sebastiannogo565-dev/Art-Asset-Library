from pathlib import Path
import json,math,hashlib,struct,xml.etree.ElementTree as ET
P=Path(__file__).parent
j=json.loads((P/'SL_BLD_C01_MAIN_01_PLAN_01.json').read_text(encoding='utf-8'))
issues=[]; area=lambda r:(r[2]-r[0])*(r[3]-r[1])
inside=lambda p,r:r[0]-1e-7<=p[0]<=r[2]+1e-7 and r[1]-1e-7<=p[1]<=r[3]+1e-7
overlap=lambda a,b:max(0,min(a[2],b[2])-max(a[0],b[0]))*max(0,min(a[3],b[3])-max(a[1],b[1]))
body=j['candidate']['body_rects']; expected=sum(map(area,body))
if expected!=3016:issues.append('body area')
for a in body:
 if not inside(a[:2],[0,0,150,28]) or not inside(a[2:],[0,0,150,28]):issues.append('body out of control')
for i,a in enumerate(body):
 for b in body[i+1:]:
  if overlap(a,b)>1e-6:issues.append('double-counted body')
for f in (1,2,3):
 rs=[r for r in j['rooms'] if r['floor']==f]
 if len([r for r in rs if r['kind']=='classroom'])!=8:issues.append('class count')
 for r in rs:
  if not inside(r['door'],r['rect']):issues.append('door outside '+r['id'])
  for x in [r['rect'][0],r['rect'][2]]:
   for y in [r['rect'][1],r['rect'][3]]:
    if not any(inside([x,y],b) for b in body):issues.append('room outside mass '+r['id'])
  if abs(area(r['rect'])-r['net_area'])>1e-6:issues.append('room area '+r['id'])
  if f>1 and overlap(r['rect'],j['candidate']['atrium'])>1e-6:issues.append('upper room in atrium '+r['id'])
  if f==3 and overlap(r['rect'],j['candidate']['terrace'])>1e-6:issues.append('room in terrace '+r['id'])
 for i,a in enumerate(rs):
  for b in rs[i+1:]:
   if overlap(a['rect'],b['rect'])>1e-6:issues.append('rooms overlap '+a['id']+' '+b['id'])
 for a in j['areas']:
  if a['floor']==f:
   calc=a['enclosed_plan_envelope']-a['atrium_void']-a['stair_void']-a['elevator_use_exclusion']
   if abs(calc-a['allocatable_horizontal_area'])>1e-6:issues.append('floor deductions')
   if abs(sum(r['net_area'] for r in rs)-a['room_public_net_sum'])>1e-6:issues.append('net sum')
for e,xy in zip(j['entrances'],[[25,0],[90,28],[150,14]]):
 if e['local']!=xy:issues.append('entrance moved')
for s in j['candidate']['stairs']:
 if abs(area(s['opening'])-25.85)>1e-6:issues.append('stair hole')
for r in j['routes']:
 calc=sum(math.dist(a,b) for a,b in zip(r['points'],r['points'][1:]))
 if abs(calc-r['length_3d_candidate_m'])>1e-7:issues.append('route length')
 # Interior portions sampled for mass containment and controlled room intrusion.
 for a,b in zip(r['points'],r['points'][1:]):
  if not (0<=a[0]<=150 and 0<=a[1]<=28 and 0<=b[0]<=150 and 0<=b[1]<=28):continue
  for k in range(21):
   p=[a[q]+(b[q]-a[q])*k/20 for q in range(3)]
   if not any(inside(p,box) for box in body):issues.append('route outside mass '+r['id'])
   if abs(p[2]/4-round(p[2]/4))<1e-5:
    floor=round(p[2]/4)+1
    for room in j['rooms']:
     if room['floor']==floor and room['access'] not in ['student','student_authorized'] and inside(p,room['rect']):issues.append('route crosses restricted '+room['id'])
protected=[]
for f in j['protected_inputs']:
 if hashlib.sha256(Path(f['path']).read_bytes()).hexdigest()!=f['sha256']:protected.append(f['path'])
images=[]
for n in range(1,9):
 name=f'SL_BLD_C01_MAIN_01_PLAN_01_P{n:02}'
 ET.parse(P/(name+'.svg'))
 b=(P/(name+'.png')).read_bytes(); wh=struct.unpack('>II',b[16:24]);images.append(dict(page=n,width=wh[0],height=wh[1]))
 if wh!=(3200,2400):issues.append('image size')
result=dict(date='2026-10-15',scope='2D/serialized planning only, not engineering navigation rendering or capacity operation',passed=not issues and not protected,issues=sorted(set(issues)),protected_input_count=len(j['protected_inputs']),protected_differences=protected,rooms=len(j['rooms']),classrooms=24,entrances_preserved=not any('entrance' in x for x in issues),room_rectangles_nonoverlapping=not any('overlap' in x for x in issues),sampled_public_paths_checked=True,native_images=images,allocatable_area_sum=sum(a['allocatable_horizontal_area'] for a in j['areas']),unverified=['exact window schedules and shading detail','shoe bank900 capacity/queues','roof RT01 compatibility','actual stairs/railings/finite character collision/3D occlusion','physical structure/fire/evacuation/engineering','new same-endpoint game times and NPC navigation','background room props/UV/material density','UE or formal model'],formal_art_images=0,model_count=0,B01_changes=0)
(P/'SL_BLD_C01_MAIN_01_CHECKS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False));raise SystemExit(0 if result['passed'] else 1)
