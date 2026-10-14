"""Parametric architectural reference only: one dimensional source -> five SVG boards.
No .blend/.fbx/UV/UE or source-map edits. Original character is embedded byte-exact.
Run Python with Pillow; render SVG with sharp (see rasterize_reference.cjs).
"""
from pathlib import Path
import json,math,hashlib,base64,html
R=Path(__file__).resolve().parent;L=R.parents[3];C=L/'.cache/b01-home-reference'
B=json.loads((C/'basis.json').read_text(encoding='utf-8')) if (C/'basis.json').exists() else json.loads((R/'SL_BLD_B01_HOME_01_REFERENCE_01_GEOMETRY.json').read_text(encoding='utf-8'))['source_basis']
CHAR=Path('D:/UE project/SchoolLife/ArtSource/Characters/StudentChibi/FrontIdle/StudentChibi_Front_Idle.png').read_bytes()
assert hashlib.sha256(CHAR).hexdigest()=='082ceb410d904f0037dfe09dd3502e50195351691ab4047cc5dbbb639147b8cd'
ROOF={'pitch_deg':22,'overhang':.55,'eave_top':6.0,'skin_vertical_depth':.18,'ridge_direction':'+X / -X'}
ROOF['ridge_top']=6+5.55*math.tan(math.radians(22));ROOF['wall_join']=6+.55*math.tan(math.radians(22))-.18
def room(i,name,rect,phase='一期必要可进入候选'):
 x0,y0,x1,y1=rect;return {'id':i,'name':name,'rect':rect,'net_area_m2':round((x1-x0)*(y1-y0),6),'phase':phase}
f1=[room('01','起居 / 餐厨',[-8.8,-4.8,-.2,-.9]),room('02','Home / 交通厅',[-5.39,-.8,-2,2.5]),room('03','齐平玄关',[-1.9,-.8,-.2,2.5]),
 room('04','浴室',[-8.8,2.6,-6.6,4.8]),room('05','洗衣 / 洗面',[-6.5,2.6,-4.4,4.8]),room('06','WC',[-4.3,2.6,-3.3,4.8]),room('07','家务 / 书写',[-3.2,2.6,-.2,4.8],'完整空间；首期简装/开放待审'),room('08','后勤过道',[-8.8,-.8,-5.49,.1])]
f2=[room('11','玩家卧室',[-4.1,-4.8,-.2,-1]),room('12','家庭卧室A',[-8.8,-4.8,-4.2,-1],'空间完整；首期保留/不新增住户NPC'),room('13','家庭卧室B',[-4.1,1,-.2,4.8],'空间完整；首期保留/不新增住户NPC'),
 room('14','二层交通厅',[-4.1,-.9,-.2,.9]),room('15','楼梯上口厅',[-5.39,-.9,-4.2,2.5]),room('16','后侧过道',[-8.8,-.9,-5.49,.1]),room('17','家用储物 / 晾衣',[-8.8,2.6,-4.2,4.8],'首期关闭/少道具；从家庭卧室B维护进入')]
STAIR={'opening_rect':[-8.8,.2,-5.49,2.5],'width_total':2.3,'flight_clear_width':1.1,'centre_gap':.1,'landing_depth':1.15,'flight_going_count':8,'going':.27,'risers':18,'riser':3/18,'rise':3,'landing_z':1.5,'opening_area_m2':2.3*3.31,'under_landing':'低净空储藏封闭；不作为穿行通道','upper_landing_clear_height':2.7,'headroom_status':'whole-bay floor opening avoids upper slab above flights; finite capsule/motion not engine-tested'}
openings=[]
def opening(i,face,u,w,sill,h,kind='window',roomid=None):openings.append({'id':i,'face':face,'u':u,'width':w,'sill':sill,'height':h,'kind':kind,'room':roomid,'phase':'design candidate, not manufactured or UE validated'})
opening('D01','F',0,1.6,0,2.3,'main_portal');openings[-1]['active_clear']=[1.2,2.1];openings[-1]['explanation']='1.6m candidate frame opening with side panels; active household passage1.2m versus original prototype2.4m, needs planning/nav review; avoids doorway spilling across玄关/LDK partition'
opening('D02','B',-.35,.85,0,2.1,'maintenance_door','08')
for args in [('WF01','F',3.7,1.3,.9,1.2,'07'),('WF02','F',-2.8,2,.65,1.45,'01'),('WF03','F',-2.85,1.8,3.8,1.3,'11'),('WF04','F',2.85,1.8,3.8,1.3,'13'),('WF05','F',0,.9,4.1,1,'14'),
 ('WB01','B',-3,1.6,1.1,.8,'01'),('WB02','B',3.7,.8,1.6,.5,'04'),('WB03','B',-2.7,1.8,3.75,1.35,'12'),('WB04','B',3.7,1.2,4.2,.8,'17'),('WB05','B',1.35,1,1.8,2.2,'STAIR'),
 ('WR01','R',-5.5,1.2,1.1,.8,'05'),('WR02','R',-3.8,.45,1.6,.5,'06'),('WR03','R',-1.7,1.2,.9,1.2,'07'),('WR04','R',-7,1.5,4.2,.8,'17'),('WR05','R',-2.5,1.8,3.8,1.3,'13'),
 ('WL01','L',-7,1.6,1.1,.9,'01'),('WL02','L',-4.5,1.8,.75,1.35,'01'),('WL03','L',-1.7,1.8,.55,1.55,'01'),('WL04','L',-6.5,1.8,3.8,1.3,'12'),('WL05','L',-2.3,1.8,3.8,1.3,'11')]:opening(*args[:6],roomid=args[6])
