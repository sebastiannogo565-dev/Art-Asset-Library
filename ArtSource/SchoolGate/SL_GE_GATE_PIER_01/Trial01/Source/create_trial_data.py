"""Editable trial geometry/UV/temporary texture method. Python + NumPy + Pillow.
One atlas, four isometric side strips plus bottom/top islands; exactly 64 px/m.
Run before build_trial.py. No photos, baked light, normal map, or engine access.
"""
from pathlib import Path
import hashlib, json, math, re
import numpy as np
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parent.parent
DESIGN=ROOT.parent/'Design'
TEX=ROOT/'Textures'
for q in (TEX,TEX/'Samples',ROOT/'Exports',ROOT/'Previews'): q.mkdir(parents=True,exist_ok=True)
G=json.loads((DESIGN/'SL_GE_GATE_PIER_01_GEOMETRY.json').read_text(encoding='utf-8-sig'))
refs=[]
lib=ROOT.parents[3]
source_doc=lib/'Docs/AssetPlanning/SchoolGate/Batch01/dimensions-and-reuse.md'
for p,wanted in re.findall(r'\| \[.*?\]\(<(.*?)>\) \| ([a-f0-9]{64}) \|',source_doc.read_text(encoding='utf-8-sig')):
 actual=hashlib.sha256(Path(p).read_bytes()).hexdigest()
 assert actual==wanted, f'Reference changed: {p}'
 refs.append({'path':p,'sha256':actual,'matches_planning':True})
assert len(refs)==13

rings=[]
for part in G['parts']:
 for z,h in part['rings_z_halfwidth']:
  if not rings or rings[-1]!=[z,h]: rings.append([z,h])
V=[]
for z,h in rings:
 V.extend([(x/100,y/100,z/100) for x,y in [(-h,-h),(h,-h),(h,h),(-h,h)]])
side_v=[16.0]
for (z0,h0),(z1,h1) in zip(rings,rings[1:]): side_v.append(side_v[-1]+math.hypot(z1-z0,h1-h0)/100*64)
F=[]; UV=[]; labels=[]; areas=[]
for i,((z0,h0),(z1,h1)) in enumerate(zip(rings,rings[1:])):
 material='M1' if z0>=32 and z1<=224 and h0==27 and h1==27 else 'M2'
 for j in range(4):
  F.append([4*i+j,4*i+(j+1)%4,4*(i+1)+(j+1)%4,4*(i+1)+j])
  c=32+j*48
  UV.append([[(c-h0/100*64)/256,side_v[i]/256],[(c+h0/100*64)/256,side_v[i]/256],
             [(c+h1/100*64)/256,side_v[i+1]/256],[(c-h1/100*64)/256,side_v[i+1]/256]])
  labels.append({'material_zone':material,'side':['south','east','north','west'][j],
                 'z_cm':[z0,z1],'detail':'seat_band_same_material' if z0==223.4 else 'profile'})
F.append([3,2,1,0]); UV.append([[(224+V[k][0]*64)/256,(64+V[k][1]*64)/256] for k in F[-1]])
labels.append({'material_zone':'M2','side':'bottom','z_cm':[0,0]})
F.append([len(V)-4+k for k in range(4)])
UV.append([[(224+V[k][0]*64)/256,(110+V[k][1]*64)/256] for k in F[-1]])
labels.append({'material_zone':'M2','side':'top','z_cm':[240,240]})
DATA={'asset_id':G['asset_id'],'revision':'TRIAL_01','unit':'meter','vertices':V,'faces':F,'face_uvs':UV,'face_zones':labels,
      'atlas_px':[256,256],'density_px_per_m':64,'side_strip_centre_u_px':[32,80,128,176],'side_v_px':side_v,
      'material_slots':1,'detail_decisions':{'seat_band':'0.006 m band retained in continuous closed mesh; same M1 surface; no forced subpixel dark line',
      'underside_drip_groove':'omitted in trial: 0.384 x 0.320 texel; keep cap projection and slope; planning review pending'},
      'design_geometry_sha256':hashlib.sha256((DESIGN/'SL_GE_GATE_PIER_01_GEOMETRY.json').read_bytes()).hexdigest(),
      'references':refs}
