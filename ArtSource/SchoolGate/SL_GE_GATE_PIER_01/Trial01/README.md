# SL_GE_GATE_PIER_01 · 单体试作01

2026-10-13。按[规划任务卡](../../../../Docs/AssetPlanning/SchoolGate/Batch01/TaskCards/SL_GE_GATE_PIER_01_TRIAL_01.md)制作，**试作文件已交付，等待规划窗口/用户审阅**。仅一个门柱源，Design原候选保留；这不是最终材质批准或UE可用资产验收。

[自然昼光A](Previews/SL_GE_GATE_PIER_01_TRIAL_VIEW_A.png) · [自然昼光B](Previews/SL_GE_GATE_PIER_01_TRIAL_VIEW_B.png) · [M1/M2与32/64比较](Previews/SL_GE_GATE_PIER_01_TRIAL_MATERIAL_COMPARE.png) · [实际网格五面及接口检查](Previews/SL_GE_GATE_PIER_01_TRIAL_CHECK.png) · [验收与待判断事项](review.md) · [清单与实际规格](manifest.json)

## 可编辑源与交换文件

- [SL_GE_GATE_PIER_01_TRIAL_01.blend](Source/SL_GE_GATE_PIER_01_TRIAL_01.blend)：Blender 5.2.2 LTS原生源。一个闭合四边面源网格，40顶点、76边、38面、76三角形。`ASSET_SOURCE_ONLY`仅主体；`PREVIEW_ONLY_*`为灯光/人物板/接地参照；独立`VALIDATION_ONLY_2_INSTANCES`场景为两个同数据实例与8×5米平台代理。预览代理不算新资产。
- [SL_GE_GATE_PIER_01_TRIAL_01.fbx](Exports/SL_GE_GATE_PIER_01_TRIAL_01.fbx)：实际二进制FBX，仅`SM_SL_GE_GATE_PIER_01`一个Mesh，76三角面。未导出平台、实例、人物、相机或光源；贴图位于相邻Textures目录。
- [厘米候选几何](../Design/SL_GE_GATE_PIER_01_GEOMETRY.json)是授权轮廓依据；[试作米制几何/UV数据](Source/SL_GE_GATE_PIER_01_TRIAL_GEOMETRY_UV.json)与[重建脚本](Source/build_trial.py)保留可编辑制作方法。材色生成方法见[create_trial_data.py](Source/create_trial_data.py)。

## 尺寸与使用边界

源网格米制**0.6×0.6×2.4m**，等于60×60×240cm；高度台座32、柱身实体191.4＋座浆0.6、压顶16cm。台座/压顶最大60、柱身54；压顶保持每侧3cm出挑、浅四向坡及中央12×12cm顶面。轴心底中心(0,0,0)，+Z上、−Y街侧正面、+X东，位置/旋转为0、缩放为1。

验证组实际测得底轴心(±3.3,0,8)m，两柱最小净口约6m，平台顶8m；道路5m只为沿用宽度参照，没有新道路网格。浮点读数与整厘米目标的误差小于0.00002cm。试作没有在SchoolLife摆放；不能把这些离线检查叫UE通行验收。

南面30×100cm可用区继续仅作注记：Y−27、X[−15,+15]、Z[90,190]cm；没有牌、字、凹槽、孔或基础埋置。V13的1.5×3m历史候选足迹未采用且未回写。

## UV、临时材质与预览

实际1个UV层、6个UV岛、1个共享材质槽。四个侧面用按实际斜长展开的连续条带，顶面/底面各一个岛；实际每三角面面积核对约64px/m。不是用256px图集边长推定密度。

临时[BaseColor](Textures/SL_GE_GATE_PIER_01_TRIAL_BaseColor.png)为256×256 RGB sRGB，[Roughness](Textures/SL_GE_GATE_PIER_01_TRIAL_Roughness.png)为256×256单通道灰度、Non-Color，[UV_LAYOUT](Textures/SL_GE_GATE_PIER_01_TRIAL_UV_LAYOUT.png)为256×256检查图。4px边缘复制，Blender纹理节点Closest采样。没有法线图、AO图或通道打包；这些配置仅本轮试作，不冻结最终通道、图集边长或全城密度。

M1暖灰矿物抹面保宽缓离散色阶、极少短雨痕；M2青灰台座/压顶有少量低对比聚簇。M3座浆带保6mm实体高度但和M1同材，不强画0.384px黑线；0.6×0.5cm滴水槽本轮省略，主要轮廓不变。四张1×1m的32/64样块在Textures/Samples，是对比样块，不另算4个资产或4套正式材质。

A/B为同模型/UV/材质/日光的**真实Cycles渲染**，方位225°/45°、俯角30°、正交、原生1600×1400；原始渲染保存在Previews/Renders，阅读版只加文字和标尺。MATERIAL_COMPARE原生2300×1560，CHECK原生2600×1450；后者五面是实际网格Workbench检查，不能作为自然光证据。

原人物128×128 RGBA直接打包进.blend，原字节SHA256不变。透明可见116px按约180cm独立比例板，192×Ø68cm胶囊高度另标；两向引用同正面PNG不代表已有角色背面八向。比例板采用无照明着色，仅柱体与地面受实际日光照明；这个板不导出。

## 重建与验收方法

在装有NumPy/Pillow的Python运行`Source/create_trial_data.py`；随后用Blender后台、factory-startup、disable-autoexec运行`Source/build_trial.py`。它只在独立进程创建本资产，不加载SchoolLife或用户已有场景。运行`Source/verify_trial.py`独立重开源、回导FBX；运行`Source/assemble_preview_boards.py`加图稿标注。脚本不下载图片或访问外部API。

源文件内三张使用图像（两临时贴图＋原人物）均已打包，便于移动和编辑；FBX旁仍需保留Textures。原人物原路径仅是来源引用。UV/材色源代码和数据均保留，不将贴图阴影或AI概念图冒充模型。

尺寸/闭合网格/UV密度/原人物/13引用指纹/FBX单源与回导顶点及UV核对已通过。美术成品、亚像素运动稳定性、UE过滤/曝光/动态阴影、碰撞/导航/旋转镜头、校牌/墙/基础接口未验。没有冻结LOD、面数预算或复杂碰撞。**交付后停止，不继续其他资产或UE接入。**
