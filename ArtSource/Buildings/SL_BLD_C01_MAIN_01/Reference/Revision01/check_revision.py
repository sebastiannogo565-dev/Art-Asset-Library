from pathlib import Path
import json,hashlib,math,xml.etree.ElementTree as ET
from PIL import Image
O=Path(__file__).parent;PR='SL_BLD_C01_MAIN_01_REFERENCE_01_REV_01'
g=json.loads((O/(PR+'_GEOMETRY.json')).read_text(encoding='utf-8'))
old=json.loads(Path(g['parent_geometry']).read_text(encoding='utf-8'))
issues=[]
def check(ok,msg):
 if not ok:issues.append(msg)
def rect(q):return [q[0],q[1],q[3],q[4]]
def dist(p,b):return math.hypot(max(b[0]-p[0],0,p[0]-b[2]),max(b[1]-p[1],0,p[1]-b[3]))
def overlap(a,b):return max(0,min(a[2],b[2])-max(a[0],b[0]))*max(0,min(a[3],b[3])-max(a[1],b[1]))
def route_distance(points,obs):
 minimum=float('inf');nearest=None;maxstep=0
 for a,b in zip(points,points[1:]):
  length=math.dist(a,b);n=max(1,math.ceil(length/.005));maxstep=max(maxstep,length/n)
  for i in range(n+1):
   p=[a[j]+(b[j]-a[j])*i/n for j in range(2)]
   for name,r in obs:
    d=dist(p,r)
    if d<minimum:minimum=d;nearest={'point':p,'obstacle':name}
 # distance is1-Lipschitz; subtract half largest sample step for continuous bound.
 return {'sample_min':minimum,'continuous_lower_bound':minimum-maxstep/2,'nearest':nearest,'max_sample_step':maxstep}
check(g['control']==old['control'] and g['segments']==old['segments'] and g['entrances']==old['entrances'],'fixed control/entry')
check(g['court']==old['court'] and g['terrace']==old['terrace'] and g['floors']==old['floors'],'court/terrace/floors')
check(len([r for r in g['rooms'] if r['kind']=='classroom'])==24,'classroomcount')
for r in g['rooms']:
 prev=next(x for x in old['rooms'] if x['id']==r['id'])
 check(r['rect']==prev['rect'],'room changed')
 if r['id']!='F1_WL':check(r==prev,'room metadata changed outside WL')
check(len(g['classroom_variants']['30']['desks'])==30 and g['classroom_variants']['36']==old['classroom_variants']['36'],'30/36')
for it in g['classroom_variants']['30']['desks']:
 b=it['bounds'];sx,sy,sz=it['seat']
 check(41<=b[0]<b[3]<=49.4 and 12.7<=b[1]<b[4]<=21.7,'desk room')
 check(sx+.25+.225<=49.4 and sy+.225<=21.7 and sy-.225>=12.7,'pulledchair room')
interfaces=g['player_interface'];player={}
baseobs=[('west_wall',[40.8,12.7,41,21.7]),('east_wall',[49.4,12.7,49.6,21.7]),
 ('north_wall',[41,21.7,49.4,22]),('door_left',[41,12.5,44.2,12.7]),('door_right',[45.8,12.5,49.4,12.7]),
 ('board',[41.05,15,41.12,19]),('teacher',[41.45,16.4,42.05,17.6])]
for state,offset in [('rest',0),('pulled',.25)]:
 obs=baseobs[:]
 for it in g['classroom_variants']['30']['desks']:
  obs.append((it['id'],rect(it['bounds'])));x,y,z=it['seat']
  obs.append((it['id']+'_chair',[x+offset-.225,y-.225,x+offset+.225,y+.225]))
 result={}
 for key in ['route_to_approach','route_return_via_teaching']:
  v=route_distance(interfaces[key],obs);result[key]=v
  check(v['continuous_lower_bound']>=.34,'capsule route '+state+key)
  check(v['continuous_lower_bound']>=g['character']['visible_front_width']/2,'visiblewidth proxy '+state+key)
 business=min((dist([45,19.5],r),name) for name,r in obs)
 recovery=min((dist([45,18.7],r),name) for name,r in obs)
 check(business[0]>=.34 and recovery[0]>=.34,'business/recoverycapsule')
 check(business[0]>=g['character']['visible_front_width']/2,'businessvisiblewidth proxy')
 player[state]={'routes':result,'business_min_distance':business,'recovery_min_distance':recovery}
capacity=sum(b['columns']*b['rows']*b['faces'] for b in g['lockers']);check(capacity==900,'900nominal')
check(next(r for r in g['rooms'] if r['id']=='F1_WL')['door_width']==3,'innerdoor3')
check(next(o for o in g['openings'] if o['id']=='F1_WL_D_REV')['hi']-23.5==3,'csvdoor3')
shoeparts=[p for p in g['primitives'] if p['type']=='box' and p['bounds'][2]<1.92 and
 (p['id'].startswith(('LOCKER_MAIN_','CELL_MAIN_','P1_','F1_WL_N_REV')))]
