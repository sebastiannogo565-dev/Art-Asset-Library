# 尺寸依据、差异与复用核对

2026-10-13，只读文件核对，未调用UE/Blender、未测量实时Actor、未修改工程。V13几何决定城市位置/校园边界；本轮用户要求局部资产优先适配已建灰盒施工尺寸。生成整图不提供尺寸。

## 依据优先级

1. 已建灰盒：[Step2/ActorRecipe.json](<D:/UE project/SchoolLife/Docs/Validation/LifeCoreBlockout/Step2/ActorRecipe.json>)内LC2_Gate_*变换；[prepare_geometry.py](<D:/UE project/SchoolLife/Docs/Validation/LifeCoreBlockout/Step2/prepare_geometry.py>)对dim/100缩放的解释；[2026-10-12保存重开与通行/镜头历史报告](<D:/UE project/SchoolLife/Docs/Validation/LifeCoreBlockout/Step2/Observations.md>)。这是本次读到的施工证据，不是本次重新跑的UE验收。
2. 工程坐标：[Step1/Plan.json](<D:/UE project/SchoolLife/Docs/Validation/LifeCoreBlockout/Step1/Plan.json>)的GATE01入口与origin_world_xy_m；[V13正式JSON](<D:/Art Asset Library/ArtSource/MapDesign/V13/SL_WORLD_V13_LAYOUT_01.json>)／[正式平面SVG](<D:/Art Asset Library/ArtSource/MapDesign/V13/SL_WORLD_V13_PLAN_01.svg>)的campus.world_gate与gate_design。概念图只作氛围，无尺寸权威。
3. 人物：[认可原生128×128 PNG](<D:/UE project/SchoolLife/ArtSource/Characters/StudentChibi/FrontIdle/StudentChibi_Front_Idle.png>)及[历史导入记录](<D:/UE project/SchoolLife/Docs/Validation/StudentChibiFrontPreview/ImportedAssets.json>)。原图已直接查看：黑发、深蓝制服、白衬衫、酒红领带、灰裤黑鞋Q版。PNG原字节不改；当前约1.8m可见高只作设计参照。灰盒胶囊直径68cm/总高192cm与人物可见高分开，不能缩人物/门口来掩盖尺度。

## 施工数值

| 对象 | 记录尺寸/位置（cm） | 解释/状态 |
| --- | --- | --- |
| 局部原点 | world(2190.909090909091,1918.181818181818)m | X东/Y北/Z上；1m=100UEcm；保持校园360×320m/核心520×400m |
| 单柱 | 60×60×240；旧基本体中心(−330,0,920)或(+330,0,920) | 底面Z800、顶面1040；单一正式源复用2次；不是30×30×110的家院门柱 |
| 门口 | 内面X−300/+300 → 净600 | 5m通学/校内路居中；无横梁，现状开放 |
| 平台 | 800×500×20；中心(0,200,790) | 顶Z800，X[−400,400]、Y[−50,450]；保持范围不新加共面层 |
| 接近道路 | LC2_Road_R1_05、LC2_Road_R2_00均500名义宽 | 原折线、道路每端40cm覆盖保持；接触段不是全部街区新资产 |
| 地面高差 | 住宅0/校门和校园800；Z=clamp((Y+14000)×800/14000,0,800) | 灰盒连续候选坡面，约5.71%；保留，不新加坡/楼梯或改高度 |
| 局部未知 | 校牌尺寸/挂点；墙线/截面；路缘/排水/补边包络 | 读到的文件没有足够数据，必须待核；不按图片估成固定值 |

## V13门柱足迹与已建灰盒的差异

V13门柱左右矩形足迹各1.5×3m，左中心相对门点(−3.75,+1.5)m、右(+3.75,+1.5)m；两内侧仍相距6m，未给可直接采用的完整单柱高度。灰盒是0.6×0.6m柱、相对中心(±3.3,0)m、高2.4m。两者不能混成同一尺寸。

本批采用已建灰盒的60×60×240cm作门柱设计约束；V13世界/校园/门点/净6m通路保持。该差异单列，不改V13 JSON，不擅自用1.5×3m规划矩形扩大网格。若后续用户选择更大门柱，先重新比平台、开口、地界与道路，再授权调整施工，不在本卡里暗改。

## 已有资源与复用深度

