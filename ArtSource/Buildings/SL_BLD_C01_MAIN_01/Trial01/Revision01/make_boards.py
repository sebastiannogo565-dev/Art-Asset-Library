"""Editable dimensional evidence generated directly from LAYOUT/SHOE_CHECKS."""
import json,html,csv
from pathlib import Path
O=Path(__file__).parent;D=O/'Boards';D.mkdir(exist_ok=True)
L=json.loads((O/'LAYOUT.json').read_text(encoding='utf-8'));S=L['shoe'];C=json.loads((O/'SHOE_CHECKS.json').read_text(encoding='utf-8'))
P='SL_BLD_C01_MAIN_01_TRIAL_01_REV_01'
class Board:
 def __init__(self,title,sub):
  self.a=['<svg xmlns="http://www.w3.org/2000/svg" width="3200" height="2400" viewBox="0 0 3200 2400"><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8Z" fill="context-stroke"/></marker></defs><rect width="3200" height="2400" fill="#f4f3ee"/><g font-family="Microsoft YaHei, sans-serif" fill="#233c42">']
  self.text(80,96,title,52);self.text(80,155,sub,29);self.line([(80,185),(3120,185)],'#8aa3a6',2)
 def text(self,x,y,t,size=30,color='#233c42'):
  self.a.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}">{html.escape(str(t))}</text>')
 def rect(self,x,y,w,h,fill='none',stroke='#71898e',sw=2,dash=''):
  self.a.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '+(f'stroke-dasharray="{dash}"' if dash else '')+'/>')
 def line(self,pts,color='#3d7077',width=4,dash='',arrow=False):
  self.a.append('<polyline points="'+' '.join(f'{x:.3f},{y:.3f}' for x,y in pts)+f'" fill="none" stroke="{color}" stroke-width="{width}" stroke-linejoin="round" '+(f'stroke-dasharray="{dash}" ' if dash else '')+('marker-end="url(#arrow)" ' if arrow else '')+'/>')
 def circle(self,x,y,r,color):self.a.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>')
 def save(self,n):
  self.text(80,2345,'REV_01 · 米制 / 同一 LAYOUT.json · 检查示意与实际模型预览分开 · 未作游戏内验收',27)
  (D/(P+'_'+n+'.svg')).write_text('\n'.join(self.a+['</g></svg>'])+'\n',encoding='utf-8',newline='\n')
class Plan:
 def __init__(self,b,x,y,s,origin):self.b=b;self.x=x;self.y=y;self.s=s;self.ox,self.oy=origin
 def xy(self,x,y):return self.x+(x-self.ox)*self.s,self.y-(y-self.oy)*self.s
 def rect(self,r,fill='none',stroke='#71898e',sw=2,dash=''):
  x,y=self.xy(r[0],r[3]);self.b.rect(x,y,(r[2]-r[0])*self.s,(r[3]-r[1])*self.s,fill,stroke,sw,dash)
 def text(self,x,y,t,size=24,c='#233c42'):a,b=self.xy(x,y);self.b.text(a,b,t,size,c)
 def path(self,pts,c,w=5,dash='',arrow=True):self.b.line([self.xy(*v) for v in pts],c,w,dash,arrow)
b=Board('C01 试作局部修订01｜玩家席连续空间验证','保 8.40×9.00m / 30席 / 原入口 / 原业务点 · 仅该尺寸假设下通过，不是原人物动作验收')
p=Plan(b,150,1790,155,(41,12.7));p.rect(L['room'],'#e4e9e6','#233c42',5)
status={v['id']:v['state'] for v in L['seats']}
for d,c in zip(L['desks'],L['chairs']):
 x,y=d['x'],d['y'];p.rect([x-.225,y-.325,x+.225,y+.325],'#c5af89','#715e43',2)
 cx,cy=c['x'],c['y'];p.rect([cx-.225,cy-.225,cx+.30 if c['player'] else cx+.225,cy+.225],'#839ca1','#385b63',2)
 state=status[d['id']];color='#26835a' if '连续' in state else '#b78922' if '可达' in state else '#ae5450'
 a,bb=p.xy(x-.1,y);b.circle(a,bb,13,color);p.text(x-.20,y+.48,d['id'].split('DESK_')[1],22)
p.path([[45,12.7],[45,18.8],[48.8,18.8],[48.8,19.08]],'#238356',7)
p.path([[48.29,19.87],[48.29,18.8],[41.7,18.8],[45,18.8],[45,12.7]],'#3879b2',4,'12 7')
p.rect([48.05,19.645,49.2,20.095],'none','#b47922',4,'9 7')
p.rect([48.29-.34,19.87-.519827586,48.29+.34,19.87+.519827586],'none','#238356',3)
for x,y,name in [(45,19.5,'业务点保留'),(45,18.7,'恢复候选保留')]:
 a,bb=p.xy(x,y);b.circle(a,bb,10,'#aa5c20');p.text(x-.50,y+.20,name,24)
