# 最新主审阅图：原图底层＋限定修改图层

[限定组稿PNG](../../../ArtSource/MapDesign/V13/SL_WORLD_V13_SCOPED_COMPOSITION_01.png)／[可编辑分层SVG](../../../ArtSource/MapDesign/V13/SL_WORLD_V13_SCOPED_COMPOSITION_01.svg)／[中文标注SVG](../../../ArtSource/MapDesign/V13/SL_WORLD_V13_SCOPED_ANNOTATED_01.svg)／[标注PNG](../../../ArtSource/MapDesign/V13/SL_WORLD_V13_SCOPED_ANNOTATED_01.png)。V12附件作未改底层，只在8个局部图层引用一次AI编辑候选，图层可逐一关闭。其余区域RGB完全一致（核验排除裁切边缘2px抗锯齿）。这不是模型原生整图，1374×1145是SVG原尺寸组稿，不冒称3072达标。AI原图与处理来源完整保留。

为遵守“其他不变”，AI扩大空地/替换背景楼的广场没有整块采纳，仅显示现有门前退界的短停片段；796m²小广场仍在米制规划板比較。井台不移，背景屋不据图拆。关键店门/社区/家身份和PS02正反几何仍以可编辑规划图为准；像素图不足识别的设施不伪标成通过。[范围与处理记录](../../../ArtSource/MapDesign/V13/SL_WORLD_V13_SCOPED_COMPOSITION_RECORD_01.json)。

# 当前有效交付：九项限定编辑

以用户第二张V12附件作直接编辑底图。世界/校园/生活核心/楼门/路线/桥/出口正式几何全部保持。当前审阅图是[限定候选](../../../ArtSource/MapDesign/V13/SL_WORLD_V13_SCOPE_RESTRICTED_01.png)，及[中文可编辑标注](../../../ArtSource/MapDesign/V13/SL_WORLD_V13_SCOPE_RESTRICTED_ANNOTATED_01.svg)／[标注预览](../../../ArtSource/MapDesign/V13/SL_WORLD_V13_SCOPE_RESTRICTED_ANNOTATED_01.png)。前述七初始＋三修订保留为过程稿，不能作为这次限定修改的最终图。新航标与新夜景任务不属于当前变更。

实际原生1374×1145不透明PNG；内置image_gen.imagegen，一次直接编辑，内部模型ID未暴露。原字节在Originals，未放大、拼接或重编码。[实际提示词](prompts/SL_WORLD_V13_SCOPE_RESTRICTED_01.md)／[逐次记录](../../../ArtSource/MapDesign/V13/SL_WORLD_V13_GENERATION_01.json)／[范围说明](latest-scope.md)。



# 澄坂市V13 · 空间一致、功能识别与昼夜生活深化

正式几何沿用V12：19.19008km²/校园360×320m/核心520×400m、31重要及候选楼/29复用用途/112背景、三桥/15出口对/六路线保持。七初始候选＋三次授权定点修订已完成，停审；候选并未全部通过。

- [总平面PNG](../../../ArtSource/MapDesign/V13/SL_WORLD_V13_PLAN_01.png) / [可编辑SVG](../../../ArtSource/MapDesign/V13/SL_WORLD_V13_PLAN_01.svg) / [权威JSON](../../../ArtSource/MapDesign/V13/SL_WORLD_V13_LAYOUT_01.json)
- [板01校园神社](../../../ArtSource/MapDesign/V13/SL_WORLD_V13_BOARD_01_CAMPUS_SHRINE_IDENTITY.svg) / [板02公共站前](../../../ArtSource/MapDesign/V13/SL_WORLD_V13_BOARD_02_PUBLIC_STATION.svg) / [板03海滩河口渔务](../../../ArtSource/MapDesign/V13/SL_WORLD_V13_BOARD_03_BEACH_RIVER_PORT.svg) / [板04比例几何](../../../ArtSource/MapDesign/V13/SL_WORLD_V13_BOARD_04_SCALE_GEOMETRY.svg) / [板05夜景季节](../../../ArtSource/MapDesign/V13/SL_WORLD_V13_BOARD_05_NIGHT_PALETTE_SEASONS.svg)
- [整城初稿](../../../ArtSource/MapDesign/V13/SL_WORLD_V13_CONCEPT_DAY_01.png) / [整城修订](../../../ArtSource/MapDesign/V13/SL_WORLD_V13_CONCEPT_DAY_02.png) / [中文标注](../../../ArtSource/MapDesign/V13/SL_WORLD_V13_ANNOTATED_01.svg)
- [PS02 A修订](../../../ArtSource/MapDesign/V13/SL_CORE_V13_PS02_VIEW_A_DAY_02.png) / [B修订](../../../ArtSource/MapDesign/V13/SL_CORE_V13_PS02_VIEW_B_DAY_02.png) / [A黄昏](../../../ArtSource/MapDesign/V13/SL_CORE_V13_PS02_VIEW_A_DUSK_01.png) / [A夜](../../../ArtSource/MapDesign/V13/SL_CORE_V13_PS02_VIEW_A_NIGHT_01.png) / [海滩](../../../ArtSource/MapDesign/V13/SL_BEACH_V13_VIEW_DAY_01.png) / [神社夜](../../../ArtSource/MapDesign/V13/SL_SHRINE_V13_VIEW_NIGHT_01.png)
- [建筑用途阶段](building-use-phase-index.md) / [公共后勤](public-logistics-cards.md) / [动作状态](public-state-design.md) / [路线](routes.md) / [出口](exits-transport.md) / [变更比较](candidate-change-comparison.md)
- [共享局部](local-sample.md) / [昼夜航路](night-buoy.md) / [参考采用](external-reference-adoption.md) / [实际生成与尺寸](generation.md) / [三层验收](review.md)

原生整城1374×1145，其余1672×941，全部不透明PNG，目标原生尺寸未达，无放大。正式规划/候选视觉/实际游戏分别报告。神社恢复、海滩邻接改善、A昼夜稳定；泉渠/门窗/航标/小桥残留未通过。

最终候选航标M01/M02经过叉积校正；所有图像依据修前AT_GENERATION快照，正式路楼水系不变，修前图板已归档，不将图像反写布局。接续先用户审阅，再另安排局部建模设计；本轮不模型/UE/新系统。
