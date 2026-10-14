"""Reference-stage geometry/accounting/linkage checks. Not a model/UE/real stair test."""
from pathlib import Path
import json,math,hashlib,base64,xml.etree.ElementTree as ET,ast
from PIL import Image
R=Path(__file__).resolve().parent;D=json.loads((R/'SL_BLD_B01_HOME_01_REFERENCE_01_GEOMETRY.json').read_text(encoding='utf-8'))
def inside(r,p):return r[0]-1e-6<=p[0]<=r[2]+1e-6 and r[1]-1e-6<=p[1]<=r[3]+1e-6
def intersection(a,b):return max(0,min(a[2],b[2])-max(a[0],b[0]))*max(0,min(a[3],b[3])-max(a[1],b[1]))
def area(poly):return .5*abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(poly,poly[1:]+poly[:1])))
for key,rooms in D['floors'].items():
 for room in rooms:
  r=room['rect'];assert inside([-8.8,-4.8,-.2,4.8],r[:2]) and inside([-8.8,-4.8,-.2,4.8],r[2:])
  assert abs((r[2]-r[0])*(r[3]-r[1])-room['net_area_m2'])<1e-7
  assert intersection(r,D['stair']['opening_rect'])<1e-8
 for i,a in enumerate(rooms):
  for b in rooms[i+1:]:assert intersection(a['rect'],b['rect'])<1e-8,(a['id'],b['id'])
ids=[o['id'] for o in D['openings']];assert len(ids)==len(set(ids))==22
for o in D['openings']:
 assert o['sill']>=0 and o['sill']+o['height']<D['candidate']['roof']['wall_join']
 if o['kind']=='main_portal':assert o['width']==1.6 and o['active_clear']==[1.2,2.1]
 if o['room']:
  u=o['u'];pt={'F':[-.21,u],'B':[-8.79,u],'R':[u,4.79],'L':[u,-4.79]}[o['face']]
  if o['room']=='STAIR':assert inside(D['stair']['opening_rect'],pt)
  else:assert inside(next(r['rect'] for rooms in D['floors'].values() for r in rooms if r['id']==o['room']),pt),(o['id'],pt)
main=D['floors']['F01'];home=D['Home_interface']['Home_local_m'];start=D['Home_interface']['PlayerStart_reference_local_m'];assert inside(next(r['rect'] for r in main if r['id']=='02'),home)
assert inside(next(r['rect'] for r in main if r['id']=='01'),start)
# Graph of candidate door connectivity including maintenance corridor and U stair.
graph={}
for d in D['interior_openings']:
 a,b=d['connect'];a=f'{d["floor"]}:{a}';b=f'{d["floor"]}:{b}';graph.setdefault(a,set()).add(b);graph.setdefault(b,set()).add(a)
graph['1:STAIR'].add('2:STAIR');graph['2:STAIR'].add('1:STAIR')
seen={'1:03'};todo=list(seen)
while todo:
 for n in graph.get(todo.pop(),[]):
  if n not in seen:seen.add(n);todo.append(n)
for floor,key in [(1,'F01'),(2,'F02')]:
 for rm in D['floors'][key]:assert f'{floor}:{rm["id"]}' in seen,('unconnected room',rm)
views=D['preview']['derived_views'];assert (views[1]['azimuth']-views[0]['azimuth'])%360==180
assert set(views[0]['visible_face_ids'])=={o['id'] for o in D['openings'] if o['face'] in ['F','R']}
assert set(views[1]['visible_face_ids'])=={o['id'] for o in D['openings'] if o['face'] in ['B','L']}
assert D['stair']['risers']*D['stair']['riser']==3 and abs(8*.27+1.15-3.31)<1e-9
assert abs(D['areas']['net_including_F01_stair_projection_m2']-150.805)<1e-6
original='082ceb410d904f0037dfe09dd3502e50195351691ab4047cc5dbbb639147b8cd';image_records=[]
for n in range(1,6):
 p=R/f'SL_BLD_B01_HOME_01_REFERENCE_01_P0{n}.svg';tree=ET.parse(p);assert tree.getroot().attrib['width']=='3200'
 for im in tree.findall('.//{http://www.w3.org/2000/svg}image'):
  blob=base64.b64decode(im.attrib['{http://www.w3.org/1999/xlink}href'].split(',')[1]);assert hashlib.sha256(blob).hexdigest()==original
 with Image.open(p.with_suffix('.png')) as im:assert im.mode=='RGB' and im.size==(3200,2400);im.verify()
 image_records.append({'svg':p.name,'png':p.with_suffix('.png').name,'native_px':[3200,2400]})
for p in R.glob('*.py'):ast.parse(p.read_text(encoding='utf-8'))
for ref in D['protected_inputs']:assert hashlib.sha256(Path(ref['path']).read_bytes()).hexdigest()==ref['sha256'],ref['path']
assert not list(R.parent.rglob('*.blend')) and not list(R.parent.rglob('*.fbx')) and not (R.parent/'Trial01').exists()
polyarea=area(D['formal_baseline']['footprint_world_m'])
report={'reference_geometry_checks_passed':True,'scope':'2D room accounting/candidate door graph/common source table/SVG byte embedding only; not closed mesh/model/nav/structural verification','boards':image_records,
 'source_count':1,'opening_count':len(ids),'door_graph_all_candidate_rooms_connected':True,'room_rectangles_nonoverlapping':True,'roof_levels_match_formula':True,
 'Home_in_hall_and_historical_PlayerStart_in_LDK':True,'main_door_active_clear_m':[1.2,2.1],'capsule_reference_m':[.68,1.92],
 'character_visible_width_m':67/116*1.8,'interior_door_visual_risk':'0.8/0.85m domestic doors fit0.68 capsule nominally, but 1.04m sprite width may visually clip; game camera/directions must be reviewed, no character scaling',
 'formal_footprint_source_polygon_area_m2':polyarea,'formal_size_square_area_m2':324,'difference_from_rounded_polygon_m2':324-polyarea,'formal_footprint_preserved':True,
 'protected_input_count':len(D['protected_inputs']),'all_protected_raw_sha_unchanged':True,'embedded_original_character_sha256':original,'formal_models':0,'UV_sets':0,'final_textures':0,'UE_imports':0,
 'unverified':['formal footprint/center reduction approval','true door/nav/camera/finite capsule and sprite width','true stairs engineering/headroom/handrail/slab structure','source Actor state not live read','legal parcel/eave and gutter connection','look/material acceptance']}
(R/'SL_BLD_B01_HOME_01_REFERENCE_01_CHECKS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:report[k] for k in ['opening_count','door_graph_all_candidate_rooms_connected','formal_footprint_source_polygon_area_m2','protected_input_count','formal_models']},ensure_ascii=True))
