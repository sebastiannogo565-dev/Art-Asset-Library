"""Label actual Blender render frames and assemble evidence boards; no AI repainting.
Python + Pillow. Raw A/B frames remain preserved in Previews/Renders.
"""
from pathlib import Path
import json, math
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent.parent
CACHE=ROOT.parents[3]/'.cache/gate-pier-trial01'
M=json.loads((ROOT/'Source/blender_measurements.json').read_text(encoding='utf-8'))
V=json.loads((ROOT/'Source/verification_results.json').read_text(encoding='utf-8'))
FONT='C:/Windows/Fonts/msyh.ttc';BOLD='C:/Windows/Fonts/msyhbd.ttc'
ink='#243d43';muted='#526669';accent='#9b643a';paper='#f6f4ee';border='#b5bfba'
def font(size,bold=False):return ImageFont.truetype(BOLD if bold else FONT,size)
def text(d,x,y,s,size=25,color=ink,bold=False,anchor=None):d.text((x,y),s,font=font(size,bold),fill=color,anchor=anchor)
def paragraph(d,x,y,rows,size=25,step=40,color=muted):
 for i,s in enumerate(rows):text(d,x,y+i*step,s,size,color)
def dashed(d,a,b,fill=accent,width=2):
 x1,y1=a;x2,y2=b;length=math.hypot(x2-x1,y2-y1)
 for t in range(0,int(length),14):
  aa=t/length;bb=min(t+8,length)/length;d.line((x1+(x2-x1)*aa,y1+(y2-y1)*aa,x1+(x2-x1)*bb,y1+(y2-y1)*bb),fill=fill,width=width)
def dim_vertical(d,x,y0,y1,label,right):
 dashed(d,(x,y0),(x,y1));d.line((x-9,y0,x+9,y0),fill=accent,width=2);d.line((x-9,y1,x+9,y1),fill=accent,width=2)
 text(d,x+(14 if right else -14),(y0+y1)/2,label,24,accent,anchor='lm' if right else 'rm')
def dim_h(d,x1,x2,y,label):
 d.line((x1,y,x2,y),fill=muted,width=2)
 for x in [x1,x2]:d.line((x,y-8,x,y+8),fill=muted,width=2)
 text(d,(x1+x2)/2,y-12,label,23,muted,anchor='ms')

for key in ['A','B']:
 raw=ROOT/f'Previews/Renders/SL_GE_GATE_PIER_01_TRIAL_VIEW_{key}_RENDER.png'
 im=Image.open(raw).convert('RGB');assert im.size==(1600,1400);d=ImageDraw.Draw(im)
 d.rectangle((0,0,1600,118),fill=paper);d.rectangle((0,1280,1600,1400),fill=paper)
 text(d,42,22,'SL_GE_GATE_PIER_01 · 单体试作01',34,bold=True)
 label='A 西南 → 东北 / 225°' if key=='A' else 'B 东北 → 西南 / 45°'
 text(d,42,76,label+' · 俯角30° · 正交 · 同一模型 / UV / 中性日光',24,muted)
 text(d,1560,32,'64 px/m 临时材质',26,accent,anchor='ra')
 pts=M['views'][key]['reference_points_px'];cx=pts['0'][0];foot=pts['0'][1]
 right=key=='B';delta=1 if right else -1
 dim_vertical(d,cx+delta*250,pts['1.8'][1],foot,'约180 cm',right)
 dim_vertical(d,cx+delta*390,pts['1.92'][1],foot,'192 cm',right)
 text(d,cx,foot+24,'原正面PNG · 独立比例板',23,accent,anchor='ma')
 paragraph(d,42,1296,['实际网格 60×60×240 cm · 台座32 / 柱身192（含座浆0.6）/ 压顶16 · 底中心轴心，街侧 −Y',
                     '原人物128×128字节未改；116px可见高按约180cm。192×Ø68cm胶囊另作参照，不是柱碰撞规格。',
                     '柱体与阴影为真实Cycles日光渲染；人物比例板不受照明，不代表背面八向。试作材质未最终批准，UE未验。'],21,31)
 im.save(ROOT/f'Previews/SL_GE_GATE_PIER_01_TRIAL_VIEW_{key}.png')

# Four native metre samples; enlarged by exact nearest-neighbour integer factors.
im=Image.new('RGB',(2300,1560),paper);d=ImageDraw.Draw(im)
text(d,60,35,'SL_GE_GATE_PIER_01 · M1 / M2 临时材质与像素密度',40,bold=True)
text(d,60,101,'下方样块为无光照基础色；四张同1×1m。整柱64px/m实际效果见日光预览A/B。',26,muted)
for zone,y in [('M1',220),('M2',900)]:
 title='M1 暖灰矿物抹面' if zone=='M1' else 'M2 青灰细洗石混凝土'
 text(d,80,y-66,title,30,bold=True)
 for j,N in enumerate([32,64]):
  x=80+j*570
  sample=Image.open(ROOT/f'Textures/Samples/{zone}_{N}px_per_m_1m.png').convert('RGB');assert sample.size==(N,N)
  im.paste(sample.resize((384,384),Image.Resampling.NEAREST),(x,y));d.rectangle((x,y,x+384,y+384),outline=border,width=2)
  text(d,x,y+409,f'{N} px/m · 原生{N}×{N} · 1×1 m',24,muted)
  text(d,x,y+450,'32 仅比较' if N==32 else '64 优先试作',25,accent)
 rows=(['宽缓色阶与少量短雨痕','没有固定阳光阴影','54cm柱面宽约35px','191.4cm实体高约122px'] if zone=='M1' else
       ['较深矿物底色','少量低对比聚簇','同程序材色场按米制采样','非照片缩小或碎噪滤镜'])
 paragraph(d,1080,y+70,rows,24,46)