| 来源 | 实际可复用 | 不能据此声称 |
| --- | --- | --- |
| CampusLifeBlockout.umap | 文件存在；平台/道路/双柱位置与标高可据记录沿用 | 没有现场读取当前Actor；二进制文件存在不等于所有源网格已提取 |
| MI_BlockoutGround/Path/Wall/Prop.uasset | 四文件存在，可占位/参考材质命名和槽位 | 灰盒颜色不是获认可的像素环境纹理；未读取材质图，不套人物导入设置给环境 |
| Art Asset Library / SchoolLife已查模型目录 | 未找到校门门柱/校牌/路缘对应的blend/fbx或SM_专用源 | 不断言引擎或全部外部库没有任何通用模型；没有可确认的正式门柱复用源 |
| 其他灰盒物件 | Rest_Bench160×60×90cm只能作校内占位参考；家院门柱30×30×110cm不能当校门柱 | 不搬现有校内家具/家院门柱到门口；不把相同基本体实例算独特源 |

## 引用文件指纹

用于后续聊天发现来源变化，非把文件复制进美术库。读取日期2026-10-13，当前文件一致性不代表重新做历史运行验收。

| 参考 | SHA256 |
| --- | --- |
| [v13](<D:/Art Asset Library/ArtSource/MapDesign/V13/SL_WORLD_V13_LAYOUT_01.json>) | 20149b825e420c885ce80468da052067caddc46e9663128471538be047518e72 |
| [svg](<D:/Art Asset Library/ArtSource/MapDesign/V13/SL_WORLD_V13_PLAN_01.svg>) | eb7af2e9b15c08a4b8d4d6642a0cbb757b687229329719cb78f571fc792e32a1 |
| [step1](<D:/UE project/SchoolLife/Docs/Validation/LifeCoreBlockout/Step1/Plan.json>) | 69b9d71e299f5e3f4dec5da370dd77c28c9109ea3a23a28d6ad436ceee205db8 |
| [recipe](<D:/UE project/SchoolLife/Docs/Validation/LifeCoreBlockout/Step2/ActorRecipe.json>) | 68225f5fd79bb471495b176ed50b7be518ffde19af9b442bf92158bf9b77f146 |
| [observations](<D:/UE project/SchoolLife/Docs/Validation/LifeCoreBlockout/Step2/Observations.md>) | 89e3ff5068e32a2742dcbe88117c34c768a271109a5f66fafa48e9ebb9a170fd |
| [calc](<D:/UE project/SchoolLife/Docs/Validation/LifeCoreBlockout/Step2/prepare_geometry.py>) | 69ffd3785f466b8875b07eeeb5e6c08b124c71b0adfd1b2b60d9983ca3d600df |
| [character](<D:/UE project/SchoolLife/ArtSource/Characters/StudentChibi/FrontIdle/StudentChibi_Front_Idle.png>) | 082ceb410d904f0037dfe09dd3502e50195351691ab4047cc5dbbb639147b8cd |
| [charRecord](<D:/UE project/SchoolLife/Docs/Validation/StudentChibiFrontPreview/ImportedAssets.json>) | 07ba6a55a9502969a0d55a56136d80871b348dda17b05b25c7de21fdb9d58520 |
| [map](<D:/UE project/SchoolLife/Content/SchoolLife/Maps/CampusLifeBlockout.umap>) | 44fdd13420290da7d2d3f094ad7c0823a65cc1285a21dd613dacd3179d40455f |
| [wall](<D:/UE project/SchoolLife/Content/SchoolLife/Blockout/Materials/MI_BlockoutWall.uasset>) | d2562ab74154902c8c74ed456e4f986d55a1f42316b12ad86610f7044546ac0c |
| [ground](<D:/UE project/SchoolLife/Content/SchoolLife/Blockout/Materials/MI_BlockoutGround.uasset>) | e523fe034d85e9f378094d78040da34828532a1af961ccfb59e4e01d840806fb |
| [road](<D:/UE project/SchoolLife/Content/SchoolLife/Blockout/Materials/MI_BlockoutPath.uasset>) | 6a31436e9cc4b9684eedfae4ea296fb5887f608ace952b1598ebe2ec546faf1b |
| [prop](<D:/UE project/SchoolLife/Content/SchoolLife/Blockout/Materials/MI_BlockoutProp.uasset>) | ed03280ba5b9ea85f40b059c8c6364acda2891a2ee84d77f172653b0e67fd7fd |

需要接续核对的部分：现场实际门柱/平台若与记录不同，以差异表回报；局部地形缺口边界；校牌名称与载体尺寸；校墙有无/接点；道路边缘是否确需路缘及排水去向。它们不阻塞本轮规划表，但会阻塞对应条件资产开工。
