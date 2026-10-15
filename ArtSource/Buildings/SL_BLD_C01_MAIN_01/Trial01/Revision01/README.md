# C01整栋试作局部修订01 · 独立回件

已实际修改玩家桌椅、九列柜体和照片板位置，保原整栋外观/分层/材色/未改UV。玩家席只在声明的尺寸假设下连续检查通过；西连接1.4m门双向未通过。**本包不代表30席完整通过、900人运营或整栋最终通过。**

[修订Blend](SL_BLD_C01_MAIN_01_TRIAL_01_REV_01.blend) / [建筑FBX](SL_BLD_C01_MAIN_01_TRIAL_01_REV_01.fbx) / [规格与取舍](SPEC.md) / [针对性验收](review.md) / [统一几何](GEOMETRY.json) / [低细度布局](LAYOUT.json)。源可编辑，默认整栋建筑显示、CHECK层隐藏，代理不导出。

- [P01_CLASS_CONTINUOUS：同坐标30席、站立/椅活动/坐姿三层与19阶段证据](Boards/SL_BLD_C01_MAIN_01_TRIAL_01_REV_01_P01_CLASS_CONTINUOUS.png) · [可编辑SVG](Boards/SL_BLD_C01_MAIN_01_TRIAL_01_REV_01_P01_CLASS_CONTINUOUS.svg)
- [P02_SEAT_STATUS：30稳定ID，1假设连续/6站立/23当前候选受阻](Boards/SL_BLD_C01_MAIN_01_TRIAL_01_REV_01_P02_SEAT_STATUS.png) · [可编辑SVG](Boards/SL_BLD_C01_MAIN_01_TRIAL_01_REV_01_P02_SEAT_STATUS.svg)
- [P03_SHOES_LAYOUT：双操作/公共路/等候/门冲突与两套面积账](Boards/SL_BLD_C01_MAIN_01_TRIAL_01_REV_01_P03_SHOES_LAYOUT.png) · [可编辑SVG](Boards/SL_BLD_C01_MAIN_01_TRIAL_01_REV_01_P03_SHOES_LAYOUT.svg)

实际局部预览，2560×1440、同原日光约30°；蓝色为明确假设的姿态体，绿色/赭色为有限操作/等候检查层；原PNG只以原字节站立参照出现，切片不是游戏画面：

- [CLASS_REST_OPERATOR：椅复位、原人物站立/门口与操作位置](Previews/SL_BLD_C01_MAIN_01_TRIAL_01_REV_01_CLASS_REST_OPERATOR.png)
- [CLASS_PULLED_APPROACH：自己的椅子拉出，原尺寸代理站在椅前](Previews/SL_BLD_C01_MAIN_01_TRIAL_01_REV_01_CLASS_PULLED_APPROACH.png)
- [CLASS_TRANSITION_HALF：t=0.5定尺寸关节/全宽包络假设](Previews/SL_BLD_C01_MAIN_01_TRIAL_01_REV_01_CLASS_TRANSITION_HALF.png)
- [CLASS_SEATED_ASSUMPTION：t=1坐定假设，真实椅座接触](Previews/SL_BLD_C01_MAIN_01_TRIAL_01_REV_01_CLASS_SEATED_ASSUMPTION.png)
- [CLASS_RESTORED：起身逆过程后退出/椅复位，路线同坐标](Previews/SL_BLD_C01_MAIN_01_TRIAL_01_REV_01_CLASS_RESTORED.png)
- [SHOES_MAIN_SIMULTANEOUS：主厅两侧有限操作包络与同时进出路线](Previews/SL_BLD_C01_MAIN_01_TRIAL_01_REV_01_SHOES_MAIN_SIMULTANEOUS.png)
- [SHOES_LINK_DOOR_CONFLICT：补柜双侧操作/侧袋等候，原1.4门红框/2.4建议蓝框](Previews/SL_BLD_C01_MAIN_01_TRIAL_01_REV_01_SHOES_LINK_DOOR_CONFLICT.png)

900名义格=主468+西连接432，实际占地15.048㎡。旧18m主柜加深新增纠正为1.08㎡，见[两账](AREAS.csv)。唯一推荐取舍为原西连接内门同中心1.4→2.4m；未改实际门，暂停该接口精作交规划。三张凳被移除，换鞋坐凳/真实换鞋流程仍未解决。

[30席状态](SEATS.csv) / [柜列与腔体](CABINETS.csv) / [新旧坐标](COORDINATES.csv) / [变更范围](CHANGE_SCOPE.json) / [图稿依赖](VIEW_DEPENDENCIES.json) / [原生检查](SOURCE_CHECK.json) / [回导检查](FBX_CHECK.json) / [只读输入](protected_inputs.json) / [文件清单](manifest.json)。

原Trial包与旧manifest保持；[原整栋A](../Previews/SL_BLD_C01_MAIN_01_TRIAL_01_A.png)/[B](../Previews/SL_BLD_C01_MAIN_01_TRIAL_01_B.png)仅为原版未受影响外观；[64/32对照](../README.md)沿原实际纹理。复用父Textures48文件，新纹理0。无AI生图/正式动画/UE。

复现顺序：validate_layout.py → check_shoes.py → update_model.py → render_revision.py → verify_revision.py → make_boards.py → SVG按3200×2400栅格化 → make_delivery.py。所有写出只在本修订目录。不要运行原版收尾脚本覆盖原包。验证脚本保留失败证据，未通过西连接门不设置成成功。

RT01待设计不开放；B01/SchoolLife/校门/认可人物保持。交规划及用户针对性审阅后停止，不开展下一阶段。
