"""Compose reading boards, document measured results, protected-input audit and manifest."""
from pathlib import Path
import json,hashlib,math
from PIL import Image,ImageDraw,ImageFont
OUT=Path(__file__).parent;ROOT=Path('D:/Art Asset Library');P='SL_BLD_C01_MAIN_01_TRIAL_01'
def load(n):return json.loads((OUT/n).read_text(encoding='utf-8'))
def write(n,s):(OUT/n).write_text(s,encoding='utf-8',newline='\n')
def js(n,o):write(n,json.dumps(o,ensure_ascii=False,indent=2)+'\n')
G=load('GEOMETRY.json');S=load('STATISTICS.json');N=load('NATIVE_REOPEN.json');F=load('FBX_REIMPORT.json');H=load('HIGH_FREQUENCY_CHECKS.json');HR=load('STAIR_HEADROOM.json')
BUS=H['player_states'][1]['business_distance'];REC=H['player_states'][1]['recovery_distance'];ROUTES=load('MAIN_ROUTES.json');SEAT=load('SEATED_STATIC_CHECK.json')
BOARD=OUT/'Boards';BOARD.mkdir(exist_ok=True);PRE=OUT/'Previews'
fontpath='C:/Windows/Fonts/msyh.ttc'
def font(n):return ImageFont.truetype(fontpath,n)
def board(title,sub):
 im=Image.new('RGB',(3200,2400),'#EEEDE7');d=ImageDraw.Draw(im)
 d.text((60,38),title,font=font(50),fill='#223638');d.text((60,108),sub,font=font(28),fill='#4A6264')
 return im,d