p.path([[44.2,12.7],[45.8,12.7]],'#1a3844',10,arrow=False)
p.text(44.25,12.30,'原门净宽 1.60m',28);p.text(41,22.10,'北 ↑ / 教室 F2_W4 · FL +4.00',31)
p.text(41,12.0,'横向 8.40m；纵向 9.00m；教学前场在西侧',28)
b.text(1600,260,'连续顺序与最窄证据',37)
names=['原门→横通道','横通道→操作侧','原尺寸转向','接近自己的椅子','转向椅背','拉椅 0.625m','回到横通道','移至椅前','椅前接近','连续坐下（1000区间）','连续起身（逆过程）','椅前退出','返回操作侧','返回操作点','椅子推回（逆过程）','回横通道','经教学前场','回原门中轴','退出原门']
for i,(s,n) in enumerate(zip(L['segments'],names)):
 val=s.get('min_separation');suffix=f'  Δ≥{max(0,val)*1000:.1f}mm' if val is not None else ('  逆向同一几何' if 'reverse_of' in s else '  自身椅连续扫掠通过')
 b.text(1600,315+i*48,f'{i+1:02d}  {n}{suffix}',27,'#277652')
for i,t in enumerate(['绿线：站立进入；蓝虚线：经教学前场返回。','赭色框：本席椅活动；绿色框：完整站立包络。','30席编号不变；玩家指定改为 5_5，原3_5仍保留。','桌 X47.715；椅 X48.275→48.900；Y19.870。','站位 (48.29,19.87,+4.00)，原门仍 (45,12.7)。','最小站立余量10mm；转向18.08mm；坐定允许椅面接触0。','保留自身椅、桌腿和托盘；没有瞬移、缩体或删椅。']):b.text(120,1955+i*49,t,29)
for i,t in enumerate(['原图可见高1.80m / 宽1.039655m；胶囊另列0.68×1.92m。','坐姿无认可原图：上身、全宽下段、双腿均为尺寸假设。','下段定尺寸铰转，不缩宽；大腿/小腿各0.44m、半径0.06m。','双臂各0.40+0.40m；新椅背把手用于有限拉椅检查。','10µm数值容差；零内缩；刚好接触不计穿透。']):b.text(1600,1320+i*50,t,28)
# Three local XZ views share the same scale and real own-chair/desk dimensions.
for i,t in enumerate([0,.5,1]):
 q=Plan(b,1650+i*480,2230,195,(47.6,4));q.text(47.6,6.28,f't={t:.1f} / XZ',25)
 for ob in L['obstacles']:
  if ob['id'].startswith(('F2_W4_DESK_5_5','F2_W4_CHAIR_5_5')):
   x,y,z,X,Y,Z=ob['bounds'];dx=.625 if 'CHAIR' in ob['id'] else 0;q.rect([x+dx,z+4,X+dx,Z+4],'#a8b8b5','#637b80',1)
 pose=next(v for v in L['seated_motion']['poses'] if abs(v['t']-t)<1e-8)
 for part in pose['parts']:
  x,y,z,X,Y,Z=part['bounds'];q.rect([x,z,X,Z],'none','#397bb3',1)
 q.path([[47.6,4],[49.5,4]],'#233c42',2,arrow=False)
b.save('P01_CLASS_CONTINUOUS')
b=Board('C01 试作局部修订01｜30席逐席状态','站立到达与完整姿态转换分别记录；其他23间教室维持原试作，未外推玩家席结果')
for block in range(2):
 x=90+block*1570;b.text(x,265,'ID      站立 / 椅活动                 入座与离席',33)
 for i,s in enumerate(L['seats'][block*15:(block+1)*15]):
  y=335+i*112;sid=s['id'].split('DESK_')[1];player='连续' in s['state'];reachable='可达' in s['state'];color='#277652' if player else '#a47817' if reachable else '#ae5450'
  b.text(x,y,sid,33,color);b.text(x+160,y,s['state'],29,color)
  b.text(x+160,y+41,('连续19阶段 / 尺寸假设通过' if player else '坐姿转换：未验证')+f"；拉椅净距 {s['chair_travel_clearance']:.3f}m",25)
  b.text(x+160,y+77,s['reason'],24)
