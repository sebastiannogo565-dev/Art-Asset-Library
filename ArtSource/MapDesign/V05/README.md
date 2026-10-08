# V05 图稿与真实生成资料

当前底稿01，继承V04最新01b的27重要ID/功能/阶段。正文入口：[V05总索引](../../../Docs/MapDesign/V05/README.md)。

|SL_CITY_V05文件|用途／尺寸／性质|
|---|---|
|WORLD_01.svg / .png|连续世界示意3072×2560，北向、区界、ID、道路、水系、交通、出口；无米制比例尺|
|TOPOLOGY_01.svg / .png|九区与13对连接，3072×2560；不是UE关卡实现|
|CAMPUS_01.svg / .png|1800×1400导出；校园360×320m候选，南／东门、后门、鞋柜、教室投影与路线|
|CORE_01.svg / .png|1800×1400导出；生活核心520×400m候选，住宅／校前／旧街一期同室外图|
|LAYOUT_01.json|唯一当前布局，明确世界设计DU与两个局部m坐标空间|
|CHECK_01.json|二维足迹／线段／私院／网络／公交顺序／ID用途阶段核验|
|REFERENCE_01.svg / .png|同一最终布局的少文字空间参考，3072×2560|
|INPUT_01.png|实际上传参考字节快照，与REFERENCE_01 PNG哈希一致|
|LAYOUT_AT_GENERATION_01.json|实际生图时布局快照01，生成后没有移动底稿|
|INPUT_RECORD_01.json|参考／布局／提示词SHA256、目标与模型未知字段|
|PROMPT_01.md|真实完整提示词，只调用一次|
|GENERATION_01.json|真实渠道、次数、尺寸、格式、模型未知、原图字节哈希和处理|
|Originals/SL_CITY_V05_OVERALL_01.png|1374×1145 RGB PNG，无alpha；唯一实际原图，低于目标、不裁切／放大／重编码|
|ANNOTATED_01.svg / .png|2400×2160标注页，原图1:1外链；追加规划定位、27功能入口阶段、公交与出口文字|
|MANIFEST_01.json|图稿／布局／输入／提示词／原图的实际字节和SHA256|

标注SVG外链Originals/SL_CITY_V05_OVERALL_01.png，保持相对目录，新检出需git lfs pull。PNG预览由SVG渲染；标注页增大只是新增矢量面板，不能称原图原生2400×2160。图层可分别选择编辑：original_raster、candidate_region_annotations、candidate_readable_landmarks、planned_building_function_index、planned_locations。

区域/少量地标标签仅近似可辨形象；B01–B07与部分校园翼不能逐栋可靠对应，准确功能在独立规划索引/定位图。偏差详见[验收](../../../Docs/MapDesign/V05/review.md)，不反写道路与铁路。

独特模型、复用模块、材质纹理、店招、室内套件、摆放实例后续分开计；本轮无3D/UV/UE资产。停止供审阅，不继续批量生成或建模。

导出复核时调整局部校园/核心SVG水渠层位于底色之上，仅显示层序修正；JSON、世界图、上传INPUT_01与原图未改变。实际生成仍引用冻结01。
