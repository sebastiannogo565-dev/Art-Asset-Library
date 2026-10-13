# SL_GE_SIGN_PLATE_01 · 载体设计候选01

2026-10-13。用户已转交[规划设计卡](../../../../Docs/AssetPlanning/SchoolGate/Batch01/TaskCards/SL_GE_SIGN_PLATE_01_DESIGN_01.md)，当前**设计交付待审**。计划1独立源、1目标实例；校名字面另算后续图形层。本轮没有模型、UV、最终纹理、正式文字图形或UE产出。

[定尺SVG](SL_GE_SIGN_PLATE_01_DESIGN.svg) · [阅读PNG](SL_GE_SIGN_PLATE_01_DESIGN.png) · [规格](SL_GE_SIGN_PLATE_01_SPEC.md) · [统一厘米JSON](SL_GE_SIGN_PLATE_01_GEOMETRY.json) · [设计核对](SL_GE_SIGN_PLATE_01_CHECKS.json) · [审阅回件](review.md) · [可编辑绘图方法](build_design.py)

推荐24×84cm折边载体，牌体深1cm、含支承总突出2cm，前皮2mm、R4mm转角。比较22×76/26×92，不把30×100可用面当批准牌尺寸。推荐装在左柱南面，接触基准轴心在柱局部(0,−27,140)cm，主体高范围98—182，预留面侧余3/上下余8cm。字面20×76只为空白排布候选。

上下两支座18×2.4×1.6cm＋0.2cm隔离垫，四轴候选为柱局部X±7/Z110和170。所有新数值、左/右选择、材种/材色及固定方式都待审；没有孔径/孔深/承载验收，也没在宿主打孔。

SVG/PNG原生3600×3420，包含正背侧顶、安装正视/侧剖、留边比较、两向30°参照和原人物尺度栏。两方向同几何；东北B图使用明确标注的宿主剖透层，实际不透明柱会遮住南面牌，不代表新增背面牌或宿主材质改变。图为定尺设计与材色示意，非自然光模型渲染/游戏效果。

## 实际参考

- [资产清单](../../../../Docs/AssetPlanning/SchoolGate/Batch01/asset-list.md)、[制作顺序](../../../../Docs/AssetPlanning/SchoolGate/Batch01/production-order.md)、[门柱审阅/接受记录](../../../../Docs/AssetPlanning/SchoolGate/Batch01/review-trial-01.md)：源/图形分离及已接受基准。
- [门柱Trial01索引](../../SL_GE_GATE_PIER_01/Trial01/README.md)、[接受状态manifest](../../SL_GE_GATE_PIER_01/Trial01/manifest.json)、[几何/UV数据](../../SL_GE_GATE_PIER_01/Trial01/Source/SL_GE_GATE_PIER_01_TRIAL_GEOMETRY_UV.json)：本图宿主轮廓来源。旧README“待审”保留原交付历史，当前接受状态以manifest/规划记录为准。
- [宿主.blend](../../SL_GE_GATE_PIER_01/Trial01/Source/SL_GE_GATE_PIER_01_TRIAL_01.blend)、[宿主FBX](../../SL_GE_GATE_PIER_01/Trial01/Exports/SL_GE_GATE_PIER_01_TRIAL_01.fbx)：文件只读字节核对；本轮未重开Blender、未回导FBX，其尺寸采用已接受实际几何数据和既有制作侧测量，未冒称重新读取源拓扑。
- [原厘米设计JSON](../../SL_GE_GATE_PIER_01/Design/SL_GE_GATE_PIER_01_GEOMETRY.json)、[灰盒尺寸依据](../../../../Docs/AssetPlanning/SchoolGate/Batch01/dimensions-and-reuse.md)、[V13正式布局](../../../MapDesign/V13/SL_WORLD_V13_LAYOUT_01.json)：门位/预留/包络/工程尺度；V13大足迹差异保留，不改来源。
- [认可原人物](<D:/UE project/SchoolLife/ArtSource/Characters/StudentChibi/FrontIdle/StudentChibi_Front_Idle.png>)：原128PNG字节嵌入、180可见高/192胶囊另标。SchoolLife仅只读参考。

宿主25原交付指纹在开始时按manifest核对，包含当前manifest、宿主文件及工程/人物引用的41项输入另记录开始时原字节SHA，收尾再次核对保护结果。未覆盖原门柱、Trial01或Design源。

用Python运行build_design.py可从JSON重建SVG；PNG用支持SVG/中文字体的渲染器按原生尺寸导出。本轮没有AI生图或外部图片生成，面明暗只是可编辑设计示意。

紧固/牌材/文字及尺寸等具体待判断项见review。Git实绩由仓库交接和最终报告记录；PNG约0.86MB按小型预览普通Git，无新增LFS二进制。设计交付后停止，认可并另行授权后才发布校牌网格试作卡；SchoolLife只读、UE接入由开发聊天负责。
