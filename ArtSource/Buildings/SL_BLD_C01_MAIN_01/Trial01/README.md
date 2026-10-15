# C01 整栋Blender试作01 · 待规划与用户审阅

2026-10-15。依据已接受Reference/Revision01重新构建整栋试作网格，原6642参考指示未导入或改名。入口、教室、鞋柜与三梯先行复建后完成整栋；固定基准不变。本轮停止于试作回件，不自动进入正式生产或UE。

- [可编辑整栋Blend](SL_BLD_C01_MAIN_01_TRIAL_01.blend) / [建筑FBX](SL_BLD_C01_MAIN_01_TRIAL_01.fbx)
- [整体两向与入口](Boards/01_OVERVIEW.png) / [教室与人物](Boards/02_CLASSROOM.png) / [900格与冲突](Boards/03_SHOES.png)
- [分层与楼梯](Boards/04_LAYERS_STAIR.png) / [实际UV与32/64](Boards/05_UV_TEXTURE.png)
- [规格](SPEC.md) / [三类验收与待判断](review.md) / [尺寸接口JSON](GEOMETRY.json)
- [实测统计](STATISTICS.json) / [原生重开](NATIVE_REOPEN.json) / [实际FBX回导](FBX_REIMPORT.json) / [检查](CHECKS.json)
- [真实纹理清单](TEXTURES.json) / [实际相机](CAMERAS.json) / [保护输入](PROTECTED_CHECK.json) / [回件指纹](manifest.json)

原生整体及主要检查预览2560×1440，密度及鞋格近查1600×1200；阅读合板3200×2400。所有图都是同一试作的渲染或其检查切片，非独立AI拼图。自然光预览、临时纹理检查与实际游戏效果有明确边界。

源默认WHOLE可见；CHECK_ONLY_NO_EXPORT默认隐藏，内有派生切片、原人物及有限代理，按需开关。CONTEXT_NO_EXPORT为日光/地面/相机。FBX只含建筑，不含人物、地面、CUT或代理。模型坐标已保留，不能逐件重置原点。

当前：2224建筑网格对象、786实际网格源、1438共享追加摆放；摆放后三角896744，14共享材质、48张PNG（主体42＋密度比较6）。无LOD/性能/复杂碰撞定稿。

已测指定主路与业务家具净区；成对距组内改1.06m消除保守静态肩宽重叠，余约20mm。**完整入座、全部座位、鞋柜双面/交叉/队列未通过**。900仅名义格，主柜0.66m是组内试作候选。详情见review，不把失败隐藏在总体验收中。

复现顺序：prepare_trial.py（首次快照）→ Blender build_trial.py → render_trial.py → enhance_checks.py → finalize_mesh.py → verify_trial.py → bundled Python finish_trial.py。脚本仅写Trial01及指定交接文档，原Reference/Revision01/Planning不改。
