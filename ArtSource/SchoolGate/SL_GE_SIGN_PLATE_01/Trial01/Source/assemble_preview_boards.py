"""Annotate existing real renders; never alter geometry or original character bytes."""
from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent.parent
D=json.loads((ROOT/'Source/SL_GE_SIGN_PLATE_01_TRIAL_GEOMETRY_UV.json').read_text(encoding='utf-8'))
M=json.loads((ROOT/'Source/blender_measurements.json').read_text(encoding='utf-8'))
def font(n):return ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',n)
def text(draw,pos,t,n=26,color='#293f46'):draw.text(pos,t,font=font(n),fill=color)
for key in ['A','B']:
 im=Image.open(ROOT/f'Previews/Renders/SL_GE_SIGN_PLATE_01_TRIAL_INSTALL_{key}_RENDER.png').convert('RGB');d=ImageDraw.Draw(im)
 d.rectangle((0,0,1600,115),fill='#edf2ef');d.rectangle((0,1268,1600,1400),fill='#edf2ef')
 text(d,(35,15),f'SL_GE_SIGN_PLATE_01 · Trial01 安装{key} / 同源真实日光',36)
 text(d,(35,65),f'方位{225 if key=="A" else 45}° · 俯角30° · 不透明宿主 · 24×84cm / 总突出2cm',26)
 text(d,(35,1280),'牌轴心工程(−330,−27,940)cm；左柱南面中心140cm；校名空白。',27)
 text(d,(35,1325),'原人物PNG原字节 / 180cm可见高、192cm胶囊高；人物无光比例板。非UE效果。',25)
 points=M['views'][key]['character_reference_points_px'];base=points['0'][1];vis=points['1.8'][1];cap=points['1.92'][1];px=points['0'][0]
 x=px-270 if key=='A' else px+270;d.line((x,base,x,cap),fill='#4c6770',width=3)
 for yy,lab in [(base,'0'),(vis,'180 可见'),(cap,'192 胶囊')]:
  d.line((x-8,yy,x+8,yy),fill='#4c6770',width=3);text(d,(max(25,x-165) if key=='A' else x+15,yy-13),lab,21)
 if key=='B':text(d,(35,120),'南面牌被柱完全遮挡；没有北面复制牌或透明宿主。',25)
 im.save(ROOT/f'Previews/SL_GE_SIGN_PLATE_01_TRIAL_INSTALL_{key}.png')

board=Image.new('RGB',(3400,1850),'#edf2ef');d=ImageDraw.Draw(board)
text(d,(45,25),'SL_GE_SIGN_PLATE_01 · Trial01 尺寸 / 接触 / UV / 临时材质检查',45)
text(d,(45,88),'前/背/侧/顶为同一实际网格的正交Workbench检查；拆分只为读支承；右侧是同源真实自然光材质。',29)
columns=[('FRONT',50,480,'南正面 −Y / 空白'),('REAR',600,480,'北背视 +Y / 未装柱'),('EAST',1150,360,'东侧 +X / 服务口'),('EXPLODED_REAR',1580,850,'背部拆分检查 / 非安装可见性')]
for key,x,w,title in columns:
 text(d,(x,152),title,28)
 im=Image.open(ROOT/f'Previews/Renders/CHECK_{key}.png').convert('RGB')
 if key=='EXPLODED_REAR':im=im.resize((700,865),Image.Resampling.LANCZOS)
 board.paste(im,(x,205))
for x,t in [(50,'24宽 × 84高 / R4mm'),(600,'接触垫Y0 / 座宽18 / 钩宽16'),(1150,'牌体1 / 含支承总深2'),(1580,'左：柱侧座与垫；右：牌侧组件')]:text(d,(x,1090),t,26)
coat=Image.open(ROOT/'Previews/Renders/SL_GE_SIGN_PLATE_01_TRIAL_COATING_RENDER.png').convert('RGB');board.paste(coat,(2580,205))
text(d,(2580,152),'哑光青灰 / 真日光单体近视',29)
text(d,(2580,1335),'#60767A / 涂装铝假设',27)
text(d,(2580,1380),'Roughness 209/255≈0.82',25)
text(d,(2580,1425),'Metallic0 / IOR1.45 / Closest',25)
text(d,(2580,1470),'低频±2色值；无太阳阴影/AO',25)
top=Image.open(ROOT/'Previews/Renders/CHECK_TOP.png').convert('RGB');board.paste(top,(50,1190));text(d,(50,1160),'顶视 +Z / 24宽 × 2深；后接触面中心轴心',26)
uv=Image.open(ROOT/'Textures/SL_GE_SIGN_PLATE_01_TRIAL_UV_LAYOUT.png').convert('RGB').resize((512,512),Image.Resampling.NEAREST);board.paste(uv,(800,1220));text(d,(800,1160),'UV原生256²（此处2×最近邻读图）',25)
text(d,(1410,1215),'源：1套 / 11个可编辑组件 / 1共享材质。',30)
text(d,(1410,1270),f'实际{M["total_vertices"]}点 / {M["total_polygons"]}多边形 / {M["total_triangles"]}三角；无最终预算。',28)
den=D.get('actual_uv_density_px_per_m',{'min':64,'max':64})
text(d,(1410,1325),f'实测密度 {den["min"]:.3f}—{den["max"]:.3f}px/m。',28)
text(d,(1410,1380),f'{D["uv"]["planar_chart_count"]}平面图块，2px间隔；256图集≠256px/m。',27)
text(d,(1410,1435),'薄边保几何，亚像素处同材，不画粗黑线/螺丝。',27)
text(d,(1410,1490),'20×76字面预留：仅12.8×48.64环境像素，文字另定。',27)
text(d,(1410,1545),'侧口：X11.8..12 / Y−1.8..−1 / Z−31.8..−30.9。',27)
text(d,(1410,1600),'下座防抬滑舌右退1cm；止退/锚固/工具公差未验。',27)
text(d,(45,1770),'本板＝几何检查 + 临时材质试作（拆分排版缩放，原生另存）。装配另见ASSEMBLY；校名/最终纹理/UE未完成。',30)
board.save(ROOT/'Previews/SL_GE_SIGN_PLATE_01_TRIAL_CHECK.png')
print('annotated A/B 1600×1400 and check 3400×1850 saved')