def panel(im,d,key,x,y,w=1510,h=850,label=''):
 p=PRE/(P+'_'+key+'.png');src=Image.open(p).convert('RGB');src.thumbnail((w,h),Image.Resampling.LANCZOS)
 im.paste(src,(x+(w-src.width)//2,y+(h-src.height)//2));d.text((x,y+h+12),label,font=font(27),fill='#223638')
def lines(d,items,x,y,size=29,gap=48):
 for i,s in enumerate(items):d.text((x,y+gap*i),s,font=font(size),fill='#263D3E')
im,d=board('C01 · 整栋 Blender 试作01','真实试作自然光预览 / 2026-10-15 / 不作为游戏内效果证明')
panel(im,d,'A',60,175,label='A 西南→东北 · 30° · 原生2560×1440')
panel(im,d,'B',1630,175,label='B 东北→西南 · 30° · 同一几何 / 同日光')
panel(im,d,'ENTRY',60,1120,label='暖木主入口 · 空白校名带 · 30°')
panel(im,d,'ROOF',1630,1120,label='屋顶辅助75° · 玻璃13.65 / 含框最高13.68m')
lines(d,['150×28m控制 / 3016㎡退进围护足迹 / 52—12—30—12—44m / FL0、4、8m',
 '原三入口、24班、108㎡通高庭、60㎡露台保持；RT01原588㎡只留待设计元数据、不开放。',
 '图板3200×2400为阅读合板；各独立预览保持原生尺寸。'],60,2080)
im.save(BOARD/'01_OVERVIEW.png')
im,d=board('C01 · 玩家教室 / 两椅态与有限尺度','源模型实排30席；36席只沿用冻结参考作比较，不混入本轮建筑或FBX')
panel(im,d,'CLASS_REST',60,175,label='原位 · 门→实际站位→教学前场→原门')
panel(im,d,'CLASS_PULLED',1630,175,label='后拉0.25m · 蓝色坐姿仅为包络候选')
panel(im,d,'FINITE_CLASS',60,1120,label='同镜头30° · 原图可见高1.80m / 胶囊高1.92m、直径0.68m')
lines(d,['已核：指定主线两态净宽约1.1000m。',
 f'业务(45,19.5,4)：家具净距约{BUS:.5f}m。',
 f'恢复候选(45,18.7,4)：净距约{REC:.5f}m。',
 '原人物正面宽1.039655m；窄处单侧仅约30mm。',
 '未通过：不能站立穿过自身椅背完成入座。',
 '组内调整成对距1.06m；静态肩宽余约20mm。',
 '已消静态重叠；需规划审坐姿、动态与其他席。',
 '本轮不改变30席、业务点或230cm交互半径。'],1630,1180,size=31,gap=78)
im.save(BOARD/'02_CLASSROOM.png')
im,d=board('C01 · 900名义鞋格 / 有效腔体与操作冲突','主柜600 + 连接柜300；容量为格数，不是900人集散验收')
panel(im,d,'SHOES_ONE_SIDE',60,175,label='一侧操作检查条件 · 主柜加深后过路余1.24m')
panel(im,d,'FINITE_SHOE_FAIL',1630,175,label='双面 / 前端交叉 / 上排排队冲突 · 橙色操作包络')
panel(im,d,'SHOE_CELL',60,1110,w=1160,h=870,label='实际柜体截取 · 两只290×105×115mm鞋包络假设')
lines(d,['原0.60m总深 → 0.66m候选；主柜面积增加0.54㎡。',
 '有效腔深0.274 → 0.304m；鞋长0.290 + 预留0.010m。',
 '典型有效宽0.288m / 可用高0.263m。',
 '半高滑门净开高约0.138m；五金与上排实际取用未验。',
 '排距2.60m不改，柜间净1.94m。',
 '单侧操作0.70m后余1.24m；双侧余0.54m，未通过。',
 '0.54m < 胶囊0.68m < 人物正面1.039655m。',
 '若保双操作并留1.10m过路：每条柜间距需再增0.56m。',
 '两段间距合计需1.12m，本室柜列余量不能无代价吸收。',
 '前端去回交叉与上排排队支路均未通过，不用“让行”消去。'],1290,1150,size=29,gap=70)
im.save(BOARD/'03_SHOES.png')
im,d=board('C01 · 分组 / 跨层洞口 / 典型楼梯','均由同一试作源渲染；切面为检查展示，不导入FBX')
panel(im,d,'LAYERS',60,175,label='隐藏屋顶、外墙与顶面；各层板与楼梯独立保留')
panel(im,d,'F02',1630,175,label='F02隔离组合 · 三梯支撑仍保留')
panel(im,d,'STAIR',60,1120,label='S1实际楼梯 · 30° · 人物与上下平台比例')
panel(im,d,'COURT_TERRACE',1630,1120,label='108㎡庭洞与60㎡露台 · 完成面8.03 / 围护顶9.23m')
lines(d,[f"三梯：2.20m净跑 / 24级每4m / 踏步0.30m / 半平台2.20m / 实测射线最小头顶净空 {HR['min_clear']:.3f}m。",
 'F02/F03的庭、梯、井洞均在实体楼板与下层顶面核穿通；不是只隐藏板面。',
 '原RT01无新增承托、专梯或可用接近；结构、消防、排水和实际导航未验证。'],60,2080,size=29)
im.save(BOARD/'04_LAYERS_STAIR.png')
im,d=board('C01 · 实际UV / 临时像素密度对照','同1m面、相机与日光；左64px/m、右32px/m / 均为实际PNG材质渲染')
panel(im,d,'DENSITY_64',60,180,w=1510,h=1120,label='64px/m · 256²图块覆盖4×4m')
panel(im,d,'DENSITY_32',1630,180,w=1510,h=1120,label='32px/m · 128²直绘比较图覆盖同4×4m / 同UV与板缝尺度')
samples=load('UV_SAMPLES.json')
for index,s in enumerate([samples[1],samples[2]]):
 x0=60+index*850;y0=1450;w=770;h=650
 faces=s['uv_faces'];pts=[v for f in faces for v in f['uv']]
 lo=[min(v[i] for v in pts) for i in [0,1]];hi=[max(v[i] for v in pts) for i in [0,1]]
 scale=min((w-40)/max(.01,hi[0]-lo[0]),(h-80)/max(.01,hi[1]-lo[1]))
 d.rectangle((x0,y0,x0+w,y0+h),outline='#8EAAA6',width=3)
 for face in faces:
  xy=[(x0+20+(v[0]-lo[0])*scale,y0+h-50-(v[1]-lo[1])*scale) for v in face['uv']]
  if len(xy)>2:d.line(xy+[xy[0]],fill='#5C8991',width=1)
 d.text((x0,y0+h+12),s['object']+' UV采样≤140面',font=font(23),fill='#263D3E')
lines(d,[f"≥1cm²面测量 {N['density_min']:.3f}—{N['density_max']:.3f}px/m。",
 '每面按米投影；坡屋面按斜面实际长度映射。',
 '平铺与复用主动重叠；没有宣称整栋独占UV。',
 '14共享材质；主体42张256² PNG。',
 '另6张128²仅32密度比较；M为外置分区参考。',
 '推荐近处继续64；远处32是否足够待实际镜头验证。',
 '无照片降采样、固定太阳阴影或最终通道承诺。'],1800,1460,size=28,gap=76)
im.save(BOARD/'05_UV_TEXTURE.png')
protection=[]
for v in load('protected_inputs.json'):
 p=Path(v['path']);sha=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
 protection.append(dict(path=v['path'],unchanged=sha==v['sha256'],before=v['sha256'],after=sha))
js('PROTECTED_CHECK.json',dict(count=len(protection),unchanged=sum(x['unchanged'] for x in protection),files=protection))
topology=N['topology'];nonman=[v for v in topology if v['nonmanifold_edges']]
checks=dict(protected_inputs_pass=all(x['unchanged'] for x in protection),protected_count=len(protection),
 native_reopen=True,fbx_actual_reimport=True,fbx_objects_match=F['mesh_objects']==S['mesh_objects'] and not F['missing_names'] and not F['extra_names'],
 fbx_group_names_pass=not F['missing_group_properties'],fbx_uv_present=not F['uv_missing'],
 expected_bbox=[[0,0,-.25],[150,28,13.68]],source_bbox=N['bbox'],fbx_bbox=F['bbox'],
 bbox_max_error=max(abs(N['bbox'][i][j]-F['bbox'][i][j]) for i in range(2) for j in range(3)),
 uv_missing=N['missing_uv'],zero_area_faces=sum(x['degenerate_faces'] for x in topology),
 nonmanifold_source_meshes=len(nonman),nonmanifold_detail=nonman,holes_pass=all(x['slab_clear'] and x['lower_ceiling_clear'] for x in N['holes']),
 headroom_min=HR['min_clear'],headroom_capsule_pass=not HR['below_capsule'],high_frequency=H,main_routes=ROUTES,seated_static=SEAT,
 images={p.name:dict(size=list(Image.open(p).size),mode=Image.open(p).mode) for p in PRE.glob('*.png')},
 note='Static trial evidence only. No gameplay, compliance, structural or crowd claim.')
js('CHECKS.json',checks)
write('README.md',f"""# C01 整栋Blender试作01 · 待规划与用户审阅

2026-10-15。依据已接受Reference/Revision01重新构建整栋试作网格，原6642参考指示未导入或改名。入口、教室、鞋柜与三梯先行复建后完成整栋；固定基准不变。本轮停止于试作回件，不自动进入正式生产或UE。

- [可编辑整栋Blend]({P}.blend) / [建筑FBX]({P}.fbx)
- [整体两向与入口](Boards/01_OVERVIEW.png) / [教室与人物](Boards/02_CLASSROOM.png) / [900格与冲突](Boards/03_SHOES.png)
- [分层与楼梯](Boards/04_LAYERS_STAIR.png) / [实际UV与32/64](Boards/05_UV_TEXTURE.png)
- [规格](SPEC.md) / [三类验收与待判断](review.md) / [尺寸接口JSON](GEOMETRY.json)
- [实测统计](STATISTICS.json) / [原生重开](NATIVE_REOPEN.json) / [实际FBX回导](FBX_REIMPORT.json) / [检查](CHECKS.json)
- [真实纹理清单](TEXTURES.json) / [实际相机](CAMERAS.json) / [保护输入](PROTECTED_CHECK.json) / [回件指纹](manifest.json)

原生整体及主要检查预览2560×1440，密度及鞋格近查1600×1200；阅读合板3200×2400。所有图都是同一试作的渲染或其检查切片，非独立AI拼图。自然光预览、临时纹理检查与实际游戏效果有明确边界。

源默认WHOLE可见；CHECK_ONLY_NO_EXPORT默认隐藏，内有派生切片、原人物及有限代理，按需开关。CONTEXT_NO_EXPORT为日光/地面/相机。FBX只含建筑，不含人物、地面、CUT或代理。模型坐标已保留，不能逐件重置原点。

当前：{S['mesh_objects']}建筑网格对象、{S['unique_mesh_sources']}实际网格源、{S['linked_placements']}共享追加摆放；摆放后三角{S['placed_triangles']}，14共享材质、{S['texture_pngs']}张PNG（主体42＋密度比较6）。无LOD/性能/复杂碰撞定稿。

已测指定主路与业务家具净区；成对距组内改1.06m消除保守静态肩宽重叠，余约20mm。**完整入座、全部座位、鞋柜双面/交叉/队列未通过**。900仅名义格，主柜0.66m是组内试作候选。详情见review，不把失败隐藏在总体验收中。

复现顺序：prepare_trial.py（首次快照）→ Blender build_trial.py → render_trial.py → enhance_checks.py → finalize_mesh.py → verify_trial.py → bundled Python finish_trial.py。脚本仅写Trial01及指定交接文档，原Reference/Revision01/Planning不改。
""")
write('SPEC.md',f"""# SL_BLD_C01_MAIN_01_TRIAL_01 · 实际试作规格

## 依据与坐标

[任务卡](../../../../Docs/AssetPlanning/BuildingProduction/TaskCards/SL_BLD_C01_MAIN_01_TRIAL_01.md)、[规划回审](../../../../Docs/AssetPlanning/BuildingProduction/review-C01-reference-revision-01.md)、[统一修订JSON](../Reference/Revision01/SL_BLD_C01_MAIN_01_REFERENCE_01_REV_01_GEOMETRY.json)。来源SHA与只读输入当前快照见protected_inputs / PROTECTED_CHECK；不重写旧manifest。

米制，根为控制SW(0,0,0)，+X东/+Y北/+Z上，街侧−Y。世界XY偏移(2190.909090909091,1969.181818181818)，工程XY=(x,y+51)，工程Z=z+8。控制150×28m / 实际退进足迹3016㎡，52—12—30—12—44m，3层24班。实体含板底的包络Z为−0.25..13.68，建筑最高相对首层13.68m，不将板底计入批准屋高。

主入口(25,0)净3×3.2，北(90,28)/东(150,14)净3×3；鞋柜厅口(25,8.8)净3×2.6。开放滑门停放在墙内侧，门框在规定净洞以外；不是将门扇埋进实体墙。等候凳为避开主门停放扇组内改位，详见authorized_internal_adjustments。

FL0/4/8，楼板0.25，净顶3.45。教学浅坡5°，玻璃峰13.65/含框13.68；108㎡庭在二/三层板与下层顶面实际同位开洞。电梯井只留2.4×2.4空间及上层洞，无运行系统或承诺井坑构造。露台60㎡，完成面8.03、门底8.03/顶10.63、围护顶9.23/有效1.20。候选槽管保持；未用30mm面层冒充完整排水坡度。

RT01原[38,3,66,24]、588㎡/入口(49,14)/ID独立保留在JSON；没有可用平台、承托或路线几何。462㎡投影不等于可用承托，缺126㎡、旧核及标高语义仍待原阶段设计。

## 高频空间

玩家F2_W4净8.4×9，门(45,12.7)净1.6×2.6，30桌椅。桌面0.45×0.65/高0.72；椅座0.45×0.45/高0.43、椅背顶0.84，后拉0.25。实际主路线双态最小净宽约1.100006m；业务点(45,19.5,4)距家具约{BUS:.6f}；候选恢复(45,18.7,4)约{REC:.6f}。只通过指定站立路线和家具净区，未通过完整入座运动与全部座位可达。蓝色坐姿是有限代理，原人物未变形伪造坐姿。

试作组内将玩家班成对距0.90→1.06，六列Y13.47/14.53/16.67/17.73/19.87/20.93，五排X沿用。保守人物宽1.039655下每对仅余0.020345，两条有人横道净1.100345m。指定席Y19.625→19.87，实际站位Y18.7→18.8；原业务点和恢复候选不动。共享桌腿横向±0.26→±0.29仍在0.65桌宽内，为有限膝部留净区。静态坐姿代理接触面1mm内缩检查见SEATED_STATIC_CHECK，不能据此通过连续运动。其余23班保低深度摆放，未逐席放人物验收。

指定后拉席的坐姿代理大腿/小腿保持原尺寸，向椅侧+X收腿60mm，避开原静态姿态与桌下托盘的相交；这只是有限坐姿候选，不编辑原人物PNG或认定实际角色能完成动作。三条高频室内水平段/平台共{sum(v['stations'] for v in ROUTES['routes'])}采样站，实际WHOLE BVH按0.20m站距、16方位/5高度胶囊截面核对；详见MAIN_ROUTES。楼梯运动、连续扫掠及室外地图不由该结果推定。

认可人物原128²透明PNG字节未改，原图可见1.80m、宽1.0396551724m；独立胶囊1.92m高/直径0.68。原图在门、窄处、转角、座位侧和梯平台检查层使用。全班720席是低深度家具摆放，不增加NPC，不宣称全部可用。

鞋柜主600 + 连接300＝900名义腔体，8柜列逐列见JSON。主柜总深0.60→0.66，连接0.70不变；主柜新增占地0.54㎡，不扩房。共享背板12mm、隔板/层板12mm，前部候选16mm厚上固定片与6mm下滑片，板边作为导向候选；有效腔宽0.288/保守可用高0.263/主柜深0.304m（实体前后内净约0.308，再留4mm安装空间）。门开高约0.138。导向槽、止退及运动公差未精作，不将候选薄片当成熟五金。

鞋假设每只290×105×115mm、成对宽235mm、深预留10mm。旧有效深0.274不通过，新0.304在该静态假设下余4mm；实际鞋型、包和全尺寸适配未验。实际开格截取及鞋包络见SHOE_CELL，不是900块实心面板冒充鞋格。上排底1.20m/把手约1.328m，实际伸取未验。

主柜排距2.60、柜间1.94；单操作0.70后余1.24，双操作余0.54失败。若双操作+1.10净路，每条排距需3.16，即每间隔+0.56；三排两间隔累计+1.12m，不能在本室不动其他接口就声称解决。前端交叉与上排队列也未通过。

三梯：每层24级/4m，每跑12级、11踏面×0.30，净跑2.20；孔4.7×5.5，半平台2.20深，层平台约2.40深。扶手在净跑外侧，高1.10。实体射线最小头顶净空{HR['min_clear']:.4f}m，见STAIR_HEADROOM。该静态采样不替代规范/导航/拥挤验证。

## 分组与制作深度

ROOF / EXTERIOR / SLAB_F01–03 / INTERIOR_F01–03 / STAIR_CORE_S1–S3。另列PARTITIONS_F01–03和CEILING_F01–03供遮挡隐藏。全部共坐标，梯和平台不会随楼层或屋顶隐藏带走。SHOW层保原点，不含从工程迁来的资产。

全壳体、四面真实开窗及遮阳、屋面、三入口/房间门窗、廊/梯、庭和露台完成试作；玩家班、鞋柜、主要公共陈设优先。其余23班使用链接桌椅低深度复制，管理/卫生/辅助室只放用途需要的低深度块体。没有全楼精装承诺。内部正交组合去除重叠体和共面内表面；共面网格分割已做合并，最终拓扑仍供后续精作评估。

## UV与实际纹理

14共享建筑材质，主体42张256×256 PNG：BC/R/M各14。BC与R实际接节点并打包；M是外置材质分区参考遮罩，未强行冻结最终通道。另有墙/入口木/地板的BC/R共6张128²直绘比较图，保持相同4m物理花纹与UV，只将密度改为32px/m。共{S['texture_pngs']}张外置PNG可定位，主体28张节点图像、比较6张和原人物打包；不是环境图统一128²，也不改变UV来放大板缝冒充纯密度对照。

面积≥1cm²面的实际投影密度{N['density_min']:.3f}..{N['density_max']:.3f}px/m（单精度误差），每面按实际米长映射、坡面按斜长。更小接头片的浮点测量全范围保留在NATIVE_REOPEN.density_measurement，不据此冻结正式精度；所有面的UV存在性与拓扑均检查。阅读板的代表UV采样每源前140面，不是全栋独占布局。平铺/链接实例有意重叠，不宣称整栋唯一烘焙UV。克制色阶、少量板缝/磨损，无摄影降采样或固定太阳投影；玻璃用透射与粗糙度，无自发光补亮。近处先64，远处32只作为同镜头对照建议，实际UE镜头待验。

## 交付和检查界限

建筑对象{S['mesh_objects']}，独立网格源{S['unique_mesh_sources']}，共享追加摆放{S['linked_placements']}；源顶点{S['source_vertices']}/三角{S['source_triangles']}，摆放顶点{S['placed_vertices']}/三角{S['placed_triangles']}。建筑材质14，不包含CHECK代理材质；统计不含地面/相机/人物/CUT。实际数据见STATISTICS，不冻结预算。

FBX以米、−Y Forward/Z Up，展开共享实例；回导{F['mesh_objects']}建筑对象，名称及group自定义属性保留，最大坐标偏差{checks['bbox_max_error']:.8f}m。FBX只承载网格、UV、材质和基础图像链接；Blender玻璃/节点效果不能视为UE材质。源文件打包图像，外置纹理目录同时交付。

整体A225°/B45°方位、30°俯角，同日光/AgX；局部主查30°，层拆40°、屋顶75°为辅助并明标。原生大小/相机逐张见CAMERAS，阅读合板为缩排。没有宣称UE或最终光照通过。

源重开/真实FBX回导、UV/零面积面/洞口/射线与有限代理、保护输入核对见检查记录。结构锚固、防水排水、消防、电梯、全席姿态/恢复/导航/八向镜头/高峰人群/性能/LOD/复杂碰撞均未完成游戏或工程验收。
""")
write('review.md',f"""# C01 Trial01 · 交规划审阅

2026-10-15。停止于完整建筑试作。没有自动正式精修、UE导入、下一栋或游戏系统开发。

## 试作已验证

- 新建完整外壳/三层/24班/廊/三梯/庭/露台和复用家具，未导入原参考Blend；固定尺寸、三入口、坐标标高保持。
- [实际源重开](NATIVE_REOPEN.json)及[FBX回导](FBX_REIMPORT.json)：{S['mesh_objects']}建筑对象、分组属性/UV/材质可追溯；外廓150×28、最高13.68，回导误差约{checks['bbox_max_error']:.8f}m。
- F02/F03庭、三梯和电梯井的实体板/下层顶面洞口逐点穿通；源中楼层与屋顶独立隐藏，梯平台保留。三梯射线最小头顶净空{HR['min_clear']:.3f}m（静态采样）。
- 主30席两态指定站立主路1.10m、原业务家具净距{BUS:.5f}m；恢复仅候选{REC:.5f}m。成对距1.06m消除原0.14m静态肩宽重叠，余约20mm；完整入座段不计站立路线通过。
- 指定后拉态静态坐姿代理三角表面相交数：{sum(v['triangle_surface_intersections'] for v in SEAT['results'])}（接触面内缩1mm、收腿60mm、不改变代理尺寸）；三条室内路线{sum(v['stations'] for v in ROUTES['routes'])}采样站/阻塞{sum(len(v['blocked_stations']) for v in ROUTES['routes'])}。这些是有限静态检查，未把它们等同完整运动或导航。
- 900真实名义腔体复算；对假设鞋长290mm，新主柜保守有效深304mm，旧274mm失败。新深度只为候选，不认定通用鞋、包或五金。
- 实际UV、14共享材质/{S['texture_pngs']} PNG（42主体＋6比较）、64/32同镜头同物理花纹/UV对照。零面积面{checks['zero_area_faces']}；非流形网格源{checks['nonmanifold_source_meshes']}，详见CHECKS而非隐去。
- {len(protection)}项当前只读输入SHA核对。SchoolLife、人物原图、B01、校门及Reference/Revision01/Planning不改。

## 未通过或待取舍

1. **完整入座未通过**：原人物无获认可坐姿，静态蓝色代理不能证明连续关节运动；终点有自身椅子，站立胶囊不能穿背。组内将成对距0.90→1.06，原图保守宽1.039655下消除静态重叠，但两席仅余20mm；站位(46.425,18.8)与席Y19.87为试作家具候选，原恢复点/业务点不改。指定通道单侧仅约30mm，不能称全部30席舒适可达；背景23班未逐席核。
2. **鞋柜双操作未通过**：加深0.06m后，单操作余1.24m，双操作仅0.54m。维持两操作0.70+1.10路需每间隔+0.56、两间隔+1.12m；当前室内纵向余量不足，不擅自减格/扩房。0.66m主柜新增占地0.54㎡，门轨/上排伸取/公差仍候选。
3. **交叉/队列未通过**：y1.375前端到达/离开包络相交；22.9/6.2、22.9/7.9上排等候占用柜端支路，不以“让行”判断通过。不能据900格总数接受高峰运营。
4. 露台门底/围护/槽管几何同步，但排水坡/防水/结构与锚固未验；电梯井只留空间。RT01原588㎡不开放，承托、旧核和标高冲突未解决。
5. 当前网格和纹理是试作深度。非流形统计、玻璃暗部、重复平铺和中远景可读性供审阅；没有LOD、规范、最终材质或性能认证。

## 游戏内未验证

UE导入/材质、有限角色八方向镜头与遮挡、全部席入座离席动画、业务交互及230cm半径、恢复点、寻路、三条日常路径耗时、碰撞、拥挤/等待、NPC容量与性能全部未验。未开发相关系统，也未修改SchoolLife。

## 规划窗口需要判断

先审实际整体外观/入口/分层，再判断：组内成对距1.06/玩家席Y19.87/站位Y18.8候选及仅20mm余量能否接受；主柜0.66m候选是否继续，以及900格与双面操作/支路容量的整体取舍。固定基准没有暗改，未受影响全栋已交齐；不代用户或规划宣布通过。
""")
js('AUTHORIZED_ADJUSTMENTS.json',dict(changes=G['authorized_internal_adjustments'],fixed_baselines_changed=False,protected_inputs_modified=False))
write('SOURCE_MAP.md',"""# 来源与试作对应

|来源|用途|处理|
|---|---|---|
|Reference/Revision01 GEOMETRY.json / OPENINGS.csv|控制、房间、开口、桌椅位置、标高、材色|只读参数输入；不导入primitives或参考Blend|
|任务卡与最新针对性审阅/审计|前段验证、完整建筑、停止点|保固定接口，失败量化|
|原人物FrontIdle PNG|门、家具、楼梯尺度|原字节打包检查层，不进建筑FBX|
|build_trial.py|真实网格源、实例与分组|正交实心并集、真实洞口、桌椅源/柜腔/闭合阶梯轮廓|
|prepare_trial.py|临时像素图|原创程序绘制、少量色阶接缝，无AI/照片|
|render_trial.py / enhance_checks.py|同栋自然光、有限包络、实际柜格截取|CUT/人物/代理独立默认隐藏，不进FBX|
|verify_trial.py|重开与实际回导、静态净区|不以二维/静态代理代替UE结论|

36席仅保留在冻结参考中的对照，不在Trial建筑或导出中复制。原RT01仅元数据待设计，没有假接近或承托模型。其他来源SHA逐项见protected_inputs和PROTECTED_CHECK。
""")
# Four handoff documents and current indexes are updated only after artifacts/checks exist.
entry=f"""# C01整栋Blender试作01实际回件 · 2026-10-15

[试作包](../ArtSource/Buildings/SL_BLD_C01_MAIN_01/Trial01/README.md) / [三类验收](../ArtSource/Buildings/SL_BLD_C01_MAIN_01/Trial01/review.md)。已按用户转交整栋卡重建真实网格、实际UV/临时纹理、自然光、FBX并真实回导；{S['mesh_objects']}建筑对象、{S['unique_mesh_sources']}网格源，原参考不改名。指定主路/业务净区通过静态核；完整入座/并排坐姿、鞋柜双面/交叉/队列未通过。主柜0.60→0.66m仅组内候选，900名义格保持。

原Reference/Revision01/Planning、SchoolLife/B01/人物/校门只读，{len(protection)}输入指纹核过；RT01588㎡不开放。停止供规划与用户审阅，无正式精修/UE/下一栋。实际Git/LFS结果正常同步收尾另记，原3无关脚本保留。

"""
for n in ['progress.md','handoff.md','decision-log.md','execution-plan.md']:
 p=ROOT/'Docs'/n;old=p.read_text(encoding='utf-8')
 if not old.startswith('# C01整栋Blender试作01实际回件'):p.write_text(entry+old,encoding='utf-8',newline='\n')
for path,link in [(ROOT/'README.md','ArtSource/Buildings/SL_BLD_C01_MAIN_01/Trial01/README.md'),(ROOT/'Docs/AssetPlanning/BuildingProduction/README.md','../../../ArtSource/Buildings/SL_BLD_C01_MAIN_01/Trial01/README.md')]:
 old=path.read_text(encoding='utf-8')
 if not old.startswith('# 当前回件：C01整栋Blender试作01'):
  path.write_text(f"# 当前回件：C01整栋Blender试作01 · 2026-10-15\n\n[真实试作、预览与验收]({link})已完成待规划审阅。入座/并排肩宽、900名义格双面操作及交叉队列有未通过项，未伪造整体通过；RT01不开放，B01/SchoolLife不变。不自动正式精修或UE。以下保留历史。\n\n"+old,encoding='utf-8',newline='\n')
# Manifest excludes itself; text LF normalized so Git checkout conversion does not invalidate assets.
files=[]
for p in sorted(OUT.rglob('*')):
 if not p.is_file() or p.name=='manifest.json' or p.suffix=='.blend1' or '__pycache__' in str(p):continue
 data=p.read_bytes()
 if p.suffix in ['.py','.md','.json','.csv','.svg','.cjs']:data=data.replace(b'\r\n',b'\n')
 files.append(dict(path=p.relative_to(OUT).as_posix(),sha256=hashlib.sha256(data).hexdigest(),bytes=len(data)))
js('manifest.json',dict(asset=P,text_normalization='LF',files=files))
print('DELIVERY',len(files),'protected',sum(v['unchanged'] for v in protection),'/',len(protection),'nonmanifold',len(nonman))
