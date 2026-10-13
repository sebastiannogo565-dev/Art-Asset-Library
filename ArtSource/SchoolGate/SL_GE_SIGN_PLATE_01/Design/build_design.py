"""Rebuild one centimetre-based sign carrier design SVG. No mesh/UV/texture files.
Installed projections use the accepted pillar's immutable trial geometry data.
"""
from pathlib import Path
import base64, hashlib, html, json, math

HERE=Path(__file__).resolve().parent
G=json.loads((HERE/'SL_GE_SIGN_PLATE_01_GEOMETRY.json').read_text(encoding='utf-8'))
HOST=json.loads((HERE/G['host_reference']['geometry_data_relative']).read_text(encoding='utf-8'))
CHAR=Path('D:/UE project/SchoolLife/ArtSource/Characters/StudentChibi/FrontIdle/StudentChibi_Front_Idle.png')
raw=CHAR.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='082ceb410d904f0037dfe09dd3502e50195351691ab4047cc5dbbb639147b8cd'
URI='data:image/png;base64,'+base64.b64encode(raw).decode('ascii')
W,H=3600,3420
ink,muted,accent,line,paper='#243d43','#52676a','#aa7042','#acb9b5','#f6f4ee'
plate=G['carrier_candidate']['color_srgb'];rail='#728180';pad='#535c59'
host_colors={'M1':'#d8d3c5','M2':'#899795'}
out=[f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
 '<title>SchoolLife SL_GE_SIGN_PLATE_01 独立校牌载体设计候选01</title>',
 '<desc>One candidate geometry in cm; 24x84cm folded carrier, 2cm total mounting depth. All dimensions, fastener axes and material are unapproved design candidates. Accepted pillar unchanged. No final school-name graphic.</desc>',
 '<defs><marker id="arr" markerWidth="7" markerHeight="7" refX="3.5" refY="3.5" orient="auto-start-reverse"><path d="M7,0 L0,3.5 L7,7" fill="none" stroke="#52676a" stroke-width="1"/></marker></defs>',
 f'<rect width="{W}" height="{H}" fill="{paper}"/><g font-family="Microsoft YaHei, Noto Sans CJK SC, sans-serif">']
def tx(x,y,s,size=24,fill=ink,anchor='start',weight='normal'):
 out.append(f'<text x="{x:.3f}" y="{y:.3f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{html.escape(str(s))}</text>')
def lines(x,y,ss,size=24,step=39,fill=muted):
 for i,s in enumerate(ss):tx(x,y+i*step,s,size,fill)
