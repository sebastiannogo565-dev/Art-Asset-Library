# 来源与试作对应

|来源|用途|处理|
|---|---|---|
|Reference/Revision01 GEOMETRY.json / OPENINGS.csv|控制、房间、开口、桌椅位置、标高、材色|只读参数输入；不导入primitives或参考Blend|
|任务卡与最新针对性审阅/审计|前段验证、完整建筑、停止点|保固定接口，失败量化|
|原人物FrontIdle PNG|门、家具、楼梯尺度|原字节打包检查层，不进建筑FBX|
|build_trial.py|真实网格源、实例与分组|正交实心并集、真实洞口、桌椅源/柜腔/闭合阶梯轮廓|
|prepare_trial.py|临时像素图|原创程序绘制、少量色阶接缝，无AI/照片|
|render_trial.py / enhance_checks.py|同栋自然光、有限包络、实际柜格截取|CUT/人物/代理独立默认隐藏，不进FBX|
|verify_trial.py|重开与实际回导、静态净区|不以二维/静态代理代替UE结论|

36席仅保留在冻结参考中的对照，不在Trial建筑或导出中复制。原RT01仅元数据待设计，没有假接近或承托模型。其他来源SHA逐项见protected_inputs和PROTECTED_CHECK。
