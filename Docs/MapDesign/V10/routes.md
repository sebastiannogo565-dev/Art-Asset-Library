# V10同端点路线与生活闭环

正式折线见[路线JSON](../../../ArtSource/MapDesign/V10/SL_WORLD_V10_ROUTES_01.json)，继承V09同起终点/中途顾客门，六条线均无变化。

|路线ID|起/终m|V09m|V10m|差m|
|---|---|---|---|---|
|V10_HOME_GATE|2150.28, 1771.26 → 2190.91, 1918.18|170.16|170.16|0.00|
|V10_GATE_BOOK_HOME|2190.91, 1918.18 → 2150.28, 1771.26|456.01|456.01|0.00|
|V10_GATE_CAFE_HOME|2190.91, 1918.18 → 2150.28, 1771.26|522.70|522.70|0.00|
|V10_GATE_BOOK_CAFE_HOME|2190.91, 1918.18 → 2150.28, 1771.26|540.70|540.70|0.00|
|V10_STATION_GATE|4470.91, 1950.91 → 2190.91, 1918.18|2553.12|2553.12|0.00|
|V10_STATION_OLD|4470.91, 1950.91 → 2351.82, 1808.18|2304.78|2304.78|0.00|

家校170.16m；放学书店456.01m、咖啡522.70m、书店咖啡540.70m；旧便利/书店480.60m继续保留，不把不同购物目标当缩距。站校2553.12m、站旧街2304.78m是跨区访问，公交可选，非上学强制步行。校门到教室99.15m/教学图书103.25m/教学体育98.32m继续。高差校前8m是候选，楼梯/坡度及实际耗时未验证；不修改角色步速时钟。

## 六住户与配送

### HH01 学生家庭

B01→CLASS（walk）；CLASS→C03（walk）；C03→C08（walk）；C08→B03（walk）；B03→B02（walk）；B02→B01（walk）

### HH02 医护家庭

BG_W_01→B20_staff（walk）；B20_staff→BG_W_02（walk）；BG_W_02→B22（walk）；B22→BG_W_01（walk）

### HH03 外地通勤家庭

BG_W_07→S01（walk）；S01→S06（bus_future_local）；S06→B09（walk）；B09→EXT（rail_future_destination）；EXT→B09（rail_future_destination）；B09→S06（walk）；S06→S05（bus_future_local）；S05→B32（walk）；B32→S05（walk）；S05→S01（bus_future_local）；S01→BG_W_02（walk）；BG_W_02→BG_W_07（walk）

### HH04 青年店员

BG_E_03→B04_staff（walk）；B04_staff→BG_S_01（walk）；BG_S_01→LOOKOUT（walk）；LOOKOUT→BG_E_03（walk）

### HH05 旧街店主

BG_S_01→B03（walk）；B03→BG_S_04（walk）；BG_S_04→WELL（walk）；WELL→BG_S_01（walk）

### HH06 退休居民

BG_G_01→SN1（walk）；SN1→S02（bus_future_north_branch）；S02→S01（bus_future_local）；S01→B21（walk）；B21→BG_W_02（walk）；BG_W_02→S01（walk）；S01→S02（bus_future_local）；S02→SN1（bus_future_north_branch）；SN1→PARK（walk）；PARK→BG_G_01（walk）

40段=31步行/7未来公交/2图外铁路；31步行授权角色条件下二维重查连通，未新增游戏NPC。9原后勤点可达，新B44顾客/后勤/卸货/观船、U28两门及湖岸停留另检；公共图不允许进入B44工具院，校外公众绕校。补货/垃圾与海滩、湿地及私院分开；图外供货不构成已验证运输运营。
