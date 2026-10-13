"""Rebuild editable design SVG from one centimetre-based source; no mesh/Blender/UE.
Run with Python + Pillow. Rasterize the SVG separately, at its native 3200 x 3100.
"""
from pathlib import Path
import base64, hashlib, html, json, math
from PIL import Image

HERE = Path(__file__).resolve().parent
G = json.loads((HERE / 'SL_GE_GATE_PIER_01_GEOMETRY.json').read_text(encoding='utf-8'))
CHAR = Path(G['character_reference']['path'])
raw = CHAR.read_bytes()
im = Image.open(CHAR)
assert im.size == (128, 128) and im.getbbox() == (31, 4, 98, 120)
assert hashlib.sha256(raw).hexdigest() == '082ceb410d904f0037dfe09dd3502e50195351691ab4047cc5dbbb639147b8cd'
URI = 'data:image/png;base64,' + base64.b64encode(raw).decode('ascii')
W, H = 3200, 3100
ink, muted, accent, line, paper = '#243d43', '#58696c', '#b87841', '#a9b8b5', '#f6f4ee'
colors = {'M1': '#d8d3c5', 'M2': '#899795', 'M3': '#64706d'}
out = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
       '<title>SL_GE_GATE_PIER_01 定尺设计候选01</title>',
       '<desc>Five orthographic and two opposite 30-degree views derived from one centimetre geometry source. Embedded character PNG is byte-exact. Diagram only, no game render.</desc>',
       '<defs><marker id="arr" markerWidth="7" markerHeight="7" refX="3.5" refY="3.5" orient="auto-start-reverse"><path d="M7,0 L0,3.5 L7,7" fill="none" stroke="#58696c" stroke-width="1"/></marker></defs>',
       f'<rect width="{W}" height="{H}" fill="{paper}"/>',
       '<g font-family="Microsoft YaHei, Noto Sans CJK SC, sans-serif">']

def tx(x, y, s, size=24, fill=ink, anchor='start', weight='normal'):
    out.append(f'<text x="{x:.3f}" y="{y:.3f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{html.escape(str(s))}</text>')

def lines(x, y, texts, size=24, step=38, fill=muted):
    for i, t in enumerate(texts): tx(x, y+i*step, t, size, fill)

def rect(x, y, w, h, fill='none', stroke=line, sw=1.5, dash=None, rx=0):
    out.append(f'<rect x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')

def ln(x1, y1, x2, y2, stroke=line, sw=1.5, dash=None, arrows=False):
    out.append(f'<line x1="{x1:.3f}" y1="{y1:.3f}" x2="{x2:.3f}" y2="{y2:.3f}" stroke="{stroke}" stroke-width="{sw}"' + (f' stroke-dasharray="{dash}"' if dash else '') + (' marker-start="url(#arr)" marker-end="url(#arr)"' if arrows else '') + '/>')

def poly(points, fill, stroke=ink, sw=1.5, dash=None):
    coords = ' '.join(f'{x:.3f},{y:.3f}' for x, y in points)
    out.append(f'<polygon points="{coords}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')

def group(id): out.append(f'<g id="{id}">')
def end(): out.append('</g>')

def dh(x1, x2, y, label, witness_y=None):
    if witness_y is not None:
        ln(x1,witness_y,x1,y+8); ln(x2,witness_y,x2,y+8)
    ln(x1,y,x2,y,muted,1.3,arrows=True); tx((x1+x2)/2,y-12,label,22,muted,'middle')

def dv(x, y1, y2, label, side='right', witness_x=None):
    if witness_x is not None:
        ln(witness_x,y1,x,y1); ln(witness_x,y2,x,y2)
    ln(x,y1,x,y2,muted,1.3,arrows=True)
    tx(x+(12 if side=='right' else -12),(y1+y2)/2+8,label,22,muted,'start' if side=='right' else 'end')

def pivot(x,y):
    ln(x-12,y,x+12,y,accent,2); ln(x,y-12,x,y+12,accent,2)
    out.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{paper}" stroke="{accent}" stroke-width="2"/>')

def panel(x,y,w,h,title,kicker=None):
    rect(x,y,w,h,'#fcfbf7',line,1.4,rx=10)
    tx(x+26,y+48,title,30,ink,weight='bold')
    if kicker: tx(x+26,y+85,kicker,22,muted)