b.text(90,2125,'合计：1席该假设下连续通过 / 6席仅站立可达 / 23席当前候选受阻。其余29席坐姿转换未验证。',34)
b.text(90,2185,'受阻是本候选站位与拉椅方向的结果，并非证明不存在其他布局；不把一个玩家席通过扩大为30席或全楼通过。',29)
b.text(90,2240,'站立搜索网格0.05m；完整0.68m深×1.039655m宽保守矩形，候选拉椅保留自身椅；原门与业务点不迁移。',28)
b.save('P02_SEAT_STATUS')
b=Board('C01 试作局部修订01｜900格与同时使用候选','主厅468 + 西连接432 = 900；实际原内门1.4m不改，双向接口仍未通过；不以错时使用替代几何')
plans=[(Plan(b,130,1320,112,(18.3,.3)),[18.3,.3,29.7,8.8],'F1_WL 主鞋柜厅'),(Plan(b,1660,1320,112,(52.3,13)),[52.3,13,63.7,21.7],'F1_LW 西连接补柜区')]
for p,r,title in plans:
 p.rect(r,'#e4e9e6','#233c42',5);p.text(r[0],r[3]+.55,title,34)
 room='F1_WL' if 'WL' in title else 'F1_LW'
 for op in C['operators']:
  if op['room']==room:p.rect(op['rect'],'#d5e2d4','#90ae94',1)
 for bank in S['banks']:
  if bank['room']!=room:continue
  x,y,z,X,Y,Z=bank['bounds'];p.rect([x,y,X,Y],'#6a858d','#274853',2);p.text(x+.05,y+.2,bank['id'].replace('REV_',''),18,'#ffffff')
 for q in S['queues']:
  if q['room']==room:p.rect(q['bounds'],'#e2c894','#a47817',2)
 if room=='F1_WL':
  for k,c in [('main_in_path','#26835a'),('main_out_path','#397bb3')]:p.path(S[k],c,5)
  p.text(23.6,5.5,'中央2.80m',23);p.text(23.7,4.9,'原门3.00m',23)
  p.path([[22.6,1.69],[22.6,4.21]],'#a47817',2,arrow=False);p.text(19.5,3.1,'0.70 + 1.12 + 0.70',23)
 else:
  for k,c in [('link_proposed_in','#26835a'),('link_proposed_out','#397bb3')]:p.path(S[k],c,5,'8 6')
  p.path([[57.3,13],[58.7,13]],'#b64740',12,arrow=False);p.path([[56.8,12.87],[59.2,12.87]],'#397bb3',4,'8 6',False)
  p.text(56.6,12.35,'实门1.40 / 候选2.40',27);p.text(60.6,21.2,'等候6位→',25)
 p.text(r[0],r[1]-.6,f"净范围 {r[2]-r[0]:.2f} × {r[3]-r[1]:.2f}m / 北↑",25)
for i,t in enumerate(['柜间净面距2.52m；双操作0.70+公共1.12+0.70m。','主厅三对：西3.00m×10列，东0.90m×3列。','六层×双面：每对156格；主厅合468格。','单列深0.64m，有效腔深0.304m；开放格候选。','主厅柜端绕行≥1.12m；两条同时路径最小余量13.08mm。','主厅不设排队；原两凳移除，不宣称实际换鞋动作已验。']):b.text(100,1480+i*52,t,29)
for i,t in enumerate(['西连接：单面16列×6=96；双面14×6×2×2=336。','柜长4.8 / 4.2 / 4.2m；深0.35 / 0.70 / 0.70m。','操作带外公共净1.12m；队列在东侧口袋，避开柜端。','原1.4m内门：两个人物宽需2.07931m，差0.67931m。','唯一推荐取舍：同中心内门扩至2.4m，交规划判断。','虚线为2.4m候选路径；实际源和FBX仍保1.4m原门。']):b.text(1650,1480+i*52,t,29)
b.text(100,1855,'旧加深纠错（不覆盖原包）',34)
b.text(100,1910,'18.00m × (0.66−0.60)m = 1.08㎡；10.80→11.88㎡，原0.54㎡错误。',30)
b.text(100,1970,'新布局另算：主厅11.70×0.64=7.488㎡；西连接4.80×0.35+8.40×0.70=7.560㎡。',30)
b.text(100,2030,'合计15.048㎡；原试作18.180㎡；变化−3.132㎡。柜体占地，不含操作/通路/等候带。',30)
b.text(100,2100,'腔宽0.288m / 净口高0.276m；鞋290×105×115mm，双鞋宽235mm；新增手包络仅尺寸假设。',28)
b.text(100,2150,'六层最上层底1.50m，取用点1.60m；假设臂长0.80m，静态需求0.766m。真实抓握/力、换鞋坐凳未验证。',28)
b.text(100,2200,'证据覆盖有限指定同时使用者；不等于900人高峰或任意全柜取用通过。原门接口精作暂停，保900目标交审。',28)
b.save('P03_SHOES_LAYOUT')
with (O/'CABINETS.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f,lineterminator='\n');w.writerow(['ID','room','axis','columns','rows','faces','cells','depth_m','area_m2','cavity_width_depth_openheight_m','bounds_m'])
 for q in S['banks']:
  x,y,z,X,Y,Z=q['bounds'];w.writerow([q['id'],q['room'],q['axis'],q['columns'],q['rows'],q['faces'],q['nominal'],q['depth'],(X-x)*(Y-y),q['cavity'],q['bounds']])
with (O/'AREAS.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f,lineterminator='\n');w.writerow(['ledger','main_m2','westlink_m2','total_m2','main_increase_m2'])
 w.writerows([['original_depth_060',10.8,6.3,17.1,0],['original_trial_depth_066',11.88,6.3,18.18,1.08],['revision_layout',7.488,7.56,15.048,'separate new layout'],['revision_minus_old_trial',-4.392,1.26,-3.132,'not the old depth correction']])
print('THREE_EDITABLE_BOARDS_READY')
