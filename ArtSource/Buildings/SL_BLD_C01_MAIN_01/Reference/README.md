# C01整栋多视图参考01

2026-10-15。已按用户确认的PLAN_01深化，交规划聊天/用户审阅，停止。B01原状态、Planning原图、已认可校门与SchoolLife只读。没有AI调用、正式模型精修、最终UV纹理或UE接入。

|图页|内容|
|---|---|
|[P01](SL_BLD_C01_MAIN_01_REFERENCE_01_P01.png)|整栋外观、偏西主入口、到达关系|
|[P02](SL_BLD_C01_MAIN_01_REFERENCE_01_P02.png)|完整三层、24班、三入口、访问边界|
|[P02A](SL_BLD_C01_MAIN_01_REFERENCE_01_P02A.png)|同室30/36席、900名义鞋格实排|
|[P02B](SL_BLD_C01_MAIN_01_REFERENCE_01_P02B.png)|公共实排、U梯、原人物门桌栏尺度|
|[P02C](SL_BLD_C01_MAIN_01_REFERENCE_01_P02C.png)|入口集合、北门等候、受控露台与路线|
|[P03](SL_BLD_C01_MAIN_01_REFERENCE_01_P03.png)|同源四立面、窗位/遮阳/材色|
|[P04](SL_BLD_C01_MAIN_01_REFERENCE_01_P04.png)|屋顶、通高庭剖面、RT01原位冲突/候选接近|
|[P04A](SL_BLD_C01_MAIN_01_REFERENCE_01_P04A.png)|入口/梯剖面、孔/顶面/分组接口|
|[P05](SL_BLD_C01_MAIN_01_REFERENCE_01_P05.png)|西南→东北、东北→西南实际30°日光预览|
|[P05A](SL_BLD_C01_MAIN_01_REFERENCE_01_P05A.png)|玩家班、鞋柜、庭、连接剖透预览|
|[P05B](SL_BLD_C01_MAIN_01_REFERENCE_01_P05B.png)|入口近景、32/64px/m表面示意比较|

每页同名SVG可编辑，原生3200×2400，浅色不透明底。预览原生2304×1296，SVG嵌入只作排版；没有放大冒称新原生。四立面、屋顶、平面、剖面和预览都源于[GEOMETRY.json](SL_BLD_C01_MAIN_01_REFERENCE_01_GEOMETRY.json)，[OPENINGS.csv](OPENINGS.csv)提供精确开口表。

[规格与全部接口](SL_BLD_C01_MAIN_01_REFERENCE_01_SPEC.md)／[实际完成与待审](review.md)／[机器检查](SL_BLD_C01_MAIN_01_REFERENCE_01_CHECKS.json)／[指纹](manifest.json)。共享[可编辑参考简模](SL_BLD_C01_MAIN_01_REFERENCE_01_REFERENCE_ONLY.blend)只用于投影和空间检查，WHOLE与CUT_展示副本分开；不作为正式模型交付或UE导入依据。

重制：bundled Python运行build_reference.py→独立Blender 5.2.2 LTS后台运行render_reference.py→再运行build_reference.py嵌入已完成预览→bundled Node/sharp运行rasterize_reference.cjs→check_reference.py。数据/板与预览先后生成，中途编辑几何后必须重制Blender，不以旧预览代入新JSON。

规划需判断：RT01缺126㎡投影承托、坡面/原核/高程/接近方案；30席狭侧道与36席可见人物冲突；900格运营与1.4m入口廊口瓶颈；浅屋面/采光顶/材色及露台8.03面层。用户确认整栋外观关键尺寸后才进入完整试作。Git实际收尾见仓库handoff与最终回件，未预填推送成功。