group('header')
tx(70,75,'SchoolLife  /  校门入口',26,muted)
tx(70,137,'SL_GE_GATE_PIER_01 · 一侧门柱',48,ink,weight='bold')
tx(70,187,'设计候选 01  ·  一个源 / 左右复用两次  ·  60 × 60 × 240 cm  ·  待用户审阅',27,muted)
tx(3130,80,'2026-10-13',24,muted,'end')
tx(3130,123,'写实结构 / 像素表面 / 自然昼光',25,ink,'end')
tx(3130,166,'定尺图与示意预览；实际游戏效果未验证',24,accent,'end')
end()

# All silhouettes come directly from the same square rings.
S, baseY = 2.45, 934
for i, (name, title, direction, left_label, right_label) in enumerate([
    ('south','01 南正面','街侧 −Y；画面右 +X','−X 西','+X 东'),
    ('north','02 北背面','校内 +Y；画面右 −X','+X 东','−X 西'),
    ('east','03 东侧','观察 +X；画面右 +Y','−Y 南','+Y 北'),
    ('west','04 西侧','观察 −X；画面右 −Y','+Y 北','−Y 南')]):
    x=70+i*580; cx=x+245
    group(name+'_orthographic')
    panel(x,230,550,866,title,direction)
    for part in G['parts']:
        rings=part['rings_z_halfwidth']
        points=[(cx-h*S,baseY-z*S) for z,h in rings] + [(cx+h*S,baseY-z*S) for z,h in reversed(rings)]
        poly(points,colors[part['material']])
    # Ring boundaries and a hidden underside drip-groove indication.
    for z,h in [(28,30),(32,27),(224,30),(237,30),(238,29)]: ln(cx-h*S,baseY-z*S,cx+h*S,baseY-z*S,ink,1)
    ln(cx-28*S,baseY-224.5*S,cx+28*S,baseY-224.5*S,muted,1,'4 4')
    if name=='south':
        q=G['sign_reserve']; z0,z1=q['z']; x0,x1=q['x']
        rect(cx+x0*S,baseY-z1*S,(x1-x0)*S,(z1-z0)*S,'none',accent,2,'8 6')
        tx(cx,baseY-148*S,'预留',21,accent,'middle')
        tx(cx,baseY-135*S,'无牌',19,accent,'middle')
        ln(cx+15*S,baseY-190*S,cx+122,baseY-190*S,accent,1.5)
        tx(cx+132,baseY-190*S+8,'Z190',20,accent)
        ln(cx+15*S,baseY-90*S,cx+122,baseY-90*S,accent,1.5)
        tx(cx+132,baseY-90*S+8,'Z90',20,accent)
        dh(cx-15*S,cx+15*S,baseY-75*S,'30',baseY-90*S)
    ln(cx-117,baseY,cx+117,baseY,ink,2)
    pivot(cx,baseY)
    dv(cx-120,baseY-240*S,baseY,'240','left',cx-30*S)
    dh(cx-30*S,cx+30*S,baseY+52,'60',baseY)
    dh(cx-27*S,cx+27*S,baseY-200*S,'54')
    if name!='south':
        dv(cx+112,baseY-240*S,baseY-224*S,'16',witness_x=cx+30*S)
        dv(cx+112,baseY-224*S,baseY-32*S,'192',witness_x=cx+30*S)
        dv(cx+112,baseY-32*S,baseY,'32',witness_x=cx+30*S)
    tx(cx-117,baseY+105,left_label,21,muted)
    tx(cx+117,baseY+105,right_label,21,muted,'end')
    end()

