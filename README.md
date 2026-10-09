# SchoolLife 美术资产项目

独立工作区：D:/Art Asset Library。负责地图布局、场景概念、资产规划和获授权的生成；不连接或修改SchoolLife游戏代码仓库（获指定的评审与人物文件仅只读参考），不负责玩法或UE开发。

澄坂市V11“功能显形、地区身份与生活核心”继承V10正式米制布局，深化日常建筑门面、四种公共边缘和东西身份。渔务7000m²候选地块包住原作业院纠错；模型/UE/新系统0。

## 当前交付

[V11正文](Docs/MapDesign/V11/README.md) · [源图索引](ArtSource/MapDesign/V11/README.md)：同一JSON总图/四板与PS02共同150×145m平面。整城1374×1145，局部A/B各1672×941；B相反方向失败，原图与漂移保留[验收](Docs/MapDesign/V11/review.md)。世界19.19008km²/校园360×320/核心520×400、六路线不改。V02—V10全部保留。

校园拟独立成图，住宅/校前/旧街一期同室外图，九概念区不等于九UE图。天台/泳池/祭场/新店/探索是未来环境空间，未开发交通/切图/经营/关系/小游戏/奇幻。无缝世界不要求。

## 目录与交接

- Docs/execution-plan.md：目标、步骤、验收与不做内容。
- Docs/progress.md：完成／未验证／阻塞及历史记录。
- Docs/handoff.md：当前成果、接续入口、Git收尾。
- Docs/decision-log.md：已确认约束、候选、待审阅和被替代决定。
- Docs/MapDesign/：版本化正文、建筑／交通／出口／验收索引。
- ArtSource/MapDesign/：SVG、JSON、PNG、提示词／参考／真实原图，Originals/不重编码。
- ArtApproved/：认可素材目录预留；认可人物只读副本在V10/References，批准目录不据此批量制作。

## 工作边界

本轮只设计和交接，不建模、全城室内、额外视角、批量素材、UE、交通／地图切换代码或游戏规则。06:00/08:00/15:00仅生活用途情境，不重设时间倍率、疲劳、票价、等待或学习奖励。停止供用户审阅，未获指令不进入下一阶段。

## Git与素材

独立origin：[Art-Asset-Library](https://github.com/sebastiannogo565-dev/Art-Asset-Library)。main跟踪origin/main，正常提交推送，不强推／改历史。实际哈希和远端核验见[交接](Docs/handoff.md)与结束报告。

保留blender_mcp/独立工具目录与原有三个未跟踪帮助脚本，不纳入本轮。缓存、日志、凭据/API Key和本地配置由.gitignore排除，不提交或打印凭据。大型设计二进制沿用LFS；V10原图和同尺寸标注PNG添加精确LFS路径，其他小预览普通Git；新检出需git lfs pull。设计稿、提示词、认可素材和必要源文件保留历史。作者沿用仓库本地配置。
