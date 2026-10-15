"""Snapshot read-only inputs and draw original, unlit pixel tiles. Run with bundled Python."""
from pathlib import Path
import json, hashlib, random
from PIL import Image, ImageDraw
ROOT=Path('D:/Art Asset Library')
OUT=Path(__file__).parent
PREFIX='SL_BLD_C01_MAIN_01_TRIAL_01'
REF=OUT.parent/'Reference/Revision01'
G=json.loads((REF/'SL_BLD_C01_MAIN_01_REFERENCE_01_REV_01_GEOMETRY.json').read_text(encoding='utf-8'))
def write(name,data):
 (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
paths={Path(x['path']) for x in G['protected_inputs']}
for folder in [OUT.parent/'Reference',OUT.parent/'Planning']:
 paths.update(p for p in folder.rglob('*') if p.is_file() and p.suffix!='.blend1')
paths.update([ROOT/'Docs/AssetPlanning/BuildingProduction/TaskCards/SL_BLD_C01_MAIN_01_TRIAL_01.md',
 ROOT/'Docs/AssetPlanning/BuildingProduction/review-C01-reference-revision-01.md',
 ROOT/'Docs/AssetPlanning/BuildingProduction/C01/reference-revision-01-planning-audit.json'])
if not (OUT/'protected_inputs.json').exists():
 write('protected_inputs.json',[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(paths) if p.exists()])
tex=OUT/'Textures';tex.mkdir(exist_ok=True)
palette={'WALL':'DDD9CB','FRAME':'53686B','GLASS':'779CA4','ROOF':'687D80',
 'WOOD':'AC875A','FLOOR':'D4CEC0','METAL':'7D8B89','BOARD':'38625A',
 'CHAIR':'B39365','RAIL':'768A89','SKYLIGHT':'A2C3C8','ENTRY_WOOD':'CFA878',
 'ENTRY_FRAME':'99A59D','BAND_REV':'BAC1B8'}
catalog=[]
for name,h in palette.items():
 c=tuple(bytes.fromhex(h));im=Image.new('RGB',(256,256),c);d=ImageDraw.Draw(im)
 def tint(delta):return tuple(max(0,min(255,v+delta)) for v in c)
 # Four metre seamless tile. Sparse deliberate clusters, no photographic noise or sunlight.
 if name in ['WOOD','ENTRY_WOOD','CHAIR']:
  for x in range(0,256,16):
   d.line((x,0,x,255),fill=tint(-9))
   for y in range((x*7)%71,256,83):d.line((x+5,y,x+5,y+18),fill=tint(-4))
 elif name in ['ROOF','METAL','FRAME','RAIL','ENTRY_FRAME']:
  for x in range(0,256,32):d.line((x,0,x,255),fill=tint(-7))
 elif name in ['WALL','FLOOR','BAND_REV']:
  if name=='FLOOR':
   for x in range(0,256,32):d.line((x,0,x,255),fill=tint(-6))
   for y in range(0,256,32):d.line((0,y,255,y),fill=tint(-6))
  else:
   for x,y in [(17,36),(104,180),(218,74),(160,230)]:
    d.rectangle((x,y,x+2,y+6),fill=tint(-4))
 im.save(tex/(name+'_BC.png'))
 rough=180 if name not in ['GLASS','SKYLIGHT','METAL','FRAME','RAIL'] else (65 if name in ['GLASS','SKYLIGHT'] else 125)
 Image.new('L',(256,256),rough).save(tex/(name+'_R.png'))
 Image.new('L',(256,256),255 if name in ['GLASS','SKYLIGHT'] else 0).save(tex/(name+'_M.png'))
 catalog.append(dict(material=name,files=[name+'_BC.png',name+'_R.png',name+'_M.png'],size=[256,256],tile_m=4,base_density_px_m=64,
  uv='per-face metric planar; intentional repeat overlap',mask='glass membership; no baked shadow'))
 if name in ['WALL','ENTRY_WOOD','FLOOR']:
  # Draw low-density comparison directly on 128px at SAME four-metre motif dimensions.
  # No UV rescale and no photograph/downsample: only the pixel grid differs.
  cmp=Image.new('RGB',(128,128),c);cd=ImageDraw.Draw(cmp)
  if name=='ENTRY_WOOD':
   for x in range(0,128,8):
    cd.line((x,0,x,127),fill=tint(-9))
    for y in range(((x*2*7)%71)//2,128,42):cd.line((x+2,y,x+2,y+9),fill=tint(-4))
  elif name=='FLOOR':
   for x in range(0,128,16):cd.line((x,0,x,127),fill=tint(-6))
   for y in range(0,128,16):cd.line((0,y,127,y),fill=tint(-6))
  else:
   for x,y in [(17,36),(104,180),(218,74),(160,230)]:cd.rectangle((x//2,y//2,x//2+1,y//2+3),fill=tint(-4))
  cmp.save(tex/(name+'_32_BC.png'));Image.new('L',(128,128),rough).save(tex/(name+'_32_R.png'))
  catalog[-1]['comparison32']=dict(files=[name+'_32_BC.png',name+'_32_R.png'],size=[128,128],tile_m=4,px_m=32,method='direct drawing on32 grid; same physical motif and UV')
write('TEXTURES.json',catalog)
print('protected',len(paths),'textures',len(list(tex.glob('*.png'))))
