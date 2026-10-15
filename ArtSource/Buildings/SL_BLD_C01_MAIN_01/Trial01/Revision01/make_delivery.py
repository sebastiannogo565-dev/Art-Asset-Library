"""Finalize scoped documentation from the actual revision evidence, preserve all earlier files."""
import json,csv,hashlib,math,re
from pathlib import Path
from PIL import Image
O=Path(__file__).parent;R=Path('D:/Art Asset Library');P='SL_BLD_C01_MAIN_01_TRIAL_01_REV_01'
def read(n):return json.loads((O/n).read_text(encoding='utf-8'))
def write(n,v):(O/n).write_text((json.dumps(v,ensure_ascii=False,indent=2) if not isinstance(v,str) else v).rstrip()+'\n',encoding='utf-8',newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
L=read('LAYOUT.json');S=L['shoe'];SC=read('SOURCE_CHECK.json');FC=read('FBX_CHECK.json');ST=read('STATISTICS.json')
assert SC['sha256']==sha(O/(P+'.blend')) and FC['fbx_sha256']==sha(O/(P+'.fbx'))
assert FC['source_blend_sha256']==SC['sha256']
assert all(x['passed'] for x in L['segments']) and S['nominal']==900
changed=[v['path'] for v in read('protected_inputs.json') if sha(Path(v['path']))!=v['sha256']]
assert not changed,changed
coords=[('business','unchanged',[45,19.5,4],[45,19.5,4]),('recovery','candidate_unchanged',[45,18.7,4],[45,18.7,4]),
 ('designated_chair','candidate_reassigned',[46.175,19.87,4.43],L['player']['chair_rest']),
 ('standing_approach','candidate',[46.425,18.8,4],L['player']['approach']),
 ('physical_desk_5_5','local_change',[47.675,19.87,4.72],L['player']['desk']),
 ('physical_chair_5_5','local_change',[48.075,19.87,4.43],L['player']['chair_rest']),
 ('player_chair_pulled','candidate',[46.425,19.87,4.43],L['player']['chair_pulled'])]
with (O/'COORDINATES.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f,lineterminator='\n');w.writerow(['interface','status','old_local_m','new_local_m','new_engineering_m','new_world_xy_m_local_z'])
 for n,status,a,b in coords:w.writerow([n,status,a,b,[b[0],b[1]+51,b[2]+8],[b[0]+2190.909090909091,b[1]+1969.181818181818,b[2]]])
clear=[]
for name,p in [('business',L['business']),('recovery_candidate',L['recovery_candidate'])]:
 furniture=[ob for ob in L['obstacles'] if ob['id'].startswith('F2_W4')]
 dist=min(math.hypot(max(ob['bounds'][0]-p[0],0,p[0]-ob['bounds'][3]),max(ob['bounds'][1]-p[1],0,p[1]-ob['bounds'][4])) for ob in furniture)
 clear.append(dict(id=name,point=p,point_to_furniture_xy_m=dist,scope='point-to-footprint distance only;230cm game interaction radius and actual recovery logic unchanged/unverified'))
write('INTERFACE_CHECK.json',dict(points=clear,original_class_door=[45,12.7,4],business_radius_engineering_cm_unchanged=230,
 source_unchanged_objects=SC['unchanged_objects_checked'],actual_link_door_width_m=1.4,proposal_only=2.4))
boards=[('P01_CLASS_CONTINUOUS','同坐标30席、站立/椅活动/坐姿三层与19阶段证据'),('P02_SEAT_STATUS','30稳定ID，1假设连续/6站立/23当前候选受阻'),('P03_SHOES_LAYOUT','双操作/公共路/等候/门冲突与两套面积账')]
views=[('CLASS_REST_OPERATOR','椅复位、原人物站立/门口与操作位置'),('CLASS_PULLED_APPROACH','自己的椅子拉出，原尺寸代理站在椅前'),('CLASS_TRANSITION_HALF','t=0.5定尺寸关节/全宽包络假设'),('CLASS_SEATED_ASSUMPTION','t=1坐定假设，真实椅座接触'),('CLASS_RESTORED','起身逆过程后退出/椅复位，路线同坐标'),('SHOES_MAIN_SIMULTANEOUS','主厅两侧有限操作包络与同时进出路线'),('SHOES_LINK_DOOR_CONFLICT','补柜双侧操作/侧袋等候，原1.4门红框/2.4建议蓝框')]
deps=[]
for n,label in boards:
 for ext in ['svg','png']:deps.append(dict(file=f'Boards/{P}_{n}.{ext}',inputs=['LAYOUT.json','SHOE_CHECKS.json','make_boards.py'],meaning=label,kind='editable dimensional check board' if ext=='svg' else 'reading raster, not game'))
for n,label in views:
 deps.append(dict(file=f'Previews/{P}_{n}.png',inputs=[P+'.blend','LAYOUT.json','CAMERAS.json','render_revision.py'],meaning=label,kind='actual revised mesh + separate editable CHECK-only context/cut/proxy; natural light; not game'))
write('VIEW_DEPENDENCIES.json',dict(current=deps,unchanged_originals=[dict(file='../Previews/SL_BLD_C01_MAIN_01_TRIAL_01_'+n+'.png',version='original Trial01; unchanged whole appearance only, not new local layout') for n in ['A','B']],textures='../Textures;48 unchanged original files, no new image generation'))
write('SPEC.md',f'''# C01整栋试作局部修订01规格 · 2026-10-16

只更新已接受整栋试作中的玩家班局部、主鞋柜厅与西连接柜列；本次不判整栋最终通过。原Trial/Reference/Planning原字节保留。

## 固定范围与坐标

150×28m控制、三层/24班、52—12—30—12—44m、原三外门/主厅3m内廊口、108㎡庭/60㎡露台、13.65玻璃/13.68最高、露台FL8.03全部沿原几何。单位m，共原点，+X东/+Y北/+Z上。worldXY=(2190.909090909091,1969.181818181818)+localXY；工程=(X,Y+51,Z+8)m。人物与源模型不各自归零。

教室净[41,12.7,49.4,21.7]，8.4×9m、FL4；原门(45,12.7,4)/净1.6×2.6，业务(45,19.5,4)与230cm工程交互半径均不改。恢复(45,18.7,4)仍候选；见[新旧坐标](COORDINATES.csv)及[点净区](INTERFACE_CHECK.json)。点到家具距离不是整个交互半径内无家具承诺。

## 教室候选及连续条件

保30席与稳定ID。玩家指定候选由原C30_DESK_3_5改为F2_W4_DESK_5_5，原3_5仍为普通席保留。只把5_5桌X47.675→47.715(+40mm)、自己的椅子X48.075→48.275(+200mm)；椅拉出X48.900、行程0.625m。Y19.870不变。椅座高0.430、椅宽/深0.450m，原背顶0.840m；局部新把手顶0.880，最外X=椅心+0.300m。把手在背上实体搭接10mm；几何始终包含在低细度保守HANDLE[+0.16..+0.30,±0.10,+0.80..+0.88]内。独立椅网格不传播至其余719把椅子。

站立路线分原门→(45,18.8)→(48.8,18.8)→操作点(48.8,19.08)；保人物在场拉出自己的椅子；退回横道，经(48.29,18.8)到椅前(48.29,19.87)。坐下和起身为连续逆过程；退出后回操作点推椅，经教学前场(41.7,18.8)回原门。完整19阶段在[LAYOUT](LAYOUT.json)；图P01分别画站立、椅活动、姿态包络。

**仅称“该尺寸假设下连续空间检查通过”**。原PNG可见1.80m高/1.039655m正面宽，与游戏0.68m直径×1.92m高胶囊分别保留；原PNG未重绘或压缩。站立脚段宽0.64m覆盖原脚宽0.6362m，中段/上段均保全宽。坐姿不是原人物：髋高0.93→0.52m、上身0.34深×1.039655宽×0.87高；定尺寸0.34深×1.039655宽×0.77长的下段绕Y铰转90°，覆盖原图低处手臂/服装的宽度，不缩短/缩窄。该包络是几何假设，不从PNG推断人体结构。双腿各大腿/小腿0.44m，半径0.06m；足包络0.28×0.64×0.30不撤走。手臂每侧0.40+0.40m，总伸达限制0.8m，有限抓握位置只为几何候选，不是已验证抓握/力学。

髋轨迹X=48.29+0.585·sin(πt/2)，Z=4+0.93−0.41t²；踝(X48.29,Z4.07)固定，两连杆IK前膝。姿态转换用1000区间的单调/sin/cos/IK区间包络，定宽下段分24条、每条腿12段，只细分保守包络而不缩体。旋转≤0.25°区间并加曲率垫，平移≤1cm分段。全部包含桌下托盘、桌腿、自身椅/背/腿/把手及墙门。10µm数值容差，无1mm内缩。坐定臀底4.430与椅面接触，最小分离约0；最小站立余量10mm，操作转向18.08mm。没有靠终点采样冒充整段，也没有瞬移、删椅或正式动画/入座系统。

[逐席表](SEATS.csv)：1玩家席上述假设下连续通过，6席仅站立可达，23席当前候选站位或拉椅受阻；其余29席的入座/离席姿态均未验证。站立搜索0.05m网格、固定朝西、0.68深×1.039655宽保守矩形；非玩家席拉椅目标=桌X+1.25。受阻不证明不存在其他方案。其余23班全部对象变换/网格/UV/材质指纹保持，未继承此次玩家通过结论。

## 鞋柜900目标与实际腔体

当前柜列为低细度真实可用腔体试作，不精作未获接受的柜门/五金。原五层滑面候选改为**六层开放格候选**，不隐瞒层数和面型取舍。无外凸拉手或门扇扫掠，前沿内收唇4mm；共享原材色/实际64px/m UV，不新生纹理。

|区域/柜列|长/深m|列×层×面|格数|有效腔宽/深/净口高m|
|---|---|---|---|---|
|主厅西×3|3.00/0.64|10×6×2×3|360|0.288/0.304/0.276|
|主厅东×3|0.90/0.64|3×6×2×3|108|同上|
|西连接靠西单面|4.80/0.35|16×6×1|96|0.288/0.328/0.276|
|西连接中/东两列|各4.20/0.70|14×6×2×2|336|0.288/0.334/0.276|
|合计|||900|主厅468/西连接432|

柜腔深为保留前沿/安装余量后的保守值；原生射线对900格逐格穿至背板，实际射线深不小于这些值。中格宽0.288、层净高0.288，内唇令有效净口高0.276；鞋290×105×115mm、两只合宽235mm仅设计包络，不是通用鞋适配认证。新增手80×180×25mm，鞋+手总高0.150、净口余0.126m。六层顶部1.80、上排底1.50、取点1.60m；假设肩1.0/臂0.8，横偏0.37、前后0.30、竖差0.60需0.7661m伸达。真实手、抓握、力量与儿童适用性未验。

柜列坐标/朝向逐项见[CABINETS](CABINETS.csv)。主厅排Y1.05/4.21/7.37，柜深0.64，面距2.52；净分解0.70操作+1.12公共+0.70操作。中央脊通路2.80m，对原外门/内廊门均净3m，外门坐标不改；侧柜端绕行≥1.12m。西连接柜列纵向自Y15.4，前端净2.4m；单面靠西/两双面，公共带1.12m；东侧(X62.9,Y14.55..20.05)六等候位避开柜端与X61.6公共线。照片板原网格/UV保留，平移(+34,+19.65)，到[63.45,20.85..63.70,21.55]，不堵新绕行路。

双面有限操作包络同时在场，不用错时、NPC让行或排队规则作为解法。检验移动人物全可见宽1.039655×厚0.34的外接圆半径0.546919m，精确线段/角点扫掠对柜体、两侧操作矩形和队列。主厅两条同时进出路径最小清距13.08mm，二者包络间余0.60616m；西连接有限单人完整环路清距13.08mm。均只覆盖[命名路径与有限操作位置](SHOE_CHECKS.json)，不是任意全柜同时取用/900人峰值运营。外墙边0.70m是使用带，不能同时称人物背后通路。

**未解决：西连接原(58,13)内门净1.40m仍保原实体**。两个人物正面并行需2.07931m，差0.67931m；外接圆保守并行需2.18768，差0.78768m。布置给2.4m建议门的双向轨迹在真实1.4m门框中穿入0.44692m，明确失败。

**唯一推荐取舍：请规划判断将该内部廊口同中心1.4→2.4m（两侧各扩0.50m）**。保持900、两区边界、外门及主厅3m内廊口；代价为该处门框/门片及约2.6㎡墙面开口变更，需规划核墙体/用途。蓝色2.4框和虚线路径仅CHECK/建议图，不导出；实际Blend/FBX保持原门。2.4m建议条件下双向轨迹检查最小清距13.08/53.08mm，彼此余0.10616m，但不替代批准。该接口精作暂停；保柜列验证候选，不宣称整体运营通过。

原主厅两凳和西连接一凳移除以恢复操作/绕行；**换鞋坐凳和实际换鞋动作没有解决或验证**，列规划判断，不将储鞋操作通过当换鞋流程通过。本轮不另加空间/家具任务或减格建议。

## 面积两本账

|原版纠错基准|主柜占地㎡|
|---|---:|
|18.00m总长×0.60m|10.800|
|原Trial加深后18.00×0.66|11.880|
|原加深实际新增18×0.06|**1.080（原0.540错误）**|

|实际版本|主厅㎡|西连接㎡|合计㎡|
|---|---:|---:|---:|
|原Trial|11.880|6.300|18.180|
|本修订|7.488|7.560|**15.048**|
|相对原Trial|−4.392|+1.260|**−3.132**|

新主柜总长11.70×0.64；西连接4.80×0.35+8.40×0.70。仅柜体投影，不含操作/路/等候；1.08是旧纠错，不是新方案增减。原包不覆盖，见[AREAS](AREAS.csv)。

## 源、UV、导出及分组

修订Blend保整栋上下文；原WHOLE/ROOF/EXTERIOR、三层楼板/室内/分隔/顶面与三梯组原样，所有开孔/隐藏关系沿原试作。新9柜与独立玩家椅用实际UV_METRIC_64，4m平铺256²贴图；其他材质/UV逐字节网格指纹保持，14建筑材质。继承父目录48实际纹理（42张256²及6张128²对照），新纹理0；64/32比较沿[原版本](../Previews/SL_BLD_C01_MAIN_01_TRIAL_01_DENSITY_64.png)，不是新版几何图。未冻结最终密度/LOD/复杂碰撞或通道方案。

建筑对象{ST['mesh_objects']}，独立源网格{ST['unique_mesh_sources']}，额外链接摆放{ST['linked_placements']}，源顶点{ST['source_vertices']}，摆放三角{ST['placed_triangles']}。2214建筑对象只导出WHOLE；无人物、包络、切片/候选2.4门。CHECK层默认隐藏，可编辑21姿态样本中的t0/.5/1检查体和原人物；连续证据在JSON与验证脚本，不生成正式动画。

Blender5.2.2原生重开/900实际腔射线/零面积与非流形0/UV齐全；UV≥1cm²面实测约{SC['density_px_per_m'][0]:.3f}–{SC['density_px_per_m'][1]:.3f}px/m，细小远坐标UV浮点误差不冒称精确64。FBX回导2214对象、分组/UV/材质面积一致，包络最大误差{FC['bbox_error_m']:.9f}m；全部材质贴图路径存在。原图与材质打包可定位；真实游戏导入未做。

## 预览与剩余边界

7张2560×1440原生局部自然光，约30°，日光/world/AgX沿原试作；教室5张同镜头、柜区各1张。切片与代理独立，不冒称实际游戏。三张3200×2400 SVG/PNG同JSON定尺板，依赖见[VIEW_DEPENDENCIES](VIEW_DEPENDENCIES.json)。原整栋[A](../Previews/SL_BLD_C01_MAIN_01_TRIAL_01_A.png)/[B](../Previews/SL_BLD_C01_MAIN_01_TRIAL_01_B.png)只证明未受影响外观，标原Trial版本。

仍未验证：真实坐姿/手臂抓握和力、其他29席姿态/23班、门1.4双向冲突、换鞋坐凳/换鞋动作、任意柜位并发与峰值、真实角色八向/动画/导航/恢复/镜头、UE/碰撞。RT01原588㎡控制及入口保持待设计不开放；不增承托/接近。B01/校门/SchoolLife/原人物保持，不接UE。

来源：[当前原卡修订段](../../../../../Docs/AssetPlanning/BuildingProduction/TaskCards/SL_BLD_C01_MAIN_01_TRIAL_01.md)、[规划T01–T04](../../../../../Docs/AssetPlanning/BuildingProduction/review-C01-trial-01.md)、[审计](../../../../../Docs/AssetPlanning/BuildingProduction/C01/trial-01-planning-audit.json)、原Trial Blend/GEOMETRY/实际纹理和认可PNG。本轮只停交规划针对性审阅，不启动下阶段。
''')
write('review.md',f'''# 制作方针对性验收 · 2026-10-16

本报告为制作方实检，不代替规划窗口或用户认可。整栋不最终通过。

|范围|结果|证据与限制|
|---|---|---|
|玩家席连续19阶段|该尺寸假设下布局通过|[LAYOUT](LAYOUT.json)/P01；保全人物宽/胶囊、自身椅及托盘，无内缩。坐姿未获认可，不能称原人物动作通过|
|30席逐席|1条件连续、6仅站立、23当前候选受阻|[SEATS](SEATS.csv)/P02；其余29席姿态未验，其他23班保持原样未外推|
|原门/业务/恢复|保持|业务/候选净距见[INTERFACE_CHECK](INTERFACE_CHECK.json)，工程点/230cm半径不改|
|柜体容量/腔深|900实际腔体与逐格深度通过|主468+补432，六层开放格候选；[原生检查](SOURCE_CHECK.json)，上排伸达仅尺寸假设|
|指定双面操作/公共路/队列|有限条件部分通过|主厅双进出、补柜单环路；[SHOE_CHECKS](SHOE_CHECKS.json)，不等于所有柜位/900人运营|
|西连接原1.4门双向|**未通过**|需求2.07931m差0.67931；推荐同中心2.4，仅CHECK候选未改实际门；接口精作暂停|
|换鞋|未解决/未验证|原三凳移除，实际换鞋姿态/坐凳未落实，不以储鞋路径冒充完整流程|
|旧统计/新面积|已更正/重算|1.08㎡旧加深纠错；新15.048㎡、相对原Trial−3.132；[两账](AREAS.csv)/P03|
|局部范围/共享实例|通过|{SC['unchanged_objects_checked']}未受影响对象指纹完全保持；[CHANGE_SCOPE](CHANGE_SCOPE.json)|
|源拓扑/UV/导出|本修订源检查通过|零面积0/非流形0/UV全有；真实[FBX回导](FBX_CHECK.json)，不含CHECK|
|原版与保护对象|通过|{len(read('protected_inputs.json'))}项SHA逐项一致；旧manifest不重写|
|游戏内/导航/恢复/镜头/碰撞|未验证|SchoolLife只读，无UE接入/正式动画/新系统|

规划需判断：同中心西连接1.4→2.4m内部廊口这一项推荐取舍；六层开放格及取消坐凳是否符合学校使用需求；是否接受玩家指定席与保守姿态假设。保30席与900目标，未擅自减数或改固定边界/外门。其他未通过项保留，不自动精修或扩展下一栋。
''')
links='\n'.join(f'- [{n}：{label}](Boards/{P}_{n}.png) · [可编辑SVG](Boards/{P}_{n}.svg)' for n,label in boards)
images='\n'.join(f'- [{n}：{label}](Previews/{P}_{n}.png)' for n,label in views)
write('README.md',f'''# C01整栋试作局部修订01 · 独立回件

已实际修改玩家桌椅、九列柜体和照片板位置，保原整栋外观/分层/材色/未改UV。玩家席只在声明的尺寸假设下连续检查通过；西连接1.4m门双向未通过。**本包不代表30席完整通过、900人运营或整栋最终通过。**

[修订Blend]({P}.blend) / [建筑FBX]({P}.fbx) / [规格与取舍](SPEC.md) / [针对性验收](review.md) / [统一几何](GEOMETRY.json) / [低细度布局](LAYOUT.json)。源可编辑，默认整栋建筑显示、CHECK层隐藏，代理不导出。

{links}

实际局部预览，2560×1440、同原日光约30°；蓝色为明确假设的姿态体，绿色/赭色为有限操作/等候检查层；原PNG只以原字节站立参照出现，切片不是游戏画面：

{images}

900名义格=主468+西连接432，实际占地15.048㎡。旧18m主柜加深新增纠正为1.08㎡，见[两账](AREAS.csv)。唯一推荐取舍为原西连接内门同中心1.4→2.4m；未改实际门，暂停该接口精作交规划。三张凳被移除，换鞋坐凳/真实换鞋流程仍未解决。

[30席状态](SEATS.csv) / [柜列与腔体](CABINETS.csv) / [新旧坐标](COORDINATES.csv) / [变更范围](CHANGE_SCOPE.json) / [图稿依赖](VIEW_DEPENDENCIES.json) / [原生检查](SOURCE_CHECK.json) / [回导检查](FBX_CHECK.json) / [只读输入](protected_inputs.json) / [文件清单](manifest.json)。

原Trial包与旧manifest保持；[原整栋A](../Previews/SL_BLD_C01_MAIN_01_TRIAL_01_A.png)/[B](../Previews/SL_BLD_C01_MAIN_01_TRIAL_01_B.png)仅为原版未受影响外观；[64/32对照](../README.md)沿原实际纹理。复用父Textures48文件，新纹理0。无AI生图/正式动画/UE。

复现顺序：validate_layout.py → check_shoes.py → update_model.py → render_revision.py → verify_revision.py → make_boards.py → SVG按3200×2400栅格化 → make_delivery.py。所有写出只在本修订目录。不要运行原版收尾脚本覆盖原包。验证脚本保留失败证据，未通过西连接门不设置成成功。

RT01待设计不开放；B01/SchoolLife/校门/认可人物保持。交规划及用户针对性审阅后停止，不开展下一阶段。
''')
# Root indexes are append-history documents, preserve their entire earlier contents.
root_updates={
 'README.md':('# 当前回件：C01整栋试作局部修订01 · 2026-10-16\n\n[独立修订源与检查](ArtSource/Buildings/SL_BLD_C01_MAIN_01/Trial01/Revision01/README.md) / [规划回审](Docs/AssetPlanning/BuildingProduction/C01/trial-revision-01-handoff.md)。真实局部网格/Blend/JSON/FBX与3定尺板/7预览已交；玩家席仅尺寸假设下连续通过，30席状态1/6/23分列。900格重排主468+补432，新占地15.048㎡，旧加深纠正1.08㎡。原西连接1.4m门双向未通过，唯一推荐同中心2.4m待判，实际门未改。原包/外观/分层/纹理全保，RT01不开放，无UE；停针对性审阅，不判整栋最终通过。\n\n'),
 'Docs/progress.md':('# C01 Trial01局部修订01实际完成 · 2026-10-16\n\n[修订包](../ArtSource/Buildings/SL_BLD_C01_MAIN_01/Trial01/Revision01/README.md)实交独立Blend/FBX/统一与低细度JSON、3SVG/PNG、7局部原生预览及逐席/柜列/面积/坐标表。2214建筑对象，900真实腔体，2202未改对象指纹保持，零面积/非流形0、实际FBX回导通过。玩家19阶段仅保守尺寸假设通过；6席仅站立、23候选受阻，其余29席姿态未验。旧1.08㎡更正，新15.048㎡。西连接1.4门双向仍失败，2.4建议未落实际模型；换鞋坐凳/抓握/峰值/游戏仍未验。原Trial/B01/校门/SchoolLife保持，停审不最终通过。Git实际结果另记。\n\n'),
 'Docs/execution-plan.md':('# C01 Trial01局部修订01执行记录 · 2026-10-16\n\n起点main/8c1ddb206b654f002577f09607fd6c0f525205f8，读原卡顶部修订/T01–T04/审计与仓库规则，核原3脚本未跟踪、原版指纹。先低细度19连续阶段/30席与900目标双侧操作验证，再只改玩家桌椅、九柜列/三凳移除/照片板位置；原全楼外观/分层/其他UV材质/23班不改。独立版本输出实际源、建筑FBX回导、3板/7局部自然光、统计与依赖。椅把手边接触诊断后改10mm实体搭接，原生拓扑复核0；不是缩代理通过。西连接原1.4门双向失败保留，推荐同中心2.4交规划，不改门/精作该接口。检查保护/一致性后只相关文件错开Git正常同步；停针对性审阅，不接UE或下一阶段。\n\n'),
 'Docs/decision-log.md':('# C01 Trial01局部修订01组内候选及保留冲突 · 2026-10-16\n\n玩家指定5_5，桌+40mm/自己的椅+200mm、拉出625mm，保30/房间/原门/业务恢复点；原人物站立原字节/1.8可见/1.92胶囊分开。完整连续只在明确保守关节/服装包络下通过，其他席不外推。900目标主468/补432改六层开放格候选，双面净2.52=0.70+1.12+0.70，等候六位放补柜东袋；取消原三凳，换鞋坐凳未解。旧主柜新增更正1.08㎡，新15.048㎡另账。西连接1.4内门双向差0.67931m；唯一推荐同中心2.4m（墙门改动待规划），实际源/FBX仍1.4m，蓝框只CHECK。整栋不最终通过，原Trial/Reference/RT01/B01/SchoolLife不改，无新玩法或UE。\n\n'),
 'Docs/handoff.md':('# 当前制作回件：C01整栋试作局部修订01 · 2026-10-16\n\n入口：[独立修订包](../ArtSource/Buildings/SL_BLD_C01_MAIN_01/Trial01/Revision01/README.md) / [规划针对性回审](AssetPlanning/BuildingProduction/C01/trial-revision-01-handoff.md)。真实Blend/建筑FBX/JSON/3板7图及900柜腔/原生回导已完成；玩家19阶段只在明确尺寸假设下通过，其他29席完整姿态未验。900主468/补432，新占地15.048㎡；原加深纠正1.08㎡。原西连接1.4m内门双向仍失败，唯一推荐同中心2.4m交规划，实际门未改、该接口精作暂停；换鞋坐凳与真实动作未解。原版及2202未受影响对象保持。RT01不开放，SchoolLife/B01/校门/人物不改，无UE；停审，不整栋最终通过。Git/LFS实绩收尾另记，原3无关脚本保留。\n\n'),
 'Docs/AssetPlanning/BuildingProduction/README.md':('# 当前制作回件：C01 Trial01局部修订01 · 2026-10-16\n\n[修订包](../../../ArtSource/Buildings/SL_BLD_C01_MAIN_01/Trial01/Revision01/README.md) / [规划回审入口](C01/trial-revision-01-handoff.md)。只改玩家班局部、九柜列/等候与照片板，不重做全楼。1玩家假设连续/6站立/23候选受阻分开；900格、新15.048㎡和旧1.08㎡纠错同步。原西连接1.4门双向仍失败，建议2.4但未改实际模型，接口精作暂停。原包/B01/RT01阶段/SchoolLife保持，停针对性审阅、不判全栋最终通过或UE。\n\n')}
for path,(prefix) in root_updates.items():
 f=R/path;old=f.read_text(encoding='utf-8')
 if not old.startswith(prefix):f.write_text(prefix+old,encoding='utf-8',newline='\n')
handoff=R/'Docs/AssetPlanning/BuildingProduction/C01/trial-revision-01-handoff.md'
handoff.write_text('''# C01 Trial01局部修订01 · 交规划针对性审阅

2026-10-16，制作方回件；不是规划已通过记录。

[回件入口](../../../../ArtSource/Buildings/SL_BLD_C01_MAIN_01/Trial01/Revision01/README.md) / [SPEC](../../../../ArtSource/Buildings/SL_BLD_C01_MAIN_01/Trial01/Revision01/SPEC.md) / [分类验收](../../../../ArtSource/Buildings/SL_BLD_C01_MAIN_01/Trial01/Revision01/review.md)。保原卡/审阅/原Trial字节，独立REV_01实际网格/Blend/JSON/FBX与3板7预览，不是只写文档。

请重点复核：

1. 玩家指定5_5的19阶段连续包络；保自身椅与桌下结构，站立10mm/转向18mm、臀座接触0。没有认可坐姿，仅在完整宽/高的保守尺寸假设下通过。30席1条件连续、6仅站立、23当前候选受阻；其他29席完整姿态/其他23班未外推。
2. 900格主468/西连接432、六层开放格候选与真实腔深/净口，上排静态伸达假设；双操作0.70+公共1.12+0.70、侧袋六等候/柜端路径的有限检查，不是900人运营认证。
3. **唯一推荐固定接口取舍：原西连接同中心(58,13)内门1.4→2.4m**。两人物可见宽需求2.07931m，原门差0.67931m；代价两侧各扩0.5m、约2.6㎡门墙开口。该建议只CHECK，实际Blend/FBX保原门1.4m，真实双向检查失败保留，接口精作暂停。原三外门与主厅3m内廊口不变。三凳被移除，换鞋坐凳/实际换鞋流程未解决，请判断用途取舍，不默认站立储鞋等于换鞋完成。
4. 两本面积账：旧18×(0.66−0.60)=1.08㎡更正，原10.80→11.88；新主7.488+补7.560=15.048㎡，相对原Trial18.18减少3.132㎡。只柜体投影。

原生重开/900腔深射线/零面积非流形0/UV齐全，真实FBX回导2214建筑对象及分组/材质面积/包络检查。2202未受影响对象网格/UV/材料/变换完全保持；其他23班不传播玩家椅修改。全楼未受影响A/B沿原版并明确旧版本，父48纹理原字节复用，新纹理0；CHECK/人物/建议门均不导出。

RT01原588㎡/入口保持待设计不开放；B01、SchoolLife、校门和原人物PNG不改，无UE/新玩法/正式动画。不把局部证据扩为全席、全楼或游戏通过。停止本轮，等规划和用户审阅。Git完整结果见Docs/handoff收尾实绩及制作最终报告。
''',encoding='utf-8',newline='\n')
previews=list((O/'Previews').glob('*.png'));pngs=list((O/'Boards').glob('*.png'))
assert len(previews)==7 and len(pngs)==3
assert all(Image.open(p).size==(2560,1440) for p in previews)
assert all(Image.open(p).size==(3200,2400) for p in pngs)
write('CHECKS.json',dict(protected_inputs=len(read('protected_inputs.json')),protected_changed=changed,low_segments=19,low_passed=19,seat_states=dict(conditional_continuous=1,standing_only=6,current_candidate_blocked=23,other_pose_unverified=29),
 nominal=900,native_cavity_rays=900,native_source_sha256=SC['sha256'],native_fbx_sha256=FC['fbx_sha256'],source_zero_area=SC['zero_area'],source_nonmanifold=SC['nonmanifold'],
 unchanged_objects=2202,actual_link_door=1.4,proposed_link_door=2.4,actual_two_way_passed=False,boards_svg=3,boards_png=3,previews_png=7,whole_building_final_passed=False,game_verified=False))
# Verify repository-local Markdown links in new package and new handoff.
linkbad=[]
for f in list(O.glob('*.md'))+[handoff]:
 for target in re.findall(r'\]\(([^)]+)\)',f.read_text(encoding='utf-8')):
  target=target.strip('<>')
  if target.startswith(('http','#','D:','C:')) or target=='manifest.json':continue # generated immediately below
  if not (f.parent/target.split('#')[0]).resolve().exists():linkbad.append((str(f),target))
assert not linkbad,linkbad
files=[p for p in O.rglob('*') if p.is_file() and p.name!='manifest.json' and p.suffix not in ['.blend1','.pyc'] and '__pycache__' not in p.parts]
write('manifest.json',[dict(path=p.relative_to(O).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(files)])
print('DELIVERY_READY',len(files),'protected',len(read('protected_inputs.json')),'local_links_ok',flush=True)
