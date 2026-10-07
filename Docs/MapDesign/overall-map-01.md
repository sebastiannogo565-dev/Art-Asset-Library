# 澄坂市整体概念地图候选01

更新：2026-10-08。**已生成一张，待用户评价；部分验收未通过。** 不自动重试或增加视角。

## 来源与执行

依据[城市正文](city-design.md)、[校园](campus-design.md)、[美术方向](art-direction.md)、[原始平面](../../ArtSource/MapDesign/city-plan-v02.svg)和[布局JSON](../../ArtSource/MapDesign/layout-v02.json)。[参考SVG](../../ArtSource/MapDesign/OverallMap/SL_CITY_V02_OVERALL_01_REFERENCE.svg)仅局部绕开塔基、压路店屋和家门接路；[参考PNG](../../ArtSource/MapDesign/OverallMap/SL_CITY_V02_OVERALL_01_REFERENCE.png)为3072×2560底图导出。原始V02 SVG/JSON未改。

用户“直接调用生图模型生成”替代FrameRonin浏览器路径。内置image_gen传入同一参考PNG，提交一次，返回一个候选。底层模型版本、任务ID和费用未由工具公开，不猜测。

## 实际文件

|文件|内容|
|---|---|
|[真实原图](../../ArtSource/MapDesign/OverallMap/SL_CITY_V02_OVERALL_01.png)|PNG，1374×1145，RGB/sRGB，无透明，3,836,945字节；与工具返回文件SHA256一致|
|[可编辑标注](../../ArtSource/MapDesign/OverallMap/SL_CITY_V02_OVERALL_01_ANNOTATED.svg)|1514×1335，相对链接同目录原图；地名、北向、图例独立可编辑|
|[带标注预览](../../ArtSource/MapDesign/OverallMap/SL_CITY_V02_OVERALL_01_PREVIEW.png)|1514×1335派生PNG；包含边框与标注，不是第二次生图|
|[实际提示词](../../ArtSource/MapDesign/OverallMap/SL_CITY_V02_OVERALL_01_PROMPT_DIRECT.md)|本次直接模型调用完整提示词|
|[生成记录](../../ArtSource/MapDesign/OverallMap/SL_CITY_V02_OVERALL_01_RECORD.json)|实际格式、尺寸、工具、参考/原图哈希与偏差|
|[历史提示词](../../ArtSource/MapDesign/OverallMap/SL_CITY_V02_OVERALL_01_PROMPT.md)|FrameRonin准备稿，未在网站执行|

**目标约3072×2560未达到。** 保留1374×1145真实原图，未插值充当目标尺寸。原图与预览纳入Git LFS，参考PNG普通Git。

## 验收与偏差

|重点|结论|
|---|---|
|完整性、北向|全城主体未裁切，北坡在上、河在下；主要区域类型可辨识|
|区域位置|校园东北、住宅西南、商店街东南、医院东侧、高端住宅北坡大方向成立，不能认定精确坐标一致|
|铁路、两桥|两桥与两铁路隧道口可见；西穿越口被放到站西，而底图在站东，位置验收未通过；车站向中心/东偏移|
|环路、捷径|隧道北出口、北坡分支和校园接路部分受遮挡；两生活环路与通学捷径连续拓扑未通过核验；标注不补画虚假连线|
|地点身份|玩家家、公共图书馆、社区中心、公交候车处为画面候选识别，仍需确认；公交可见但专用候车棚不明确|
|高差、年代差|河岸低地、校园台地、北坡挡墙/台阶明显；新站前与旧商店街有体量和材质区别|
|地标、避让|青帽塔可辨，道路看起来绕行；净空未工程验证。神社更偏西，北坡支路被树冠遮挡|
|画风、季节|日式二次元屋顶/立面统一；像素纹理偏弱，更接近绘画插画；神社粉色开花树偏离初夏绿叶候选|
|标注、尺寸|地名/北向/图例独立可编辑；原图分辨率低于目标|

绿色圆点表示画面可辨识地点，琥珀菱形表示候选身份；标注不代表批准，也不修复生图布局。

## 接续

交付后停止等待用户评价。先审阅错位穿越口、环路/捷径、设施身份、像素质感和分辨率。未经新指令不重生成，不制作额外视角、V02.1详细剖面、局部深化、模型或UE资产。