shoeobs=[(p['id'],rect(p['bounds'])) for p in shoeparts]
shoeobs += [('active_use_strip',g['shoe_circulation']['operating_strip_active'])]
for i,p in enumerate(g['shoe_circulation']['queue_markers']):
 shoeobs.append((f'queue{i}',[p[0]-.52,p[1]-.52,p[0]+.52,p[1]+.52]))
shoe={}
# to_wait starts inside the users own operation strip; standing-route check begins after reaching walk lane.
paths={'arrival':g['shoe_circulation']['arrival'],'waiting':g['shoe_circulation']['to_wait'][1:],
       'departure':g['shoe_circulation']['departure']}
for key,pp in paths.items():
 v=route_distance(pp,shoeobs);shoe[key]=v
 check(v['continuous_lower_bound']>=g['character']['visible_front_width']/2,'shoe visiblewidth proxy '+key)
foot=g['shoe_circulation']['operation_footprint']
check(all(overlap(foot,rect(p['bounds']))==0 for p in shoeparts),'cabinet operation footprint intersectsfurniture')
check(foot[2]-foot[0]>=g['character']['visible_front_width'] and foot[3]-foot[1]>=.68-1e-9,'operatingfinitebbox')
for f in (2,3):
 for p in [p for p in g['primitives'] if p['group']==f'SLAB_F{f:02}' or p['group']==f'INTERIOR_F{f-1:02}_CEILING']:
  for h in [g['court']]+[s['opening'] for s in g['stairs']]:check(overlap(rect(p['bounds']),h)==0,'slab/ceilinghole')
maxz=max(max(v[2] for v in p['vertices']) if p['type']=='mesh' else p['bounds'][5] for p in g['primitives'])
check(abs(maxz-13.68)<1e-8,'highest13.68')
door=next(o for o in g['openings'] if o['id']=='TERRACE_ACCESS');check(door['z0']==8.03 and door['z1']==10.63,'terracedoor')
for p in [p for p in g['primitives'] if p['id'].startswith('TERRACE_GUARD')]:
 check(p['bounds'][2]==8.03 and abs(p['bounds'][5]-p['bounds'][2]-1.2)<1e-8,'guard effectiveheight')
check(g['rt01']['rect']==[38,3,66,24] and g['rt01']['entry']==[49,14] and 'NOT OPEN' in g['rt01']['status'],'RT01status')
protected=[]
for it in g['protected_inputs']:
 if hashlib.sha256(Path(it['path']).read_bytes()).hexdigest()!=it['sha256']:protected.append(it['path'])
check(not protected,'original/read-only sources changed')
for f in O.glob(PR+'_P*.svg'):
 ET.parse(f);im=Image.open(f.with_suffix('.png'));check(im.mode=='RGB' and im.size==(3200,2400),'pageRGB/native')
check(len(list(O.glob(PR+'_P*.png')))==10,'10affectedpages')
for f in O.glob(PR+'_*.png'):
 if '_P0' in f.name:continue
 im=Image.open(f);check(im.mode=='RGB' and im.size==(2304,1296),'previewnative')
report=json.loads((O/'BLENDER_REPORT.json').read_text(encoding='utf-8'))
geomhash=hashlib.sha256((O/(PR+'_GEOMETRY.json')).read_bytes()).hexdigest()
check(report['geometry_sha256']==geomhash and report['entry_control_geometry_unchanged'],'render/source/control match')
native=json.loads((O/'NATIVE_REOPEN_REPORT.json').read_text(encoding='utf-8'))
check(native['passed'] and native['geometry_sha256']==geomhash,'native source')
result={'date':'2026-10-15','passed':not issues,'issues':issues,'scope':'finite2D reference checks and native source correspondence, NOT gameplay/engineering acceptance',
 'player':player,'shoe':shoe,'operating_footprint':foot,'nominal_shoe_cells':capacity,'highest_actual':maxz,
 'protected_inputs':len(g['protected_inputs']),'protected_differences':protected,'native':native,
 'unverified':['standing-to-seated posture transition','other seats/pair gaps not all through paths','8direction actual sprite/camera',
 'game collision/navigation/recovery/interactions','opposing cabinet operation/queue yielding','cabinet shoe fit.30/depth/slidinghardware',
 'terrace slopes/waterproofing/outlet','structural/fire/operatingcrowds','finalUV/pixeltexture/UE']}
(O/'CHECKS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
print(json.dumps({'passed':not issues,'issues':issues,'business_rest':player['rest']['business_min_distance'],'business_pulled':player['pulled']['business_min_distance'],'shoe':shoe},ensure_ascii=False))
if issues:raise SystemExit(1)
manifest={'asset':g['asset'],'revision':g['revision'],'date':'2026-10-15','status':'local reference revision awaiting planning review, not formalTrial',
 'git_base':g['git_base'],'original_unchanged':True,'files':[]}
for f in sorted(O.iterdir()):
 if f.is_file() and f.name!='manifest.json' and f.suffix!='.blend1':
  b=f.read_bytes();mode='raw'
  if f.suffix in ('.py','.cjs','.md','.json','.svg','.csv'):b=b.replace(b'\r\n',b'\n');mode='LF normalized text'
  manifest['files'].append({'file':f.name,'sha256':hashlib.sha256(b).hexdigest(),'bytes':f.stat().st_size,'hash_mode':mode,'lfs':f.suffix=='.blend'})
(O/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
