# 海滩窗口收尾纠正

正式V12窗口[1350,510,1490,815]＝140×305m已准确继承。复核发现早先V13输入实际用了[1370,655,1490,815]＝120×160m细节裁切并误写入继承元数据；现在恢复正式窗口，旧AT_GENERATION与原图保持真实来源，不称早先候选覆盖完整原窗口。另附SL_BEACH_V13_FORMAL_WINDOW_01.svg/png完整窗口。岸线、门位、路线及世界几何没有调整。

# 最新输出处理补记

一次AI直接编辑仍保存全部原字节，但有范围外重绘。为遵守用户范围，另交原V12底层＋8个可关闭AI片段的原生SVG组稿与PNG预览。SL_WORLD_V13_SCOPED_COMPOSITION_01.svg/png，1374×1145、不透明、未插值；这是SVG组稿，不是另一张生图，也不是原生3072达标。2px裁切边缘外RGB逐像素完全一致，详见COMPOSITION_RECORD。整块清屋式大广场排除，仅原公共门前退界局部；其余背景房/道路/塔/湖/铁路不改。

# 最新追加：九项限定直接编辑一次

当前最终审阅选择SL_WORLD_V13_SCOPE_RESTRICTED_01，原生1374×1145/3394291字节/不透明PNG，SHA256 17ac540f77e1e944e0f4e2e84513da8dd4340c38c1b1c22b80a9bcd94add72c0。以用户V12附件直接编辑，不以旧V13重排稿为底图。提示词与两输入原字节已保存，冻结布局SL_WORLD_V13_LAYOUT_AT_SCOPE_EDIT_01；一次user_scope_edit独立记录，不混计为旧七初始或三定点次数。总调用11：旧7+3过程，加最新1限定编辑。内部模型名未暴露，无放大/转码。此前选择已移到GENERATION.historical_selection。


# 实际生成与原图

渠道：内置image_gen.imagegen，模型内部ID未暴露，未猜名称。7项初次一次＋3项定点修订（整城/A/B各一次），其他4项未重抽。总调用10次，全部原生不透明PNG，原图原字节在Originals、根目录副本同SHA。无插值、锐化、重编码、改后缀。实际|候选|次数/类型|真实原生尺寸|字节|提示词|
|---|---|---|---|---|
|SL_WORLD_V13_CONCEPT_DAY_01|initial|1374×1145|3341956|[完整提示词](prompts/SL_WORLD_V13_CONCEPT_DAY_01.md)|
|SL_CORE_V13_PS02_VIEW_A_DAY_01|initial|1672×941|2832684|[完整提示词](prompts/SL_CORE_V13_PS02_VIEW_A_DAY_01.md)|
|SL_CORE_V13_PS02_VIEW_A_DAY_02|targeted|1672×941|3122262|[完整提示词](prompts/SL_CORE_V13_PS02_VIEW_A_DAY_02.md)|
|SL_CORE_V13_PS02_VIEW_B_DAY_01|initial|1672×941|3439212|[完整提示词](prompts/SL_CORE_V13_PS02_VIEW_B_DAY_01.md)|
|SL_CORE_V13_PS02_VIEW_A_DUSK_01|initial|1672×941|2932622|[完整提示词](prompts/SL_CORE_V13_PS02_VIEW_A_DUSK_01.md)|
|SL_CORE_V13_PS02_VIEW_A_NIGHT_01|initial|1672×941|2685033|[完整提示词](prompts/SL_CORE_V13_PS02_VIEW_A_NIGHT_01.md)|
|SL_BEACH_V13_VIEW_DAY_01|initial|1672×941|2262376|[完整提示词](prompts/SL_BEACH_V13_VIEW_DAY_01.md)|
|SL_SHRINE_V13_VIEW_NIGHT_01|initial|1672×941|2323270|[完整提示词](prompts/SL_SHRINE_V13_VIEW_NIGHT_01.md)|
|SL_WORLD_V13_CONCEPT_DAY_02|targeted|1374×1145|3230478|[完整提示词](prompts/SL_WORLD_V13_CONCEPT_DAY_02.md)|
|SL_CORE_V13_PS02_VIEW_B_DAY_02|targeted|1672×941|3229771|[完整提示词](prompts/SL_CORE_V13_PS02_VIEW_B_DAY_02.md)|

目标整城3072×2560/局部2560×1440均未原生达成；矢量总图3072×2560和五板3072×2048则由SVG原尺寸渲染，不能据此称AI原图达标。原字符2076B/128×128透明，生成角色只是示意。

[逐次记录JSON](../../../ArtSource/MapDesign/V13/SL_WORLD_V13_GENERATION_01.json)包含issued_prompt原文、SHA、每项参考SHA/上传时文件名/归档快照、真实工具原文件路径、实际尺寸与冻结底稿SHA。A02用于A黄昏/夜间编辑及B材色身份对照；B第一参考始终B自身体块。原图从下载路径复制，未删除下载文件。

生图冻结为[AT_GENERATION](../../../ArtSource/MapDesign/V13/SL_WORLD_V13_LAYOUT_AT_GENERATION_01.json)，最终只校正候选M01/M02两点侧位，不改任何正式路/楼/水系。修前PNG/SVG已在References/AtGeneration归档。生成图使用修前布局与板，最终航标不报告视觉位置通过，也未追加生成。

审阅选择：整城02、A02、B02；黄昏/夜/海滩/神社01。所有01原图保留，02是单次修订，非替换原始文件。