doors=[{'id':'I01','floor':1,'axis':'Y','fixed':-.85,'centre':-4.8,'width':1.0,'connect':['01','02']},
 {'id':'I02','floor':1,'axis':'X','fixed':-1.95,'centre':0,'width':1.2,'connect':['02','03'],'type':'doorless'},
 {'id':'I03','floor':1,'axis':'Y','fixed':2.55,'centre':-4.95,'width':.8,'connect':['02','05']},
 {'id':'I04','floor':1,'axis':'X','fixed':-6.55,'centre':3.7,'width':.8,'connect':['05','04']},
 {'id':'I05','floor':1,'axis':'Y','fixed':2.55,'centre':-3.8,'width':.8,'connect':['02','06']},
 {'id':'I06','floor':1,'axis':'Y','fixed':2.55,'centre':-2.6,'width':.8,'connect':['02','07']},
 {'id':'I07','floor':1,'axis':'X','fixed':-5.44,'centre':-.35,'width':.85,'connect':['02','08']},
 {'id':'S01','floor':1,'axis':'X','fixed':-5.44,'centre':.75,'width':1.1,'connect':['02','STAIR'],'type':'doorless'},
 {'id':'S02','floor':2,'axis':'X','fixed':-5.44,'centre':1.95,'width':1.1,'connect':['STAIR','15'],'type':'doorless'},
 {'id':'I11','floor':2,'axis':'Y','fixed':-.95,'centre':-2.6,'width':.85,'connect':['14','11']},
 {'id':'I12','floor':2,'axis':'Y','fixed':-.95,'centre':-6.8,'width':.85,'connect':['16','12']},
 {'id':'I13','floor':2,'axis':'Y','fixed':.95,'centre':-2.6,'width':.85,'connect':['14','13']},
 {'id':'I14','floor':2,'axis':'X','fixed':-4.15,'centre':3.6,'width':.8,'connect':['13','17']},
 {'id':'I15','floor':2,'axis':'X','fixed':-4.15,'centre':0,'width':1.2,'connect':['14','15'],'type':'doorless'},
 {'id':'I16','floor':2,'axis':'X','fixed':-5.44,'centre':-.4,'width':.9,'connect':['15','16'],'type':'doorless'}]
areas={'formal_size_footprint_m2':324,'formal_full_two_floor_gross_m2':648,'formal_finish_inside_before_partitions_void_m2':2*17.6**2,'candidate_shell_footprint_m2':90,'candidate_gross_two_floor_m2':180,
 'candidate_physical_floor_projection_m2':180-STAIR['opening_area_m2'],'inside_exterior_walls_per_floor_m2':8.6*9.6,'F01_room_corridor_net_m2':sum(x['net_area_m2'] for x in f1),'F02_room_corridor_net_m2':sum(x['net_area_m2'] for x in f2),'stair_F01_horizontal_projection_m2':STAIR['opening_area_m2'],
 'roof_horizontal_projection_m2':10.1*11.1,'porch_floor_is_existing_ground':'no new ground slab/steps, awning .9x3.2',
 'definition':'scheme geometry accounting, not statutory construction/sale area; no porch/roof/court in interior net'}
areas['net_rooms_corridors_excluding_F01_stair_m2']=areas['F01_room_corridor_net_m2']+areas['F02_room_corridor_net_m2']
areas['net_including_F01_stair_projection_m2']=areas['net_rooms_corridors_excluding_F01_stair_m2']+STAIR['opening_area_m2']
theta=math.radians(20);cc=math.cos(theta);ss=math.sin(theta)
def local_from_world(p):
 d=[p[i]-B['entrance']['world_xy_m'][i] for i in [0,1]];return [cc*d[0]+ss*d[1],-ss*d[0]+cc*d[1]]
player_world=[B['Home']['world_xy_m'][0],B['Home']['world_xy_m'][1]-1.5]
D={'asset_id':'SL_BLD_B01_HOME_01','revision':'REFERENCE_01','status':'whole_house_reference_candidate_awaiting_planning_and_user; major footprint recommendation NOT approved','date':'2026-10-14','units':'m',
 'coordinate':{'shared_pivot':[0,0,0],'meaning':'D01 entrance threshold ground centre; shared ROOF/EXTERIOR/INTERIOR_F01/F02 root, not shell geometric centre','front':'+X','side_right':'+Y (standing outside front looking inward)','up':'+Z','world_yaw_deg':20,'world_pivot_m':B['entrance']['world_xy_m']+[0],'engineering_pivot_cm':B['entrance']['ue_xy_cm']+[0],'world_formula':'worldXY=entryWorldXY+R20*localXY; engineeringXY=(worldXY-originWorldXY)*100'},
 'formal_baseline':{'size':[18,18],'floors':2,'center':B['B01']['world_center'],'entry':B['B01']['world_entry'],'footprint_world_m':B['B01']['world_footprint'],'footprint_local_m':B['formal_footprint_local_m'],'status':'kept read-only building footprint, NOT renamed as courtyard'},
 'candidate':{'shell_bounds':{'min':[-9,-5,-.2],'max':[0,5,ROOF['wall_join']]},'body_size':[9,10],'floors':2,'floor_tops':[0,3],'floor_slab_z':[[-.2,0],[2.8,3]],'ceilings':[2.7,5.7],'wall_outer':.2,'wall_partition':.1,'roof':ROOF,'porch':{'plan':[-.1,-1.6,.9,1.6],'awning_top':2.5,'awning_soffit':2.35,'support':'short wall-header-supported canopy candidate; no freestanding grand columns','no_new_step':True},'actual_shell_bottom_center_local':[-4.5,0,0],'major_change':'requires formal building footprint change324->90m² and centre shift; entrance and two floors retained; no source map/UE edited'},
 'floors':{'F01':f1,'F02':f2},'stair':STAIR,'openings':openings,'interior_openings':doors,'areas':areas,
 'Home_interface':{'original':B['Home'],'prototype_room_local_m':B['gray_room_local_m'],'Home_local_m':B['home_local_m'],'PlayerStart_reference_local_m':local_from_world(player_world),'PlayerStart_reference_centre_z':.98,'PlayerStart_status':'derived from historical worldY-1.5m report, not live actor read','ground_z':0,'gray_floor_actor':next(x for x in B['home_actors'] if x['name']=='LC2_Home_Floor'),'door_active_clear_candidate':[1.2,2.1],'original_door_width':2.4,'owned_approach_width':2.8,'geometry_replacement':'old floor/1.1m walls/furniture are prototype actors; must eventually be replaced by development chat, not kept overlapping. No operation this round'},
 'group_separation':{'ROOF':'roof faces+undersides/ridge/eaves/gutters/porch canopy; independent closed/finished underside','EXTERIOR':'one owner for exterior walls BOTH surfaces, gables and all door/window openings/frames/porch attachment/mailbox/necessary court interfaces/downpipes; no duplicate interior exterior-wall skin','INTERIOR_F01':'slab [-.2,0], partitions/ceilings, one stair structure0->3m, initial necessary living/wet rooms furniture','INTERIOR_F02':'slab[2.8,3] with SAME stair void, partitions/ceiling/upper landing guard/player sleeping; reserved family spaces closed/unfinished props','common_reassembly':'all retain entrance-ground root and yaw20; never recenter each floor; no UE runtime hide/switch code'},
 'materials':{'wall':'matte warm off-white #D8D3C5; understated larger plaster variation','roof':'muted bluegray #899795, simple low gable22°, restrained course lines','porch':'small warm wood #8B7564','frames':'muted gray-green #A6ACA6','glass':'muted #738D93, design indication only; optical material not created','density':'64px/m as first environment comparison reference only; final indoor/roof density/atlas/slots decided during whole trial, never globally128'},
 'preview':{'type':'dimension-based editable vector massing / common light direction indication, NOT model render or UE','views':[{'id':'A','local_azimuth_deg':45,'world_azimuth_deg':65,'elevation_deg':30},{'id':'B','local_azimuth_deg':225,'world_azimuth_deg':245,'elevation_deg':30}],'sun_world_incoming':[.5,.6,-1],'same_dimensions_openings_roof_materials':True},
 'protected_inputs':B['protected_inputs'],'source_basis':B,'production_counts':{'reference_building_schemes':1,'formal_models':0,'UV_sets':0,'final_textures':0,'UE_imports':0,'next_buildings':0},
 'review_required':['formal footprint324->90m²/bodycentre shift without moving entry; 18x18 NOT court','1.2m active door vs2.4m prototype / navigation and finite capsule','candidate8.242m total height/3m floor/22°roof/9x10 dimensions','preservedHome and historicalPlayerStart with replacement gray actors','boundary/eave/porch beyond former front footprint into owned approach; legal parcel/neighbor rights not known','stair whole opening/real structure/finite capsule/camera','room opening phases; no new family NPC or gameplay','old watercourse actual position, drain outlet/foundation utility interfaces']}