group('top_orthographic')
panel(2390,230,740,866,'05 顶视','观察 +Z；+Y 朝上 / +X 朝右')
cx,cy,ts=2760,602,5.2
rect(cx-30*ts,cy-30*ts,60*ts,60*ts,colors['M2'],ink,2)
rect(cx-29*ts,cy-29*ts,58*ts,58*ts,'#96a3a0',ink,1)
rect(cx-6*ts,cy-6*ts,12*ts,12*ts,'#adb7b1',ink,1)
for ax,ay in [(-1,-1),(1,-1),(1,1),(-1,1)]: ln(cx+ax*29*ts,cy+ay*29*ts,cx+ax*6*ts,cy+ay*6*ts,muted,1)
rect(cx-27*ts,cy-27*ts,54*ts,54*ts,'none',muted,1,'7 5')
dh(cx-30*ts,cx+30*ts,cy+30*ts+56,'60',cy+30*ts)
dv(cx+30*ts+53,cy-30*ts,cy+30*ts,'60')
dh(cx-6*ts,cx+6*ts,cy-6*ts-22,'12')
ln(cx,cy-190,cx,cy-230,accent,2); tx(cx,cy-249,'北 +Y',23,accent,'middle')
ln(cx-40,cy+30*ts,cx+40,cy+30*ts,accent,5)
tx(cx,cy+30*ts-18,'南面预留方向',22,accent,'middle')
lines(2420,924,['虚线：下方 54 × 54 柱身轮廓','顶缘 Z238 → 中央 Z240，浅四向排水坡','中央顶面 12 × 12；顶帽最大 60 × 60'],24,43)
end()

def proj(p, az, cx, cy, s=2.35):
    x,y,z=p; a=math.radians(az); e=math.radians(30)
    right=(-math.sin(a),math.cos(a)); d=(math.cos(a),math.sin(a))
    return (cx+s*(right[0]*x+right[1]*y),cy+s*(math.sin(e)*(d[0]*x+d[1]*y)-math.cos(e)*z))

def shade(color, normal):
    v=G['light_preview_direction']; n=math.sqrt(sum(t*t for t in v)); v=[t/n for t in v]
    factor=.72+.28*max(0,sum(a*b for a,b in zip(v,normal)))
    return '#'+''.join(f'{min(255,round(int(color[i:i+2],16)*factor)):02x}' for i in (1,3,5))

def view3d(x,az,title,subtitle):
    group('axonometric_'+str(az)); panel(x,1130,1010,910,title,subtitle)
    cx,cy,s=x+540,1800,2.1
    # Same physical light in both views. No baked cast shadow.
    pp=lambda p:proj(p,az,cx,cy,s)
    poly([pp(p) for p in [(-150,-30,0),(55,-30,0),(55,30,0),(-150,30,0)]],'#eeeee6',line,1)
    for part in G['parts']:
        rings=part['rings_z_halfwidth']
        for (z0,h0),(z1,h1) in zip(rings,rings[1:]):
            b=[(-h0,-h0,z0),(h0,-h0,z0),(h0,h0,z0),(-h0,h0,z0)]
            t=[(-h1,-h1,z1),(h1,-h1,z1),(h1,h1,z1),(-h1,h1,z1)]
            for j,norm in [(0,(0,-1,0)),(1,(1,0,0)),(2,(0,1,0)),(3,(-1,0,0))]:
                a=math.radians(az)
                if norm[0]*math.cos(a)+norm[1]*math.sin(a)<=0: continue
                nz=(h0-h1)/(z1-z0) if h0!=h1 else 0
                nn=(norm[0],norm[1],nz); L=math.sqrt(sum(v*v for v in nn)); nn=tuple(v/L for v in nn)
                poly([pp(b[j]),pp(b[(j+1)%4]),pp(t[(j+1)%4]),pp(t[j])],shade(colors[part['material']],nn))
        z,h=rings[-1]
        # Exposed horizontal shelves at the base and cap are represented by their rings.
        if part['id']=='cap': poly([pp((-h,-h,z)),pp((h,-h,z)),pp((h,h,z)),pp((-h,h,z))],shade(colors['M2'],(0,0,1)))
    if az==225:
        q=G['sign_reserve']; y=q['face_y']; x0,x1=q['x']; z0,z1=q['z']
        poly([pp((x0,y,z0)),pp((x1,y,z0)),pp((x1,y,z1)),pp((x0,y,z1))],'none',accent,2,'8 5')
        p=pp((15,y,140)); ln(p[0],p[1],x+870,p[1],accent,1.5); tx(x+883,p[1]+8,'候选预留区',22,accent)
    p=pp((0,0,0)); pivot(*p)
    # Original sprite as independent scale layer; alpha bbox, not 128px canvas, is 180cm.
    group('character_original_'+str(az))
    ground=pp(tuple(G['character_reference']['world_billboard_position_cm']))
    visible=180*s*math.cos(math.radians(30)); full=visible*128/116
    xx=ground[0]-full*(64.5/128); yy=ground[1]-visible-full*(4/128)
    out.append(f'<image x="{xx:.3f}" y="{yy:.3f}" width="{full:.3f}" height="{full:.3f}" image-rendering="pixelated" preserveAspectRatio="none" xlink:href="{URI}"/>')
    # Capsule is separate documentation overlay, not collision design for this module.
    capheight=192*s*math.cos(math.radians(30)); capwidth=68*s
    rect(ground[0]-capwidth/2,ground[1]-capheight,capwidth,capheight,'none',accent,1.5,'8 7',rx=capwidth/2)
    dx=ground[0]+(-112 if az==225 else 120)
    dv(dx,ground[1]-visible,ground[1],'180',side='left' if az==225 else 'right')
    dx2=ground[0]+(-184 if az==225 else 193)
    dv(dx2,ground[1]-capheight,ground[1],'192',side='left' if az==225 else 'right')
    end()
    # Small axis indicator, common coordinate source.
    o=pp((75,65,0))
    for vec,label,col in [((30,0,0),'+X',muted),((0,30,0),'+Y',muted),((0,0,30),'+Z',accent)]:
        p2=pp((75+vec[0],65+vec[1],vec[2])); ln(*o,*p2,col,2); tx(p2[0]+7,p2[1]-5,label,20,col)
    lines(x+28,1960,['原人物正面 PNG 独立比例层：可见高 180 cm / 虚线胶囊 192 × Ø68 cm',
                       '两向同几何、同光方向；人物不代表背面造型。无实际 UE 光照/通行验收。'],21,33)
    end()

