# C01 PLAN_01源图索引

2026-10-15。8页3200×2400可编辑SVG＋阅读PNG，统一SL_BLD_C01_MAIN_01_PLAN_01.json；本轮是候选规划，不是正式建筑模型或生成效果图。

[完整说明与图页索引](../../../../Docs/AssetPlanning/BuildingProduction/C01/README.md)／[验收](../../../../Docs/AssetPlanning/BuildingProduction/C01/review.md)／[结构化检查](SL_BLD_C01_MAIN_01_CHECKS.json)。

- P01校园关系；P02/P03/P04三层；P05四立面/屋顶；P06剖面/分组；P07通路；P08体量/教室/原人物。
- build_planning.py可重制SVG、JSON和面积/路线表；check_planning.py核数据、XML/PNG规格及只读来源。PNG由本机bundled Node/sharp直接栅格化，无插值放大、无AI调用。
- 原人物PNG只读内嵌data URI、像素邻近显示；没修改原字节。P08是最高屋面包络体块，不是实际坡屋面模型/自然光。
- 29项来源指纹写JSON；B01参考全包及其任务卡/审阅不变，V13正式地图和SchoolLife只读。
- 本輪产出：规划图8套、统一数据/检查/源脚本；正式美术候选/模型/UV/UE均0。字体使用本机Microsoft YaHei/Noto Sans fallback，SVG仍可编辑，无字体文件随库提交。
