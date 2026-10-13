"""Create assembly supplement BEFORE any mesh data; then metric trial geometry/UV/textures.
No generation model, no modification of host or SchoolLife. Python + Pillow.
"""
from pathlib import Path
import json, math, hashlib, html
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parent.parent
CACHE=ROOT.parents[3]/'.cache/sign-plate-trial01'
def save(name,data):
 (ROOT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')

# Assembly operations are parameters used by the later source/check scenes.
assembly={
 'status':'visual installation candidate; engineering anchorage/anti-retreat not validated',
 'source_envelope_cm':{'min':[-12,-2,-42],'max':[12,0,42]},
 'mount_pivot_host_cm':[0,-27,140],'mount_pivot_engineering_cm':[-330,-27,940],
 'fixed_parts':['COLUMN_SEAT_UPPER','COLUMN_SEAT_LOWER','PAD_UPPER','PAD_LOWER'],
 'moving_parts':['CARRIER_TRAY','PLATE_HOOK_UPPER','PLATE_HOOK_LOWER','SLIDER_GUIDE','LOCKED_SLIDER','LOCK_STOP','RELEASE_STOP'],
 'order':[
  '柱侧：先放0.2cm垫及两道18cm座；四轴只作紧固位置参照，真实锚固另核；牌尚未遮住座时从南侧施工。',
  '牌侧：两道16cm倒U挂钩、滑舌导座及两端止位先在牌背装妥；连接工艺另核。',
  '将防抬舌向+X退1.0cm至解锁位；仅移动牌侧组件，柱侧座/垫保持不动。',
  '牌侧先上抬1.8cm、向街侧(-Y)外移0.6cm；对齐后沿+Y靠向柱，再沿-Z落1.8cm挂入两座。',
  '从东侧(+X)折边服务口伸入细钩工具，将滑舌向-X推1.0cm至止位；舌顶抵下座底面，阻止牌上抬。',
  '最后检查侧向防自退：拟用导座止退弹片/定位槽，当前只记功能，不冻结弹片尺寸、力或锁紧等级。',
  '拆卸：从同一东侧口解除止退，钩拉滑舌+X 1.0cm；牌上抬1.8cm后向-Y离柱0.6cm，再取下。'
 ],
 'side_service_opening_cm':{'x':[11.8,12],'y':[-1.8,-1],'z':[-31.8,-30.9]},
 'slider_locked_cm':{'min':[8.2,-1.2,-31.5],'max':[10.6,-.6,-31.2]},
 'tool_channel_candidate_cm':{'y':[-1.5,-1.2],'z':[-31.5,-31.2],'purpose':'east-side bent hook access; open through release stop; tool manufacture/clearance pending'},
 'slider_pull_eye_candidate_cm':{'x':[10.05,10.35],'z':[-31.425,-31.275],'through_y':[-1.2,-.6],'purpose':'functional pull eye, not an anchor/screw detail; trial dimensions only'},
 'slider_released_delta_cm':[1,0,0],
 'hook_y_clearance_cm':.05,
 'movement_envelope_notice':'1.8cm up / 0.6cm out is temporary assembly sweep, not installed/source size. During service highest host Z183.8, still below available190; no permanent envelope change.',
 'design_delta':'Design的实心支座外包络改为柱侧U座+牌侧倒U钩；新增下座右侧防抬滑舌/导座/止位及折边服务口。原Design不覆盖，外形/2cm总突出/位置保持。',
 'engineering_pending':['四轴锚固方式/孔径/深度/柱基承载','牌背连接工艺','滑舌止退弹片或可替换锁紧件、抗振/防误退','0.5mm接合间隙和薄板成型公差','工具尺寸/实际维护可操作性','耐候排水及接触垫材种']
}
save('Source/assembly_parameters.json',assembly)
s=[]
def raw(v):s.append(v)
def text(x,y,t,size=25,color='#283d43'):
 raw(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}">{html.escape(t)}</text>')
def rect(x,y,w,h,fill='#ffffff',stroke='#d4dedb'):
 raw(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
def line(x1,y1,x2,y2,color='#d08a40',arrow=False,dash=False):
 raw(f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{color}" stroke-width="4"'+(' marker-end="url(#a)"' if arrow else '')+(' stroke-dasharray="9 6"' if dash else '')+'/>')
def polygon(points,fill):raw('<polygon points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in points)+f'" fill="{fill}" stroke="#304a51" stroke-width="2"/>')
raw('<svg xmlns="http://www.w3.org/2000/svg" width="2600" height="1800" viewBox="0 0 2600 1800"><defs><marker id="a" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6" fill="#d08a40"/></marker></defs><g font-family="Microsoft YaHei, sans-serif">')
rect(0,0,2600,1800,'#edf2ef')
text(65,75,'SL_GE_SIGN_PLATE_01 · Trial01 装配 / 锁定 / 拆卸补充',42)
text(65,120,'先完成本说明，再生成网格。尺寸cm；示意工艺待核；非施工/锚固认证。',25)
rect(50,160,1220,675);rect(1300,160,1250,675);rect(50,870,1220,665);rect(1300,870,1250,665)
text(80,205,'01 先固定柱侧座，再挂入牌体',31)
# Front installed diagram with correct metric proportion and independent arrows.
sx=5.8;cx=310;cz=500
rect(cx-15*sx,cz-50*sx,30*sx,100*sx,'#e1dfd4')
rect(cx-12*sx,cz-42*sx,24*sx,84*sx,'#60767a')
for z in [-30,30]:
 rect(cx-9*sx,cz-z*sx-1.2*sx,18*sx,2.4*sx,'#adc3be')
for x in [-7,7]:
 for z in [-30,30]:
  raw(f'<circle cx="{cx+x*sx}" cy="{cz-z*sx}" r="5" fill="#e5bc77"/>')
line(560,600,560,540,arrow=True);text(595,570,'上抬1.8',24)
text(635,270,'① 垫 → 柱侧座；牌未遮座时',26)
text(635,310,'    从南面安装，四轴不等于已定孔。',24)
text(635,375,'② 倒U钩/导座预装在牌背。',26)
text(635,435,'③ 滑舌先退+X 1.0至解锁位。',26)
text(635,495,'④ 抬高1.8、外移−Y 0.6，',26)
text(635,535,'    再向+Y靠近、沿−Z落座。',26)
text(635,600,'支承布置Z中心±30，柱侧宽18。',24)
text(635,642,'牌侧挂钩宽16，不顶折边。',24)
text(635,702,'永久包络仍24×84×2；服务扫掠另计。',24)
text(80,800,'正视只示意层关系；青色座在实际正面被牌皮遮住。',22)
text(1330,205,'02 同源截面 · 柱侧U座 / 牌侧倒U钩',31)
fixed=[(-.2,28.8),(-.2,31),(-.55,31),(-.55,29),(-.8,29),(-.8,30.8),(-1,30.8),(-1,28.8)]
mobile=[(-1.8,29.2),(-1.6,29.2),(-1.6,31),(-.75,31),(-.75,29.6),(-.55,29.6),(-.55,31.2),(-1.8,31.2)]
def yz(p):return (1430+(p[0]+2)*280,685-(p[1]-28.8)*150)
polygon([yz(p) for p in fixed],'#a5b9b5');polygon([yz(p) for p in mobile],'#60767a')
rect(1990,325,65,360,'#8d9692');text(2070,350,'垫0.2',24)
line(2055,275,2055,735,'#b2aca0');text(2070,420,'柱接触Y0',24)
text(1400,755,'横向放大：X宽省略，Y/Z比例不同；以标注数值为准。',22)
text(2070,490,'前皮 Y−2..−1.8',23)
text(2070,535,'折边回深到Y−1',23)
text(2070,580,'钩净隙0.05候选',23)
text(2070,625,'上抬1.8可越过座顶',23)
text(2070,670,'板厚/公差不作制造保证',22)
text(80,915,'03 右侧防抬滑舌 · 闭合正面后仍有入口',31)
# Lower seat and slider in X/Z orthographic rear detail.
ox=190;oz=1190;sc=38
def xz(x,z):return (ox+(x-7.5)*sc,oz-(z+31.2)*sc)
q=xz(7.5,-28.8);rect(q[0],q[1],1.5*sc,2.4*sc,'#a5b9b5')
q=xz(8.2,-31.2);rect(q[0],q[1],2.4*sc,.3*sc,'#60767a')
q=xz(9.2,-31.2);raw(f'<rect x="{q[0]}" y="{q[1]}" width="{2.4*sc}" height="{.3*sc}" fill="none" stroke="#d08a40" stroke-width="3" stroke-dasharray="7 5"/>')
q=xz(10.4,-31);rect(q[0],q[1],1.2*sc,.7*sc,'#b8c4bf')
line(425,1250,490,1250,arrow=True);text(100,1300,'虚线＝+X退1.0，舌左端9.2越过座右端9.0',22)
line(560,1170,440,1170,arrow=True);text(570,1180,'+X侧细钩工具 →',24)
text(635,1000,'锁位：舌X8.2..10.6，顶Z−31.2。',24)
text(635,1042,'解锁：舌X9.2..11.6（仍在宽24内）。',24)
text(635,1084,'与下座右端8mm重叠，限制上抬。',24)
text(635,1240,'东侧折边服务口：',26)
text(635,1280,'Z−31.8..−30.9，Y−1.8..−1。',24)
text(635,1320,'导座留通道、末止位开口、舌片留钩孔。',23)
text(90,1400,'末步：拟止退弹片/定位槽防滑舌自退；只作功能注记，尺寸/力/抗振待核。',23)
text(90,1450,'未做亚像素螺丝；舌挡抬升的几何成立 ≠ 已验证可长期自锁/承载。',23)
text(1330,915,'04 拆卸与尺寸边界',31)
for i,t in enumerate(['从同一东侧口解除止退 → 钩拉滑舌+X 1.0。','牌侧组件抬高1.8 → 向街侧−Y移0.6 → 取下。','柱侧座/接触垫留柱，拆座时才再次露出四轴。','服务期间可临时超出静态Z/Y；不是扩大成品。','抬升后宿主局部最高Z183.8，仍低于可用190。','永久局部包络X±12 / Y−2..0 / Z±42。','安装轴心：宿主(0,−27,140)，工程(−330,−27,940)。','原柱未改；净口600、道路500、平台800保持。','新增：分离座/钩、滑舌/导座/止位及折边服务口。','未定：锚固/止退/接头工艺/工具公差/承载/耐候。']):
 text(1340,978+i*49,t,24)
text(65,1600,'装配候选：先座后牌、挂接落座、右侧防抬、同侧释放。校名空白；仅此一源、一安装实例。',28)
text(65,1650,'此图＝可编辑设计补充；网格实测与真实日光预览另交。隐藏部件示意不等于不透明宿主背向可见。',24)
text(65,1710,'规划待判断：是否接受该挂接/侧口方案；如何验证止退与真实锚固；校名及后续独立字面继续待定。',24)
raw('</g></svg>')
(ROOT/'Source/SL_GE_SIGN_PLATE_01_TRIAL_ASSEMBLY.svg').write_text('\n'.join(s)+'\n',encoding='utf-8',newline='\n')
print('ASSEMBLY_SVG_SAVED_BEFORE_GEOMETRY',flush=True)

# This editable supplement precedes mesh construction. Raster is produced by sharp separately.
parts=[]
def add(name,verts,faces,role):
 parts.append({'name':name,'role':role,'vertices':[[c/100 for c in v] for v in verts],'faces':faces})
def extrude_x(name,polygon,x0,x1,role):
 n=len(polygon);v=[(x,y,z) for x in [x0,x1] for y,z in polygon]
 f=[list(range(n-1,-1,-1)),list(range(n,2*n))]+[[i,(i+1)%n,(i+1)%n+n,i+n] for i in range(n)]
 add(name,v,f,role)
def box(name,lo,hi,role):
 x,y,z=lo;X,Y,Z=hi
 add(name,[(x,y,z),(X,y,z),(X,Y,z),(x,Y,z),(x,y,Z),(X,y,Z),(X,Y,Z),(x,Y,Z)],[[3,2,1,0],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]],role)

# Thin solid tray: one skin with integral open-back folded return, R4mm outer/R2mm inner.
outer=[];inner=[]
for cx,cz,a0 in [(11.6,41.6,0),(-11.6,41.6,90),(-11.6,-41.6,180),(11.6,-41.6,270)]:
 for step in range(7):
  a=math.radians(a0+step*15);outer.append((cx+.4*math.cos(a),cz+.4*math.sin(a)));inner.append((cx+.2*math.cos(a),cz+.2*math.sin(a)))
outer.extend([(12,-31.8),(12,-30.9)]);inner.extend([(11.8,-31.8),(11.8,-30.9)])
n=len(outer);v=[]
for contour,y in [(outer,-2),(outer,-1.8),(inner,-1.8),(outer,-1),(inner,-1)]:v.extend((x,y,z) for x,z in contour)
f=[list(range(n)),list(range(3*n-1,2*n-1,-1))]
slot=28
for i in range(n):
 j=(i+1)%n
 f.append([i,j,n+j,n+i])
 if i!=slot:
  f.extend([[n+i,n+j,3*n+j,3*n+i],[2*n+j,2*n+i,4*n+i,4*n+j],[3*n+i,3*n+j,4*n+j,4*n+i]])
 else:
  f.append([n+j,n+i,2*n+i,2*n+j])
for i in [28,29]:f.append([n+i,3*n+i,4*n+i,2*n+i])
add('CARRIER_TRAY',v,f,'moving; front sheet and folded return, side access slot; graphic empty')
for tag,z in [('UPPER',0),('LOWER',-60)]:
 extrude_x('COLUMN_SEAT_'+tag,[(y,h+z) for y,h in fixed],-9,9,'fixed to column concept; no anchor holes modelled')
 extrude_x('PLATE_HOOK_'+tag,[(y,h+z) for y,h in mobile],-8,8,'moving with tray; rear attachment method unvalidated')
 box('PAD_'+tag,[-9,-.2,28.8+z],[9,0,31.2+z],'fixed; contact rear datum Y0; isolation material candidate')
guide=[(-1.8,-31.7),(-.5,-31.7),(-.5,-31.5),(-1.5,-31.5),(-1.5,-31.2),(-.5,-31.2),(-.5,-31),(-1.8,-31)]
extrude_x('SLIDER_GUIDE',guide,10.4,11.6,'moving; channel open to east service tool access')
# Solid slider, with a functional Y-through pull eye for the bent side tool.
out=[(8.2,-31.5),(10.6,-31.5),(10.6,-31.2),(8.2,-31.2)]
inside=[(10.05,-31.425),(10.35,-31.425),(10.35,-31.275),(10.05,-31.275)]
v=[(x,y,z) for y in [-1.2,-.6] for contour in [out,inside] for x,z in contour];f=[]
for i in range(4):
 j=(i+1)%4
 f.extend([[i,j,4+j,4+i],[8+j,8+i,12+i,12+j],[i,8+i,8+j,j],[4+j,12+j,12+i,4+i]])
add('LOCKED_SLIDER',v,f,'sliding 1cm toward +X to release; functional pull eye; anti-retreat not validated')
box('LOCK_STOP',[8,-1.8,-31.5],[8.2,-1.15,-31.2],'moving; locked stop forward of seat, not obstructing lift')
release=[(-1.8,-31.7),(-.6,-31.7),(-.6,-31.2),(-1.2,-31.2),(-1.2,-31.5),(-1.5,-31.5),(-1.5,-31.2),(-1.8,-31.2)]
extrude_x('RELEASE_STOP',release,11.6,11.8,'moving; release stop with open side-tool channel')

# Every planar face receives an undistorted chart at 64px/m, including fractional-width thin edges.
# 256 is a trial atlas packing choice, not a global environmental or letter resolution.
def sub(a,b):return [a[i]-b[i] for i in range(3)]
def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def unit(v):
 l=math.sqrt(sum(q*q for q in v));return [q/l for q in v]
def dot(a,b):return sum(a[i]*b[i] for i in range(3))
charts=[]
for p in parts:
 p['face_uvs']=[None]*len(p['faces'])
 p['bounds_m']={'min':[min(v[i] for v in p['vertices']) for i in range(3)],'max':[max(v[i] for v in p['vertices']) for i in range(3)]}
 for fi,face in enumerate(p['faces']):
  vv=[p['vertices'][i] for i in face];a=vv[0];normal=[0,0,0]
  for k in range(1,len(vv)-1):
   c=cross(sub(vv[k],a),sub(vv[k+1],a));normal=[normal[i]+c[i] for i in range(3)]
  normal=unit(normal)
  tangent=unit(sub(vv[1],a));bitangent=unit(cross(normal,tangent))
  pp=[[dot(sub(q,a),tangent)*64,dot(sub(q,a),bitangent)*64] for q in vv]
  lo=[min(q[i] for q in pp) for i in [0,1]];pp=[[q[i]-lo[i] for i in [0,1]] for q in pp]
  size=[max(q[i] for q in pp) for i in [0,1]]
  charts.append({'part':p['name'],'face':fi,'pp':pp,'size_px':size,'pad':2,'rect_px':[math.ceil(size[0])+4,math.ceil(size[1])+4]})
charts.sort(key=lambda c:c['rect_px'][1],reverse=True)
x=y=row=0
for c in charts:
 w,h=c['rect_px']
 if x+w>256:x=0;y+=row;row=0
 assert y+h<=256,'atlas full'
 c['origin_px']=[x+2,y+2];x+=w;row=max(row,h)
 p=next(p for p in parts if p['name']==c['part'])
 p['face_uvs'][c['face']]=[[(c['origin_px'][i]+q[i])/256 for i in [0,1]] for q in c['pp']]
base=Image.new('RGB',(256,256),'#60767a');rough=Image.new('L',(256,256),209);uvimage=Image.new('RGB',(256,256),'#e9eeeb')
bd=ImageDraw.Draw(base);rd=ImageDraw.Draw(rough);ud=ImageDraw.Draw(uvimage)
for c in charts:
 x,y=c['origin_px'];w,h=c['size_px'];fill=(87,94,93) if c['part'].startswith('PAD_') else (96,118,122)
 bd.rectangle((x-2,256-y-h-2,x+w+2,256-y+2),fill=fill)
 rd.rectangle((x-2,256-y-h-2,x+w+2,256-y+2),fill=230 if c['part'].startswith('PAD_') else 209)
 poly=[(x+q[0],256-y-q[1]) for q in c['pp']];ud.line(poly+[poly[0]],fill=(45,82,89),width=1)
 if c['part']=='CARRIER_TRAY' and c['face']==0:
  for px in range(math.floor(x),math.ceil(x+w)):
   for py in range(math.floor(y),math.ceil(y+h)):
    # Low-frequency clustered coat variation only; no sunlight/AO/lettering in BaseColor.
    delta=[0,0,1,-1,0,2,-2][((px//4)*13+(py//5)*7)%7]
    base.putpixel((px,255-py),tuple(q+delta for q in fill))
for im,name in [(base,'BaseColor'),(rough,'Roughness'),(uvimage,'UV_LAYOUT')]:im.save(ROOT/f'Textures/SL_GE_SIGN_PLATE_01_TRIAL_{name}.png')
data={'asset_id':'SL_GE_SIGN_PLATE_01','revision':'TRIAL_01','units':'metres','source_count':1,'target_instance_count':1,
 'coordinate':{'origin':'rear contact datum centre','pivot_m':[0,0,0],'front':'-Y','up':'+Z'},
 'overall_bounds_m':{'min':[-.12,-.02,-.42],'max':[.12,0,.42]},'dimensions_cm':{'width':24,'height':84,'body_depth':1,'overall_depth':2,'sheet':.2,'radius':.4},
 'parts':parts,'assembly':assembly,'uv':{'atlas_px':[256,256],'reference_density_px_per_m':64,'planar_chart_count':len(charts),'padding_px':2,'charts':charts,'thin_edges':'fractional texel geometry preserved, uniform coating; no enlarged seam colour'},
 'material':{'slots_per_part':1,'shared_materials':1,'base_srgb':'#60767A','roughness_byte_metal':209,'roughness_byte_pad':230,'metallic':0,'ior':1.45,'interpolation':'Closest','textures':'temporary; no baked lighting / AO / names'},
 'protected_inputs':json.loads((CACHE/'protected-inputs.json').read_text(encoding='utf-8')),
 'unverified':assembly['engineering_pending']+['校名/字面规格','UE导入/碰撞/导航/游戏光照']}
save('Source/SL_GE_SIGN_PLATE_01_TRIAL_GEOMETRY_UV.json',data)
print(json.dumps({'parts':len(parts),'charts':len(charts),'atlas_occupied_rows':y+row,'geometry_created_after_assembly_svg':True}))
