# V12真实生成记录

4个指定任务，各一次，重抽0。入口functions.exec→tools.image_gen__imagegen，沿用项目V08—V11；未切服务，精确模型版本工具不暴露，记录null。完整提示词位于prompts，冻结参考SHA、角色与Gemini快照在源目录JSON。

|输出|请求尺寸|真实原生尺寸/格式|是否达标|
|---|---|---|---|
|SL_WORLD_V12_CONCEPT_01|3072×2560|1374×1145 png|未达；未放大|
|SL_CORE_V12_PS02_VIEW_B|2560×1440|1672×941 png|未达；未放大|
|SL_CORE_V12_PS02_VIEW_A|2560×1440|1672×941 png|未达；未放大|
|SL_BEACH_V12_VIEW_01|2560×1440|1672×941 png|未达；未放大|

顺序整城→B→A→海滩，B不使用A生图，A/B各自同几何方向INPUT。原下载字节保存在Originals，根副本hash相等；中文标注另SVG/PNG，原文件不改。冻结布局SHA dd763c0b33a0f9f7011107db55dd033db66f98d78037a66b3d25bf19d6fe6421，生图后JSON修改0。模型输出额外桥/港/农田/屋面/人物偏差见review，不反向修正式图。

[完整机器记录](../../../ArtSource/MapDesign/V12/SL_WORLD_V12_GENERATION_01.json) / [冻结](../../../ArtSource/MapDesign/V12/SL_WORLD_V12_FREEZE_01.json)。原生不足不是插值后达标；全部不透明，无后期材色改图或其他视角。
