"""Three editable check boards, directly projected from revision data."""
import ast,json,html,math,csv
from pathlib import Path
O=Path(__file__).parent;B=O.parent/'Revision01';D=O/'Boards';D.mkdir(exist_ok=True);P='SL_BLD_C01_MAIN_01_TRIAL_01_REV_02'
L=json.loads((O/'LAYOUT.json').read_text(encoding='utf-8'));A=json.loads((O/'ACTIVITY_DISTANCE.json').read_text(encoding='utf-8'));OLD=json.loads((B/'LAYOUT.json').read_text(encoding='utf-8'))
tree=ast.parse((B/'make_boards.py').read_text(encoding='utf-8'));exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.ClassDef)],type_ignores=[]),'inherited SVG helpers','exec'),globals())
def save(b,n):
 b.text(80,2345,'REV_02 · 同一 LAYOUT / ACTIVITY_DISTANCE 数据 · 米制几何、UE候选厘米分别标注 · 非游戏验收',27)
 (D/(P+'_'+n+'.svg')).write_text('\n'.join(b.a+['</g></svg>'])+'\n',encoding='utf-8',newline='\n')
b=Board('C01 试作局部修订02｜实际2.4m内门＋双人换鞋坐面','保900格/原房界/外门 · 原三外门与主厅3m口不变 · 两个同时坐面使用者与柜前操作、公共路、等候并存')
p=Plan(b,150,1635,133,(52.3,13));p.rect([52.3,13,63.7,21.7],'#e4e9e6','#233c42',5)
for op in L['operators']:
 if op['room']=='F1_LW':p.rect(op['rect'],'#d5e2d4','#90ae94',1)
for c in L['shoe_banks']:
 if c['room']!='F1_LW':continue
 x,y,z,X,Y,Z=c['bounds'];p.rect([x,y,X,Y],'#6a858d','#274853',2);p.text(x+.05,y+.1,c['id'].replace('REV_LINK_',''),20,'#ffffff')
for q in L['queues']:p.rect(q['bounds'],'#e2c894','#a47817',2)
for u in L['bench']['usage_bounds']:p.rect(u,'#cddbea','#397bb3',3,'8 6')
p.rect([52.8,13.15,55.2,13.6],'#c5af89','#715e43',3);p.text(52.8,12.5,'2.40×0.45m双人坐面',27)
for q in L['paths']:
 if q['id'] in ['DOOR_IN_SIMULTANEOUS','DOOR_OUT_SIMULTANEOUS']:p.path(q['points'],'#26835a' if 'IN_' in q['id'] else '#397bb3',5)
for q in L['paths']:
 if q['id'] in ['DOOR_TO_TAKE','BENCH_APPROACH','RISE_TO_PUBLIC']:p.path(q['points'],'#a47720',3,'8 6')
