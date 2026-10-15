# C01整栋试作局部修订02 · 实际资产回件

[可编辑Blend](SL_BLD_C01_MAIN_01_TRIAL_01_REV_02.blend) / [实际建筑FBX](SL_BLD_C01_MAIN_01_TRIAL_01_REV_02.fbx) / [统一几何](GEOMETRY.json) / [布局与包络](LAYOUT.json) / [规格](SPEC.md) / [分类验收](review.md)。原Trial/Revision01完整保留，整栋上下文沿原版，仅门洞墙带/框扇与新双人凳改动。

实际内门同中心净2.4×2.6m、900格和新双人坐面已交；有限取鞋/换鞋/起身/等候/离开空间通过。**玩家工程兼容仍未通过实证：正式规划Z1200条件d96/98cm，历史Z800条件d496/498cm超限；现用运行位置未回读。** 不移动原锚点、不扩大230cm、不传送，暂停最终席绑定，交规划/开发核定。预览与Enter只在同一可达操作点验算，不要求19阶段全程留圈或新增入座前提。

- [P01_DOOR_SHOE_LOOP：实际门区、坐面与双侧操作/等候](Boards/SL_BLD_C01_MAIN_01_TRIAL_01_REV_02_P01_DOOR_SHOE_LOOP.png) · [可编辑SVG](Boards/SL_BLD_C01_MAIN_01_TRIAL_01_REV_02_P01_DOOR_SHOE_LOOP.svg)
- [P02_ACTIVITY_DISTANCE：P/E/G/A口径、两来源Z与三维余量](Boards/SL_BLD_C01_MAIN_01_TRIAL_01_REV_02_P02_ACTIVITY_DISTANCE.png) · [可编辑SVG](Boards/SL_BLD_C01_MAIN_01_TRIAL_01_REV_02_P02_ACTIVITY_DISTANCE.svg)
- [P03_CHANGE_CHECKS：换鞋包络、局部路径及面积分账](Boards/SL_BLD_C01_MAIN_01_TRIAL_01_REV_02_P03_CHANGE_CHECKS.png) · [可编辑SVG](Boards/SL_BLD_C01_MAIN_01_TRIAL_01_REV_02_P03_CHANGE_CHECKS.svg)

4张2560×1440实际局部自然光，30°；蓝色为未获认可的定尺寸姿态假设、绿色柜前操作/路径、赭色等待/取鞋循环。原人物PNG仅原字节站立对照，检查切片和代理不是游戏画面：

- [WESTLINK_CHANGE_LOOP：真实柜列/2.4门/双人坐面与有限同时使用包络](Previews/SL_BLD_C01_MAIN_01_TRIAL_01_REV_02_WESTLINK_CHANGE_LOOP.png)
- [CHANGE_SEAT_CLOSE：从室内看坐面：定尺寸坐姿与65°弯腰假设](Previews/SL_BLD_C01_MAIN_01_TRIAL_01_REV_02_CHANGE_SEAT_CLOSE.png)
- [DOOR_HALL_APPROACH：真实廊侧停扇、门框及打开的2.4×2.6洞口](Previews/SL_BLD_C01_MAIN_01_TRIAL_01_REV_02_DOOR_HALL_APPROACH.png)
- [CLASS_OPERATION_P_EQUALS_E：原人物站立操作点、3_5关系候选、5_5旧研究区分](Previews/SL_BLD_C01_MAIN_01_TRIAL_01_REV_02_CLASS_OPERATION_P_EQUALS_E.png)

[P/E三维距离8条CSV](ACTIVITY_DISTANCE.csv) / [完整来源与距离](ACTIVITY_DISTANCE.json) / [地面/Actor/锚/椅坐标](COORDINATES.csv) / [门框停扇表](OPENING_CHANGE.csv) / [柜列表](CABINETS.csv) / [30席继承状态](SEATS.csv) / [面积分账](AREAS.csv)。

[实际源检查](SOURCE_CHECK.json) / [回导检查](FBX_CHECK.json) / [局部差异指纹](CHANGE_SCOPE.json) / [19阶段继承](INHERITED_STUDY.json) / [代码SHA](CODE_EVIDENCE.json) / [图稿依赖](VIEW_DEPENDENCIES.json) / [保护输入](protected_inputs.json) / [清单](manifest.json)。

900格主468/补432与15.048㎡柜体不变；新凳2.4×0.45m投影1.080㎡，与旧18×0.06=1.080㎡纠错是不同账目。三变化网格实际UV64px/m起点，父Textures48文件原字节继承、新贴图0。其他2212建筑对象完全保持，原19阶段/900腔验继承而不重跑。原[整栋A](../Previews/SL_BLD_C01_MAIN_01_TRIAL_01_A.png)/[B](../Previews/SL_BLD_C01_MAIN_01_TRIAL_01_B.png)仅看原Trial外观；[主厅图](../Revision01/Previews/SL_BLD_C01_MAIN_01_TRIAL_01_REV_01_SHOES_MAIN_SIMULTANEOUS.png)为未变修订01部分，不能当新版门/坐面图。

复现：prepare_revision.py（只提取旧定义，不运行旧写出）→build_revision.py→render_revision.py→verify_revision.py→make_boards.py→SVG原生3200×2400栅格化→finalize_delivery.py。只写本修订目录和本轮授权交接索引；不要执行原版收尾脚本覆盖旧包。

RT01原状态不开放；B01/SchoolLife/校门/人物不变，无UE/新系统/正式动画。真实角色动作/抓握、任意高峰运营、当前世界Actor变换与资格仍未验。回审决定整栋最终状态，停止本轮。