(ROOT/'Source/SL_GE_GATE_PIER_01_TRIAL_GEOMETRY_UV.json').write_text(json.dumps(DATA,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')

def material_color(p,zone):
 x,y,z=p
 if zone=='M1':
  v=2.2*math.sin(4.7*x+3.9*y+1.9*z)+1.7*math.cos(7.1*z-2.1*x+2.3*y)
  v-=3.5*math.exp(-((x-.16)**2/.0015+(z-1.45)**2/.50))
  base=np.array([216,211,197],float)
 else:
  v=1.8*math.sin(8*x+5*y+4*z)+1.7*math.cos(z*10-x*3+y*2)
  # Sparse coherent aggregate clusters, no independent per-texel random noise.
  u=x+y*.63; cell=(math.floor(u/.14),math.floor(z/.14))
  key=(cell[0]*92821+cell[1]*68917)%97
  if key<37:
   cx=(cell[0]+.25+(key%7)*.07)*.14; cz=(cell[1]+.25+(key%5)*.09)*.14
   r=math.hypot(u-cx,z-cz)
   if r<.025+(key%3)*.003: v+=7 if key%2 else -5
  v-=2.5*math.exp(-(z/.11)**2)
  base=np.array([137,151,149],float)
 # Discrete neighbouring material colours. No sunlight, occlusion, or specular colour.
 level=round(v/2)*2
 return tuple(np.clip(base+level,0,255).astype(np.uint8))

base=np.zeros((256,256,3),np.uint8);base[:]=[216,211,197]
rough=np.full((256,256),225,np.uint8);mask=np.zeros((256,256),bool)
for face,uv,zone in zip(F,UV,labels):
 points=np.array([V[k] for k in face]);coords=np.array([(u*256,(1-v)*256) for u,v in uv])
 for tri in [(0,1,2),(0,2,3)]:
  tt=coords[list(tri)];pp=points[list(tri)]; xmin,ymin=np.floor(tt.min(0)).astype(int);xmax,ymax=np.ceil(tt.max(0)).astype(int)
  A=np.column_stack((tt[1]-tt[0],tt[2]-tt[0])); det=np.linalg.det(A)
  if abs(det)<1e-10:continue
  inv=np.linalg.inv(A)
  for py in range(max(0,ymin),min(256,ymax+1)):
   for px in range(max(0,xmin),min(256,xmax+1)):
    a,b=inv@(np.array([px+.5,py+.5])-tt[0])
    if a>=-1e-8 and b>=-1e-8 and a+b<=1+1e-8:
     p=pp[0]+a*(pp[1]-pp[0])+b*(pp[2]-pp[0])
     col=material_color(p,zone['material_zone']);base[py,px]=col
     rough[py,px]=218 if zone['material_zone']=='M1' else 232
     mask[py,px]=True
occupied=int(mask.sum())
# Four texels of replicated border, sufficient for this trial's Closest sampling.
for _ in range(4):
 b2=base.copy();r2=rough.copy();m2=mask.copy()
 for dy,dx in [(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,-1),(1,-1),(-1,1)]:
  ys=slice(max(0,dy),min(256,256+dy));xs=slice(max(0,dx),min(256,256+dx))
  sy=slice(max(0,-dy),min(256,256-dy));sx=slice(max(0,-dx),min(256,256-dx))
  take=(~m2[ys,xs]) & mask[sy,sx]
  b2[ys,xs][take]=base[sy,sx][take];r2[ys,xs][take]=rough[sy,sx][take];m2[ys,xs][take]=True
 base,rough,mask=b2,r2,m2
Image.fromarray(base).save(TEX/'SL_GE_GATE_PIER_01_TRIAL_BaseColor.png')
Image.fromarray(rough).save(TEX/'SL_GE_GATE_PIER_01_TRIAL_Roughness.png')
layout=Image.new('RGB',(256,256),'#f5f3ec');dr=ImageDraw.Draw(layout)
for uv,zone in zip(UV,labels):
 pts=[(u*256,(1-v)*256) for u,v in uv]
 dr.polygon(pts,fill='#d8d3c5' if zone['material_zone']=='M1' else '#899795',outline='#30464a')
for j,name in enumerate(['S','E','N','W']): dr.text((26+j*48,241),name,fill='#243d43')
dr.text((211,218),'BASE',fill='#243d43');dr.text((212,134),'TOP',fill='#243d43')
layout.save(TEX/'SL_GE_GATE_PIER_01_TRIAL_UV_LAYOUT.png')
for zone in ['M1','M2']:
 for N in [32,64]:
  a=np.zeros((N,N,3),np.uint8)
  for row in range(N):
   for col in range(N): a[row,col]=material_color(((col+.5)/N-.5,-.27,(N-row-.5)/N),zone)
  Image.fromarray(a).save(TEX/f'Samples/{zone}_{N}px_per_m_1m.png')
stats={'atlas_px':[256,256],'occupied_texels_before_padding':occupied,'padding_px':4,'sampling':'Closest',
       'actual_mesh_texture_files':2,'comparison_sample_files':4,'density_px_per_m':64,'normal_maps':0}
(ROOT/'Source/texture_statistics.json').write_text(json.dumps(stats,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Trial data:',len(V),'vertices;',len(F),'quads;',len(F)*2,'triangles; 64px/m atlas 256x256;',occupied,'covered texels')
