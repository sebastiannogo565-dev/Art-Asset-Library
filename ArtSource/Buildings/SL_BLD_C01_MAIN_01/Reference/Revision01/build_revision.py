"""Local reference revision, load original read-only and save only Revision01."""
from pathlib import Path
import json,copy,hashlib,csv,ast,math,html,base64
ROOT=Path('D:/Art Asset Library');OUT=Path(__file__).parent;BASE=OUT.parent
OLD='SL_BLD_C01_MAIN_01_REFERENCE_01';PREFIX=OLD+'_REV_01'
original=json.loads((BASE/(OLD+'_GEOMETRY.json')).read_text(encoding='utf-8'))
G=copy.deepcopy(original);G['revision']='REFERENCE_01_REV_01'
G['parent_geometry']=str(BASE/(OLD+'_GEOMETRY.json'))
G['parent_sha256']=hashlib.sha256((BASE/(OLD+'_GEOMETRY.json')).read_bytes()).hexdigest()
snapshot=ROOT/'.cache/c01_revision/protected.json'
G['protected_inputs']=json.loads(snapshot.read_text(encoding='utf-8')) if snapshot.exists() else json.loads((OUT/(PREFIX+'_GEOMETRY.json')).read_text(encoding='utf-8'))['protected_inputs']
G['git_base']='45f00a233481e9cc73be30ac83b455523d12c551'
G['rt01']['status']='retained original588m2 control, NOT OPEN, approach/support NOT established'
G['roof'].update(glass_peak=13.65,geometry_max=13.68,terrace_finish_top=8.03,terrace_effective_guard_height=1.2)
def box(name,b,mat,group):
 G['primitives'].append(dict(id=name,type='box',bounds=b,material=mat,group=group))
# 30 seats: 5 teaching rows, 6 columns in 3 pairs. Wide cross aisle follows original door x45.
G['primitives']=[p for p in G['primitives'] if not p['id'].startswith('C30_')]
xs=[42.625,43.575,45.775,46.725,47.675]
ys=[14.125,15.025,16.875,17.775,19.625,20.525]
desks=[]
for i,x in enumerate(xs):
 for j,y in enumerate(ys):
  id=f'C30_DESK_{i+1}_{j+1}';b=[x-.225,y-.325,4.69,x+.225,y+.325,4.72]
  seat=[x+.4,y,4.43];desks.append(dict(id=id,kind='desk',bounds=b,seat=seat,pulled_seat=[seat[0]+.25,y,4.43]))
  box(id,b,'WOOD','INTERIOR_F02_PLAYER')
  for lx in [x-.18,x+.18]:
   for ly in [y-.26,y+.26]:box(id+f'_leg{lx}_{ly}',[lx-.02,ly-.02,4,lx+.02,ly+.02,4.69],'FRAME','INTERIOR_F02_PLAYER')
  sx,sy,sz=seat
  box(id+'_CHAIR',[sx-.225,sy-.225,sz-.035,sx+.225,sy+.225,sz],'CHAIR','INTERIOR_F02_PLAYER')
  box(id+'_CHAIR_BACK',[sx+.16,sy-.225,sz,sx+.22,sy+.225,4.84],'CHAIR','INTERIOR_F02_PLAYER')
  for lx in [sx-.18,sx+.18]:
   for ly in [sy-.18,sy+.18]:box(id+f'_CHAIRLEG_{lx}_{ly}',[lx-.018,ly-.018,4,lx+.018,ly+.018,sz-.035],'FRAME','INTERIOR_F02_PLAYER')
G['classroom_variants']['30']={'room':'F2_W4','rect':[41,12.7,49.4,21.7],'front':'west -X','rows':5,'columns':6,
 'groups':'3 paired columns; .25 pair gaps NON-THROUGH; aisles y15.35..16.55 and18.1..19.3',
 'desks':desks,'desk_size':[.45,.65,.72],'chair_size':[.45,.45,.43],
 'main_cross_aisle_rest':[44.2,12.7,45.55,21.7],'main_cross_aisle_pulled':[44.45,12.7,45.55,21.7],
 'min_main_rest':1.2,'min_main_pulled':1.1,'pair_gap':.25,'front_clear':1.4,'rear_rest':1.1,'rear_pulled':.85,
 'north_remainder':.85,'south_remainder':1.1,'chair_pullback_allowance':.25,
 'note':'Main nominated route checked with finite2D envelopes in two states. Pair gap .25,row gaps .10,rear .85 after pull not declared routes. Seat transfer remains a posture/interaction transition, not standing walk through own chair.'}