p.path([[56.8,13],[59.2,13]],'#26835a',10,arrow=False)
for x,X in L['door']['leaf_x']:p.rect([x,12.71,X,12.75],'#a3b7ba','#385b63',3)
p.text(56.8,12.2,'实际净2.40×2.60',28);p.text(52.3,22.2,'北↑ / 西连接 11.40×8.70m / FL0',31)
b.text(1820,270,'同中心接口及真实构件',37)
notes=['房间界面中心 (58,13,0)m；墙中线Y12.90。','洞口X56.80..59.20，墙厚Y12.80..13.00。','左右各扩0.50m；竖向开口多2.60㎡，地面新增0。','框实际在Y12.80..13.00，框外不侵净2.40×2.60。','停扇X55.53..56.73 / 59.27..60.47。','停扇Y12.71..12.75，距墙南面0.05m，避开通路。','双操作：0.70＋公共1.12＋0.70＝净面距2.52m。','取鞋：中列西面第2列第3层；其他操作位仍在。','坐面2席X53.40 / 54.60，朝北，座高0.43m。','全宽起身点Y14.05；换鞋使用北界Y14.45。','六等候仍在东侧；未移柜、未减900格。']
for i,t in enumerate(notes):b.text(1820,335+i*49,t,27)
# Door elevation, actual clear aperture and parked leaves from same source dimensions.
q=Plan(b,1880,1735,200,(55.2,0));q.rect([55.2,0,60.8,3.45],'#e4e9e6','#71898e',1)
q.rect([56.8,0,59.2,2.6],'#f4f3ee','#26835a',4)
for x,X in L['door']['leaf_x']:q.rect([x,0,X,2.6],'none','#385b63',3)
q.text(56.8,2.85,'2.40m 净宽',29);q.text(56.9,1.25,'2.60m 净高',27)
q.text(55.2,-.3,'南看北 / 停扇在廊侧，不嵌入墙体',27)
for i,t in enumerate(['闭环：取鞋→携鞋→坐面/弯腰→起身→侧袋等候→离开。','蓝虚框=坐面使用/腿脚；绿色=柜前操作；赭色=有限换鞋路线。','新凳投影1.080㎡；双人使用2.703㎡、起身1.414㎡（含自身重叠）。','柜体仍主7.488＋补7.560＝15.048㎡，没有拿坐面面积充柜体账。','人物可见1.80m/宽1.039655m与0.68×1.92m胶囊分开保留。']):b.text(110,1840+i*61,t,30)
for i,t in enumerate(['源网格/净宽高与停扇另作原生射线核对；结构工法未验。','有限命名同时使用，不等于任意柜位并发或900人高峰。','六层开放格/真实坐姿/抓握/换鞋动作仍是尺寸假设。']):b.text(110,2185+i*45,t,28)
save(b,'P01_DOOR_SHOE_LOOP')
b=Board('C01 试作局部修订02｜玩家席关系候选与预览/Enter三维距离','不移动原业务锚点 / 不增230cm / 不默认传送 · 操作P=E同处，入座不是当前活动启动条件')
p=Plan(b,140,1590,137,(41,12.7));p.rect(OLD['room'],'#e4e9e6','#233c42',5)
for d,c in zip(OLD['desks'],OLD['chairs']):
 x,y=d['x'],d['y'];p.rect([x-.225,y-.325,x+.225,y+.325],'#c5af89','#715e43',2);x,y=c['x'],c['y'];p.rect([x-.225,y-.225,x+.3 if c['player'] else x+.225,y+.225],'#839ca1','#385b63',2)
 p.text(d['x']-.2,d['y']+.44,d['id'].split('DESK_')[1],20)
p.path([[45,12.7],[45,18.8],[45,19.5]],'#26835a',8)
for x,y,t,c in [(45,19.5,'G / P=E','#26835a'),(46.175,19.87,'3_5关系候选','#a47817'),(48.275,19.87,'5_5旧研究','#397bb3')]:
 x0,y0=p.xy(x,y);b.circle(x0,y0,12,c);p.text(x-.45,y+.85,t,25,c)
p.text(41,22.15,'北↑ / 原门与30席、全部家具不动',29);p.text(44.1,12.3,'原门1.60×2.60m',25)
b.text(1510,270,'P / E Actor中心，A地点Actor锚点',36)
texts=['G脚下 local(45,19.50,4.00)m。','候选UE工程G=(4500,7050,1200)cm。','P=E：Actor按默认+0.96m或示例+0.98m分别算。','P/E local Z=4.96 / 4.98，不是脚底或贴图中心。','历史A=(4500,7050,800)cm：仅历史Recipe。','正式A候选=(4500,7050,1200)cm：规划约定。','现用运行地图A/Actor变换、scaled半高尚未实测。','不得用正式Z1200冒充“现用原锚点”。']
for i,t in enumerate(texts):b.text(1510,335+i*47,t,28)
b.text(1510,760,'统一UE候选世界cm；每行 P=E 均分别验算',29)
b.text(1510,815,'来源 / Actor偏移 ｜ d(cm) ｜ 230−d(cm) ｜ 条件',28)
rows=[q for q in A['cases'] if q['mode']=='PREVIEW_P']
for i,r in enumerate(rows):
 label=('历史Z800' if r['anchor_case'].startswith('HIST') else '规划Z1200')+f" / +{r['actor_offset_m']:.2f}m"
 b.text(1510,875+i*56,f"{label} ｜ {r['distance_cm']:.3f} ｜ {r['margin_cm']:+.3f} ｜ "+('条件内' if r['within230'] else '失败'),27,'#26835a' if r['within230'] else '#ae5450')
