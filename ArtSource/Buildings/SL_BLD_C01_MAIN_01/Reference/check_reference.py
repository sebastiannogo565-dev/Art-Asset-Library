"""Cross-view contract checks; does not assert finite navigation/engineering acceptance."""
from pathlib import Path
import json,hashlib,math,base64,xml.etree.ElementTree as ET,re
from PIL import Image
O=Path(__file__).parent;PR='SL_BLD_C01_MAIN_01_REFERENCE_01'
g=json.loads((O/(PR+'_GEOMETRY.json')).read_text(encoding='utf-8'))
p=json.loads(Path(g['plan_source']).read_text(encoding='utf-8-sig'))
issues=[]
def check(ok,msg):
 if not ok:issues.append(msg)
def overlap(a,b):return max(0,min(a[2],b[2])-max(a[0],b[0]))*max(0,min(a[3],b[3])-max(a[1],b[1]))
def union_area(rs,clip=None):
 xs=sorted(set(v for r in rs+([clip] if clip else []) for v in (r[0],r[2])))
 ys=sorted(set(v for r in rs+([clip] if clip else []) for v in (r[1],r[3])))
 area=0
 for a,c in zip(xs,xs[1:]):
  for b,d in zip(ys,ys[1:]):
   x=(a+c)/2;y=(b+d)/2
   if any(r[0]<x<r[2] and r[1]<y<r[3] for r in rs) and (clip is None or clip[0]<x<clip[2] and clip[1]<y<clip[3]):area+=(c-a)*(d-b)
 return area
check(g['rooms']==p['rooms'],'PLAN rooms changed')
check(g['entrances']==p['entrances'],'three original entrances changed')
check(g['segments']==p['candidate']['segments'],'accepted segments changed')
check(g['control']==[0,0,150,28] and g['floors']==[0,4,8],'control/floors')
classes=[r for r in g['rooms'] if r['kind']=='classroom']
check(len(classes)==24 and all(abs(r['net_area']-75.6)<1e-8 for r in classes),'24classroom/75.6')
check(abs(union_area(g['body_rects'])-3016)<1e-8,'footprint3016')
check(g['court']==[74,15,86,24] and g['terrace']==[64,0,74,6],'court/terrace moved')
ids=[o['id'] for o in g['openings']];check(len(ids)==len(set(ids)),'opening IDs duplicated')
for o in g['openings']:
 check(o['hi']>o['lo'] and o['z1']>o['z0'],'opening negative')
 if o['kind']=='teaching':
  r=next(r for r in classes if r['id']==o['room'])
  check(o['side']=='N' and abs(o['line']-22)<1e-8 and r['rect'][0]<o['lo']<o['hi']<r['rect'][2],'classroom north window ownership')
  check(abs(o['z0']-((r['floor']-1)*4+.9))<1e-8,'classroom sill')
check(sum(o['kind']=='teaching' for o in g['openings'])==72,'72teachingwindows')
for n in ['30','36']:
 v=g['classroom_variants'][n];check(len(v['desks'])==int(n),'seat count')
 a,b,c,d=v['rect']
 for it in v['desks']:
  q=it['bounds'];sx,sy,sz=it['seat']
  check(a<=q[0]<q[3]<=c and b<=q[1]<q[4]<=d,'desk outside classroom')
  check(a<=sx-.225<sx+.225<=c and b<=sy-.225<sy+.225<=d,'chair outside classroom')
check(g['classroom_variants']['30']['rect']==g['classroom_variants']['36']['rect'],'comparison changed room')
capacity=0
for i,b in enumerate(g['lockers']):
 q=b['bounds'];r=next(r for r in g['rooms'] if r['id']==b['room']);a,c,d,e=r['rect']
 check(a<=q[0]<q[3]<=d and c<=q[1]<q[4]<=e,'locker outside assignedroom')
 capacity+=b['columns']*b['rows']*b['faces']
 for other in g['lockers'][i+1:]:
  check(overlap([q[0],q[1],q[3],q[4]],[other['bounds'][0],other['bounds'][1],other['bounds'][3],other['bounds'][4]])==0,'locker banks overlap')
check(capacity==900,'nominal900cells')
for it in g['furniture']:
 q=it['bounds'];r=g['terrace'] if it['room']=='TERRACE' else next(r['rect'] for r in g['rooms'] if r['id']==it['room'])
 check(r[0]<=q[0]<q[3]<=r[2] and r[1]<=q[1]<q[4]<=r[3],'public furnishing outside assigned room '+it['id'])
# Physical reference slabs/ceiling tiles must have ZERO positive intersection with required holes.
for floor in [2,3]:
 holes=[g['court']]+[s['opening'] for s in g['stairs']]
 for ob in [o for o in g['primitives'] if o['group']==f'SLAB_F{floor:02}']:
  b=ob['bounds'];r=[b[0],b[1],b[3],b[4]]
  for h in holes:check(overlap(r,h)==0,'slab bridges hole '+ob['id'])
 for ob in [o for o in g['primitives'] if o['group']==f'INTERIOR_F{floor-1:02}_CEILING']:
  b=ob['bounds'];r=[b[0],b[1],b[3],b[4]]
  for h in holes:check(overlap(r,h)==0,'lower ceiling bridges hole '+ob['id'])