G['player_interface']={'business_semantic_xy':[45,19.5],'floor_local':4,'engineering_z':12,
 'designated_seat_id':'C30_DESK_3_5','seat_rest':[46.175,19.625,4.43],'seat_pulled':[46.425,19.625,4.43],
 'standing_approach':[46.425,18.7,4],'candidate_recovery':[45,18.7,4],
 'business_footprint_clear_target':['capsule radius.34','visible width1.039655/2 proxy'],
 'route_to_approach':[[45,12.7],[45,18.7],[46.425,18.7]],
 'seat_transfer':[[46.425,18.7],[46.425,19.625]],
 'route_return_via_teaching':[[46.425,18.7],[45,18.7],[41.7,18.7],[45,18.7],[45,12.7]],
 'seat_transfer_status':'non-standing seating transition; own chair occupies endpoint; NOT a proven continuous standing path',
 'candidate_recovery_status':'reference candidate only, no engineering/UE point or interaction radius change'}
# Main shoe banks thinner to .60m, 900 nominal grid remains. One cabinet-face use strip .70m,
# opposite face in an aisle inactive: 2.0-.70=1.30 walking remainder; not simultaneous queues.
for b in G['lockers']:
 if b['room']=='F1_WL':
  y=(b['bounds'][1]+b['bounds'][4])/2;b['bounds'][1]=y-.3;b['bounds'][4]=y+.3;b['depth_each']=.30
for p in G['primitives']:
 if p['id'].startswith('LOCKER_MAIN_'):
  bank=next(b for b in G['lockers'] if p['id']=='LOCKER_'+b['id']);p['bounds']=bank['bounds'][:]
 elif p['id'].startswith('CELL_MAIN_'):
  bank=next(b for b in G['lockers'] if p['id'].startswith('CELL_'+b['id']+'_'))
  # Existing thin sliding-door face keeps no outward swing. Move with bank depth.
  face=int(p['id'].split('_')[-3]);b=bank['bounds'];y=b[1]-.005 if face==0 else b[4]+.005
  p['bounds'][1]=y-.007;p['bounds'][4]=y+.007
for it in G['furniture']:
 if it['id'] in ('P1_CHANGE_W','P1_WAIT'):
  it['bounds'][1]=.3;it['bounds'][4]=.75
  next(p for p in G['primitives'] if p['id']==it['id'])['bounds']=it['bounds'][:]
room=next(r for r in G['rooms'] if r['id']=='F1_WL');room['door_width']=3.0
G['openings'].append(dict(id='F1_WL_D_REV',axis='X',line=8.9,lo=23.5,hi=26.5,z0=0,z1=2.6,kind='sliding_internal',room='F1_WL',side='INTERIOR',normal=0))
box('F1_WL_N_REV_L',[18.3,8.8,0,23.5,9,3.45],'WALL','INTERIOR_F01_WALLS')
box('F1_WL_N_REV_R',[26.5,8.8,0,29.7,9,3.45],'WALL','INTERIOR_F01_WALLS')
box('F1_WL_N_REV_HEADER',[23.5,8.8,2.6,26.5,9,3.45],'WALL','INTERIOR_F01_WALLS')
G['shoe_capacity'].update(main_bank_gap=2.0,main_bank_depth=.6,main_operating_strip=.7,
 active_face_walking_remainder=1.3,inner_door_width=3.0,inner_door_previous=1.4,
 door_policy='vertical sliding cell-door candidate, no outward swing; hardware not validated',
 operating_policy='one active cabinet face per aisle, opposite queue held; two active faces leaves .6m, NOT accepted',
 queue_waiting='side niches only, never within23.5..26.5 main passage',
 main_bank_depth_tradeoff='.35->.30 each face; adult shoe fit/door hardware must be verified')
G['shoe_circulation']={'arrival':[[25,0],[24.25,1.375],[24.25,3.95],[21,3.95]],
 'operation':[[21,3.95],[21,2.962]],'operation_footprint':[20.48,2.622,21.52,3.302],
 'to_wait':[[21,2.962],[21,3.95],[24.25,3.95],[24.25,1.375],[28,1.375]],
 'departure':[[28,1.375],[25.75,1.375],[25.75,8.9],[25.75,10.9]],
 'waiting_point':[28,1.375],'queue_markers':[[22.9,6.2],[22.9,7.9]],
 'operating_strip_active':[18.7,2.612,22.3,3.312],
 'opposite_strip_inactive':[18.7,3.9,22.3,4.6],
 'operational_limit':'front1.375 crossing requires yielding; two queue markers only outside nominated lower-bank route; upper-bank access must release queue. Actual cell-face projection.012m leaves1.276m not nominal1.30m; inactive opposite strip unoccupied'}