b.text(1510,1150,'d=√((Px−Ax)²+(Py−Ay)²+(Pz−Az)²)',31)
b.text(1510,1200,'平方比较≤52900；未舍入的实值见JSON/CSV。',28)
# Vertical source contrast at identical XY. The feet and actor centres must not be merged.
q=Plan(b,1620,1815,75,(0,0));q.path([[0,0],[8,0]],'#71898e',2,arrow=False)
q.path([[0,4],[8,4]],'#71898e',2,arrow=False)
q.text(.1,0.15,'历史 A / 工程Z8m',26,'#ae5450');q.text(.1,4.15,'正式FL / 工程Z12m',26)
q.path([[6,0],[6,4.96]],'#ae5450',5,arrow=False);q.text(6.1,2.2,'ΔZ4.96m',27,'#ae5450')
q.path([[4,4],[4,4.96]],'#26835a',5,arrow=False);q.text(2.0,5.2,'P=E工程Z12.96m',27);q.text(0,5.85,'同XY的Z差异 / 不同来源不能混用',28)
for i,t in enumerate(['门口→横通道→操作点：全宽站立与胶囊检查最小分离0.21m。','3_5椅(46.175,19.87,4.43)仅关系候选，完整入座未通过/未验。','5_5及原19阶段不改、不重跑；不是最终绑定席。','预览/Enter在G操作点进行，不附加19阶段全过程在圈要求。','历史锚点若仍Z800：最小竖差496cm，超过230cm达266cm。','唯一推荐：暂停最终席绑定，交开发/规划只读核定现用变换再判断。']):b.text(110,1870+i*61,t,30)
b.text(110,2260,'规划条件距离内 ≠ 当前工程兼容通过；资格/最近地点选择/地图变换/真实游戏仍未验证。',29)
save(b,'P02_ACTIVITY_DISTANCE')
b=Board('C01 试作局部修订02｜换鞋包络与针对性检查','保原19阶段方法，只检查本轮改变的门区/坐面/必要操作支路；不增入座系统或无关阶段')
b.text(110,270,'坐面、腿脚、弯腰与抓握假设（同尺寸）',37)
pose=next(q for q in L['bench_poses'] if q['t']==1)
for i,(t,lean) in enumerate([(0,False),(1,False),(1,True)]):
 p=Plan(b,150+i*1000,1070,370,(13.05,0));p.text(13.05,2.0,('起身/就座端点' if t==0 else '坐定' if not lean else '弯腰换鞋65°'),29)
 p.rect([13.15,.395,13.6,.43],'#c5af89','#715e43',2)
 for q in next(v for v in L['bench_poses'] if v['t']==t)['parts']:
  if lean and q['name']=='UPPER':continue
  x,y,z,X,Y,Z=q['bounds'];p.rect([y,z,Y,Z],'none','#397bb3',1)
 if lean:
  bb=L['shoe_change']['poses'][-1]['bounds'];p.rect([bb[1],bb[2],bb[4],bb[5]],'none','#88a1b4',1,'6 6')
  aa=math.radians(65);verts=[[13.635+y*math.cos(aa)+z*math.sin(aa),.52-y*math.sin(aa)+z*math.cos(aa)] for y,z in [(-.34,0),(0,0),(0,.87),(-.34,.87),(-.34,0)]];p.path(verts,'#397bb3',3,arrow=False)
  sh,el,ha=L['shoe_change']['shoulder'],L['shoe_change']['elbow'],L['shoe_change']['hand'];p.path([[sh[1],sh[2]],[el[1],el[2]],[ha[1],ha[2]]],'#a47817',4,arrow=False)
  p.rect([14.10,.015,14.39,.13],'#e2c894','#a47817',2)
 p.path([[13.05,0],[14.85,0]],'#233c42',2,arrow=False);p.text(13.05,-.18,'横轴Y / 竖轴Z，米制',26)
