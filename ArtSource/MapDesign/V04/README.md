# SL_CITY_V04 图稿索引

当前布局修订01b，所有名字/历史年代仍候选。可编辑米制JSON/SVG不是导航地图或3D工程资产。文字层独立，可在SVG编辑器修改。

|文件|用途/实际规格|
|---|---|
|[LAYOUT_01.json](SL_CITY_V04_LAYOUT_01.json)|唯一当前坐标；1280×1080m、27重要建筑、46背景、八校园、路/水/区界/入口/历史/公共私院|
|[PLAN_01.svg](SL_CITY_V04_PLAN_01.svg) / [PNG](SL_CITY_V04_PLAN_01.png)|3072×2560定尺总平面，北向/200m尺/ID名称/边界/主线环路/六生长史开关层|
|[CHECK_01.json](SL_CITY_V04_CHECK_01.json)|足迹/路宽带/私院/路线/铁路穿越/整体连通；196节点，30目标可达；未实测项|
|[REFERENCE_02.svg](SL_CITY_V04_REFERENCE_02.svg) / [PNG](SL_CITY_V04_REFERENCE_02.png)|当前布局01b空间参考，3072×2560；未用于额外生图|
|[原图](Originals/SL_CITY_V04_OVERALL_01.png)|一次模型输出PNG RGB/sRGB、不透明，1374×1145，真实下载字节；低于目标|
|[ANNOTATED_01.svg](SL_CITY_V04_ANNOTATED_01.svg) / [PNG](SL_CITY_V04_ANNOTATED_01.png)|2064×1465，可编辑功能对应/北向/图例/偏差层，原图1:1嵌入；SVG须保留Originals相对路径|
|[PROMPT_01.md](SL_CITY_V04_PROMPT_01.md)|目的/用途/参考/数量/规格/背景/命名/验收/下一步及实际英文提示词|
|[GENERATION_01.json](SL_CITY_V04_GENERATION_01.json)|工具、实际格式/原生尺寸/文件字节/hash、处理方法、修订说明；未知模型ID不虚构|
|[REFERENCE_01.svg](SL_CITY_V04_REFERENCE_01.svg) / [PNG](SL_CITY_V04_REFERENCE_01.png)|本次真实上传空间参考快照，3072×2560；保留意外西支跨轨首段，不再用于后续规划|
|[LAYOUT_AT_GENERATION_01.json](SL_CITY_V04_LAYOUT_AT_GENERATION_01.json)|真实生图输入时布局快照，非当前底稿；修订原因见review|

[地图正文](../../../Docs/MapDesign/V04/README.md)。概念位置偏差及原生分辨率不足如实记录；不插值冒充达标。原图与ANNOTATED PNG按现有精确路径规则使用LFS，定尺/参考预览普通Git。
