# SL_CITY_V03 01 文件索引

V03首次建立，1280×1080m候选，北上；旧V02不覆盖。全部结果等待审阅。

|文件|用途/规格|
|---|---|
|[LAYOUT_01.json](SL_CITY_V03_LAYOUT_01.json)|唯一布局数据：区域、道路、入口、校园、占地、阶段、标高、路线和背景统计|
|[PLAN_01.svg](SL_CITY_V03_PLAN_01.svg)|定尺总平面，可编辑，3072×2560，图内1.8px/m；北向、比例尺、区界、路径与建筑ID|
|[PLAN_01.png](SL_CITY_V03_PLAN_01.png)|一张定尺预览，3072×2560，不透明；SVG确定性渲染|
|[REFERENCE_01.png](SL_CITY_V03_REFERENCE_01.png)|本次生图实际参考，地图区域裁切等比适配3072×2560；无游戏模型含义|
|[Originals/OVERALL_01.png](Originals/SL_CITY_V03_OVERALL_01.png)|一次生图的真实PNG，1374×1145、不透明，未插值；LFS|
|[ANNOTATED_01.svg](SL_CITY_V03_ANNOTATED_01.svg)|同图可编辑名称/功能/北向，2034×1345；相对引用Originals/原图，须保留目录关系|
|[ANNOTATED_01.png](SL_CITY_V03_ANNOTATED_01.png)|派生标注预览，2034×1345、不透明；LFS，非第二次生图|
|[PROMPT_01.md](SL_CITY_V03_PROMPT_01.md)|实际发送完整提示词|
|[GENERATION_01.json](SL_CITY_V03_GENERATION_01.json)|实际工具、模型公开程度、尺寸/哈希、参考和处理方法|
|[CHECK_01.json](SL_CITY_V03_CHECK_01.json)|二维占地/道路/入口/路线检查，非3D验收|

[设计正文](../../../Docs/MapDesign/V03/README.md) · [建筑索引](../../../Docs/MapDesign/V03/building-index.md) · [偏差](../../../Docs/MapDesign/V03/review.md)。将来修改布局要追加版本并同步JSON/SVG/索引，不能依据模型偏差搬动原布局。
