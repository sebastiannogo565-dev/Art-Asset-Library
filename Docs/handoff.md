# 交接入口

更新：2026-10-08。当前成果：**澄坂市V04布局01b与一次概念候选01，等待用户审阅。**

## 阅读入口

1. [V04总索引](MapDesign/V04/README.md) · [历史骨架与修改](MapDesign/V04/history-and-revisions.md)。
2. [定尺总平面](../ArtSource/MapDesign/V04/SL_CITY_V04_PLAN_01.png) · [可编辑SVG](../ArtSource/MapDesign/V04/SL_CITY_V04_PLAN_01.svg) · [唯一当前布局JSON](../ArtSource/MapDesign/V04/SL_CITY_V04_LAYOUT_01.json)。
3. [真实原图](../ArtSource/MapDesign/V04/Originals/SL_CITY_V04_OVERALL_01.png) · [功能标注预览](../ArtSource/MapDesign/V04/SL_CITY_V04_ANNOTATED_01.png) · [独立标注SVG](../ArtSource/MapDesign/V04/SL_CITY_V04_ANNOTATED_01.svg)。
4. [27建筑索引](MapDesign/V04/building-index.md) · [城区身份](MapDesign/V04/district-identity.md) · [校园扩建](MapDesign/V04/campus-design.md) · [路线对照](MapDesign/V04/routes-comparison.md)。
5. [验收/偏差](MapDesign/V04/review.md) · [方法参考](MapDesign/V04/references.md) · [提示词](../ArtSource/MapDesign/V04/SL_CITY_V04_PROMPT_01.md) · [实际生成记录](../ArtSource/MapDesign/V04/SL_CITY_V04_GENERATION_01.json)。
6. [源稿索引](../ArtSource/MapDesign/V04/README.md)说明真实参考01/输入快照与校正后参考02的区别。

## 成果与接续规则

1280×1080m候选框，300×240m八组校园，27重要ID/用途/阶段保留、46背景体量。底稿二维检查通过；校园C01后门/公共回廊补齐，校门到所有组团整体可达，铁路只两定义下穿。家→校门223.3m，校门经书店/便利店→家611.9m，仅算术长度/步行估计，通勤容忍尚未批准。

一次生图实际1374×1145，未达目标且仍偏写实；铁路抬高形象改善但新增西穿越，部分翼/小店/路口与出口偏离。标签是可辨形象或候选对应，不能当精确建筑归属证明。未实测的3D/工程/耗时项目保持未验证。

当前底稿revision01b：专项复核删除无定义跨铁路首段，不移动建筑。REFERENCE_02与当前底稿相同；本次实际上传REFERENCE_01和LAYOUT_AT_GENERATION_01保存真实历史，未用修订02追加生成。任何下一视图必须使用当前LAYOUT_01/PLAN_01/REFERENCE_02，不依据概念图反写布局。

标注SVG外链Originals/SL_CITY_V04_OVERALL_01.png，原图1:1，不改图像字节；下载LFS后保持相对目录。历史标注层可在SVG编辑器分别开关。V02/V03完整保留。

## 下一步与Git

停止供评价。用户认可后另行安排校园局部深化或单段HD2D样板；不自动重生成/批量视角、建模、完整室内、UE或玩法规则。最新认可角色图仍未提供，人物比例不能据此宣称实测。

main跟踪独立[Art-Asset-Library](https://github.com/sebastiannogo565-dev/Art-Asset-Library)。本轮仅暂存V04目录、必要索引/README/四交接与精确LFS属性。原3帮助脚本未跟踪保留，无关工具忽略。起始提交61986ca8d88ed15c6588e462141ef13571f9ab4c与远端一致；原图/标注2个新对象沿用LFS。实际提交、推送与完整远端hash由收尾及最终报告提供，不强推或跳过LFS钩子。
