# B01玩家家 · 完整住宅参考01

2026-10-14。完成用户授权参考，停审；正式模型/UV/纹理/UE=0。1套候选，五页原生3200×2400 SVG/PNG共用尺寸及门窗表。

|页|阅读PNG|编辑SVG|
|---|---|---|
|P01 总平面 / 面积 / 人物|[PNG](SL_BLD_B01_HOME_01_REFERENCE_01_P01.png)|[SVG](SL_BLD_B01_HOME_01_REFERENCE_01_P01.svg)|
|P02 两层平面|[PNG](SL_BLD_B01_HOME_01_REFERENCE_01_P02.png)|[SVG](SL_BLD_B01_HOME_01_REFERENCE_01_P02.svg)|
|P03 四立面|[PNG](SL_BLD_B01_HOME_01_REFERENCE_01_P03.png)|[SVG](SL_BLD_B01_HOME_01_REFERENCE_01_P03.svg)|
|P04 屋顶 / 入口及楼梯剖面 / 分组|[PNG](SL_BLD_B01_HOME_01_REFERENCE_01_P04.png)|[SVG](SL_BLD_B01_HOME_01_REFERENCE_01_P04.svg)|
|P05 相反两向30° / 材色|[PNG](SL_BLD_B01_HOME_01_REFERENCE_01_P05.png)|[SVG](SL_BLD_B01_HOME_01_REFERENCE_01_P05.svg)|

[规格与面积/接口](SL_BLD_B01_HOME_01_REFERENCE_01_SPEC.md) · [尺寸JSON](SL_BLD_B01_HOME_01_REFERENCE_01_GEOMETRY.json) · [图面检查](SL_BLD_B01_HOME_01_REFERENCE_01_CHECKS.json) · [规划回件](review.md) · [指纹](manifest.json) · [可选AI请求](AI_REFERENCE_REQUEST.md)

原18×18是正式建筑足迹，不是院落：单层324/两层满铺648m²。推荐9×10普通两层住宅：毛180、房间/走道净143.192、含首层梯投影净150.805m²；正式足迹324→90/体量中心仍须规划批准。保原门点/yaw20/两层/Home与首层0；候选门框1.6×2.3、活动口1.2×2.1对原型2.4为待审差异。

共同入口底轴心；ROOF/EXTERIOR/INTERIOR_F01/F02归属明确，外墙双面不重复，楼梯/板洞同位。内部门窗檐管整栋处理。必要生活/睡眠空间先安排，不增加NPC/玩法。84保护SHA不变，原人物180/192分列。

图面检查通过：净房间不交叠、门连接图覆盖两层及后勤口、22外洞口对应房间/立面、屋顶/层高公式与相反两向一致。P05是向量体量/光向示意，非真实模型日光。门口/人物视觉宽/梯/镜头/导航/工程/地界/最终材色未驗。

复现：Python build_reference.py读取缓存或本JSON内source_basis；Node rasterize_reference.cjs读取sharp（可由NODE_PATH指定bundled模块）；Python check_reference.py。人物路径只读，无AI或正式模型文件。

仅此参考和交接正常Git，与规划错开，实绩收尾后记录。参考通过且用户确认外观/关键尺寸后，才一次整栋试作，不自动下一栋。
