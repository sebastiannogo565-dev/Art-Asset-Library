# V06 图稿与真实生成记录

当前正文：[V06审阅索引](../../../Docs/MapDesign/V06/README.md)。V02—V05原文件保留，本目录独立。

|文件|用途／格式与真实尺寸|
|---|---|
|SL_WORLD_V06_LAYOUT_01.json|最终统一布局；世界2700×2150 DU，非米；两个局部候选米制|
|SL_WORLD_V06_PLAN_01.svg / .png|可编辑世界布局／3072×2560定版预览，北向/区域/入口/路网/历史|
|SL_WORLD_V06_LIFE_ECONOMY_01.svg / .png|同坐标生活经济／3072×2560预览；六住户/U用途/后勤供排水独立图层|
|SL_WORLD_V06_REFERENCE_01.svg / .png|同版空间参考／3072×2560，减少标签，不移建筑|
|SL_WORLD_V06_INPUT_01.png|实际输入参考快照，字节与REFERENCE_01 PNG相同|
|SL_WORLD_V06_LAYOUT_AT_GENERATION_01.json|生图时布局字节快照，与最终LAYOUT_01相同|
|SL_WORLD_V06_PROMPT_01.md|实际提示词全文，没有另用未记录提示词|
|SL_WORLD_V06_INPUT_RECORD_01.json|冻结输入/布局/提示词SHA256|
|Originals/SL_WORLD_V06_CANDIDATE_01.png|一次工具原图，1374×1145 RGB PNG、不透明，字节原样复制|
|SL_WORLD_V06_ANNOTATED_01.svg / .png|可编辑名称/功能/27ID/24U/入口/公交/阶段，2880×2200；原图1:1，不放大冒充原生|
|SL_WORLD_V06_GENERATION_01.json|实际渠道/次数/尺寸/格式/未知模型字段/原图SHA256|
|SL_WORLD_V06_CHECK_01.json|二维布局网络/足迹/六住户闭环检查，非工程验证|
|SL_WORLD_V06_MANIFEST_01.json|除本清单自身外，本目录交付文件大小/格式/尺寸/SHA256|

SVG采用可编辑矢量、Microsoft YaHei字体。功能标注SVG通过相对Originals/引用原图；移动交付时保留目录关系。开启/关闭图层可在SVG编辑器中操作，图层ID在源文件；各SVG共用JSON数据。PLAN是正北平面，斜俯原图不可当米制平面或导航资产。

实际入口：内置image_gen.imagegen，沿用V05已核验渠道，一次调用1张。本轮未切换FrameRonin或其它服务、未批量重试。具体模型ID/版本/任务ID/计费没有返回，JSON保留null而非推断。最新认可人物文件仍缺，仅Q版128×128方向，不能声称比例实测。

原图保存日期2026-10-08，目标3072×2560、实际1374×1145。未将JPG改扩展名，未插值/重编码原图。功能标注只添加SVG文字及独立规划定位面板；无法确认的生成建筑不贴重要ID。额外桥/伸海道等偏差见[review](../../../Docs/MapDesign/V06/review.md)，不回写布局。输入冻结后没有改底稿。

本目录没有模型、UV、UE资产、游戏代码或交通功能实现。工具缓存脚本留在忽略.cache/不提交。大型原图和标注PNG按精确路径LFS，其他小PNG/文本普通Git。