view3d(70,225,'06 西南 → 东北','正交比例预览；方位角 225° / 俯角 30°；南面 + 西面')
view3d(1110,45,'07 东北 → 西南','正交比例预览；方位角 45° / 俯角 30°；北面 + 东面')

group('interface_plan_and_ground')
panel(2150,1130,980,910,'08 底轴心与接口','施工参照图；实例仅示意，不创建整门或地面')
px,py,ps=2640,1606,.85
mp=lambda x,y:(px+x*ps,py-y*ps)
a=G['platform']['min']; b=G['platform']['max']
q=mp(a[0],b[1]); rect(*q,(b[0]-a[0])*ps,(b[1]-a[1])*ps,'#eceee7',line,1)
# A centre road band only as retained width reference.
q=mp(-250,450); rect(*q,500*ps,500*ps,'#dde5df','none')
for pos in G['future_instances']:
    xx,yy,_=pos; q=mp(xx-30,yy+30); rect(*q,60*ps,60*ps,colors['M2'],ink,1.5); pivot(*mp(xx,yy))
dh(*[mp(-300,0)[0],mp(300,0)[0]],py-75,'最小净开口 600',py-30*ps)
dh(mp(-250,0)[0],mp(250,0)[0],py-166,'保留道路 500')
dh(mp(-400,0)[0],mp(400,0)[0],py+92,'既有平台 800',py+50*ps)
tx(px,1192,'北 +Y ↑',22,accent,'middle')
tx(px,py+40,'南 −Y / 街侧',22,accent,'middle')
tx(mp(-330,0)[0],py+151,'左 (−330, 0, 800)',20,muted,'middle')
tx(mp(330,0)[0],py+151,'右 (+330, 0, 800)',20,muted,'middle')
lines(2180,1820,['源底轴心 (0, 0, 0)，+Z 上；平台顶 = 工程 Z800。',
                  '柱底平落平台；无外露脚板、台阶或新增地面层。',
                  '基础埋置/墙接口待工程核实，本图不设锚栓或基础。',
                  '旧中心 Z920 → 新底轴心 Z800；勿沿用旧中心高度。'],22,40)
end()

group('materials_and_density')
panel(70,2070,2050,860,'09 材质分区与像素密度比较','纹理示意：同一程序化色块场按两档采样，无照片、无贴图通道或最终纹理产出')
palette=['#c9c4b7','#cfcabc','#d5d0c2','#dad5c8','#dfdacd','#e3ded2']
def sample(u,v):
    # Sparse, broad mineral patches and two restrained rain traces. No random noise.
    value=.62+.055*math.sin(u*8+v*4)+.035*math.cos(v*11-u*3)
    value-=.10*math.exp(-((u-.23)**2/.0012+(v-.45)**2/.085))
    value-=.07*math.exp(-((u-.78)**2/.001+(v-.64)**2/.04))
    for a,b in [(.08,.17),(.42,.69),(.68,.28),(.86,.87),(.31,.39)]:
        value-=.07*math.exp(-((u-a)**2+(v-b)**2)/.0007)
    return palette[max(0,min(5,int(value*7)))]
