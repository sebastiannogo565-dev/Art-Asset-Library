"""Evidence-driven docs/indices/manifest for this revision only; no old assets rewritten."""
from pathlib import Path
import json,hashlib,csv,re
from PIL import Image
O=Path(__file__).parent;B=O.parent/'Revision01';R=Path('D:/Art Asset Library');P='SL_BLD_C01_MAIN_01_TRIAL_01_REV_02'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def write(n,v):(O/n).write_text((v if isinstance(v,str) else json.dumps(v,ensure_ascii=False,indent=2)).rstrip()+'\n',encoding='utf-8',newline='\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
L=read(O/'LAYOUT.json');A=read(O/'ACTIVITY_DISTANCE.json');SC=read(O/'SOURCE_CHECK.json');FC=read(O/'FBX_CHECK.json');ST=read(O/'STATISTICS.json');old=read(B/'LAYOUT.json')
assert SC['blend_sha256']==sha(O/(P+'.blend')) and FC['source_blend_sha256']==SC['blend_sha256'] and FC['fbx_sha256']==sha(O/(P+'.fbx'))
assert all(q['passed'] for q in L['paths']) and L['bench_transition']['passed'] and L['shoe_change']['passed'] and L['carried_shoes']['passed']
protected=read(O/'protected_inputs.json');bad=[q['path'] for q in protected if sha(q['path'])!=q['sha256']];assert not bad,bad
G=read(O/'GEOMETRY.json')
G['player_layout']['binding_semantics']='No final player seat bound. Revision01 player flag identifies historical5_5 study only.'
for q in G['player_layout']['explicit_chairs']:
 if 'player' in q:q['study_5_5']=q.pop('player')
write('GEOMETRY.json',G)
with (O/'SEATS.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f,lineterminator='\n');w.writerow(['ID','geometry_changed','role_REV02','inherited_REV01_status','full_pose_scope','evidence'])
 for q in old['seats']:w.writerow([q['id'],False,'5_5_study_only_not_bound' if q['id']=='F2_W4_DESK_5_5' else '3_5_relationship_candidate_not_bound' if q['id']=='F2_W4_DESK_3_5' else 'ordinary_unchanged',q['state'],q['transition'],'../Revision01/LAYOUT.json, no new seating requirement'])
points=[('operation_G','candidate',[45,19.5,4]),('Actor_P_equals_E_096','assumed_default',[45,19.5,4.96]),('Actor_P_equals_E_098','landing_example_only',[45,19.5,4.98]),
 ('A_historical_recipe','historical_not_live',[45,19.5,0]),('A_formal_candidate','planning_not_live',[45,19.5,4]),('chair_3_5','tentative_relationship',[46.175,19.87,4.43]),
 ('approach_3_5','inherited_blocked_candidate',[46.35,19.87,4]),('chair_5_5','historical_study',[48.275,19.87,4.43]),('approach_5_5','historical_pulled_chair_only',[48.29,19.87,4]),('recovery','unchanged_candidate',[45,18.7,4])]
with (O/'COORDINATES.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f,lineterminator='\n');w.writerow(['ID','scope','local_m','engineering_m','UE_candidate_world_cm','geographic_world_xy_m_local_z','source'])
 for n,s,p in points:
  w.writerow([n,s,p,[p[0],p[1]+51,p[2]+8],[p[0]*100,(p[1]+51)*100,(p[2]+8)*100],[p[0]+2190.909090909091,p[1]+1969.181818181818,p[2]],'formal mapping is planning only; historicalA source ActorRecipe; live transform unknown'])
with (O/'OPENING_CHANGE.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f,lineterminator='\n');w.writerow(['ID','room_interface_center_m','wall_midline_y_m','net_width_m','net_height_m','frame_y_m','parked_leaf_y_m','parked_leaf_x_m','opening_face_delta_m2','ground_area_delta_m2'])
 w.writerow(['F1_LW_D',[58,13,0],12.9,2.4,2.6,[12.8,13],[12.71,12.75],L['door']['leaf_x'],2.6,0])
write('CHANGES.json',dict(base='../Revision01',base_git='ad9bb026f962dbcdce7f54ca1005c462767b6c1c',
 actual_asset_changes=['PARTITIONS_F01_DOOR_BAND local boolean opening width1.4→2.4','OPEN_F1_LW_D real frame/leaves enlarged and parked outside wall','REV02_CHANGE_BENCH added2.4x.45x.43m two users'],
 unchanged=dict(objects=2212,cabinet_banks=9,cells=900,classroom_desks=30,classroom_chairs=30,other23_classrooms=True,original_sources=len(protected)),
 data_change='No final seat binding;candidate3_5 relation and reachable operation45/19.5;Actor—Anchor3D source-separated table',
 materials='original14 architecture materials,48 original PNG textures,0 new textures',
 check_changes='four previews +3SVG/PNG; changed local route/bench/door evidence;19 stages and900 cavity checks inherited via fingerprints',
 unresolved=A['conflict'],RT01='not open,unchanged',SchoolLife='read-only;no UE integration or systems'))
boardnames=[('P01_DOOR_SHOE_LOOP','实际门区、坐面与双侧操作/等候'),('P02_ACTIVITY_DISTANCE','P/E/G/A口径、两来源Z与三维余量'),('P03_CHANGE_CHECKS','换鞋包络、局部路径及面积分账')]
viewnames=[('WESTLINK_CHANGE_LOOP','真实柜列/2.4门/双人坐面与有限同时使用包络'),('CHANGE_SEAT_CLOSE','从室内看坐面：定尺寸坐姿与65°弯腰假设'),('DOOR_HALL_APPROACH','真实廊侧停扇、门框及打开的2.4×2.6洞口'),('CLASS_OPERATION_P_EQUALS_E','原人物站立操作点、3_5关系候选、5_5旧研究区分')]
deps=[]
for n,t in boardnames:
 for ext in ['svg','png']:deps.append(dict(file=f'Boards/{P}_{n}.{ext}',inputs=['LAYOUT.json','ACTIVITY_DISTANCE.json','make_boards.py','../Revision01/LAYOUT.json'],description=t,scope='dimensional check illustration;not game'))
for n,t in viewnames:deps.append(dict(file=f'Previews/{P}_{n}.png',inputs=[P+'.blend','LAYOUT.json','CAMERAS.json','render_revision.py'],description=t,scope='actual mesh with CHECK-only cuts/proxies, same original daylight;not game or approved character motion'))
write('VIEW_DEPENDENCIES.json',dict(current=deps,inherited=[dict(file='../Revision01/Boards/SL_BLD_C01_MAIN_01_TRIAL_01_REV_01_P02_SEAT_STATUS.png',scope='unchanged geometry seat-state research,not final binding'),dict(file='../Revision01/Previews/SL_BLD_C01_MAIN_01_TRIAL_01_REV_01_SHOES_MAIN_SIMULTANEOUS.png',scope='unchanged main hall,Revision01 image'),dict(file='../Previews/SL_BLD_C01_MAIN_01_TRIAL_01_A.png',scope='original Trial01 whole appearance only'),dict(file='../Previews/SL_BLD_C01_MAIN_01_TRIAL_01_B.png',scope='original Trial01 whole appearance only')],textures='../Textures,48 original files unchanged',old_replaced='Do not use Revision01 1.4m door or missing benches as Revision02 local source. Original versions remain.') )
write('SPEC.md',f'''# C01整栋试作局部修订02规格 · 2026-10-16

执行原卡顶部修订02，基准为Trial01/Revision01。原试作/修订01/Reference/Planning保原字节。实际修改两个原对象（门洞墙带、门框与门扇）并增加一张双人坐凳；教室布局未改，席位与操作位置分开研究。整栋最终状态交回审。

## 固定条件及坐标

150×28m控制/三层/24班、52—12—30—12—44m、三外门、主厅3m内廊口、108㎡通高庭、60㎡露台/完成面8.03m、玻璃13.65/最高13.68m均沿原源。原点/轴向不变，米制；local→工程m=(X,Y+51,Z+8)，再×100为UE工程候选cm。地理worldXY=(2190.909090909091,1969.181818181818)+localXY，不能把该地理坐标与UE工程cm混算。规划映射不是现用地图Actor变换实测。[坐标表](COORDINATES.csv)逐项标地面、Actor、锚点、椅和研究点。

## 西连接门实际修改

房间边界不变[52.3,13..63.7,21.7]，接口中心(58,13,0)m；实体墙中线Y12.90、墙厚12.80..13.00。实际墙洞X56.80..59.20、Z0..2.60，左右各拓0.50m。原PARTITIONS_F01_DOOR_BAND仅该门区布尔切除；上部门头/其他层墙不重做。净门宽2.4/高2.6同步房间JSON及开口表，不只改标签。

新框在Y12.80..13.00，框条在净口外55mm，顶框从Z2.60起。两扇1.2m停放X55.53..56.73和59.27..60.47；框体厚40mm在Y12.71..12.75，距墙南面50mm，廊侧实际不嵌墙。保留原共享FRAME/GLASS材色。旧框定位线12.9、旧框深12.76..12.90的表达由本版实际墙厚/房间北界框定位替代；接口中心58/13和房界不迁。

原生射线覆盖门扇层/框/墙厚内五个Y截面、四个高度，实测最小宽{SC['native_door']['min_width_m']:.12f}m、高{SC['native_door']['min_height_m']:.12f}m；网格浮点判差容差10µm。模型标称2.4×2.6。扩大竖向开口2.60㎡，新增地面0㎡。结构/施工/消防未验，不据此作工程许可。

两条相反门区完整线从廊侧Y11.6到补柜内公共线，保所有柜前有限操作、两个坐面使用者和六等候位同时存在。定向全宽站立＋胶囊扫掠：进入最小分离40.172mm、离开80.172mm；两条独立完整线按外接圆半径{L['door_two_travellers']['enclosing_radius']:.9f}m比较，彼此最小余{L['door_two_travellers']['pair_clearance']:.9f}m。不是任意流量/合流同时性或NPC规则认证，没有用错时消除碰撞。

## 900格与换鞋坐面

九列柜体原字节网格/UV/变换保持：主厅468＋西连接432＝900，六层开放格继续候选。主柜有效腔0.288×0.304×0.276m，补柜单面深0.328/双面深0.334m；原上排取点1.60m/臂0.8m伸达研究沿原假设，不重复未受影响的900逐格射线。指纹证明九柜未变，继承Revision01的900腔深记录。柜列详[CABINETS](CABINETS.csv)。

新REV02_CHANGE_BENCH在X52.80..55.20、Y13.15..13.60，长2.40/深0.45/座高0.43m。木坐面厚35mm、六支50mm金属腿（X52.95/54/55.05，Y13.23/13.52）；沿用CHAIR/FRAME临时材质。两个坐面中心X53.40/54.60，坐定髋Y13.465；朝北。站立前位Y14.05，两个全宽使用区至Y14.45，另一坐面用户保持在场。新坐面不占柜列，不减容量或改变外门。

有限闭环：西连接门→中列西面第2列第3层取鞋(55.64,15.85,0)→携鞋/前端转向→右坐面前位(54.6,14.05,0)→连续坐下→65°弯腰换鞋假设→起身逆过程→公共主线→东侧第一等候位→廊侧离开。原六等候位在X62.9/Y14.55..20.05，自己的等待位只由同一人占用，其余五位保持；门区双向测试另保六位全部存在。柜前双侧操作0.70＋公共1.12＋0.70＝净面距2.52，坐面使用体不侵占命名公共线。

保持原认可PNG可见1.80m高/1.039655m宽；游戏0.68直径×1.92m高胶囊另列。坐/弯腰是**尺寸假设下的空间检查**，没有认可坐姿，不能称原角色动作通过。借用既有19阶段中的同一解析身体方法，旋转90°到凳位；就座/起身各同一1000区间解析界，脚、骨盆、全宽服装段、两条0.44+0.44腿及真实凳座/六腿都在，接触0允许/无内缩。原5_5的19阶段保持，未重跑未改变的教室步骤，没有新入座启动条件。

弯腰上身尺寸0.34深×1.039655宽×0.87高不变，绕北向前下缘Y13.635/Z0.52转65°，260区间保守旋转包络；固定腿脚及全宽下段不缩。肩{L['shoe_change']['shoulder']}、肘{L['shoe_change']['elbow']}、手{L['shoe_change']['hand']}m，肩手距{L['shoe_change']['hand_distance']:.9f}m≤0.8m，两连杆0.40+0.40。鞋成对0.29×0.235×0.115，示例腔宽余53mm/深余44mm；手从开放前口伸入，鞋直线抽出、携带/转向与前方放下的空间另核。地面鞋与自己的脚接触不视为与凳/柜相交。真实抓握、平衡、柔性服装和换鞋动作尚未验，未制作正式动画。

八条必要局部路径的最小分离见[LAYOUT](LAYOUT.json)：门→取鞋60mm、携鞋返回60mm、坐面接近110mm、起身→公共40.172mm、公共→等候240.172mm、等候→离开80.172mm、门双向进入/离开40.172/80.172mm。有限命名取用/同时静态用户与两条独立过路成立；任意柜位并发、任意合流、900人峰值不在通过范围，不开发排队/让行规则。

## 玩家席关系、P/E与固定锚点

教室30桌/30椅、原门(45,12.7,4)/净1.6×2.6、业务记录XY45/19.5和230cm、恢复候选45/18.7/4均不动。5_5及19阶段保既有尺寸研究，暂不绑定最终席。原附近3_5椅(46.175,19.87,4.43)列为关系候选；其旧接近候选(46.35,19.87,4)受阻/完整入座未验，不把它伪报最终可用。

可实际站立的美术操作地面G=(45,19.5,4)m，从原门经(45,18.8,4)到G，完整宽/胶囊扫掠最小分离0.21m。P与Enter E同处，无额外移动；这不是新增入座前提，也没有默认自动到椅子/传送。当前活动接口与入座空间研究分开。

代码证据SHA与规划读件一致：[CODE_EVIDENCE](CODE_EVIDENCE.json)。WorldSubsystem从运行世界TActorIterator注册PlaceActor（61–64行）；附近查找、预览及Enter分别按角色Actor—PlaceActor的三维距离≤230cm（平方52900）。地点标签+180/Marker+2不是锚点；PNG中心/椅中心/地面点也不是Actor中心。源构造胶囊半高96cm；RegionLanding helper额外+2cm只作单独示例，不能当所有时候的实测偏移。

|来源条件|G工程cm|P=E Actor工程候选cm|A来源cm|三维d / 230−d cm|
|---|---|---|---|---|
|历史Recipe，假设Actor+0.96m|(4500,7050,1200)|(4500,7050,1296)|(4500,7050,800)|496 / **−266**|
|历史Recipe，落地helper示例+0.98m|同上|(4500,7050,1298)|同上|498 / **−268**|
|正式规划，假设Actor+0.96m|同上|(4500,7050,1296)|(4500,7050,1200)|96 / **+134**|
|正式规划，落地helper示例+0.98m|同上|(4500,7050,1298)|同上|98 / **+132**|

[CSV](ACTIVITY_DISTANCE.csv)分别列P/E共8条；[JSON](ACTIVITY_DISTANCE.json)保精确XYZ、平方距离/来源/实际或假设偏移/局部与同基准cm/路线状态。上表的UE候选世界基准是规划映射；**现用地图锚点、Actor变换/缩放、scaled半高与落地偏差未回读**，没有将规划Z1200替成“现用原A”。不启动UE/PIE，源枚举运行世界并不能从代码文本推断地图Actor变换。资格、最近地点选择与真实游戏仍未验。

若现用A仍历史Z800、正式脚下Z1200，默认ActorZ1296，任何XY最优也有496cm竖差，超230达266cm，单靠换席无解。**唯一推荐取舍：保持原锚点/半径/楼层，暂停最终席绑定和该冲突部分精作，请规划/开发先只读核定现用Actor/Anchor世界变换，再判断接续方案。** 本轮不提出或执行移锚、扩半径、降楼层/缩人物/传送来“通过”。规划条件距离成立不等于工程兼容通过；其余可交门/坐面继续完成。

## 面积三项分账

|账目|主厅㎡|西连接㎡|合计/说明|
|---|---:|---:|---|
|原加深纠错|18×(0.66−0.60)=1.08||旧主10.80→11.88，不覆盖原文件|
|Revision01柜体|7.488|7.560|15.048|
|Revision02柜体|7.488|7.560|15.048，柜体增减0|
|Revision02新坐面|0|1.080|独立坐面投影，与旧1.08恰好同数但不同含义|
|双人换鞋使用|0|{L['areas']['bench_use_two_people']:.9f}|含自身坐面投影，不再与坐面直接相加|
|双人站立起身|0|{L['areas']['stand_rise_two_people']:.9f}|用途包络|
|六位等候|0|{L['areas']['queue_six_people']:.9f}|有限占位|
|柜面全长0.70操作带|16.380|15.120|用途面积，非900个人|
|主厅中央公共脊|23.436||仅该脊，不冒称全公共区面积|

柜间公共净宽1.12m、门前后命名路线另给，不把地面用途包络直接相加当总建筑面积；通路与坐面各自有同源图。完整[AREAS](AREAS.csv)。

## 模型、UV、预览与复核范围

{ST['mesh_objects']}建筑对象/{ST['unique_mesh_sources']}独立网格源/{ST['linked_placements']}额外链接摆放，源顶点{ST['source_vertices']}、摆放三角{ST['placed_triangles']}、14建筑材质、新贴图0。只对新门/坐面及切洞墙带投射实际UV_METRIC_64（4m/256²共享平铺）；其他2212对象网格/变换/UV/材质槽指纹保持。父Textures48张实际纹理及原材色继承，无AI生图。局部UV≥1cm²面实测{SC['local_density_px_per_m'][0]:.6f}–{SC['local_density_px_per_m'][1]:.6f}px/m，远坐标微小面浮点误差单列，不冻结最终密度/LOD。

屋顶/外壳/三层楼板室内/顶面/三梯与洞口保持原分组，共原点、Z上、FBX -Y forward。只有WHOLE建筑导出，CHECK/原人物/切片/姿态均排除；新CHECK默认隐藏，旧5_5检查层沿原版隐藏保留。独立Blend可编辑、图像打包；FBX空场景真实回导{FC['objects']}对象、分组/UV/材质面积一致，包络最大差{FC['bbox_max_error_m']:.12f}m，引用贴图都存在。变化的三个网格零面积/非流形0；九柜与19阶段未重验，通过原源指纹继承，未把局部重验扩为整栋最终验收。

3张3200×2400 SVG/PNG检查板与4张2560×1440原生局部预览，原日光/world/AgX、30°俯角，镜头实值[CAMERAS](CAMERAS.json)；检查体与切片不是实际游戏。近景从室内看坐面，避免用门扇遮挡身体尺寸。旧A/B只引原Trial外观、主厅引修订01原图并注明版本；不重复全楼或原19阶段预览。依赖[VIEW_DEPENDENCIES](VIEW_DEPENDENCIES.json)。

保RT01原588㎡/入口待设计不开放、B01/SchoolLife/校门/人物原PNG不变，无UE接入、正式动画、排队系统或入座启动条件。对真实游戏/运行位置未验证的边界见[分类验收](review.md)。交回规划审阅，不自行进入下一阶段。
''')
write('review.md',f'''# C01 Trial01局部修订02 · 制作方针对性验收

2026-10-16。不是规划接受记录；整栋最终状态由回审决定。

|类别|结果|证据/边界|
|---|---|---|
|实际局部资产已改|墙洞、2.4×2.6门框/停扇、双人换鞋坐面完成|[GEOMETRY](GEOMETRY.json)/Blend/实际FBX，原三外门与房界不变|
|门净宽/高与停扇|原生射线通过|最小宽{SC['native_door']['min_width_m']:.12f}、高{SC['native_door']['min_height_m']:.12f}m，10µm网格容差；停扇距墙0.05m|
|900与面积|保持|主468/补432，柜体15.048㎡不变；新凳1.080㎡与旧加深1.080㎡纠错分账|
|有限换鞋闭环|该尺寸假设下空间通过|真实凳/六腿、另一使用者、柜前双操作及等待都在；1000区间就座/起身、260区间弯腰及鞋/手空间，不是认可角色动作|
|门双向/转角/公共线|指定条件通过|8条局部路径、两条独立相反门路线彼此余{L['door_two_travellers']['pair_clearance']:.9f}m；不认证任意合流或900人峰值|
|玩家操作点可达|全宽站立空间通过|原门→(45,18.8,4)→G(45,19.5,4)，最小分离0.21m；P=E同处，无入座前提|
|正式锚点候选距离|仅规划条件验算通过|假设Actor+0.96/+0.98m，d96/98cm，余134/132cm；不代表现用地图|
|历史锚点条件距离|失败/冲突保留|Z800→P1296/1298，d496/498，超266/268cm；不改锚点/楼层/半径|
|现用工程/最终席绑定|未验证/暂停|现用Actor/Anchor、scaled半高等未回读；3_5关系候选完整入座未验，不绑定；唯一推荐先交规划/开发只读核变换|
|既有19阶段与30席|继承，未额外重跑|家具未变；5_5研究1条件连续/6仅站立/23旧候选受阻，不作为最终绑定或全班通过|
|实际源/必要回导|通过|变化三网格零面积/非流形0，2212未改指纹；FBX{FC['objects']}对象/分组/UV/材质面积核对|
|原版/只读输入|{len(protected)}项指纹保持|[protected_inputs](protected_inputs.json)，旧manifest不覆盖|
|真实游戏/资格/角色动作|未验证|无UE/PIE、动画/抓握/平衡、导航、活动资格/最近地点实测|

原始审批及来源：[原卡修订02](../../../../../Docs/AssetPlanning/BuildingProduction/TaskCards/SL_BLD_C01_MAIN_01_TRIAL_01.md)、[修订01回审](../../../../../Docs/AssetPlanning/BuildingProduction/review-C01-trial-revision-01.md)、[只读代码](CODE_EVIDENCE.json)、[源改动](CHANGE_SCOPE.json)、[继承清单](INHERITED_STUDY.json)。保持RT01/B01/SchoolLife/认可人物，停止等待规划和用户审阅。
''')
blinks='\n'.join(f'- [{n}：{t}](Boards/{P}_{n}.png) · [可编辑SVG](Boards/{P}_{n}.svg)' for n,t in boardnames)
vlinks='\n'.join(f'- [{n}：{t}](Previews/{P}_{n}.png)' for n,t in viewnames)
write('README.md',f'''# C01整栋试作局部修订02 · 实际资产回件

[可编辑Blend]({P}.blend) / [实际建筑FBX]({P}.fbx) / [统一几何](GEOMETRY.json) / [布局与包络](LAYOUT.json) / [规格](SPEC.md) / [分类验收](review.md)。原Trial/Revision01完整保留，整栋上下文沿原版，仅门洞墙带/框扇与新双人凳改动。

实际内门同中心净2.4×2.6m、900格和新双人坐面已交；有限取鞋/换鞋/起身/等候/离开空间通过。**玩家工程兼容仍未通过实证：正式规划Z1200条件d96/98cm，历史Z800条件d496/498cm超限；现用运行位置未回读。** 不移动原锚点、不扩大230cm、不传送，暂停最终席绑定，交规划/开发核定。预览与Enter只在同一可达操作点验算，不要求19阶段全程留圈或新增入座前提。

{blinks}

4张2560×1440实际局部自然光，30°；蓝色为未获认可的定尺寸姿态假设、绿色柜前操作/路径、赭色等待/取鞋循环。原人物PNG仅原字节站立对照，检查切片和代理不是游戏画面：

{vlinks}

[P/E三维距离8条CSV](ACTIVITY_DISTANCE.csv) / [完整来源与距离](ACTIVITY_DISTANCE.json) / [地面/Actor/锚/椅坐标](COORDINATES.csv) / [门框停扇表](OPENING_CHANGE.csv) / [柜列表](CABINETS.csv) / [30席继承状态](SEATS.csv) / [面积分账](AREAS.csv)。

[实际源检查](SOURCE_CHECK.json) / [回导检查](FBX_CHECK.json) / [局部差异指纹](CHANGE_SCOPE.json) / [19阶段继承](INHERITED_STUDY.json) / [代码SHA](CODE_EVIDENCE.json) / [图稿依赖](VIEW_DEPENDENCIES.json) / [保护输入](protected_inputs.json) / [清单](manifest.json)。

900格主468/补432与15.048㎡柜体不变；新凳2.4×0.45m投影1.080㎡，与旧18×0.06=1.080㎡纠错是不同账目。三变化网格实际UV64px/m起点，父Textures48文件原字节继承、新贴图0。其他2212建筑对象完全保持，原19阶段/900腔验继承而不重跑。原[整栋A](../Previews/SL_BLD_C01_MAIN_01_TRIAL_01_A.png)/[B](../Previews/SL_BLD_C01_MAIN_01_TRIAL_01_B.png)仅看原Trial外观；[主厅图](../Revision01/Previews/SL_BLD_C01_MAIN_01_TRIAL_01_REV_01_SHOES_MAIN_SIMULTANEOUS.png)为未变修订01部分，不能当新版门/坐面图。

复现：prepare_revision.py（只提取旧定义，不运行旧写出）→build_revision.py→render_revision.py→verify_revision.py→make_boards.py→SVG原生3200×2400栅格化→finalize_delivery.py。只写本修订目录和本轮授权交接索引；不要执行原版收尾脚本覆盖旧包。

RT01原状态不开放；B01/SchoolLife/校门/人物不变，无UE/新系统/正式动画。真实角色动作/抓握、任意高峰运营、当前世界Actor变换与资格仍未验。回审决定整栋最终状态，停止本轮。
''')
rootprefixes={
'README.md':'# 当前制作回件：C01整栋试作局部修订02 · 2026-10-16\n\n[独立修订包](ArtSource/Buildings/SL_BLD_C01_MAIN_01/Trial01/Revision02/README.md) / [规划回审](Docs/AssetPlanning/BuildingProduction/C01/trial-revision-02-handoff.md)。真实西连接洞/框/廊侧停扇2.4×2.6与双人换鞋凳完成；900/15.048㎡柜体不变，新凳1.080㎡分账。局部换鞋与双向条件检查、必要FBX回导完成，2212未改对象保持。操作点45/19.5可达，P=E按Actor—Anchor三维分来源：规划Z1200余134/132cm、历史Z800超266/268cm，现用变换未实测，暂停最终席绑定；19阶段不改、不新增启动条件。交回针对性审阅，不代判整栋最终通过，无UE。\n\n',
'Docs/progress.md':'# C01 Trial01局部修订02实际制作完成 · 2026-10-16\n\n[REV_02](../ArtSource/Buildings/SL_BLD_C01_MAIN_01/Trial01/Revision02/README.md)交独立Blend/建筑FBX/JSON、3SVG/PNG、4局部原生预览及坐标/距离/门片/柜列/席状态/面积表。门洞墙带/框扇实改2.4×2.6，补2.4×0.45/座高0.43双人凳，900不减。变化三网格0零面积/非流形、2212未改指纹和真实FBX回导通过；有限换鞋闭环/门区双向成立。玩家操作点门口可达、P=E；规划Z1200仅条件内，历史Z800竖差496cm超限266，现用工程未验，暂不绑最终席。旧19阶段继承不重跑；停回审，无UE/下一阶段。Git实绩收尾另记，原3脚本保留。\n\n',
'Docs/handoff.md':'# 当前制作回件：C01 Trial01局部修订02 · 2026-10-16\n\n入口：[修订包](../ArtSource/Buildings/SL_BLD_C01_MAIN_01/Trial01/Revision02/README.md) / [规划针对性回审](AssetPlanning/BuildingProduction/C01/trial-revision-02-handoff.md)。门区真实墙洞/框/停扇2.4×2.6、双人换鞋凳和局部证据已交；900柜体不变，旧1.08纠错/新凳1.08/15.048柜体分账。P=E G45/19.5/4可达，Actor偏移0.96/0.98分算；规划A1200余134/132，历史A800超266/268cm，现用Actor/Anchor未回读，暂停最终席绑定，唯一推荐先由规划/开发只读核变换。19阶段不改，不要求全程留半径或新增入座启动条件。原版/RT01/B01/SchoolLife/人物保持，无UE，交回审定整栋状态；Git实绩另记。\n\n',
'Docs/execution-plan.md':'# C01 Trial01局部修订02执行记录 · 2026-10-16\n\n起点main/ad9bb026f962dbcdce7f54ca1005c462767b6c1c，已跟踪干净/原3脚本保留；读原卡02、修订01源与回审/审计/只读代码。先低细度保持900柜列，前端安排双人坐面及腿脚/弯腰/起身/等候闭环，核扩门双向与停扇；从原门到业务XY操作点给Actor—Anchor三维P/E两来源表。历史Z8与规划楼层Z12冲突保留，暂停最终席绑定而继续门/坐面。实际新源仅洞口墙带/框扇/凳及UV，3板4预览、源重开/必要回导及保护检查；原19阶段/未改柜腔只指纹继承，不增无关阶段。错开规划Git后仅本轮文件正常提交推送，停止回审，无UE或新系统。\n\n',
'Docs/decision-log.md':'# C01 Trial01局部修订02候选与未解决边界 · 2026-10-16\n\n按已接受方向实改西连接同中心2.4×2.6，柜列900/主468补432不变；前端双人坐面2.4×0.45/高0.43、六腿，真实坐姿/换鞋仍是尺寸假设。原19阶段5_5保研究且不绑定最终席；3_5只列附近关系候选，活动P=E在45/19.5/4，完整站立门路可达，不把入座加成当前启动条件或要求全过程在圈。源代码按Actor—Anchor三维230cm；默认偏移0.96下规划A1200距96余134、历史A800距496超266，运行地图/Actor变换未核，唯一推荐暂停最终绑定并交规划/开发只读核定，不擅移锚点/半径/楼层/传送。新凳1.08与旧加深1.08另账。整栋最终状态交回审，无UE。\n\n',
'Docs/AssetPlanning/BuildingProduction/README.md':'# 当前制作回件：C01 Trial01局部修订02 · 2026-10-16\n\n[独立回件](../../../ArtSource/Buildings/SL_BLD_C01_MAIN_01/Trial01/Revision02/README.md) / [回审入口](C01/trial-revision-02-handoff.md)。实际同中心2.4×2.6门及双人换鞋坐面完成，900柜列/面积保持；仅变化三网格重验，2212未改指纹/必要回导通过。P/E同操作点到Actor锚点三维两来源分算，规划条件内不冒称现用兼容；历史Z8与楼层Z12冲突，最终席暂不绑定。原19阶段/全楼外观与UV材色保留，RT01不开放，无UE；交回审定整栋最终状态。\n\n'}
for rel,prefix in rootprefixes.items():
 f=R/rel;t=f.read_text(encoding='utf-8')
 if not t.startswith(prefix):f.write_text(prefix+t,encoding='utf-8',newline='\n')
handoff=R/'Docs/AssetPlanning/BuildingProduction/C01/trial-revision-02-handoff.md'
handoff.write_text(f'''# C01 Trial01局部修订02 · 交规划针对性审阅

2026-10-16，制作方实改回件，不代用户/规划接受。

[独立包](../../../../ArtSource/Buildings/SL_BLD_C01_MAIN_01/Trial01/Revision02/README.md) / [SPEC](../../../../ArtSource/Buildings/SL_BLD_C01_MAIN_01/Trial01/Revision02/SPEC.md) / [分类验收](../../../../ArtSource/Buildings/SL_BLD_C01_MAIN_01/Trial01/Revision02/review.md)。Blend/FBX/JSON、3定尺SVG/PNG、4原生日光局部图及表格/证据均实交。原Trial/Revision01保持，不重新命名旧简模。

请复核三项：

1. 实际内门同中心58/13净2.4×2.6，墙洞、墙厚内框及廊侧停扇全部同步。框/停扇Y和墙厚分别记录，原生多截面实测最小宽{SC['native_door']['min_width_m']:.12f}/高{SC['native_door']['min_height_m']:.12f}m；两独立门路线彼此余{L['door_two_travellers']['pair_clearance']:.9f}m，坐面用户/操作/队列同时在场。开口多2.6㎡是竖向面积，不是新增地面。
2. 900九柜完全不变，前端新增2.4×0.45/座高0.43双人凳，真实六支腿。有限取鞋/携鞋/坐定/弯腰换鞋/起身/等候/离开包络成立，全部是明确尺寸假设，原人物坐姿/真实抓握平衡未验。柜体15.048㎡、新凳1.080㎡、旧加深纠错1.080㎡分别列账，不混同；非任意柜位并发/900人运营认证。
3. 操作G=(45,19.5,4)m门口可达，P=E同处；3_5为附近席关系候选，未完成其入座，不绑定最终席。原5_5/19阶段只继承尺寸研究，无新增启动条件/全程留圈要求。按默认Actor高出脚下96cm，统一工程候选P/E=(4500,7050,1296)cm；对正式规划A=(4500,7050,1200)，d96/余134cm；对历史Recipe A=(4500,7050,800)，d496/超266cm。+98cm落地helper示例另列d98/498，不当运行时实测。代码从运行世界枚举PlaceActor，**当前地图Actor/Anchor/缩放未回读**，绝不把规划A1200替成原现用锚点通过。唯一推荐取舍：保原锚点/230/楼层，暂停最终席绑定和冲突部分精作，交规划/开发先只读核定现用变换再判接续，不在本轮移动锚点/扩半径/降楼层或默认传送。资格/最近地点/游戏未验。

变化三建筑网格原生零面积/非流形0、实际UV；2212其他对象含全部柜列与教室30桌椅指纹保持，原900腔和19阶段未重复验或扩成整栋通过。实际FBX空场景回导{FC['objects']}建筑对象、分组/UV/材质面积与包络核对，CHECK/人物不导出。{len(protected)}项原版与只读输入SHA保持；代码/历史锚点来源和精确Actor距离表可复核。

原三外门/主厅3m口、RT01原588㎡待设计不开放、B01、SchoolLife、校门/人物保持，无UE/正式动画/新系统。停止本轮，整栋最终状态由规划回审决定。实际Git/LFS见Docs/handoff收尾实绩及制作最终报告。
''',encoding='utf-8',newline='\n')
assert len(list((O/'Previews').glob('*.png')))==4 and len(list((O/'Boards').glob('*.png')))==3
assert all(Image.open(p).size==(2560,1440) for p in (O/'Previews').glob('*.png'))
assert all(Image.open(p).size==(3200,2400) for p in (O/'Boards').glob('*.png'))
write('CHECKS.json',dict(protected_files=len(protected),protected_changed=bad,changed_architecture_objects=3,unchanged_architecture_objects=2212,
 local_zero_area=0,local_nonmanifold=0,native_door=SC['native_door'],actual_export_objects=FC['objects'],all900_banks_unchanged=True,
 inherited900_cavity_rays=900,retested900_cavity_rays=0,inherited19_stages=19,retested19_stages=0,local_paths=len(L['paths']),
 local_paths_passed=all(q['passed'] for q in L['paths']),bench_transition=L['bench_transition']['passed'],shoe_bend=L['shoe_change']['passed'],
 P_equals_E=True,operation_route_passed=True,planning_distance_cases_passed=True,historical_distance_cases_passed=False,
 current_runtime_engineering_verified=False,final_seat_bound=False,game_verified=False,whole_building_final_status='planning review decides',
 source_blend_sha256=SC['blend_sha256'],fbx_sha256=FC['fbx_sha256'],boards=3,previews=4))
linkbad=[]
for f in list(O.glob('*.md'))+[handoff]:
 for target in re.findall(r'\]\(([^)]+)\)',f.read_text(encoding='utf-8')):
  target=target.strip('<>')
  if target.startswith(('http','#','D:','C:')) or target=='manifest.json':continue
  if not (f.parent/target.split('#')[0]).resolve().exists():linkbad.append([str(f),target])
assert not linkbad,linkbad
files=[p for p in O.rglob('*') if p.is_file() and p.name!='manifest.json' and p.suffix not in ['.blend1','.pyc'] and '__pycache__' not in p.parts]
write('manifest.json',[dict(path=p.relative_to(O).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(files)])
print('REV02_DELIVERY_READY',len(files),'protected',len(protected),'links_ok',flush=True)