def rect(x,y,w,h,fill='none',stroke=line,sw=1.5,dash=None,rx=0):
 out.append(f'<rect x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" rx="{rx}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
def ln(x1,y1,x2,y2,color=line,sw=1.5,dash=None,arrows=False):
 out.append(f'<line x1="{x1:.3f}" y1="{y1:.3f}" x2="{x2:.3f}" y2="{y2:.3f}" stroke="{color}" stroke-width="{sw}"'+(f' stroke-dasharray="{dash}"' if dash else '')+(' marker-start="url(#arr)" marker-end="url(#arr)"' if arrows else '')+'/>')
def poly(points,fill,stroke=ink,sw=1.4,dash=None,opacity=1):
 out.append('<polygon points="'+' '.join(f'{x:.3f},{y:.3f}' for x,y in points)+f'" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{opacity}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
def group(id):out.append(f'<g id="{id}">')
def end():out.append('</g>')
def panel(x,y,w,h,title,sub):
 rect(x,y,w,h,'#fcfbf7',line,1.4,rx=10);tx(x+26,y+48,title,29,ink,weight='bold');tx(x+26,y+87,sub,22,muted)
def dh(x1,x2,y,s,witness_y=None):
 if witness_y is not None:ln(x1,witness_y,x1,y+8);ln(x2,witness_y,x2,y+8)
 ln(x1,y,x2,y,muted,1.3,arrows=True);tx((x1+x2)/2,y-12,s,22,muted,'middle')
def dv(x,y1,y2,s,left=False,witness_x=None):
 if witness_x is not None:ln(witness_x,y1,x,y1);ln(witness_x,y2,x,y2)
 ln(x,y1,x,y2,muted,1.3,arrows=True);tx(x+(-12 if left else 12),(y1+y2)/2+8,s,22,muted,'end' if left else 'start')
def cross(x,y,color=accent,r=8):
 ln(x-r,y,x+r,y,color,2);ln(x,y-r,x,y+r,color,2)
def leader(x1,y1,x2,y2,label,color=muted):
 ln(x1,y1,x2,y2,color,1.4);tx(x2+9,y2+8,label,22,color)

group('header')
tx(70,72,'SchoolLife / 校门入口 · 独立载体',26,muted)
tx(70,139,'SL_GE_SIGN_PLATE_01 · 尺寸与安装候选01',46,ink,weight='bold')
tx(70,188,'推荐 24 × 84 cm / 牌体深 1.0 cm / 含支承总突出 2.0 cm · 全部新增尺寸均待审',27,accent)
tx(3530,77,'2026-10-13',24,muted,'end')
tx(3530,122,'计划1源 / 1目标实例 · 校名仍待确认',25,ink,'end')
tx(3530,167,'定尺设计与材色示意；无模型 / 字面 / UE产出',23,muted,'end')
end()

# Carrier front/rear, generated from the same dimensions and axis convention.
C=G['carrier_candidate'];s=7.0;cz=675
for rear,x,w,title,sub in [(False,70,820,'01 街侧正面 −Y','无成品校名；虚线为20×76字面排布候选区'),
                          (True,920,900,'02 载体背面 +Y','独立载体后视；画面右为−X，不复制正面字')]:
 cx=x+310;group('rear' if rear else 'front');panel(x,230,w,990,title,sub)
 rect(cx-12*s,cz-42*s,24*s,84*s,plate,ink,1.8,rx=C['corner_radius']*s)
 if rear:
  rect(cx-11.8*s,cz-41.8*s,23.6*s,83.6*s,'#8a9898',muted,1,rx=.2*s)
  for ob in G['support_candidates']:
   a,b=ob['min'],ob['max'];rect(cx-b[0]*s,cz-b[2]*s,(b[0]-a[0])*s,(b[2]-a[2])*s,rail,ink,1.3)
  for ob in G['contact_pad_candidates']:
   a,b=ob['min'],ob['max'];rect(cx-b[0]*s,cz-b[2]*s,(b[0]-a[0])*s,(b[2]-a[2])*s,pad,ink,1)
  for ax,ay,az in G['fastener_axes_candidate']:cross(cx-ax*s,cz-az*s,accent,6)
  dh(cx-9*s,cx+9*s,cz-30*s-28,'18',cz-30*s)
  dv(cx+145,cz-30*s,cz+30*s,'60')
  leader(cx+9*s,cz-30*s,x+580,cz-30*s,'上条座 / 2.4高')
  leader(cx+9*s,cz+30*s,x+580,cz+30*s,'下条座 / 2.4高')
  lines(x+34,1090,['两条18×2.4×1.6浅支座，中心距60；0.2隔离垫。','橙色四点为固定轴候选，未设计孔径/孔深。'],22,35)
 else:
  q=C['graphic_area_candidate'];a,b=q['x'];z0,z1=q['z']
  rect(cx+a*s,cz-z1*s,(b-a)*s,(z1-z0)*s,'none','#c7d2cd',1.6,'8 6')
  leader(cx+b*s,cz-z1*s,x+520,cz-z1*s,'字面净宽20')
  leader(cx+b*s,cz+31*s,x+520,cz+31*s,'四周留边2 / 4')
  lines(x+34,1090,['建议优先比较竖向空白排布；语言/横竖待定。','图内无校名、字体或已批准字高。'],22,35)
 dh(cx-12*s,cx+12*s,cz+42*s+56,'宽24',cz+42*s)
 dv(cx-134,cz-42*s,cz+42*s,'高84',True,cx-12*s)
 cross(cx,cz);leader(cx,cz,x+520,cz,'后接触基准轴心投影',accent)
 end()

group('side')
panel(1850,230,780,990,'03 右侧 +X','画面右为+Y；0为后接触面，不是正面')
cx=2160
mp=lambda y,z:(cx+y*36,cz-z*7)
# Separate scalar scales are avoided: body side is uniformly 7px/cm; zoom inset below is uniform 48px/cm.
cx_side=2080;sp=7
rs=lambda y,z:(cx_side+y*sp,cz-z*sp)
a,b=C['front_skin']['min'],C['front_skin']['max'];q=rs(a[1],b[2]);rect(*q,(b[1]-a[1])*sp,(b[2]-a[2])*sp,plate,ink,1)
q=rs(-1.8,42);rect(*q,.8*sp,84*sp,plate,ink,1)
for ob,color in [(t,rail) for t in G['support_candidates']]+[(t,pad) for t in G['contact_pad_candidates']]:
 a,b=ob['min'],ob['max'];q=rs(a[1],b[2]);rect(*q,(b[1]-a[1])*sp,(b[2]-a[2])*sp,color,ink,.8)
ln(cx_side,cz-44*sp,cx_side,cz+44*sp,accent,1.5,'7 5');cross(cx_side,cz)
dv(cx_side-95,cz-42*sp,cz+42*sp,'84',True)
leader(*rs(-2,32),2235,cz-32*sp,'正面 Y−2.0')
leader(*rs(-1,20),2235,cz-20*sp,'折边后缘 Y−1.0')
leader(*rs(0,0),2235,cz,'接触基准 Y0',accent)
lines(1880,1090,['全高侧视：牌体深1.0，总突出2.0。','前皮0.2；折边回深0.8；支座+垫直达后面。'],22,35)
end()

group('top')
panel(2660,230,870,990,'04 顶视 +Z','+Y向上，−Y街侧向下；图为完整安装包络')
cx,cy,st=3085,670,14
# Mapping +Y up; plate front and the two rails share the same top-projected footprints.
rect(cx-12*st,cy+1*st,24*st,1*st,plate,ink,1.8)
ln(cx-12*st,cy+1.8*st,cx+12*st,cy+1.8*st,'#a7b5b2',1)
rect(cx-9*st,cy+.2*st,18*st,1.6*st,rail,ink,1.1)
rect(cx-9*st,cy,18*st,.2*st,pad,ink,1)
ln(cx-200,cy,cx+200,cy,accent,1.5,'7 5');cross(cx,cy)
dh(cx-12*st,cx+12*st,cy+2*st+74,'24',cy+2*st)
dv(cx+12*st+53,cy,cy+2*st,'2.0')
leader(cx+9*st,cy+.5*st,3320,cy-80,'后接触面Y0',accent)
lines(2690,927,['牌体：Y[−2.0,−1.0]，深1.0。','支座：Y[−1.8,−0.2]，深1.6。','隔离垫：Y[−0.2,0]，厚0.2。','叠合含支承：24×84×2.0，不另加高度。'],23,43)
end()

def host_front(cx,base,s,sign=True):
 # Accepted metre mesh data -> centimetres; silhouette profiles are read from its vertex rings.
 vv=HOST['vertices'];rings=[(vv[i][2]*100,abs(vv[i][0])*100) for i in range(0,len(vv),4)]
 for i,((z0,h0),(z1,h1)) in enumerate(zip(rings,rings[1:])):
  zone=HOST['face_zones'][i*4]['material_zone']
  poly([(cx-h0*s,base-z0*s),(cx+h0*s,base-z0*s),(cx+h1*s,base-z1*s),(cx-h1*s,base-z1*s)],host_colors[zone],ink,1)
 if sign:
  h=G['host_reference'];px,py,pz=h['mount_pivot_in_host_candidate'];u=h['usable_area']
  rect(cx+u['x'][0]*s,base-u['z'][1]*s,u['width']*s,u['height']*s,'none',accent,1.6,'8 6')
  rect(cx-12*s,base-(pz+42)*s,24*s,84*s,plate,ink,1.4,rx=.4*s)
  rect(cx-10*s,base-(pz+38)*s,20*s,76*s,'none','#c7d2cd',1,'6 5')
  cross(cx,base-pz*s,accent,6)

group('installed_front')
panel(70,1250,1120,900,'05 南面安装正视 · 左柱候选','宿主底轴心Z0；牌后接触轴心(0,−27,140)cm')
cx,base,hs=400,1964,2.45
host_front(cx,base,hs)
ln(cx-150,base,cx+150,base,ink,2);cross(cx,base)
dv(cx-166,base-240*hs,base,'柱高240',True)
dh(cx-27*hs,cx+27*hs,base-62*hs,'柱身54')
leader(cx+15*hs,base-190*hs,615,base-190*hs,'可用面30×100',accent)
leader(cx+12*hs,base-182*hs,615,base-173*hs,'牌体24×84（候选）')
leader(cx,base-140*hs,615,base-140*hs,'中心高140；上下98—182')
lines(635,1756,['可用区余量：两侧各3，上下各8。','固定轴候选：(±7,−27,110/170)。','左柱底(−330,0,800)，右柱本轮无牌。'],22,39)
lines(100,2070,['牌世界局部包络X[−342,−318] / Y[−29,−27] / Z[898,982]cm。','牌最近通路侧边X−318，距净口边界−300仍18cm；道路500与净口600保持。'],23,39)
end()

group('installation_section')
panel(1220,1250,1000,900,'06 安装侧剖与接触细部','剖示Z70—210；宿主不打孔；不是紧固工程详图')
# Host section crop, all dimensions on a common uniform scale.
ox,by,sc=1610,2010,4.2
p=lambda y,z:(ox+y*sc,by-(z-70)*sc)
a=p(-27,210);rect(*a,54*sc,140*sc,'#e5e0d5',line,1)
ln(*p(-27,210),*p(-27,70),ink,2)
a=p(-29,182);rect(*a,.2*sc,84*sc,plate,ink,1)
a=p(-28.8,182);rect(*a,.8*sc,84*sc,plate,ink,1)
for z in [110,170]:
 a=p(-28.8,z+1.2);rect(*a,1.6*sc,2.4*sc,rail,ink,1)
 a=p(-27.2,z+1.2);rect(*a,.2*sc,2.4*sc,pad,ink,1)
 ln(*p(-29,z),*p(-27,z),accent,1,'3 3')
leader(*p(-27,201),1790,p(-27,201)[1],'柱南面Y−27')
leader(*p(-29,182),1260,p(-29,182)[1]-28,'牌面Y−29',accent)
leader(*p(-27,140),1790,p(-27,140)[1],'后接触轴心Z140',accent)
dv(1435,p(-29,182)[1],p(-29,98)[1],'84',True)
# Enlarged, uniformly scaled local contact section, through the upper rail.
tx(1770,1785,'接触层放大 / 全方向60px·cm⁻¹',20,muted)
zx,zy,ss=1870,1934,60
rect(zx-2*ss,zy-1.2*ss,.2*ss,2.4*ss,plate,ink,1)
rect(zx-1.8*ss,zy-1.2*ss,1.6*ss,2.4*ss,rail,ink,1)
rect(zx-.2*ss,zy-1.2*ss,.2*ss,2.4*ss,pad,ink,1)
rect(zx,zy-1.8*ss,1.4*ss,3.6*ss,'#e5e0d5',line,1)
dh(zx-2*ss,zx,zy+1.2*ss+43,'总突出2.0')
lines(1250,2070,['层叠：前皮0.2 + 支座1.6 + 垫0.2 = 2.0；互相接触，无悬空间隙。','支座前端抵牌背Y−28.8，后垫抵柱Y−27；孔径/孔深/承载待确认。'],22,39)
end()

group('candidate_comparison')
panel(2250,1250,1280,900,'07 尺寸留边比较与字面待定','三档都在30×100可用区内；只推荐中档，不制作三套品牌')
for j,a in enumerate(G['size_comparisons_candidate']):
 cx=2460+j*390;bb=1785;scale=4.5
 rect(cx-15*scale,bb-100*scale,30*scale,100*scale,'none',accent,1.5,'8 5')
 z0=(100-a['height'])/2
 rect(cx-a['width']/2*scale,bb-(z0+a['height'])*scale,a['width']*scale,a['height']*scale,plate,ink,1.4,rx=.4*scale)
 rect(cx-a['graphic_area'][0]/2*scale,bb-(50+a['graphic_area'][1]/2)*scale,a['graphic_area'][0]*scale,a['graphic_area'][1]*scale,'none','#c7d2cd',1,'5 5')
 tx(cx,1832,f"{a['width']} × {a['height']}",27,ink,'middle',weight='bold')
 tx(cx,1874,['小档：更克制','推荐：留边与占面平衡','大档：字面空间较多'][j],23,accent if j==1 else muted,'middle')
 tx(cx,1915,f"侧余{a['side_margin_inside_usable']} / 上下余{a['vertical_margin_inside_usable']}",22,muted,'middle')
lines(2280,1980,['推荐24×84：不占满预留；正式校名若过长，先评字面布局再选档。','三档不是已批准牌尺寸，均不扩大柱；22×76/26×92只是取舍参照。','20×76为空白排布余量，不是字高、字体、语言或校名的最终规格。'],23,42)
end()

# Installed 3D design projections. Only vector illustration geometry is produced.
def sub(a,b):return [a[i]-b[i] for i in range(3)]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def normal(v):
 a=sub(v[1],v[0]);b=sub(v[2],v[0]);n=[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
 L=math.sqrt(dot(n,n));return [x/L for x in n] if L else [0,0,0]
def rounded_profile(w,h,r):
 q=[]
 for cx,cz,a0 in [(w/2-r,-h/2+r,270),(w/2-r,h/2-r,0),(-w/2+r,h/2-r,90),(-w/2+r,-h/2+r,180)]:
  for k in range(7):
   a=math.radians(a0+k*15);q.append((cx+r*math.cos(a),cz+r*math.sin(a)))
 return q
def plate_faces():
 p=rounded_profile(24,84,.4);inside=rounded_profile(23.6,83.6,.2);ff=[]
 # Profile is CCW in XZ; its increasing XZ normal is -Y.
 ff.append(([(x,-2,z) for x,z in p],plate))
 ff.append(([(x,-1.8,z) for x,z in reversed(p)],'#819292'))
 for j in range(len(p)):
  k=(j+1)%len(p)
  # Front-skin edge; outward side face.
  ff.append(([(p[j][0],-2,p[j][1]),(p[j][0],-1.8,p[j][1]),(p[k][0],-1.8,p[k][1]),(p[k][0],-2,p[k][1])],plate))
  ff.append(([(p[j][0],-1.8,p[j][1]),(p[j][0],-1,p[j][1]),(p[k][0],-1,p[k][1]),(p[k][0],-1.8,p[k][1])],plate))
  # Inner return and rear lip keep the tray back open.
  ff.append(([(inside[j][0],-1.8,inside[j][1]),(inside[k][0],-1.8,inside[k][1]),(inside[k][0],-1,inside[k][1]),(inside[j][0],-1,inside[j][1])],plate))
  ff.append(([(p[j][0],-1,p[j][1]),(inside[j][0],-1,inside[j][1]),(inside[k][0],-1,inside[k][1]),(p[k][0],-1,p[k][1])],plate))
 return ff
def box_faces(ob,color):
 a,b=ob['min'],ob['max'];v=[(a[0],a[1],a[2]),(b[0],a[1],a[2]),(b[0],b[1],a[2]),(a[0],b[1],a[2]),
                           (a[0],a[1],b[2]),(b[0],a[1],b[2]),(b[0],b[1],b[2]),(a[0],b[1],b[2])]
 return [([v[i] for i in f],color) for f in [(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]]
def shade(c,n):
 l=[-.5,-.6,1];L=math.sqrt(dot(l,l));l=[a/L for a in l];k=.75+.25*max(0,dot(l,n))
 return '#'+''.join(f'{round(int(c[i:i+2],16)*k):02x}' for i in [1,3,5])
def installed_iso(x,az,ghost=False):
 group('installed_iso_'+str(az));panel(x,2190,1300,1050,'08 西南 → 东北' if az==225 else '09 东北 → 西南 · 宿主剖透',
  '225° / 俯角30°；南面牌，不制作校名字面' if az==225 else '45° / 俯角30°；仅图层剖透，隐蔽支承并非现实可见')
 cx,by,sc=x+560,3034,2.9;a=math.radians(az);e=math.radians(30)
 cam=[math.cos(e)*math.cos(a),math.cos(e)*math.sin(a),math.sin(e)]
 def pr(p):
  xx,yy,zz=p;return [cx+sc*(-math.sin(a)*xx+math.cos(a)*yy),by+sc*(math.sin(e)*(math.cos(a)*xx+math.sin(a)*yy)-math.cos(e)*zz)]
 faces=[]
 for f,z in zip(HOST['faces'],HOST['face_zones']):faces.append(([tuple(v*100 for v in HOST['vertices'][i]) for i in f],host_colors[z['material_zone']],True))
 pivot=G['host_reference']['mount_pivot_in_host_candidate']
 for verts,col in plate_faces()+sum([box_faces(o,rail) for o in G['support_candidates']],[])+sum([box_faces(o,pad) for o in G['contact_pad_candidates']],[]):
  faces.append(([[q[i]+pivot[i] for i in range(3)] for q in verts],col,False))
 faces.sort(key=lambda f:dot([sum(v[k] for v in f[0])/len(f[0]) for k in range(3)],cam))
 for vv,col,is_host in faces:
  nn=normal(vv)
  if dot(nn,cam)<=1e-7:continue
  poly([pr(v) for v in vv],shade(col,nn),'#acb8b2' if ghost and is_host else ink,1 if is_host else .9,
       opacity=.16 if ghost and is_host else 1)
 # Graphic allowance and mounting axes are annotations only.
 if not ghost:
  q=C['graphic_area_candidate'];pts=[(q['x'][0],-29,102),(q['x'][1],-29,102),(q['x'][1],-29,178),(q['x'][0],-29,178)]
  poly([pr(v) for v in pts],'none','#c7d2cd',1.2,'6 4')
 else:
  for q in G['fastener_axes_candidate']:
   pp=pr([q[i]+pivot[i] for i in range(3)]);cross(*pp,accent,r=5)
 pp=pr(pivot);cross(*pp,accent,r=7)
 leader(*pp,x+900,pp[1],('南面接触基准' if not ghost else '隐蔽挂点投影'),accent)
 pp=pr((0,0,0));cross(*pp,accent,r=8);tx(pp[0]+22,pp[1]+30,'柱底轴心',21,accent)
 lines(x+28,3138,['载体始终安装在−Y南面；两向共用一套厘米数据和宿主坐标。',
                 '矢量面明暗为设计材色示意，非Blender自然光渲染或实际游戏效果。'],22,36)
 end()
installed_iso(70,225,False);installed_iso(1400,45,True)

group('scale_and_surface')
panel(2730,2190,800,1050,'10 人物尺度与材色参照','原128×128 PNG字节嵌入；载体不是128cm或128px')
base,ss=2940,2.15
host_front(2912,base,ss)
cx=3300;visible=180*ss;full=visible*128/116
out.append(f'<g id="original_character_scale"><image x="{cx-full*64.5/128:.3f}" y="{base-visible-full*4/128:.3f}" width="{full:.3f}" height="{full:.3f}" image-rendering="pixelated" preserveAspectRatio="none" xlink:href="{URI}"/></g>')
dv(3135,base-180*ss,base,'180',True);dv(3460,base-192*ss,base,'192')
tx(3310,base+38,'原正面比例层',22,muted,'middle')
tx(2912,base+38,'柱240 / 牌84',22,muted,'middle')
rect(2770,3030,42,29,plate,'none');tx(2828,3055,'哑光青灰涂装金属候选',23)
lines(2760,3111,['载体64px/m参考：24×84约15×54像素。','字面20×76在64下仅约13×49，密度须另定。','校名/语言/横竖排/字高/字体均待确认。'],21,34)
end()

group('footer')
ln(70,3302,3530,3302,line,1.5)
tx(70,3347,'单位cm；新尺寸、支座及固定轴均为候选。牌整体24×84×2.0，安装后Y[−29,−27]，未超柱原有Y−30最外包络。',23,muted)
tx(70,3390,'同一SL_GE_SIGN_PLATE_01_GEOMETRY.json生成所有视图；门柱Trial01/字节/V13/SchoolLife原源保持。仅设计，交付后停审。',23,muted)
end();end();out.append('</svg>')
(HERE/'SL_GE_SIGN_PLATE_01_DESIGN.svg').write_text('\n'.join(out),encoding='utf-8',newline='\n')
print('SVG',W,H,'cm candidate; no model generated; original character SHA preserved')