text(d,1540,157,'共享BaseColor图集 · 原生256×256',25,bold=True)
atlas=Image.open(ROOT/'Textures/SL_GE_GATE_PIER_01_TRIAL_BaseColor.png').convert('RGB')
im.paste(atlas.resize((512,512),Image.Resampling.NEAREST),(1540,220));d.rectangle((1540,220,2052,732),outline=border,width=2)
paragraph(d,1540,770,['1个材质槽 / 1个BaseColor + 1个Roughness','四向侧面 + 底面 + 顶面，6个UV岛','64px/m；留4px边界复制；Closest采样'],23,36)
text(d,1540,895,'实际UV布局 · 原生256×256（放大2倍）',24,bold=True)
layout=Image.open(ROOT/'Textures/SL_GE_GATE_PIER_01_TRIAL_UV_LAYOUT.png').convert('RGB')
im.paste(layout.resize((512,512),Image.Resampling.NEAREST),(1540,940));d.rectangle((1540,940,2052,1452),outline=border,width=2)
text(d,60,1464,'0.6cm座浆带 = 0.384px：保实体高度、与M1同材，不强画黑线。滴水槽本试作省略，待规划审阅。',24,accent)
text(d,60,1511,'样块不是独立资产或最终纹理；环境不统一设128。最终过滤、曝光与亚像素稳定性留UE接入另验。',23,muted)
im.save(ROOT/'Previews/SL_GE_GATE_PIER_01_TRIAL_MATERIAL_COMPARE.png')

# Workbench mesh views + measurements from the actual separate validation scene.
im=Image.new('RGB',(2600,1450),paper);d=ImageDraw.Draw(im)
text(d,60,35,'SL_GE_GATE_PIER_01 · 实际网格与接口检查',40,bold=True)
text(d,60,103,'五面为同一试作网格的Blender Workbench轮廓检查，不是旧设计图或自然光材质预览。',26,muted)
for j,(key,title) in enumerate([('SOUTH','南正面 −Y'),('NORTH','北背面 +Y'),('EAST','东侧 +X'),('WEST','西侧 −X'),('TOP','顶视 +Z / +Y上')]):
 x=60+j*500;image=Image.open(CACHE/f'CHECK_{key}.png').convert('RGB');assert image.size==(480,680)
 text(d,x+240,171,title,25,ink,anchor='ma');im.paste(image,(x,222));d.rectangle((x,222,x+480,902),outline=border,width=2)
 text(d,x+240,922,'60 × 60 cm' if key=='TOP' else '宽60 / 高240 cm',22,muted,anchor='ma')
text(d,60,983,'独立验证组 · 实际两实例与平台包络',28,bold=True)
v=M['validation_scene'];platform=v['platform'];instances=v['instances'];px,py,s=350,1260,54
coord=lambda x,y:(px+x*s,py-y*s)
pmin=platform['bounds_m']['min'];pmax=platform['bounds_m']['max'];p1=coord(pmin[0],pmax[1]);p2=coord(pmax[0],pmin[1])
d.rectangle((*p1,*p2),fill='#e5e9df',outline=border,width=2)
road1=coord(-2.5,pmax[1]);road2=coord(2.5,pmin[1]);d.rectangle((*road1,*road2),fill='#d5e0d8')
for ob in instances:
 mn=ob['bounds_m']['min'];mx=ob['bounds_m']['max'];a=coord(mn[0],mx[1]);b=coord(mx[0],mn[1])
 d.rectangle((*a,*b),fill='#899795',outline=ink,width=2)
 cx,cy=coord(*ob['origin_m'][:2]);d.line((cx-7,cy,cx+7,cy),fill=accent,width=2);d.line((cx,cy-7,cx,cy+7),fill=accent,width=2)
dim_h(d,coord(instances[0]['bounds_m']['max'][0],0)[0],coord(instances[1]['bounds_m']['min'][0],0)[0],1188,'最小净口600 cm')
dim_h(d,coord(-2.5,0)[0],coord(2.5,0)[0],1118,'道路500 cm参照')
dim_h(d,p1[0],p2[0],1355,'平台800 × 500 cm / 顶Z800')
text(d,px,1375,'柱底轴心 (±330,0,800) cm',22,accent,anchor='ma')
source=M['mesh'];uv=V['uv_density_px_per_m']
paragraph(d,800,1003,[f"源：{source['vertices']}顶点 / {source['polygons']}四边面 / {source['triangles']}三角形；1个源、2个同数据验证实例。",
                     '实际包络 0.600000×0.600000×2.400000 m；源轴心(0,0,0)，缩放(1,1,1)。',
                     '高度分区32 / 192 / 16 cm；闭合流形、正体积、无零面积面。',
                     f"UV实测 {uv['min']:.3f}—{uv['max']:.3f} px/m；{uv['triangles_checked']}个三角形面积核对。",
                     '源文件独立重开通过；FBX回导仅1 Mesh，尺寸/顶点位置/轴心对应。',
                     'FBX不含平台、双实例、人物、相机或光源。',
                     '安装区仅注记：南面30×100 cm；未建孔、牌、墙或门叶。',
                     '接地/净口是本轮离线验证；SchoolLife只读，UE通行/碰撞/镜头未验。'],26,45)
im.save(ROOT/'Previews/SL_GE_GATE_PIER_01_TRIAL_CHECK.png')
print('A/B labelled at 1600x1400; material board 2300x1560; actual mesh check 2600x1450')
