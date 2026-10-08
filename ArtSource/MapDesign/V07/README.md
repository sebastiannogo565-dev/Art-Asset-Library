# V07 源文件与一次生成记录

正文入口：[V07](../../../Docs/MapDesign/V07/README.md)。V02—V06保留。米制布局为权威，生成图有偏差，不能当导航/3D资产。

|前缀/文件|用途/规格|
|---|---|
|SL_WORLD_V06_CALIBRATED_01 SVG/PNG/JSON|新校准对照，非历史测绘；PNG3072×2560|
|SL_WORLD_V07_LAYOUT_01a.json|当前统一世界米制，完整覆盖矩形，局部1:1|
|SL_WORLD_V07_PLAN_01a SVG/PNG|定尺总平面+同尺度旧覆盖紫线，3072×2560|
|SL_WORLD_V07_AREA_01.json|全精度公式/覆盖多边形面积/互斥分项/陆上增量|
|SL_WORLD_V07_HYDROLOGY_01 SVG/PNG|同坐标湖河、源流/分水坡/湖口/汇合/河口，3072×2560|
|SL_WORLD_V07_SECTION_01 SVG/PNG|2条简化候选剖面，2560×1680|
|SL_WORLD_V07_LIFE_ROUTES_01a SVG/PNG|六代表住户同坐标路径，可切换图层，3072×2560|
|SL_WORLD_V07_CHECK_01a / NETWORK_01a JSON|二维足迹/私院/跨水/目标/公交检查，非工程|
|SL_WORLD_V07_REFERENCE_01 SVG/PNG|最终空间参考3072×2560，不重新排城市|
|SL_WORLD_V07_INPUT_01.png|实际生图参考字节快照|
|SL_WORLD_V07_LAYOUT_AT_GENERATION_01.json|实际布局字节快照，原图使用01冻结；当前01a仅修正南公交支线|
|SL_WORLD_V07_PROMPT_01.md / INPUT_RECORD_01.json|实际提示词和冻结输入SHA256|
|Originals/SL_WORLD_V07_CANDIDATE_01.png|一次原生1374×1145 PNG，不透明，原字节|
|SL_WORLD_V07_GENERATION_01.json|真实渠道/模型未知/尺寸/hash/处理记录|
|SL_WORLD_V07_ANNOTATED_01 SVG/PNG|中文功能/27ID/24U/阶段/公交/面积，可编辑3000×2520，原图1:1|
|SL_WORLD_V07_MANIFEST_01.json|文件大小/真实格式尺寸/SHA256，本清单自身不包括|

SVG内文字与功能层可编辑。标注SVG相对引用Originals原图，交付保持目录结构；参考底稿不是AI概念替代品。全部建筑/街道足迹同米制，无校园单独倍率。立面/背面/屋顶/入口多向可见性尚待样板。

渠道为已核验内置image_gen.imagegen，本轮一次调用一个候选，未换服务/批量重试。未返回具体模型、版本、费用或任务ID，字段null。未插值或改PNG原字节，原图实际1374×1145低于目标。标注页大尺寸不等于原生概念达标。

参考来源为本仓库V06最终JSON/建筑索引/用途/住户/交通/偏差，用户本轮指定校准公式，原创V07米制底稿；没有把V06生成额外桥等当正式参考道路，未新增外部建筑奇观。认可角色文件仍未知，保留Q版128×128方向。原图使用冻结01；生成后01a只修正南公交支线沿现有公共路，建筑/道路/水系/面积和实际参考PNG不变。保留LAYOUT_01与LAYOUT_AT_GENERATION_01原数据。实际输入只含最终空间PNG，不含旧概念原图。

模型/UV/环境纹理成品/UE和交通系统均未制作；图稿必要源SVG/JSON保留版本，缓存脚本不提交。原图及大标注PNG精确LFS，其他预览普通Git。交付后停止审阅。
