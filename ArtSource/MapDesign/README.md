# 可编辑地图源图 V02

当前交付：[V07源图索引](V07/README.md)，当前01a；冻结01生图，校准/面积/湖河与标注独立保存，旧版本保留。


当前交付：[V06源图索引](V06/README.md)：世界与经济SVG/PNG/JSON、冻结输入、1374×1145唯一原图、功能标注/真实记录；DU非米，历史保留。


当前交付：[V05源图索引](V05/README.md)：示意总图无米制比例尺，两个局部标候选尺度，真实单张原图1374×1145与独立标注；下方历史保留。

## 历史索引（保留）


当前新交付：[V04/文件索引](V04/README.md)。当前01b底稿、一次概念、真实输入快照与可编辑标注分别保存；[V03历史](V03/README.md)及下方V02原文件保留。

本目录保留人工整理的V02源图；OverallMap/新增一张AI整体候选及可编辑标注、派生预览、参考和提示词。无模型或UE资产，待审阅。

|文件|用途|格式/尺寸|
|---|---|---|
|[layout-v02.json](layout-v02.json)|城区占地、道路折点、校园局部坐标和标高候选|UTF-8 JSON；米制概念坐标|
|[city-plan-v02.svg](city-plan-v02.svg)|城市平面、一期/未来区、环路/捷径/视线|SVG，1120×880，可编辑矢量|
|[campus-plan-v02.svg](campus-plan-v02.svg)|校园总平面、入口、流线和楼层关系|SVG，1120×880，可编辑矢量|
|[gate-street-plan-v02.svg](gate-street-plan-v02.svg)|校前街样板局部平面、坡向和视线|SVG，1120×880，可编辑矢量|
|[terrain-section-v02.svg](terrain-section-v02.svg)|河岸至北坡折线观察带高差示意|SVG，1120×720，可编辑矢量；横向非比例|

SVG本身是可编辑源文件，不需要另造不可编辑图片充当源稿。源文件应在支持SVG的浏览器或矢量编辑器打开；字体优先微软雅黑。预览图只用于本轮检查，置于忽略的 `.cache/`，不是认可素材。

## 同一布局约定

城区西南原点，X东Y北；城区SVG采用 `translate(60 748) scale(1.2 -1.2)`，校园采用 `translate(60 720) scale(4 -4)`。样板引用城区(390—550,291—400)上下文，黄色样板观察带为(420—455,291—351)，不移动校园或铁路；边缘构件可能出框，是裁切，不是位置变化。

JSON与SVG都可人工编辑，当前没有自动同步脚本。修改时必须同时核对区域边界、道路折点、校园原点、入口和地标；必要时升版并更新Docs引用。高差图采用多地点折线观察带，不能按它测量实际水平距离、坡度或工程净空。

设计正文：[城市](../../Docs/MapDesign/city-design.md)、[校园](../../Docs/MapDesign/campus-design.md)、[美术](../../Docs/MapDesign/art-direction.md)、[提示词](../../Docs/MapDesign/generation-briefs.md)。


## 整体候选01

[任务与验收](../../Docs/MapDesign/overall-map-01.md) · [真实原图](OverallMap/SL_CITY_V02_OVERALL_01.png) · [预览](OverallMap/SL_CITY_V02_OVERALL_01_PREVIEW.png) · [可编辑标注](OverallMap/SL_CITY_V02_OVERALL_01_ANNOTATED.svg) · [记录](OverallMap/SL_CITY_V02_OVERALL_01_RECORD.json)。原图1374×1145，预览1514×1335；两图使用LFS。SVG须与所引用原图同目录。