# Material-only geometry controls; portal bounds/vertices remain EXACTLY original.
G['materials'].update(ENTRY_WOOD='#CFA878',ENTRY_FRAME='#99A59D',BAND_REV='#BAC1B8')
material_changes=[]
def recolor(p):
 old=p['material'];new=old
 if p['id'] in ('MAIN_WOOD_PORTAL_L','MAIN_WOOD_PORTAL_R','MAIN_BLANK_NAME_STRIP'):new='ENTRY_WOOD'
 elif p['id'].startswith('C01_MAIN_') and ('frame' in p['id'] or 'mullion' in p['id']):new='ENTRY_FRAME'
 elif p['id'].startswith('BAND_'):new='BAND_REV'
 if new!=old:p['material']=new;material_changes.append({'id':p['id'],'old':old,'new':new})
for p in G['primitives']:recolor(p)
G['material_changes']=material_changes
# Threshold/sill at finish8.03; header/gap follow door clear height2.60.
for o in G['openings']:
 if o['id']=='TERRACE_ACCESS':o['z0']=8.03;o['z1']=10.63
for p in G['primitives']:
 if p['id'].startswith('TERRACE_ACCESS_'):
  p['bounds'][2]+=.03;p['bounds'][5]+=.03
 elif p['id'].startswith('TERRACE_GUARD_'):
  p['bounds'][2]=8.03;p['bounds'][5]=9.23
 elif p['type']=='box' and p['id'].startswith('W_3_'):
  b=p['bounds']
  if 68.19<=b[0]<=69.8 and b[3]<=69.801 and 5.69<=b[1]<=6.01 and abs(b[2]-10.6)<1e-7:b[2]=10.63
box('TERRACE_CHANNEL_CANDIDATE',[73.55,.15,8.01,73.8,4.7,8.03],'METAL','INTERIOR_F03_TERRACE')
box('TERRACE_DRAIN_CANDIDATE',[73.64,0,.15,73.72,.08,8.03],'METAL','EXTERIOR_DRAIN')
G['terrace_interface']={'finish':8.03,'slab_top':8,'door_bottom':8.03,'door_top':10.63,'clear_height':2.6,
 'threshold_delta':0,'guard_bottom':8.03,'guard_top':9.23,'effective_height':1.2,
 'drain_route_candidate':[[73.675,4.7,8.03],[73.675,.15,8.03],[73.68,0,.15]],
 'status':'candidate linear channel to concealed rainwater riser, local falls/waterproofing/outlet network unverified. No fictitious fixed slope over30mm finish.'}
G['cameras']['CLASS']['elevation']=50 # actual parent render used50, metadata previously said42
G['revision_cameras']={'CLASS':{'target':[45.2,17.2,4.8],'azimuth':45,'elevation':50,'scale':13},
 'SHOES':{'target':[24,4.5,.7],'azimuth':270,'elevation':55,'scale':16},
 'ENTRY':{'target':[25,3,2],'azimuth':240,'elevation':18,'scale':22}}
G['view_sync']={'P01':'original/old appearance only, not revised material preview','P02':'rebuilt','P02A':'rebuilt',
 'P02B':'rebuilt','P02C':'rebuilt','P03':'rebuilt material assignment','P04':'rebuilt/no usable RT01 route',
 'P04A':'rebuilt threshold/guard','P05':'rebuilt current A/B','P05A':'rebuilt CLASS/SHOES, unchanged COURT/LINK linked original',
 'P05B':'rebuilt exact original ENTRY before/current color-control after, actual revised ENTRY also delivered'}
G['annotations']['not_verified']+=['seating transfer from aisle to own chair','cabinet depth.30 and sliding hardware',
 'simultaneous opposing cabinet operation','queue yielding/crowds','terrace local falls/outlet/waterproofing']