for i,t in enumerate(['座面不撤走：2.4×0.45m、顶0.43m、六支腿；另一坐面使用者保持在场。','就座/起身沿原1000区间解析包络，转90°到凳位，接触允许0、无体积内缩。','上身尺寸0.34深×1.039655宽×0.87高不变，绕前下缘弯腰65°，不是认可人物动作。',f"假设肩→手距离{L['shoe_change']['hand_distance']:.6f}m≤0.80m；双连杆0.40+0.40m，真实抓握/平衡未验。",'鞋290×235×115mm成对包络，实际开放腔0.288×0.334×0.276m；宽余53mm、深余44mm。','携鞋/转向/放下另核自由前方空间；脚与鞋接触不冒充与柜体或坐凳相交。']):b.text(110,1170+i*53,t,29)
b.text(110,1560,'仅本轮变化影响检查',35)
labels={'DOOR_TO_TAKE':'门→取鞋','TAKE_TO_TURN':'携鞋返回/转向','BENCH_APPROACH':'接近坐面','RISE_TO_PUBLIC':'起身→公共线','PUBLIC_TO_WAIT':'公共线→等候','WAIT_TO_EXIT':'等候→离开','DOOR_IN_SIMULTANEOUS':'门区同时进入','DOOR_OUT_SIMULTANEOUS':'门区同时离开'}
for i,q in enumerate(L['paths']):
 x=110+(i//4)*1500;y=1635+(i%4)*63;b.text(x,y,f"{labels[q['id']]}：{q['min_clearance']*1000:.2f}mm 最小分离",30,'#277652')
b.text(110,1930,'面积分账（㎡；使用带可含自身坐面投影，不能相加冒充总建筑面积）',33)
for i,t in enumerate(['柜体：主7.488＋西连接7.560＝15.048，和Revision01相同。','新增坐面：1.080；两人换鞋使用2.703；两人站立起身1.414；六等候4.242。','柜前全长双面操作带：主16.380 / 西连接15.120；柜间公共净宽1.12m。','原加深纠错18×0.06＝1.080㎡另保；与新凳1.080㎡恰巧同数，含义不同。']):b.text(110,1990+i*55,t,29)
b.text(110,2245,'实际局部已改 / 指定条件空间通过 / 历史锚点冲突未解 / 当前游戏未验，四类分开；整栋最终状态交回审。',28)
save(b,'P03_CHANGE_CHECKS')
with (O/'AREAS.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f,lineterminator='\n');w.writerow(['category','main_m2','link_m2','total_or_width','semantics'])
 w.writerows([['original_main_deepen_correction',1.08,0,1.08,'old18x.06,not revision delta'],['Revision01_cabinet',7.488,7.56,15.048,'gross cabinet footprint'],['Revision02_cabinet',7.488,7.56,15.048,'unchanged900 banks'],['Revision02_new_bench',0,1.08,1.08,'seat projection,unrelated to old1.08'],['two_person_change_use',0,L['areas']['bench_use_two_people'],L['areas']['bench_use_two_people'],'includes own bench overlap'],['two_person_stand_rise',0,L['areas']['stand_rise_two_people'],L['areas']['stand_rise_two_people'],'usage,not new floor area'],['six_waits',0,L['areas']['queue_six_people'],L['areas']['queue_six_people'],'finite waiting footprint'],['full_face_operating_bands',16.38,15.12,31.5,'full .7m face bands,not900 people'],['main_public_spine',23.436,0,23.436,'only main spine,not all public paths'],['between_face_public_width_m',None,None,1.12,'net width .7+1.12+.7=2.52']])
with (O/'CABINETS.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f,lineterminator='\n');w.writerow(['bank','room','columns','rows','faces','cells','bounds_m','cavity_m','status'])
 for q in L['shoe_banks']:w.writerow([q['id'],q['room'],q['columns'],q['rows'],q['faces'],q['nominal'],q['bounds'],q['cavity'],'unchanged from Revision01'])
print('REV02_THREE_SVG_BOARDS_READY',flush=True)