for s in g['stairs']:
 a,b,c,d=s['opening'];check(abs(c-a-4.7)<1e-8 and abs(d-b-5.5)<1e-8,'stair opening')
 for f in [1,2]:
  steps=[o for o in g['primitives'] if o['id'].startswith(s['id']+f'_F{f}_R') and o['type']=='box']
  check(len(steps)==22,'11actualtreads/run + landing missing')
  check(all(abs(o['bounds'][3]-o['bounds'][0]-2.2)<1e-7 for o in steps),'stair clear tread width')
  for run in [0,1]:
   lo=a+run*2.5;hi=lo+2.2
   rails=[o for o in g['primitives'] if o['id'].startswith(s['id']+f'_F{f}_RAIL{run}')]
   check(len(rails)==2,'handrail pair')
   # edges entirely outside nominated tread net interval
   check(all(max(v[0] for v in q['vertices'])<lo or min(v[0] for v in q['vertices'])>hi for q in rails),'rail intrudes2.2net')
extent=[float('inf')]*3+[-float('inf')]*3
for ob in g['primitives']:
 q=ob['bounds'] if ob['type']=='box' else [min(v[j] for v in ob['vertices']) for j in range(3)]+[max(v[j] for v in ob['vertices']) for j in range(3)]
 check(q[0]>=-1e-7 and q[1]>=-1e-7 and q[3]<=150+1e-7 and q[4]<=28+1e-7,'building accessory outside control '+ob['id'])
 for j in range(3):extent[j]=min(extent[j],q[j]);extent[j+3]=max(extent[j+3],q[j+3])
support=union_area(g['body_rects'],g['rt01']['rect'])
check(abs(support-462)<1e-8 and g['rt01']['rect']==[38,3,66,24],'RT01 support/source')
protected=[]
for item in g['protected_inputs']:
 f=Path(item['path']);actual=hashlib.sha256(f.read_bytes()).hexdigest()
 if actual!=item['sha256']:protected.append(str(f))
check(not protected,'protected sources differ')
ch=Path(g['character']['source']);charhash=hashlib.sha256(ch.read_bytes()).hexdigest()
check(charhash=='082ceb410d904f0037dfe09dd3502e50195351691ab4047cc5dbbb639147b8cd','originalcharacter bytes')
images=[]
pages=sorted(O.glob(PR+'_P*.svg'))
check(len(pages)==11,'5main+6detail pages')
for path in pages:
 doc=ET.parse(path).getroot();check(doc.attrib['width']=='3200' and doc.attrib['height']=='2400','SVGnative')
 im=Image.open(path.with_suffix('.png'));check(im.size==(3200,2400) and im.mode=='RGB','nativeRGBPNG')
 images.append({'name':path.with_suffix('.png').name,'size':list(im.size),'mode':im.mode})
 for node in doc.iter('{http://www.w3.org/2000/svg}image'):
  uri=node.attrib.get('{http://www.w3.org/1999/xlink}href','')
  if uri.startswith('data:image/png;base64,'):
   raw=base64.b64decode(uri.split(',',1)[1])
   if Image.open(__import__('io').BytesIO(raw)).size==(128,128):check(hashlib.sha256(raw).hexdigest()==charhash,'embeddedoriginalcharacter')
for f in sorted(O.glob('Preview*.png')):
 im=Image.open(f);check(im.size==(2304,1296) and im.mode=='RGB','native preview spec')
check(len(list(O.glob('Preview*.png')))==7,'7previews')
hashgeom=hashlib.sha256((O/(PR+'_GEOMETRY.json')).read_bytes()).hexdigest()
report=json.loads((O/'BLENDER_REPORT.json').read_text(encoding='utf-8'))
check(report['geometry_sha256']==hashgeom,'renders stale geometry')
native=json.loads((O/'NATIVE_REOPEN_REPORT.json').read_text(encoding='utf-8'))
check(native['geometry_sha256']==hashgeom and native['whole_source_ids']==len(g['primitives']) and native['reopen_passed'],'native reference stale/source mismatch')
result={'date':'2026-10-15','passed':not issues,'scope':'reference contract only, not finite actor/game/engineering acceptance','issues':issues,
 'rooms':len(g['rooms']),'classrooms':24,'openings':len(ids),'north_classroom_windows':72,
 'building_extent_xyz':extent,'body_footprint_m2':3016,'court_area_m2':108,'terrace_area_m2':60,
 'nominal_shoe_cells':capacity,'RT01_original_m2':588,'RT01_supported_projection_m2':support,'RT01_unsupported_projection_m2':588-support,
 'protected_input_count':len(g['protected_inputs']),'protected_differences':protected,'character_sha256':charhash,
 'native_images':images,'previews':{'count':7,'native':[2304,1296]},'geometry_sha256':hashgeom,
 'actual_blender_source_reopened':native,'AI_calls':0,'formal_model':False,'final_UV_textures':False,'UE_writes':0,
 'unverified':g['annotations']['not_verified']}
(O/(PR+'_CHECKS.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
print(json.dumps({'passed':not issues,'issues':issues,'protected':len(g['protected_inputs']),'RT01_supported':support},ensure_ascii=False))
if issues:raise SystemExit(1)
manifest={'date':'2026-10-15','asset':g['asset'],'revision':'REFERENCE_01','status':'delivered reference awaiting planning and user review; no Trial authorization',
 'scope':'5main +6detail SVG/PNG,7shared reference renders,editable reference blend; no formal model/UV/UE',
 'git_base':'9a0850b4478a071d1a03760da4548cd1f70aa5d2','AI_calls':0,'files':[]}
for f in sorted(O.iterdir()):
 if not f.is_file() or f.name=='manifest.json' or f.suffix=='.blend1':continue
 raw=f.read_bytes();mode='raw'
 if f.suffix in ('.py','.cjs','.md','.json','.svg','.csv'):raw=raw.replace(b'\r\n',b'\n');mode='text normalized LF'
 manifest['files'].append({'file':f.name,'bytes':f.stat().st_size,'sha256':hashlib.sha256(raw).hexdigest(),'hash_mode':mode,'lfs':f.suffix=='.blend'})
(O/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
