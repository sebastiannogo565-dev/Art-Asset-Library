# C01整栋参考局部修订01

2026-10-15。执行原卡顶部“局部修订01”，原Reference包保留原字节。本目录为独立REV_01，当前仅参考修订回审，不是正式整栋Trial或UE资产。

[规格/尺寸与取舍](SPEC.md)／[实际验收与未验证](review.md)／[新旧变更表](changes.json)／[有限二维/原文件/源核对](CHECKS.json)／[逐文件指纹](manifest.json)。

实际修改完整GEOMETRY.json、OPENINGS.csv、REFERENCE_ONLY.blend；30席三双列组、业务净区/站位/候选恢复点、鞋柜柜深/换鞋凳/3m内廊口、入口色值与共面表面材质归属、露台门底/围护/候选排水均已落入源。没有只写文档。

|当前图稿|状态与依据|
|---|---|
|P02|三层按REV_01重制；其他房间、外门与24班继承|
|P02A|30席两椅态、门→玩家席站位→教学前场→门；原业务/恢复净区；36同室原版容量比较|
|P02B|鞋柜去回/操作/等候与900名义格；内廊口3m实排|
|P02C|鞋柜及露台实际受影响部分重制，其他公共内容继承|
|P03|四立面按REV_01材质归属重制，窗位/体量保持|
|P04/P04A|最高13.68/玻璃13.65、露台完成面8.03/门底/有效护栏/候选排水；无可用RT01通道|
|P05|新版A/B实际渲染；不拿原版两向冒充新材色|
|P05A|新CLASS/后拉态/SHOES/当前入口实际渲染|
|P05B|原ENTRY原字节before＋原形体色值/共面表面归属修正after；同相机/日光/曝光/AgX|

10页均3200×2400可编辑SVG/RGB PNG；7份预览2304×1296原生。未重做P01：[原版P01](../SL_BLD_C01_MAIN_01_REFERENCE_01_P01.png)只作未变体量/历史外观参照，不能当新版材色。原COURT/LINK仅其未变局部空间可继承；原P02/2A/B/C/3/4/4A/5/5A/5B已受影响，均不列为当前准确成果。详见JSON的view_sync。

入口before引用[原Preview_ENTRY](../Preview_ENTRY.png)，路径/SHA写BLENDER_REPORT；不复制重编码。ENTRY_AFTER是保原全部形体的材质控制，包含共面覆盖面归属修正；ENTRY_CURRENT另显示当前共享修订源，避免室内调整混入控制对比。灯光/曝光不变，不以改变门廊造型或增曝光改善。没有新增像素贴图，平色预览不算纹理完成。

重制：Python build_revision.py（读取原G与父级矢量函数，绝不运行原builder）→独立后台Blender render_revision.py→再build_revision.py嵌入已完成预览→Node/sharp rasterize_revision.cjs→Blender reopen_revision.py→check_revision.py。cache保护快照丢失时从本版已保存JSON继承，不要求创建空成果目录。WHOLE/CONTEXT为保存视口，CUT与ENTRY控制副本默认隐藏，均保可编辑。

停止供规划针对性审阅；B01/校门/SchoolLife/人物保持。游戏导航、入座/恢复、八向旋转、集散运营、柜门五金/鞋长、排水/结构、正式UV均未验证。RT01原588㎡保持待设计控制区，本次不开放。