for j,N in enumerate(G['density_candidates_px_per_m']):
    x=110+j*1000; y=2294; size=360; step=size/N
    group('density_'+str(N))
    tx(x,y-37,('A · 32 px/m' if N==32 else 'B · 64 px/m（推荐试用）'),30,ink,weight='bold')
    out.append('<g shape-rendering="crispEdges">')
    for row in range(N):
        for col in range(N): rect(x+col*step,y+row*step,step,step,sample((col+.5)/N,(row+.5)/N),'none',0)
    out.append('</g>')
    rect(x,y,size,size,'none',line,1)
    tx(x,y+size+35,'同一 1 × 1 m 表面样块 / 放大阅读',22,muted)
    lines(x+395,y+42,(['较粗的环境像素','54 cm 柱身宽 ≈ 17 px','192 cm 柱身高 ≈ 61 px','适合远景；小接缝更易消失'] if N==32 else
                     ['适中、保留细部边界','54 cm 柱身宽 ≈ 35 px','192 cm 柱身高 ≈ 123 px','先用游戏镜头验证；未冻结']),23,43)
    end()
lines(110,2805,['M1 暖灰矿物抹面：大块色阶、少量雨痕；M2 青灰细洗石混凝土：台座 / 压顶；M3 压顶下 0.6 cm 座浆缝。',
                '密度按真实米制统一；最终贴图/图集尺寸待 UV 排布。接缝与小倒角优先由几何/后续材质表达，基础色不烘太阳阴影。'],23,40)
end()

group('structure_notes')
panel(2150,2070,980,860,'10 推荐结构与审阅点','台座 + 柱身 + 压顶共同构成一个单体模块')
for i,(id,label) in enumerate([('M1','M1 暖灰矿物抹面'),('M2','M2 青灰细洗石混凝土'),('M3','M3 克制灰色座浆缝')]):
    rect(2180,2196+i*49,35,27,colors[id],'none'); tx(2230,2219+i*49,label,24,ink)
lines(2180,2383,['台座：最大 60 × 60 × 32；底 58 × 58。',
                  '底缘 1 cm 内收倒角；Z28→32 收到 54 × 54。',
                  '柱身：54 × 54；Z32→224，共 192 cm。',
                  '柱身基体连续，顶下 0.6 cm 为座浆缝示意。',
                  '压顶：最大 60 × 60 × 16；每侧出挑 3 cm。',
                  '顶缘 Z238，中央 Z240；低缓四向排水坡。',
                  '底部环形滴水槽候选 0.6 宽 / 0.5 深（内凹）。',
                  '南面安装区：30 宽 × 100 高，Z90→190。',
                  '虚线仅标可用区域；孔位、校牌厚度仍待核。'],23,42)
lines(2180,2830,['审阅：台座/压顶比例、材色、密度与预留区域。',
                  '保留 600 净口；柱身段净口 606，最窄处为 600。'],22,37,accent)
end()

group('footer')
ln(70,2970,3130,2970,line,1.5)
tx(70,3012,'全部几何来自 SL_GE_GATE_PIER_01_GEOMETRY.json；标注单位 cm。正交立面比例 2.45 px/cm，顶视 5.2 px/cm。',23,muted)
tx(70,3053,'尺寸依据：Step2 ActorRecipe / Step1 Plan；V13 1.5 × 3 m 足迹仅历史候选，未回写。源角色 128 × 128 原字节嵌入。',23,muted)
tx(3130,3088,'设计阶段  /  未建模 · 未 UV · 未导入 UE',22,accent,'end')
end(); end(); out.append('</svg>')
(HERE/'SL_GE_GATE_PIER_01_DESIGN.svg').write_text('\n'.join(out),encoding='utf-8')
print('SVG written:',W,H,'character SHA256:',hashlib.sha256(raw).hexdigest())