D['candidate']['mailbox']={'id':'MB01','bounds_m':{'min':[0,1.45,.95],'max':[.18,1.75,1.2]},'status':'small blank front-mounted household box, part of EXTERIOR, no name/independent task'}
D['candidate']['yard_interface']={'status':'short dashed interface beyond original gray gate posts only; legal boundary not frozen; does not turn18x18 into courtyard','candidate_wall_height_m':.9}
(R/'SL_BLD_B01_HOME_01_REFERENCE_01_GEOMETRY.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')

# Minimal SVG drafting helpers, all coordinates derive from D, room/opening tables.
class Sheet:
 def __init__(self,index,title,subtitle):
  self.index=index;self.p=[f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="3200" height="2400" viewBox="0 0 3200 2400"><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0 0 L7 3 L0 6" fill="#a9794b"/></marker></defs><g font-family="Microsoft YaHei,sans-serif">']
  self.rect(0,0,3200,2400,'#edf1ec',stroke='none');self.text(55,70,title,43);self.text(55,120,subtitle,26)
 def raw(self,v):self.p.append(v)
 def rect(self,x,y,w,h,fill='#ffffff',stroke='#bac6c0',sw=2,dash=False):self.raw(f'<rect x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"'+(' stroke-dasharray="10 7"' if dash else '')+'/>')
 def line(self,a,b,color='#687d78',sw=2,dash=False,arrow=False):self.raw(f'<path d="M{a[0]:.3f} {a[1]:.3f} L{b[0]:.3f} {b[1]:.3f}" fill="none" stroke="{color}" stroke-width="{sw}"'+(' stroke-dasharray="9 6"' if dash else '')+(' marker-end="url(#arrow)"' if arrow else '')+'/>')
 def polygon(self,p,fill='#d8d3c5',stroke='#65776e',sw=2):self.raw('<polygon points="'+' '.join(f'{x:.3f},{y:.3f}' for x,y in p)+f'" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
 def text(self,x,y,t,size=25,color='#2c4142',anchor=None):self.raw(f'<text x="{x:.3f}" y="{y:.3f}" font-size="{size}" fill="{color}"'+(f' text-anchor="{anchor}"' if anchor else '')+'>'+html.escape(str(t))+'</text>')
 def lines(self,x,y,ts,size=25,dy=42):
  for k,t in enumerate(ts):self.text(x,y+k*dy,t,size)
 def dim(self,a,b,label,at=None):
  self.line(a,b,'#a9794b',2);self.line((a[0]-6,a[1]-6),(a[0]+6,a[1]+6),'#a9794b',2);self.line((b[0]-6,b[1]-6),(b[0]+6,b[1]+6),'#a9794b',2)
  self.text(*(at or ((a[0]+b[0])/2,(a[1]+b[1])/2-12)),label,23,anchor='middle')
 def circle(self,p,r=6,fill='#a9794b'):self.raw(f'<circle cx="{p[0]}" cy="{p[1]}" r="{r}" fill="{fill}"/>')
 def character(self,x,ground,scale):
  full=1.8*128/116*scale;self.raw(f'<image x="{x}" y="{ground-full*120/128}" width="{full}" height="{full}" xlink:href="data:image/png;base64,{base64.b64encode(CHAR).decode()}"/>')
  self.dim((x-15,ground),(x-15,ground-1.8*scale),'180可见',at=(x-82,ground-.9*scale));self.dim((x+full+20,ground),(x+full+20,ground-1.92*scale),'192胶囊',at=(x+full+95,ground-.96*scale))
 def save(self):
  self.text(55,2350,'受审住宅候选｜同一尺寸JSON派生；正式18×18足迹/工程/校门原文件不改。参考图 ≠ 正式模型/真实日光渲染/UE。',25)
  self.raw('</g></svg>');p=R/f'SL_BLD_B01_HOME_01_REFERENCE_01_{self.index}.svg';p.write_text('\n'.join(self.p)+'\n',encoding='utf-8',newline='\n')
def plan_transform(ox,oy,sc):return lambda p:(ox+p[0]*sc,oy-p[1]*sc)
def rect_plan(sheet,q,rect,fill,stroke='#6f8077',dash=False):
 x,y,X,Y=rect;a=q([x,Y]);sheet.rect(a[0],a[1],(X-x)*abs(q([1,0])[0]-q([0,0])[0]),(Y-y)*abs(q([0,1])[1]-q([0,0])[1]),fill,stroke,2,dash)
def footprint(sheet,q,points,fill,stroke,dash=False):
 pp=[q(p) for p in points];sheet.polygon(pp,fill,stroke,2)
 if dash:
  for a,b in zip(pp,pp[1:]+pp[:1]):sheet.line(a,b,stroke,3,True)

# 01: Formal baseline is distinct from smaller recommendation and private approach.
S=Sheet('P01','B01玩家家 · 整栋参考01 / 总平面与面积口径','推荐9×10米两层，正式18×18仍只读；两者不得混称院落或已批准尺寸。')
S.rect(45,160,1905,1630);S.rect(1990,160,1165,1630)
q=plan_transform(780,780,34)
footprint(S,q,B['formal_footprint_local_m'],'#f4ecdf','#b28d63',True)
rect_plan(S,q,[-9.55,-5.55,.55,5.55],'#d2dcdb','#7f9691')
rect_plan(S,q,[-9,-5,0,5],'#d8d3c5','#6e8178')
footprint(S,q,B['gray_room_local_m'],'none','#588eaa',True)
rect_plan(S,q,[-.1,-1.6,.9,1.6],'#bba18a','#8f7964')
for a,b in zip(B['R1'][0]['world_points'][1:3],B['R1'][0]['world_points'][2:4]):
 aa=q(local_from_world(a));bb=q(local_from_world(b));S.line(aa,bb,'#d5d6c7',2.8*34)
S.line(q([0,0]),q(local_from_world(B['R1'][0]['world_points'][3])),'#a9794b',4,False,True)
for a in [a for a in B['home_actors'] if 'YardGate' in a['name']]:
 pos=a['xform']['location'];world=[pos['x']/100+B['origin_world_xy_m'][0],pos['y']/100+B['origin_world_xy_m'][1]];z=local_from_world(world);p=q(z);S.rect(p[0]-6,p[1]-6,12,12,'#9daca5','#6e8178')
 sign=1 if z[1]>-.5 else -1
 S.line(q([z[0]+sign*.018,z[1]+sign*.2]),q([z[0]+sign*.282,z[1]+sign*3]),'#7b8d81',4,True)
S.text(*q([6.3,-5.2]),'院界短段候选 / 地界待核',22)
S.circle(q([0,0]),8);S.text(*q([.35,1.0]),'D01 原入口 / 图组轴心',23)
S.circle(q(B['home_local_m']),8,'#588eaa');S.text(*q([-5,.4]),'Home不移 / Z0',22)
S.text(*q([-17,7.5]),'正式建筑足迹18×18（保留）',26)
S.text(*q([-8.5,-6.7]),'推荐外墙9×10；蓝虚线=现8×8样板',24)
S.text(*q([4,2.7]),'现2.8m院门/接近路',24)
S.text(*q([16,1.0]),'E_B01私有接近线保持',23)
S.text(*q([-17,-7.5]),'旧18×18不是新的院界',24)
S.dim(q([-9,-7.6]),q([0,-7.6]),'9.00m');S.dim(q([-11.2,-5]),q([-11.2,5]),'10.00m',at=q([-13,0]))
S.line(q([-18,11.2]),q([-18-ss*2,11.2+cc*2]),'#657b73',4,False,True);S.text(*q([-19,13.5]),'世界北N',23)
S.lines(85,1400,['坐标：图组底轴心=D01门槛中心，+X朝巷，+Y屋侧，+Z上；安装yaw20°。','入口世界(2150.275455,1771.260000)m；工程(−4063.363636,−14692.181818,0)cm。','Home精确世界点及地面0保留；样板边yaw−70°不直接当楼体朝向。','院门标记是Recipe原30cm柱；院界只标接口，正式地界/旧水道/雨水出口仍待核。','门廊0.9m悬挑、屋檐0.55m越过旧前沿：仅进入自有接近段的候选，必须审阅。'],26,62)
S.lines(2035,225,['面积与普通家庭定位','18×18 → 单层324m²','满铺两层 → 毛648m²','扣0.2外墙后仍约619.52m²','（尚未扣楼梯/分隔）','不适合作普通住宅直接照满铺。'],31,70)
S.lines(2035,720,['推荐9×10 → 外墙占地90m²','两层毛投影180m²','二层楼梯洞7.613m²','实际楼板投影172.387m²',f'净面积含一层楼梯投影{areas["net_including_F01_stair_projection_m2"]:.3f}m²',f'房间/走道净面积{areas["net_rooms_corridors_excluding_F01_stair_m2"]:.3f}m²','屋檐/门廊/院空地不计室内面积。'],29,69)
S.lines(2035,1260,['重大取舍须规划批准：','正式足迹324→90m²，体量中心改变；','保入口、20°轴向、两层与Home点。','不是把18×18改名为院地。','此面积是方案几何口径，非法定面积。'],26,66)
S.rect(45,1830,3110,455);S.character(195,2240,130)
S.lines(635,1905,['认可人物原PNG：128×128原字节嵌入，180cm可见高 / 192cm胶囊。','生活尺度：主活动通口1.2×2.1m候选；外框洞1.6×2.3m。','原型通行2.4m → 活动净口1.2m，不能把保留门点等同导航已通过。','家具尺度参照：床1×2m、餐桌1.4×0.8m、厨房台深0.6m。','普通家庭：两层低切妻、短雨棚、克制窗/暖木点缀；不加豪华大门厅/柱廊。'],29,65)
S.save()

def window_plan(sheet,q,o,sc):
 u=o['u'];w=o['width'];face=o['face']
 if face in ['F','B']:x=0 if face=='F' else -9;a=[x,u-w/2];b=[x,u+w/2]
 else:y=5 if face=='R' else -5;a=[u-w/2,y];b=[u+w/2,y]
 sheet.line(q(a),q(b),'#718d93',7)
 mid=q([(a[k]+b[k])/2 for k in [0,1]])
 if face=='F':sheet.text(mid[0]+19,mid[1],o['id'],19)
 if face=='B':sheet.text(mid[0]-95,mid[1],o['id'],19)
 if face=='R':sheet.text(mid[0],mid[1]-20,o['id'],19,anchor='middle')
 if face=='L':sheet.text(mid[0],mid[1]+36,o['id'],19,anchor='middle')
def floor_plan(sheet,num,ox,oy):
 sc=110;q=plan_transform(ox,oy,sc);rect_plan(sheet,q,[-9,-5,0,5],'#b5bcb5')
 rooms=f1 if num==1 else f2
 for rm in rooms:
  fill='#e5e1d5' if rm['phase'].startswith('一期') else '#d9e0da';rect_plan(sheet,q,rm['rect'],fill,stroke='#7a8880')
  x,y,X,Y=rm['rect'];p=q([-5.2,-4.15] if rm['id']=='01' else [(x+X)/2,(y+Y)/2]);name=rm['name']
  if name=='Home / 交通厅':name='交通厅 / Home'
  sheet.text(p[0],p[1]-8,name,25,anchor='middle');sheet.text(p[0],p[1]+28,f'{rm["net_area_m2"]:.2f}m² · {rm["id"]}',22,anchor='middle')
 rect_plan(sheet,q,STAIR['opening_rect'],'#d0dcd8' if num==1 else '#b2c5c4',stroke='#618782')
 for k in range(9):
  x=-5.49-k*.27;sheet.line(q([x,.2]),q([x,1.3]),'#69817c',2);sheet.line(q([x,1.4]),q([x,2.5]),'#69817c',2)
 sheet.line(q([-5.3,.75]),q([-7.65,.75]),'#a9794b',3,False,True);sheet.line(q([-7.65,1.95]),q([-5.3,1.95]),'#a9794b',3,False,True)
 sheet.text(*q([-8.72,1.2]),'平台1.15',21);sheet.text(*q([-7.25,1.5]),'上↑',20)
 for d in [d for d in doors if d['floor']==num]:
  a=[d['fixed'],d['centre']-d['width']/2] if d['axis']=='X' else [d['centre']-d['width']/2,d['fixed']]
  b=[d['fixed'],d['centre']+d['width']/2] if d['axis']=='X' else [d['centre']+d['width']/2,d['fixed']]
  sheet.line(q(a),q(b),'#f6f5ed',12);sheet.line(q(a),q(b),'#9b8066',2,False,d.get('type')=='doorless')
  p=q([(a[i]+b[i])/2 for i in [0,1]]);sheet.text(p[0]+8,p[1]-8,d['id'],17)
 for o in openings:
  if (num==1 and (o['sill']<3 or o['id']=='WB05')) or (num==2 and (o['sill']>=3 or o['id']=='WB05')):window_plan(sheet,q,o,sc)
 if num==1:
  footprint(sheet,q,B['gray_room_local_m'],'none','#588eaa',True)
  sheet.circle(q(B['home_local_m']),7,'#397ea1');sheet.text(*q([-4.8,-.12]),'保留Home锚点',20,'#397ea1')
  sheet.circle(q(D['Home_interface']['PlayerStart_reference_local_m']),7,'#9e7158');sheet.text(*q([-5.6,-1.7]),'历史PlayerStart',20)
  sheet.line(q(B['home_local_m']),q([0,0]),'#397ea1',3,True,True)
  for rect,lab in [([-8.6,-4.4,-8,-2],'厨房'),([-5.6,-3.2,-4.2,-2.4],'餐桌'),([-2.8,-4.5,-.8,-3.65],'沙发')]:
   rect_plan(sheet,q,rect,'#c7bbab','#9d907e');p=q([(rect[0]+rect[2])/2,(rect[1]+rect[3])/2]);sheet.text(p[0],p[1],lab,20,anchor='middle')
 else:
  rect_plan(sheet,q,[-3.5,-4.4,-1.5,-3.4],'#c4ccbd','#8b9e8d');sheet.text(*q([-3.4,-3.75]),'床2×1m',21)
  rect_plan(sheet,q,[-.85,-3.5,-.25,-2.3],'#c7bbab','#9d907e');sheet.text(*q([-1.2,-2.6]),'书桌',19)
 sheet.dim(q([-9,-6.0]),q([0,-6.0]),'外墙进深9.00m');sheet.dim(q([-10.15,-5]),q([-10.15,5]),'正面宽10.00m',at=q([-10.35,0]))
 sheet.text(*q([-.6,6.0]),'+Y右侧',22);sheet.text(*q([.3,-4.5]),'+X前',22)
S=Sheet('P02','B01玩家家 · 同套首层 / 二层简化平面','米制；房间净界、洞口和楼梯共享坐标。先做必要生活/睡眠空间，家庭备用房不生成新住户或玩法。')
S.rect(45,165,1530,1630);S.rect(1610,165,1545,1630)
S.text(75,220,'F01 地面/入口Z0；净79.189m²（含楼梯投影）',28);S.text(1640,220,'F02 完成面Z3.00；净71.616m²（不含洞口）',28)
floor_plan(S,1,1260,880);floor_plan(S,2,2825,880)
S.lines(85,1600,['蓝虚线：原Home8×8；不可保旧低墙/家具后再叠新室内。','净房间/走道71.576m² ＋ 一层楼梯投影7.613m²。'],24,55)
S.lines(1640,1600,['整块楼梯洞2.3×3.31=7.613m²；上口与一层楼梯同位。','卧室A/B及储存有完整门窗边界；首期道具与开放待审。'],24,55)
S.rect(45,1840,3110,450)
S.lines(90,1905,['入口→交通厅→起居/餐厨保持原Home点与出门方向；原PlayerStart按历史worldY−1.5m落在起居区。','首期必要候选：玄关/交通厅、LDK、洗衣洗面/浴室/WC、折返楼梯、玩家卧室；不填满所有道具。','外墙0.20m / 内墙0.10m；相邻净房间之间的分隔只造一次，不给每个房间复制四面外墙。','楼梯18等高踏步，级高0.166667 / 级进0.27 / 两跑各9级、8踏面；净跑宽1.10、平台深1.15。','门编号I/S是组内洞口说明；不逐门开任务、不开发门动画。原灰盒只读，替换与导航由开发窗口另行处理。'],29,65)
S.save()

def elevation(sheet,face,cx,base,scale):
 front=face in ['F','B'];sgn=1 if face in ['F','L'] else -1
 centre=0 if front else -4.5
 def p(u,z):return (cx+sgn*(u-centre)*scale,base-z*scale)
 lo,hi=(-5,5) if front else (-9,0)
 sheet.polygon([p(lo,0),p(hi,0),p(hi,ROOF['wall_join']),p(lo,ROOF['wall_join'])],'#d8d3c5')
 if front:
  sheet.polygon([p(-5,ROOF['wall_join']),p(5,ROOF['wall_join']),p(0,ROOF['ridge_top']-.18)],'#d8d3c5')
  sheet.polygon([p(-5.55,6),p(0,ROOF['ridge_top']),p(5.55,6),p(5.55,5.82),p(0,ROOF['ridge_top']-.18),p(-5.55,5.82)],'#899795')
 else:sheet.polygon([p(-9.55,6),p(.55,6),p(.55,ROOF['ridge_top']),p(-9.55,ROOF['ridge_top'])],'#899795')
 sheet.line(p(lo,3),p(hi,3),'#b7b4a9',2,True)
 for o in [o for o in openings if o['face']==face]:
  u=o['u'];w=o['width'];z=o['sill'];h=o['height'];pts=[p(u-w/2,z),p(u+w/2,z),p(u+w/2,z+h),p(u-w/2,z+h)]
  sheet.polygon(pts,'#738d93' if o['kind']=='window' else '#8b7564','#a6aca6',5)
  sheet.line(p(u,z),p(u,z+h),'#bdc5bc',3)
  sheet.text(*p(u,z+h+.11),o['id'],19,anchor='middle')
  if o['kind']=='main_portal':sheet.dim(p(-.6,-.3),p(.6,-.3),'活动1.20m')
 if face=='F':
  sheet.polygon([p(-1.6,2.5),p(1.6,2.5),p(1.6,2.35),p(-1.6,2.35)],'#8b7564')
  sheet.text(*p(2.0,2.45),'短雨棚',19)
  sheet.polygon([p(1.45,.95),p(1.75,.95),p(1.75,1.2),p(1.45,1.2)],'#74877f','#586f67',2)
  sheet.text(*p(1.85,1.1),'MB01',18)
 if not front:
  for x in [-8.85,-.15]:sheet.line(p(x,5.95),p(x,.15),'#70867d',6)
  sheet.text(*p(-5.5,.35),'排水管 / 出口待核',19)
 sheet.line(p(lo-.8,0),p(hi+.8,0),'#8c9e90',3)
 sheet.dim(p(lo,-.62),p(hi,-.62),'10.00m' if front else '9.00m')
 x=cx+650
 for z,lab in [(0,'±0.00'),(3,'F02 +3.00'),(6,'檐 +6.00'),(ROOF['ridge_top'],f'脊 +{ROOF["ridge_top"]:.3f}')]:sheet.line((x-18,base-z*scale),(x+10,base-z*scale),'#a9794b',2);sheet.text(x+15,base-z*scale+8,lab,21)
S=Sheet('P03','B01玩家家 · 四立面 / 同一门窗编号','相对建筑：F前+X，B后−X，R右+Y，L左−Y；世界轴另按yaw20°，不把“东侧偏南”文字用于迁门。')
for face,cx,base in [('F',710,1060),('B',2270,1060),('R',710,2130),('L',2270,2130)]:
 S.rect(cx-670,165 if face in ['F','B'] else 1235,1520,980);S.text(cx-630,210 if face in ['F','B'] else 1280,{'F':'F 前立面 / 原门点','B':'B 后立面 / 维护小门D02，不复制正门','R':'R 右立面 / 洗面与家务窗','L':'L 左立面 / 餐厨与睡眠窗'}[face],28)
 elevation(S,face,cx,base,94)
S.save()

# 04: Exact roof plan plus level/entry and U-stair sections.
S=Sheet('P04','B01玩家家 · 屋顶平面 / 入口与楼梯剖面 / 组分离','檐0.55m、坡22°、墙厚/楼板/空洞均为受审候选；无结构/消防/实物施工合规认证。')
S.rect(45,165,1450,1055);S.rect(1530,165,1625,1055);S.rect(45,1260,1450,1030);S.rect(1530,1260,1625,1030)
S.text(85,215,'ROOF 屋顶平面；脊向X / 坡向±Y',28)
q=plan_transform(1180,640,72);rect_plan(S,q,[-9.55,-5.55,.55,5.55],'#a1adaa','#708680');rect_plan(S,q,[-9,-5,0,5],'none','#aaa99d',True)
S.line(q([-9.55,0]),q([.55,0]),'#516c6b',6)
for x in [-8,-4,0]:
 S.line(q([x,.45]),q([x,4.6]),'#7e928a',3,False,True);S.line(q([x,-.45]),q([x,-4.6]),'#7e928a',3,False,True)
for y in [-5.55,5.55]:
 S.line(q([-9.55,y]),q([.55,y]),'#516c6b',6)
 for x in [-8.85,-.15]:S.circle(q([x,y]),8,'#a9794b')
rect_plan(S,q,[-.1,-1.6,.9,1.6],'#b9a58f','#8d7d6d')
S.dim(q([-9.55,-6.0]),q([.55,-6.0]),'屋面投影长10.10');S.dim(q([-10.1,-5.55]),q([-10.1,5.55]),'11.10m',at=q([-11.1,0]))
S.lines(85,1100,['橙点：檐沟落水接口；管在EXTERIOR，沟在ROOF。','院界/地下接入未核；不将雨水出口擅接旧水道。'],23,44)
S.text(1570,215,'入口剖面 A-A（Y0，沿X）',28)
def entryp(x,z):return (2420+x*150,995-z*150)
S.line(entryp(-5,0),entryp(1.5,0),'#65786a',5);S.polygon([entryp(-5,-.2),entryp(0,-.2),entryp(0,0),entryp(-5,0)],'#b8c1b5')
S.polygon([entryp(-.2,2.3),entryp(0,2.3),entryp(0,3.2),entryp(-.2,3.2)],'#d8d3c5')
S.polygon([entryp(-5,2.8),entryp(-.2,2.8),entryp(-.2,3),entryp(-5,3)],'#b8c1b5')
S.text(*entryp(-2.5,3.12),'二层板；上段墙省略',22)
S.polygon([entryp(0,2.35),entryp(.9,2.35),entryp(.9,2.5),entryp(0,2.5)],'#8b7564');S.line(entryp(-5,2.7),entryp(-.2,2.7),'#a4ada0',4)
S.line(entryp(0,0),entryp(0,2.1),'#8b7564',8);S.circle(entryp(-4,0),8,'#397ea1');S.text(*entryp(-4.5,.25),'原Home点',22)
S.dim(entryp(.45,0),entryp(.45,2.1),'净高2.10',at=entryp(1.0,1.1));S.dim(entryp(-3.7,0),entryp(-3.7,2.7),'净高2.70',at=entryp(-4.5,1.5))
S.lines(1570,1100,['门槛/室内/现接近路均Z0：不新增台阶，不移动Home出生标高。','顶板/灰盒替换、门洞缩窄与雨棚支承是后续待验证接口。'],23,44)
S.text(85,1310,'楼梯剖面 B-B：两跑投影展开（Y不同）',28)
def sp(x,z):return (1050+(x+5.49)*140,2140-z*140)
for k in range(1,9):
 x=-5.49-(k-1)*.27;z=k/6;S.line(sp(x,z-1/6),sp(x,z),'#657e77',3);S.line(sp(x,z),sp(x-.27,z),'#657e77',3)
S.line(sp(-7.65,8/6),sp(-7.65,1.5),'#657e77',3);S.line(sp(-8.8,1.5),sp(-7.65,1.5),'#657e77',8)
for k in range(1,9):
 x=-7.65+(k-1)*.27;z=1.5+k/6;S.line(sp(x,z-1/6),sp(x,z),'#8c9e85',3);S.line(sp(x,z),sp(x+.27,z),'#8c9e85',3)
S.line(sp(-5.49,1.5+8/6),sp(-5.49,3),'#8c9e85',3)
S.line(sp(-5.49,3),sp(-4.9,3),'#657e77',8);S.line(sp(-8.8,0),sp(-4.9,0),'#657e77',5)
S.line(sp(-8.8,5.7),sp(-4.9,5.7),'#a3afa4',3);S.line(sp(-8.8,2.8),sp(-5.49,2.8),'#a9794b',3,True)
S.text(*sp(-8.8,2.45),'二层此段全开洞，虚线板取消',22)
S.dim(sp(-8.8,-.35),sp(-5.49,-.35),'洞长3.31m');S.dim(sp(-4.75,3),sp(-4.75,5.7),'上口净高2.70',at=sp(-4.4,4.2))
S.lines(85,2220,['18级×0.166667=3m / 每跑8踏面×0.27=2.16m / 平台深1.15。','洞宽2.30；净跑宽1.10；平台下低净空封闭，不诱导穿行。'],23,40)
S.text(1570,1310,'一栋整包 / 共用入口底轴心，分组可复装',28)
S.lines(1570,1390,['ROOF：两坡顶/底面、脊、檐、檐沟、短雨棚。','EXTERIOR：外墙双面/山墙/门窗洞口/框/排水管/院界接口。','INTERIOR_F02：二层板[2.8,3]＋同坐标梯洞＋内墙/顶面。','INTERIOR_F01：首层板[−0.2,0]＋内墙/顶面＋整段楼梯。','外墙只由EXTERIOR拥有；室内组不再造一套重叠外墙。','楼梯结构归F01，上口护栏归F02；拆屋顶后室内仍完整。','全部保留共同根(0,0,0)及安装yaw20，不各自重置轴心。'],27,72)
S.lines(1570,1995,['分离是资产接口设计，不开发屋顶隐藏/切图/门交互。','普通门窗、檐管在整栋内处理；参考通过后一次整栋试作。','当前无正式模型、UV、贴图、碰撞/LOD预算或UE接入。'],26,72)
S.save()

# 05: Procedural vector faces, common object table and common local/world sun.
# This is a design massing preview, deliberately labelled NOT a real model render.
def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def unit(v):d=math.sqrt(dot(v,v));return [x/d for x in v]
def face_point(face,u,z,offset=.004):
 return {'F':[offset,u,z],'B':[-9-offset,u,z],'R':[u,5+offset,z],'L':[u,-5-offset,z]}[face]
faces=[]
def face(points,color,normal,kind='base',identity=None):faces.append({'points':points,'color':color,'normal':normal,'kind':kind,'id':identity})
h=ROOF['wall_join'];ridge=ROOF['ridge_top']
face([[0,-5,0],[0,5,0],[0,5,h],[0,0,ridge-.18],[0,-5,h]],'#d8d3c5',[1,0,0])
face([[-9,5,0],[-9,-5,0],[-9,-5,h],[-9,0,ridge-.18],[-9,5,h]],'#d8d3c5',[-1,0,0])
face([[-9,5,0],[0,5,0],[0,5,h],[-9,5,h]],'#d8d3c5',[0,1,0]);face([[0,-5,0],[-9,-5,0],[-9,-5,h],[0,-5,h]],'#d8d3c5',[0,-1,0])
for sy in [-1,1]:
 face([[-9.55,sy*5.55,6],[.55,sy*5.55,6],[.55,0,ridge],[-9.55,0,ridge]],'#899795',[0,sy*math.sin(math.radians(22)),math.cos(math.radians(22))],'roof')
for x,n in [(0.55,[1,0,0]),(-9.55,[-1,0,0])]:
 for sy in [-1,1]:face([[x,sy*5.55,6],[x,0,ridge],[x,0,ridge-.18],[x,sy*5.55,5.82]],'#6f817b',n,'roof_edge')
for o in openings:
 u=o['u'];w=o['width'];z=o['sill'];H=o['height'];n={'F':[1,0,0],'B':[-1,0,0],'R':[0,1,0],'L':[0,-1,0]}[o['face']]
 face([face_point(o['face'],u-w/2,z),face_point(o['face'],u+w/2,z),face_point(o['face'],u+w/2,z+H),face_point(o['face'],u-w/2,z+H)],'#738d93' if o['kind']=='window' else '#8b7564',n,'opening',o['id'])
face([[-.1,-1.6,2.5],[.9,-1.6,2.5],[.9,1.6,2.5],[-.1,1.6,2.5]],'#8b7564',[0,0,1],'canopy')
face([[.9,-1.6,2.35],[.9,1.6,2.35],[.9,1.6,2.5],[.9,-1.6,2.5]],'#806e60',[1,0,0])
face([[.18,1.45,.95],[.18,1.75,.95],[.18,1.75,1.2],[.18,1.45,1.2]],'#74877f',[1,0,0],'mailbox')
face([[0,1.45,1.2],[.18,1.45,1.2],[.18,1.75,1.2],[0,1.75,1.2]],'#74877f',[0,0,1],'mailbox')
def shade(color,n):
 rgb=[int(color[i:i+2],16) for i in [1,3,5]];sun=unit([-cc*.5-ss*.6,ss*.5-cc*.6,1]);k=.76+.24*max(0,dot(unit(n),sun));return '#'+''.join(f'{round(c*k):02x}' for c in rgb)
def preview(sheet,az,ox,oy,sc):
 a=math.radians(az);e=math.radians(30);right=[-math.sin(a),math.cos(a),0];up=[-math.sin(e)*math.cos(a),-math.sin(e)*math.sin(a),math.cos(e)];toward=[math.cos(e)*math.cos(a),math.cos(e)*math.sin(a),math.sin(e)];centre=[-4.5,0,3.4]
 def p(v):q=[v[i]-centre[i] for i in range(3)];return [ox+dot(q,right)*sc,oy-dot(q,up)*sc]
 # Direction-consistent ground shadow of building/roof silhouette, convex-hull projection.
 pts=[];sunlocal=[cc*.5+ss*.6,-ss*.5+cc*.6,-1]
 for f in faces:
  if f['kind']=='opening':continue
  for v in f['points']:pts.append([v[0]+v[2]*sunlocal[0],v[1]+v[2]*sunlocal[1]])
 def hull(points):
  pp=sorted(set(tuple(x) for x in points))
  def cr(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
  low=[];high=[]
  for q in pp:
   while len(low)>1 and cr(low[-2],low[-1],q)<=0:low.pop()
   low.append(q)
  for q in reversed(pp):
   while len(high)>1 and cr(high[-2],high[-1],q)<=0:high.pop()
   high.append(q)
  return low[:-1]+high[:-1]
 sheet.polygon([p([x,y,0]) for x,y in hull(pts)],'#d3d9d1','none',0)
 vis=[f for f in faces if dot(f['normal'],toward)>1e-6 and not (f['kind'] in ['canopy','mailbox'] and toward[0]<0)]
 # Window patches must be painted after their opaque parent wall; polygon-centroid
 # depth alone incorrectly hides low windows/doors beneath large wall polygons.
 def order(f):
  is_roof=f['kind'] in ['roof','roof_edge']
  return (2 if is_roof else 3 if f['kind'] in ['canopy','mailbox'] or max(v[0] for v in f['points'])>.6 else 1 if f['kind']=='opening' else 0,
          sum(dot(v,toward) for v in f['points'])/len(f['points']))
 vis.sort(key=order)
 for f in vis:
  color=shade(f['color'],f['normal']);sheet.polygon([p(v) for v in f['points']],color,color,1)
  if f['kind']=='opening':
   pts=f['points'];sheet.line(p(pts[0]),p(pts[1]),'#a6aca6',4);sheet.line(p(pts[1]),p(pts[2]),'#a6aca6',4);sheet.line(p(pts[2]),p(pts[3]),'#a6aca6',4);sheet.line(p(pts[3]),p(pts[0]),'#a6aca6',4)
   lo=[(pts[0][i]+pts[1][i])/2 for i in range(3)];hi=[(pts[2][i]+pts[3][i])/2 for i in range(3)];sheet.line(p(lo),p(hi),'#b9c3ba',3)
  if f['kind']=='roof':
   pts=f['points']
   for k in range(1,12):
    t=k/12;a=[pts[0][i]+t*(pts[3][i]-pts[0][i]) for i in range(3)];b=[pts[1][i]+t*(pts[2][i]-pts[1][i]) for i in range(3)];sheet.line(p(a),p(b),shade('#8c9a98',f['normal']),2)
 for side in [-1,1]:
  if dot([0,side,0],toward)>0:
   for x in [-8.85,-.15]:sheet.line(p([x,side*5.1,.15]),p([x,side*5.1,5.95]),'#6f847c',5)
 return {'azimuth':az,'elevation':30,'source_face_count':len(faces),'visible_face_ids':[f['id'] for f in vis if f['id']],'same_source':True}
S=Sheet('P05','B01玩家家 · 相反两向 / 整栋体量与材色示意','同一尺寸/门窗/屋顶；向量投影与光向示意，不是正式模型渲染。后面只有维护门D02，不镜像主门。')
S.rect(45,165,1530,1780,'#e6ebe2');S.rect(1610,165,1545,1780,'#e6ebe2')
S.text(90,230,'A 前+右 / 本地45°，世界65° / 俯角30°',29);S.text(1655,230,'B 后+左 / 本地225°，世界245° / 俯角30°',29)
pv=[preview(S,45,820,1150,87),preview(S,225,2400,1150,87)]
S.lines(85,1790,['低切妻 / 青灰屋面 / 米白抹面 / 短暖木雨棚','人物仅作下方独立比例栏，不冒充场景遮挡/受光。'],26,60)
S.lines(1650,1790,['维护小门、厨房/浴室/楼梯窗来自同一编号表','坡向/高程及投影保持，没有独立生图拼造型。'],26,60)
S.rect(45,1980,3110,310)
S.character(170,2240,100)
S.lines(635,2040,[f'墙顶{ROOF["wall_join"]:.3f} / 檐6.000 / 脊{ROOF["ridge_top"]:.3f}m；脊沿X，坡面流向±Y。','像素风：低对比成簇表面；本轮无纹理/UV，不把阴影固定烘入基础色。','原人物180可见 / 192胶囊，仅独立尺度。AI外观参考漂移不反写尺寸JSON。'],29,72)
S.save()
D['preview']['derived_views']=pv;D['preview']['common_parametric_face_count']=len(faces)
(R/'SL_BLD_B01_HOME_01_REFERENCE_01_GEOMETRY.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'boards':5,'native_each':[3200,2400],'areas':areas,'roof':ROOF,'protected':len(B['protected_inputs']),'formal_models':0},ensure_ascii=True))