(OUT/(PREFIX+'_GEOMETRY.json')).write_text(json.dumps(G,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
with (OUT/'OPENINGS.csv').open('w',encoding='utf-8-sig',newline='') as f:
 fields=sorted(set(k for o in G['openings'] for k in o))
 w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(G['openings'])
# Derive reusable vector helpers without executing original builder or writing parent package.
source=(BASE/'build_reference.py').read_text(encoding='utf-8')
tree=ast.parse(source);ns=globals()
for node in tree.body:
 if isinstance(node,(ast.FunctionDef,ast.ClassDef)) and node.name in ('Sheet','dim','plan','char','projected','roof_plan','section'):
  text=ast.get_source_segment(source,node)
  if node.name=='Sheet':text=text.replace('C01 REFERENCE_01 ·','C01 REFERENCE_01_REV_01 ·')
  if node.name=='plan':text=text.replace('(dx-.8)','(dx-r["door_width"]/2)').replace('(dx+.8)','(dx+r["door_width"]/2)')
  if node.name=='roof_plan':
   text=text.replace('route=[[34,8.8],[34,10.9],[49,10.9],[49,14]]','route=[]')
   text=text.replace("s.text(ox+30*k,oy-7*k,'S1延伸上屋面待审',22)","s.text(ox+45*k,oy-7*k,'RT01待设计 / 本次不开放',22)")
  exec(compile(text,str(BASE/'build_reference.py'),'exec'),ns)
# Helpers refer to current G/OUT/PREFIX; image override permits explicit original comparisons.
def picture(s,path,x,y,w,h):
 raw=Path(path).read_bytes();uri=base64.b64encode(raw).decode()
 s.a.append(f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet" xlink:href="data:image/png;base64,{uri}"/>')
def route(s,pts,ox,oy,k,col='#BD8556',w=6):
 for p,q in zip(pts,pts[1:]):s.line(ox+p[0]*k,oy-p[1]*k,ox+q[0]*k,oy-q[1]*k,col,w)
def classroom(s,count,ox,oy,k=90):
 v=G['classroom_variants'][str(count)];a,b,c,d=v['rect']
 s.rect(ox,oy,8.4*k,9*k,'#FBFAF5',sw=3)
 if count==30:
  for r in [[44.45,12.7,45.55,21.7],[41.2,15.35,49.4,16.55],[41.2,18.1,49.4,19.3]]:
   s.rect(ox+(r[0]-a)*k,oy+(d-r[3])*k,(r[2]-r[0])*k,(r[3]-r[1])*k,'#DFEADF','#B6C9BB',1)
 for it in v['desks']:
  q=it['bounds'];x=ox+(q[0]-a)*k;y=oy+(d-q[4])*k
  s.rect(x,y,.45*k,.65*k,'#AC875A',sw=1);sx,sy,sz=it['seat']
  s.rect(ox+(sx-.225-a)*k,oy+(d-sy-.225)*k,.45*k,.45*k,'#CCC2AA',sw=1)
  if count==30:
   s.rect(ox+(sx+.25-.225-a)*k,oy+(d-sy-.225)*k,.45*k,.45*k,'none','#B48166',1.5)
 s.rect(ox+.05*k,oy+2.7*k,.07*k,4*k,'#38625A');s.rect(ox+.45*k,oy+4.1*k,.6*k,1.2*k,'#AC875A')
 s.line(ox+3.2*k,oy+9*k,ox+4.8*k,oy+9*k,'#B3734F',8)
 for o in G['openings']:
  if o['room']=='F2_W4' and o['side']=='N':s.line(ox+(o['lo']-a)*k,oy,ox+(o['hi']-a)*k,oy,'#527A88',7)
 s.text(ox,oy-30,f'{count}席 / '+('5排×3双列组，椅实线使用 / 空线后拉0.25' if count==30 else '6×6原版容量比较，非等价可用'),27)
 if count==30:
  conv=lambda pts:[[p[0]-a,d-p[1]] for p in pts]
  # route helper has -Y projection; use negated local screenY
  for key,col in [('route_to_approach','#C0804E'),('route_return_via_teaching','#5C8A86')]:
   pp=[[p[0]-a,p[1]-d] for p in G['player_interface'][key]];route(s,pp,ox,oy,k,col,5)
  pp=[[p[0]-a,p[1]-d] for p in G['player_interface']['seat_transfer']];route(s,pp,ox,oy,k,'#8E679B',3)
  for label,p,col in [('业务',[45,19.5],'#9B5F66'),('恢复',[45,18.7],'#527B94'),('玩家席',[46.175,19.625],'#735F9A'),('站位',[46.425,18.7],'#735F9A')]:
   x=ox+(p[0]-a)*k;y=oy+(d-p[1])*k;s.rect(x-5,y-5,10,10,col,col,1);s.text(x+12,y-8,label,20)
   if label in ('业务','恢复','站位'):
    for radius,dash in [(G['character']['capsule_diameter']/2,''),(G['character']['visible_front_width']/2,'7 5')]:
     s.a.append(f'<circle cx="{x}" cy="{y}" r="{radius*k}" fill="none" stroke="{col}" stroke-width="2" stroke-dasharray="{dash}"/>')
 dim(s,ox,oy+9*k+35,ox+8.4*k,oy+9*k+35,'净8.4×9m / 门1.6×2.6')
def shoes(s,ox,oy,k=65):
 a,b,c,d=18.3,.3,29.7,8.8
 s.rect(ox,oy,11.4*k,8.5*k,'#FBF9F1',sw=3)
 for bank in [v for v in G['lockers'] if v['room']=='F1_WL']:
  q=bank['bounds'];s.rect(ox+(q[0]-a)*k,oy+(d-q[4])*k,(q[3]-q[0])*k,.6*k,'#A98B61')
 for it in G['furniture']:
  if it['room']!='F1_WL':continue
  q=it['bounds'];s.rect(ox+(q[0]-a)*k,oy+(d-q[4])*k,(q[3]-q[0])*k,(q[4]-q[1])*k,'#DBCAB1')
 for q,col in [([23.5,.3,25,8.8],'#D9EAD7'),([25,.3,26.5,8.8],'#D6E5E7'),(G['shoe_circulation']['operating_strip_active'],'#E7C8A6')]:
  s.rect(ox+(q[0]-a)*k,oy+(d-q[3])*k,(q[2]-q[0])*k,(q[3]-q[1])*k,col,'#899B8B',1)
 for key,col in [('arrival','#BA7F4E'),('to_wait','#9F8B50'),('departure','#4F8E8A')]:
  # Crop this room view at the inner opening; full outside continuation remains P02/JSON.
  points=G['shoe_circulation'][key]
  if key=='departure':points=points[:-1]
  pp=[[p[0]-a,min(p[1],d)-d] for p in points];route(s,pp,ox,oy,k,col,4)
 pp=[[p[0]-a,p[1]-d] for p in G['shoe_circulation']['operation']];route(s,pp,ox,oy,k,'#9A6951',4)
 q=G['shoe_circulation']['operation_footprint'];s.rect(ox+(q[0]-a)*k,oy+(d-q[3])*k,(q[2]-q[0])*k,(q[3]-q[1])*k,'none','#A16C52',3)
 for i,p in enumerate(G['shoe_circulation']['queue_markers']):
  x=ox+(p[0]-a)*k;y=oy+(d-p[1])*k;s.a.append(f'<circle cx="{x}" cy="{y}" r="{.52*k}" fill="none" stroke="#9D8470" stroke-width="2"/>')
  s.text(x,y,'Q'+str(i+1),18,anchor='middle')
 s.line(ox+(23.5-a)*k,oy,ox+(26.5-a)*k,oy,'#B3734F',7)
 s.text(ox,oy-25,'厅→主廊：新净3.0 / 原1.4；外门仍25/0、3.0',27)
 s.text(ox,oy+8.5*k+38,'橙去 / 黄换鞋后等候 / 青离开；前端交叉点需让行',24)
def boards():
 s=Sheet('C01 REV01 · 三层平面与修订接口','P02 / 只改30席家具与首层鞋柜内廊口；房间/外门/24班/庭露台保持')
 for f,oy in [(1,830),(2,1470),(3,2110)]:
  s.text(100,oy-530,f'F0{f} / FL{(f-1)*4}',30);plan(s,f,120,oy,19)
  s.text(120,oy+100,['F1_WL内廊口1.4→3.0；600＋300名义格，柜面错时，外门坐标不变',
    'F2_W4 30席新三双列组；业务45/19.5原样，候选恢复45/18.7，工程Z12',
    '露台门底8.03、护栏顶9.23；RT01只保控制区，不开放、不新增可用接近'][f-1],26)
 s.save('P02')
 s=Sheet('C01 REV01 · 30席通路、站位与36席比较','P02A / 使用与后拉两状态 / 绿色主通道，配对0.25缝非通路；入座段单独标')
 classroom(s,30,100,300,95);classroom(s,36,1130,300,95)
 s.note(2140,310,['30席：5排×6列＝30',
  '中横道使用1.35，后拉仍1.10',
  '两道1.20；教学前场1.40',
  '原业务45/19.5：家具净区保留',
  '玩家席46.175/19.625',
  '后拉席46.425/19.625',
  '实际站位46.425/18.70',
  '候选恢复45/18.70 / FL4',
  '门→站位→前场→门有限包络核',
  '入座段需姿态转换，不当站立路',
  '椅后拉0.25，后侧余0.85非主路',
  '36原列道0.79，仍只作比较'],25,46)
 s.note(110,1340,['原人物可见宽1.039655、胶囊0.68分别对照；主线最窄1.10，宽代理余约60mm。',
  '业务点到桌/椅最小距离与路线有限圆/座位使用区结果见CHECKS；不宣称实际恢复/入座/八向游戏通过。'],26,48)
 s.text(110,1510,'原业务点净区 / 原字节人物 / 坐姿接口',31)
 char(s,120,2170,170)
 s.note(650,1690,['原业务(45,19.5,4) → 工程(4500,7050,1200)cm',
  '候选恢复(45,18.7,4) → 工程(4500,6970,1200)cm',
  '玩家席距原业务约1.18m，后拉约1.43m，站位约1.63m',
  '仍在原230cm半径范围的二维预算；未修改工程点或半径。',
  '配对0.25缝、排间0.10缝与后拉后侧0.85余隙不列行走路。',
  '橙：门→玩家站位；青：离席站位→教学前场→原门；紫：入座姿态段。'],28,62)
 s.save('P02A')
 s=Sheet('C01 REV01 · 鞋柜分区与去回实排','P02B / 外门不迁，内廊口3m；900名义格；运营不是仅格数通过')
 shoes(s,100,320,100)
 s.note(1370,300,['主厅96.90㎡：600格；补厅99.18㎡：300格',
  '主6柜总深0.60，每面0.30，原0.70/0.35',
  '补2柜深0.70不变；名义列/行/双面未减',
  '主柜列名义净2.00，使用带0.70',
  '余名义1.30 / 含柜面实余1.276',
  '两侧操作实余0.576，不认定通过',
  '垂直上移柜门候选，无向外门扇占道',
  '主线3.00，去/回各1.50；内门同宽3.00',
  '柜端1.20与东端0.40分别标，东端非通路',
  '换鞋凳前移至y0.30–0.75，前操作区净1.25',
  '等候在东侧28/1.375，队列不伸主中央线',
  '前端去回交叉要让行；集中排队/运营未验',
  '0.30深实际鞋长、滑门五金与两侧错时待审'],27,56)
 s.text(110,1400,'补充柜列：2×15×5×2＝300；主：3×(12＋8)×5×2＝600，合900',29)
 s.note(110,1490,['正常到达：外门→西半主线→柜列通道→柜前；离开柜前回通道，再到东等候凹口。',
  '主廊离开：东等候→东半主线→3m内廊口→y10.9；返回外门另经中央通道，交叉需让行。',
  '指定柜面操作占位1.04宽×0.68深，位于0.70深使用带；不是能任意旋转的1.04m圆。',
  '每条站立主线与静态家具/候选使用区分开核。内门无外摆扇；900是名义容量，不声称高峰集散通过。'],28,64)
 s.save('P02B')
 s=Sheet('C01 REV01 · 入口/公共接口同步','P02C / 其他公共家具与访问边界继承原版；鞋柜与露台实际受影响局部重制')
 shoes(s,100,330,82)
 s.text(1250,290,'60㎡露台接口 / 平面未变',31)
 s.rect(1260,350,1200,720,'#E6E8DC',sw=4)
 for it in [v for v in G['furniture'] if v['room']=='TERRACE']:
  q=it['bounds'];s.rect(1260+(q[0]-64)*120,350+(6-q[4])*120,(q[3]-q[0])*120,(q[4]-q[1])*120,'#AF946F')
 s.line(1260+4.2*120,350,1260+5.8*120,350,'#B37D55',8)
 s.text(1260,1130,'门底8.03；南/东/西有效围护1.20，从完成面起算',27)
 route(s,[[9.675,1.3],[9.675,5.85]],1260,1070,120,'#698F9B',6)
 s.note(120,1430,['P1去回/换鞋/等候见上图；P2/P3/P4/P5公共家具、主廊与访问控制未改，原版仅这些内容可继承。',
  'P6露台门仍(69,6)，底8.03 / 净高2.60，围护底8.03顶9.23；排水口/内嵌竖管只候选。',
  'RT01：588㎡原控制区/入口(49,14)保留，当前不开放，不继承旧虚线作为可用通道。'],29,66)
 s.save('P02C')
 s=Sheet('C01 REV01 · 四立面与材质归属','P03 / 实际几何统一，温暖入口与淡层边；与旧立面材色分版')
 projected(s,'S',140,650,18.8);projected(s,'N',140,1120,18.8);projected(s,'W',130,1660,28);projected(s,'E',1210,1660,28)
 s.note(2210,1380,['玻璃13.65 / 含框13.68',
  'ENTRY_WOOD #CFA878',
  'ENTRY_FRAME #99A59D',
  'BAND_REV #BAC1B8',
  '门框/空白名带几何原样',
  '新旧日光对照见P05B',
  '层边改浅灰，不替换所有窗框'],27,53)
 s.note(110,1920,['开口表同步内廊净3.0与露台门底8.03；窗口/分段/屋面/外门未改。立面图依据REV_01。',
  '材色仍为平色参考，无新增像素贴图/UV。原版32/64小样只继承为密度示意，未作为新版实际纹理效果。'],29,60)
 s.save('P03')
 s=Sheet('C01 REV01 · 屋面高度与RT01待设计控制','P04 / 玻璃13.65，框顶/整栋几何最高13.68；RT01当前不开放')
 roof_plan(s,130,820,19)
 s.note(130,950,['最高相对首层13.68 / 工程21.68；玻璃脊13.65 / 工程21.65，两口径同时保留。',
  'RT01原588㎡、ID/范围/49,14入口原样；462投影及缺126不认定承托成立。本次无新专梯/平台/可用接近。',
  '露台FL8＋30mm＝8.03；门底8.03、围护顶9.23。历史8.25体块帽不用于当前接口。'],28,49)
 section(s,'COURT',130,2170,72)
 s.note(2270,1320,['庭孔108㎡同位，孔与分组未改',
  '玻璃顶13.65 / 框件＋0.03',
  '所有高度均相对首层',
  '工程高程额外＋8',
  '屋面坡度/檐脊继承认可版本',
  'RT01控制是待设计层，非导航面'],27,56)
 s.save('P04')
 s=Sheet('C01 REV01 · 露台门槛、围护与候选排水','P04A / 源几何已实改：门底/框/头、围护和排水；不是仅文字更名')
 s.text(100,300,'D—D 露台门侧剖 / 同单位1m＝180px',30)
 ox,oy,k=140,1330,180
 s.rect(ox,oy,1200,45,'#D4CEC0');s.rect(ox,oy-5.4,1200,5.4,'#CAC8BB')
 s.line(ox+200,oy-5.4,ox+200,oy-5.4-2.6*k,'#99A59D',10)
 s.line(ox+1100,oy-5.4,ox+1100,oy-5.4-1.2*k,'#768A89',10)
 s.text(ox+180,oy-2.6*k-65,'门底8.03 / 顶10.63 / 净2.60',28)
 s.text(ox+760,oy-1.2*k-55,'围护底8.03 / 顶9.23 / 有效1.20',26)
 char(s,ox+470,oy-5.4,k)
 s.note(1510,390,['楼板上表面8.00 / 工程16.00',
  '面层30mm→完成面8.03 / 工程16.03',
  '门槛高差0，门底同步8.03',
  '护栏从完成面计1.20，不是从FL8计',
  '线性槽候选x73.55–73.80/y.15–4.70',
  '沿南汇入内嵌竖管候选',
  '竖管落点73.68/0/0.15 / 工程Z8.15',
  '30mm面层未冻结6m全程假找坡',
  '局部坡/防水/溢流/地面管网未验',
  '不伪称排水或工程许可通过'],29,58)
 s.note(110,1580,['ROOF / EXTERIOR / SLAB_F01–03 / INTERIOR_F01–03 / STAIR_CORE共同原点继承；庭/梯洞本次不动。',
  '源新增鞋柜北界左右墙/门头并留3m开口；原外门不迁。庭孔与对应顶面、原梯连接保持。',
  '玻璃最高13.65，含框最高13.68；露台门底/围护/候选排水在JSON/Blend/图稿统一。',
  '真实游戏/碰撞/楼梯/镜头/导航/恢复及防护/排水/结构未验，RT01不开放。'],29,70)
 s.save('P04A')
 s=Sheet('C01 REV01 · 当前两向实际预览','P05 / 新几何/新材色同源重制；A225° / B45°，均30°，自然日光不变')
 s.image(PREFIX+'_A.png',80,220,3040,890);s.image(PREFIX+'_B.png',80,1180,3040,890)
 s.note(100,2140,['当前A/B已重制，显示新入口/淡层边；未用原版A/B冒充新版材色。',
  '最高13.68，三入口/体量/庭露台未改；室内调整以同版P02/局部预览为准。'],27,48)
 s.save('P05')
 s=Sheet('C01 REV01 · 教室/鞋柜修订真实预览','P05A / 新CLASS/SHOES沿用原实际相机；COURT/LINK未受影响，不重做')
 s.image(PREFIX+'_CLASS.png',80,250,1470,950);s.image(PREFIX+'_SHOES.png',1640,250,1470,950)
 s.image(PREFIX+'_CLASS_PULLED.png',80,1270,1470,880);s.image(PREFIX+'_ENTRY_CURRENT.png',1640,1270,1470,880)
 s.text(100,1220,'30席使用状态；三双列组与中央横道',27);s.text(1640,1220,'900名义格/新3m厅廊口/使用分区',27)
 s.text(100,2220,'椅后拉0.25状态；横道仍1.10，入座需姿态交互',26);s.text(1640,2220,'当前整套几何入口预览，与材色控制对照分开标',26)
 s.save('P05A')
 s=Sheet('C01 REV01 · 暖木入口材色修改前后','P05B / 原ENTRY原字节before；原形体、相机、日光、曝光/AgX保持，色值＋共面表面归属修正')
 picture(s,BASE/'Preview_ENTRY.png',80,230,1470,990);s.image(PREFIX+'_ENTRY_AFTER.png',1650,230,1470,990)
 s.text(100,1270,'BEFORE 原版ENTRY / 原字节未改',29);s.text(1650,1270,'AFTER 原形体 / 色值＋共面表面归属修正',29)
 s.note(100,1450,['原木#AC875A → 入口木#CFA878；原框#53686B → 入口框#99A59D；原层边#989E98 → #BAC1B8。',
  '原门廊/空白名带几何完全相同；灯SUN2.5、角5°、世界强度0.6、曝光0及AgX继承，未换镜头增曝光。',
  '当前修订整套入口另见ENTRY_CURRENT；控制after单独保原几何，避免内部布置改变混入材色对照。',
  '共面覆盖层表面归属修正如BLENDER_REPORT说明；无换灯光/发光或取消投影，不把平色当最终UV。',
  '本轮无新像素贴图、无AI、无最终纹理。旧32/64小样仅旧密度示意，正式试作再用UV核。'],29,68)
 s.save('P05B')
boards()
changes={'date':'2026-10-15','parent':OLD,'revision':PREFIX,'changes':[
 {'item':'30desks','before':'5columns×6rows regular pitch1.0, side.775, lane1.05','after':'5rows×3paired-columns, nominated pulled route min1.10','reason':'continuous specified route and business clear zone'},
 {'item':'business/restoration','before':'45/19.5 near desk corner .285m','after':G['player_interface'],'reason':'business retained, furniture actually moved, recovery candidate explicit'},
 {'item':'innerdoor','before':1.4,'after':3.0,'xy':[25,8.8],'reason':'retain outer25/0 and central3m; remove internal bottleneck'},
 {'item':'mainbanks','before':.7,'after':.6,'nominal':900,'reason':'one active face .70 plus walking1.30; fit/hardware pending'},
 {'item':'terrace','before':{'door_bottom':8,'guard_bottom':8,'guard_top':9.2},'after':G['terrace_interface'],'reason':'finish8.03 effective guard1.20 and threshold zero'},
 {'item':'height','before':'glass13.65 incorrectly called maximum','after':{'glass':13.65,'including_frame':13.68},'reason':'actual source maximum'},
 {'item':'materials','before':{k:original['materials'][k] for k in ['WOOD','FRAME','PLINTH']},'after':{k:G['materials'][k] for k in ['ENTRY_WOOD','ENTRY_FRAME','BAND_REV']},'reason':'same geometry/light comparison'}],
 'view_sync':G['view_sync']}
(OUT/'changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
print('REV geometry',len(G['primitives']),'seats30','cells900','10boards')
