# V11成对出口与交通

15对道路出口、4个图外方向与公交生活线继承V10；步行道路边界延续，不全变成车站。骑行只保留道路条件、不画车体；校园门内/石阶/沙滩湿地有受控或步行边界。

|连接|成对出口/区域/位置m/朝向|可用方式与边界|
|---|---|---|
|P01|E02_N R02 [2190.909, 1918.182] 按JSON到达朝向 ↔ E01_S R01 [2190.909, 1918.182] 按JSON到达朝向|["walk","cycle_to_gate_then_push"]|
|P02|E02_W R02 [1881.818, 1858.182] 按JSON到达朝向 ↔ E03_E R03 [1881.818, 1858.182] 按JSON到达朝向|["walk","cycle","bus"]|
|P03|E02_E R02 [2401.818, 1728.182] 按JSON到达朝向 ↔ E04_W R04 [2818.182, 1728.182] 按JSON到达朝向|["walk","cycle","bus"]|
|P04|E04_E R04 [3236.364, 1900] 按JSON到达朝向 ↔ E05_W R05 [4341.818, 1900] 按JSON到达朝向|["walk","cycle","bus"]|
|P05|E02_NW R02 [1971.818, 1889.235] 按JSON到达朝向 ↔ E06_S R06 [1977.273, 2045.455] 按JSON到达朝向|["walk","cycle_on_gentle_road","bus_reserved_to_entry"]|
|P06|E06_N R06 [2190.909, 2572.727] 按JSON到达朝向 ↔ E08_SW R08 [1580, 2810] 按JSON到达朝向|["walk","cycle_on_gentle_road","bus_reserved_to_entry"]|
|P07|E07_NE R07 [3063.636, 2618.182] 按JSON到达朝向 ↔ E08_SE R08 [1690, 2860] 按JSON到达朝向|["walk","cycle_on_public_road"]|
|P08|E06_E R06 [2363.636, 2500] 按JSON到达朝向 ↔ E07_W R07 [2645.455, 2500] 按JSON到达朝向|["walk","cycle_on_gentle_road"]|
|P09|E02_S R02 [2231.818, 1518.182] 按JSON到达朝向 ↔ E09_N R09 [2231.818, 1445.455] 按JSON到达朝向|["walk","cycle"]|
|P10|E04_SW R04 [2818.182, 1563.636] 按JSON到达朝向 ↔ E09_E R09 [2518.182, 1563.636] 按JSON到达朝向|["walk","cycle_then_dismount_at_lookout"]|
|P11|E03_NE R03 [1854.545, 2018.182] 按JSON到达朝向 ↔ E06_SW R06 [1936.364, 2109.091] 按JSON到达朝向|["walk","cycle_on_gentle_road"]|
|P12|E03_S R03 [1690.909, 1572.727] 按JSON到达朝向 ↔ E09_W R09 [1900, 1363.636] 按JSON到达朝向|["walk","cycle","bus_reserved_to_entry"]|
|P14|E01_E R01 [2450.909, 2038.182] 按JSON到达朝向 ↔ E02_NE R02 [2401.818, 1908.182] 按JSON到达朝向|["walk","cycle_to_gate_then_push","service_access_reserved"]|
|P15|P15_A R03 [1120, 910] 按JSON到达朝向 ↔ P15_B R09 [1450, 1100] 按JSON到达朝向|["walk","cycle_on_public_road","bus_reserved"]|
|P16|P16_A R04 [3550, 1490] 按JSON到达朝向 ↔ P16_B R09 [3650, 1120] 按JSON到达朝向|["walk","cycle_on_public_road","bus_reserved"]|

## 公交与站前

西公共服务S01→住宅S02→校外S03→旧街外口S04→东商S05→外缘站S06，道路次序不变；班次/价格/旅行分钟未设定。神社/湖入口和海岸支线为未来预留。

B09城市侧站门固定；长低站房、平台雨棚/站务门表达身份，不按生成轨数设计货运站。近门人行与导向、旁侧B10候车/短接送、外层底商租住后勤；W05站门步行联系6m候选，公交主街与人行不以停车场横切。轨后无正式目的地，故不增踏切/隧道。现两主河桥+一小支溪桥不新增；两处细溪现路交点仍需涵/踏步细部核对。
