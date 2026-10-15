"""Rebuilt architectural trial, not a reference primitive importer. Blender 5.2 background."""
import bpy, math, json, hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path('D:/Art Asset Library'); OUT=Path(__file__).parent; P='SL_BLD_C01_MAIN_01_TRIAL_01'
G=json.loads((OUT.parent/'Reference/Revision01/SL_BLD_C01_MAIN_01_REFERENCE_01_REV_01_GEOMETRY.json').read_text(encoding='utf-8'))
# Trial-only furniture refinement. Fixed room/door/business/recovery interfaces stay unchanged.
G['player_interface']['seat_rest'][1]=19.87;G['player_interface']['seat_pulled'][1]=19.87
G['player_interface']['standing_approach'][1]=18.8
for key in ['route_to_approach','route_return_via_teaching']:
 G['player_interface'][key]=[[x,18.8 if abs(y-18.7)<1e-7 else y] for x,y in G['player_interface'][key]]
G['player_interface']['seat_transfer']=[[46.425,18.8],[46.425,19.87]]
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for col in list(bpy.data.collections):
 if col.users==0:bpy.data.collections.remove(col)
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
whole=bpy.data.collections.new('WHOLE');scene.collection.children.link(whole)
groups={}
for n in ['ROOF','EXTERIOR']+[f'{a}_F{f:02}' for f in range(1,4) for a in ['SLAB','INTERIOR','PARTITIONS','CEILING']]+['STAIR_CORE_S1','STAIR_CORE_S2','STAIR_CORE_S3']:
 c=bpy.data.collections.new(n);whole.children.link(c);groups[n]=c
checks=bpy.data.collections.new('CHECK_ONLY_NO_EXPORT');scene.collection.children.link(checks)
context=bpy.data.collections.new('CONTEXT_NO_EXPORT');scene.collection.children.link(context)
mats={}
for t in json.loads((OUT/'TEXTURES.json').read_text()):
 name=t['material'];m=bpy.data.materials.new(name);m.use_nodes=True
 ns=m.node_tree.nodes;bs=ns.get('Principled BSDF');uv=ns.new('ShaderNodeTexCoord');scale=ns.new('ShaderNodeVectorMath');scale.operation='SCALE';scale.inputs[3].default_value=1;scale.name='DENSITY_64_OR_32'
 m.node_tree.links.new(uv.outputs['UV'],scale.inputs[0])
 for suffix,socket in [('_BC','Base Color'),('_R','Roughness')]:
  n=ns.new('ShaderNodeTexImage');n.image=bpy.data.images.load(str(OUT/'Textures'/(name+suffix+'.png')),check_existing=True);n.interpolation='Closest';n.extension='REPEAT'
  if suffix=='_R':n.image.colorspace_settings.name='Non-Color'
  m.node_tree.links.new(scale.outputs[0],n.inputs['Vector']);m.node_tree.links.new(n.outputs['Color'],bs.inputs[socket])
 if name in ['GLASS','SKYLIGHT']:
  bs.inputs['Transmission Weight'].default_value=.82;bs.inputs['IOR'].default_value=1.45
 elif name in ['FRAME','METAL','RAIL']:bs.inputs['Metallic'].default_value=.35
 mats[name]=m
MAT=list(mats);MIDX={m:i for i,m in enumerate(MAT)}
def mesh(name,verts,faces,material,group,indices=None):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update()
 ob=bpy.data.objects.new(name,me);(groups.get(group) or group).objects.link(ob)
 for m in MAT:me.materials.append(mats[m])
 for p in me.polygons:p.material_index=MIDX[material] if indices is None else indices[p.index]
 # Dissolve artificial coplanar grid subdivisions, preserve material borders and real sharp edges.
 import bmesh
 bm=bmesh.new();bm.from_mesh(me)
 bmesh.ops.dissolve_limit(bm,angle_limit=1e-6,use_dissolve_boundaries=False,verts=list(bm.verts),edges=list(bm.edges),delimit={'MATERIAL'})
 bm.to_mesh(me);bm.free();me.update()
 # Face-projected metric UV, 256 pixels/4 metres. Independent faces deliberately tile/overlap.
 uv=me.uv_layers.new(name='UV_METRIC_64')
 for poly in me.polygons:
  normal=poly.normal;axis=max(range(3),key=lambda i:abs(normal[i]))
  # Preserve slope metric length on planar roofs as well.
  basis=Vector((0,1,0)) if axis==0 else Vector((1,0,0))
  basis=(basis-normal*basis.dot(normal)).normalized();v=normal.cross(basis)
  for li in poly.loop_indices:
   co=me.vertices[me.loops[li].vertex_index].co;uv.data[li].uv=(co.dot(basis)/4,co.dot(v)/4)
 ob['group']=group if isinstance(group,str) else group.name
 ob['purpose']='TRIAL_ARCHITECTURE' if ob.name not in [] else ''
 return ob
class Parts:
 def __init__(self):self.v=[];self.f=[];self.m=[];self.boxes=[]
 def box(self,b,mat='WALL'):
  x,y,z,X,Y,Z=b
  if min(X-x,Y-y,Z-z)<1e-7:return
  self.boxes.append((b,mat))
  i=len(self.v);self.v += [(x,y,z),(X,y,z),(X,Y,z),(x,Y,z),(x,y,Z),(X,y,Z),(X,Y,Z),(x,Y,Z)]
  for f in [(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]:
   self.f.append(tuple(i+j for j in f));self.m.append(MIDX[mat])
 def finish(self,name,group):
  # Exact orthogonal solid union: no shared/coplanar internal box faces, including partial contacts.
  import numpy as np
  if not self.boxes:return mesh(name,[],[],'WALL',group,[])
  axes=[sorted(set(round(b[i],7) for b,m in self.boxes)|set(round(b[i+3],7) for b,m in self.boxes)) for i in range(3)]
  ix=[{v:i for i,v in enumerate(a)} for a in axes]
  shape=tuple(len(a)-1 for a in axes);grid=np.full(shape,-1,dtype=np.int16)
  for b,m in self.boxes:
   spans=[slice(ix[i][round(b[i],7)],ix[i][round(b[i+3],7)]) for i in range(3)]
   grid[tuple(spans)]=MIDX[m]
  if name=='EXT_WHOLE_UNION':
   valid=np.array([[inside((axes[0][i]+axes[0][i+1])/2,(axes[1][j]+axes[1][j+1])/2) for j in range(shape[1])] for i in range(shape[0])])
   grid[~valid,:]=-1
  vv=[];ff=[];mm=[];lookup={}
  specs=[((-1,0,0),(0,3,7,4)),((1,0,0),(1,5,6,2)),((0,-1,0),(0,4,5,1)),((0,1,0),(3,2,6,7)),((0,0,-1),(0,1,2,3)),((0,0,1),(4,7,6,5))]
  # Specs are inward above, reverse on emit to ensure positive outside normals.
  for i,j,k in np.argwhere(grid>=0):
   x,X=axes[0][i:i+2];y,Y=axes[1][j:j+2];z,Z=axes[2][k:k+2]
   corners=[(x,y,z),(X,y,z),(X,Y,z),(x,Y,z),(x,y,Z),(X,y,Z),(X,Y,Z),(x,Y,Z)]
   for delta,face in specs:
    a,b,c=i+delta[0],j+delta[1],k+delta[2]
    if 0<=a<shape[0] and 0<=b<shape[1] and 0<=c<shape[2] and grid[a,b,c]>=0:continue
    f=[]
    for q in reversed(face):
     v=corners[q]
     if v not in lookup:lookup[v]=len(vv);vv.append(v)
     f.append(lookup[v])
    ff.append(f);mm.append(int(grid[i,j,k]))
  return mesh(name,vv,ff,'WALL',group,mm)
def box(name,b,mat,group):
 p=Parts();p.box(b,mat);return p.finish(name,group)
def inrect(x,y,r,eps=0):return r[0]-eps<x<r[2]+eps and r[1]-eps<y<r[3]+eps
BODY=G['body_rects'];COURT=[74,15,86,24];LIFT=[80,.8,82.4,3.2]
def inside(x,y):return any(inrect(x,y,r) for r in BODY)
def outer_wall_footprints():
 xs=sorted(set(v for r in BODY for v in [r[0],r[2]]));ys=sorted(set(v for r in BODY for v in [r[1],r[3]]));result=[]
 for x,X in zip(xs,xs[1:]):
  for y,Y in zip(ys,ys[1:]):
   if not inside((x+X)/2,(y+Y)/2):continue
   if not inside((x+X)/2,y-.001):result.append([x-.3,y,X+.3,y+.3])
   if not inside((x+X)/2,Y+.001):result.append([x-.3,Y-.3,X+.3,Y])
   if not inside(x-.001,(y+Y)/2):result.append([x,y-.3,x+.3,Y+.3])
   if not inside(X+.001,(y+Y)/2):result.append([X-.3,y-.3,X,Y+.3])
 return result
EXT_FOOTPRINTS=outer_wall_footprints();EXT_SOLIDS=Parts()
def planar_union(name,rects,z0,z1,group,mat='FLOOR',holes=[],clip_body=False):
 xs=sorted(set(round(v,6) for r in rects+holes+BODY for v in [r[0],r[2]]));ys=sorted(set(round(v,6) for r in rects+holes+BODY for v in [r[1],r[3]]))
 cells=set()
 for i in range(len(xs)-1):
  x=(xs[i]+xs[i+1])/2
  for j in range(len(ys)-1):
   y=(ys[j]+ys[j+1])/2
   if any(inrect(x,y,r) for r in rects) and not any(inrect(x,y,h) for h in holes) and (not clip_body or inside(x,y)):cells.add((i,j))
 p=Parts()
 for i,j in cells:p.box([xs[i],ys[j],z0,xs[i+1],ys[j+1],z1],mat)
 ob=p.finish(name,group);ob['hole_rects']=json.dumps(holes);return ob
def slopebeam(p1,p2,width,depth,name,group,mat='RAIL'):
 d=Vector(p2)-Vector(p1);length=d.length
 ob=box(name,[-width/2,-depth/2,-length/2,width/2,depth/2,length/2],mat,group)
 ob.location=(Vector(p1)+Vector(p2))/2;ob.rotation_euler=d.to_track_quat('Z','Y').to_euler();return ob
# FIRST: true furniture sources and 30-seat high frequency room, before the building shell.
dp=Parts();dp.box([-.225,-.325,.69,.225,.325,.72],'WOOD')
for x in [-.18,.18]:
 for y in [-.29,.29]:dp.box([x-.018,y-.018,0,x+.018,y+.018,.69],'FRAME')
dp.box([-.14,-.24,.54,.14,.24,.56],'METAL')
desk=dp.finish('F2_W4_DESK_1_1','INTERIOR_F02')
cp=Parts();cp.box([-.225,-.225,.395,.225,.225,.43],'CHAIR')
cp.box([.16,-.225,.43,.22,.225,.84],'CHAIR')
for x in [-.18,.18]:
 for y in [-.18,.18]:cp.box([x-.015,y-.015,0,x+.015,y+.015,.395],'FRAME')
chair=cp.finish('F2_W4_CHAIR_1_1','INTERIOR_F02')
def linked(src,name,location,group):
 ob=bpy.data.objects.new(name,src.data);groups[group].objects.link(ob);ob.location=location;ob['group']=group;ob['purpose']='TRIAL_ARCHITECTURE';return ob
chairs=[];desks=[];classcounts={}
classes=[r for r in G['rooms'] if r['kind']=='classroom']
classes.sort(key=lambda r:r['id']!='F2_W4')
first=True
for r in classes:
 x0,y0,x1,y1=r['rect'];z=(r['floor']-1)*4;gr=f"INTERIOR_F{r['floor']:02}"
 xs=[x0+t for t in [1.625,2.575,4.775,5.725,6.675]];ys=[y0+t for t in [1.425,2.325,4.175,5.075,6.925,7.825]]
 if r['id']=='F2_W4':ys=[13.47,14.53,16.67,17.73,19.87,20.93]
 for i,x in enumerate(xs):
  for j,y in enumerate(ys):
   name=r['id']+f'_DESK_{i+1}_{j+1}'
   if first:de=desk;ch=chair;de.location=(x,y,z);ch.location=(x+.4,y,z);first=False
   else:de=linked(desk,name,(x,y,z),gr);ch=linked(chair,name.replace('DESK','CHAIR'),(x+.4,y,z),gr)
   desks.append(de);chairs.append(ch)
   if r['id']=='F2_W4':ch['player_room_chair']=True
 classcounts[r['id']]=30
 box(r['id']+'_BOARD',[x0+.035,y0+2.3,z+1,x0+.09,y0+6.3,z+2.25],'BOARD',gr)
 pp=Parts();pp.box([x0+.45,y0+3.7,z+.72,x0+1.05,y0+4.9,z+.75],'WOOD')
 for x in [x0+.5,x0+1]:
  for y in [y0+3.75,y0+4.85]:pp.box([x,y,z,x+.035,y+.035,z+.72],'FRAME')
 pp.finish(r['id']+'_TEACHER',gr)
print('HIGH_FREQUENCY furniture constructed',flush=True)
# Actual cabinet carcasses, shelves, vertical dividers, shared back, and half-height sliding fronts.
# 600 main cavities: .66m gross double bank, +.06m vs reference. 300 link: .70m unchanged.
banks=[]
for b in G['lockers']:
 x0,y0,z0,x1,y1,z1=b['bounds'];cy=(y0+y1)/2;dep=.66 if b['room']=='F1_WL' else .70;y0=cy-dep/2;y1=cy+dep/2
 pa=Parts();n=b['columns'];pitch=.30;t=.012
 pa.box([x0,cy-.006,0,x1,cy+.006,1.5],'METAL')
 for i in range(n+1):
  x=x0+i*pitch
  # outer boards sit in the pitch; every net cavity remains >=.288m wide
  lo=max(x0,x-.006);hi=min(x1,x+.006)
  pa.box([lo,y0,0,hi,y1,1.5],'METAL')
 for j in range(6):
  z=j*.3;lo=max(0,z-.006);hi=min(1.5,z+.006)
  pa.box([x0,y0,lo,x1,cy-.006,hi],'METAL');pa.box([x0,cy+.006,lo,x1,y1,hi],'METAL')
 carcass=pa.finish('LOCKER_'+b['id']+'_CARCASS','INTERIOR_F01')
 fronts=Parts()
 for face in [-1,1]:
  yy=cy+face*(dep/2-.008)
  for i in range(n):
   for j in range(5):
    # Upper half fixed, lower half slides vertically behind upper. One nominated cell shown open.
    x=x0+i*.3+.008;z=j*.3+.008;opened=b['id']=='MAIN_W1' and i==7 and j==2 and face==1
    fronts.box([x,yy-.008,z+.142,x+.284,yy+.008,z+.284],'ENTRY_FRAME')
    lz=z+.142 if opened else z
    fronts.box([x,yy-.003,lz,x+.284,yy+.003,lz+.138],'METAL')
    fronts.box([x+.115,yy-.009,z+.122 if not opened else z+.264,x+.165,yy+.009,z+.128 if not opened else z+.270],'FRAME')
 fronts.finish('LOCKER_'+b['id']+'_FRONTS','INTERIOR_F01')
 banks.append(dict(id=b['id'],room=b['room'],bounds=[x0,y0,0,x1,y1,1.5],columns=n,rows=5,faces=2,nominal=n*10,
  cavity=[.288,(dep-.012)/2-.020,.263],open_clear_height=.138,front='two panel vertical half lift; candidate hardware'))
print('HIGH_FREQUENCY true locker cavities',sum(b['nominal'] for b in banks),flush=True)
# Slabs: common-coordinate union; voids removed in actual mesh, no demonstration caps.
stairholes=[s['opening'] for s in G['stairs']]
for f in range(1,4):
 z=(f-1)*4;holes=[] if f==1 else [COURT,LIFT]+stairholes
 planar_union('SLAB_F%02d_ACTUAL'%f,BODY,z-.25,z,f'SLAB_F{f:02}',holes=holes+EXT_FOOTPRINTS)
 # Ceiling immediately below next slab: same holes, including court and stair; top level stops below roof.
 ceilingholes=[COURT,LIFT]+stairholes
 if f==3:ceilingholes += [[64,0,74,6]]
 planar_union('CEILING_F%02d'%f,BODY,z+3.45,z+3.48,f'CEILING_F{f:02}','WALL',ceilingholes+EXT_FOOTPRINTS)
for o in [o for o in G['openings'] if o['id'] in ['C01_MAIN','C01_N','C01_E']]:
 a,b=o['lo'],o['hi'];ln=o['line'];d,D=sorted([ln,ln-o['normal']*.3])
 box('ENTRY_THRESHOLD_'+o['id'],[a,d,-.25,b,D,0] if o['axis']=='X' else [d,a,-.25,D,b,0],'FLOOR','SLAB_F01')
# Boundary extraction of the stepped footprint, merge collinear outlines.
xs=sorted(set(v for r in BODY for v in [r[0],r[2]]));ys=sorted(set(v for r in BODY for v in [r[1],r[3]]))
edges={}
for i in range(len(xs)-1):
 for j in range(len(ys)-1):
  x,X=xs[i:i+2];y,Y=ys[j:j+2]
  if not inside((x+X)/2,(y+Y)/2):continue
  for axis,line,a,b,n,px,py in [('X',y,x,X,-1,(x+X)/2,y-.001),('X',Y,x,X,1,(x+X)/2,Y+.001),('Y',x,y,Y,-1,x-.001,(y+Y)/2),('Y',X,y,Y,1,X+.001,(y+Y)/2)]:
   if not inside(px,py):edges.setdefault((axis,line,n),[]).append((a,b))
boundary=[]
for (axis,line,n),intervals in edges.items():
 intervals.sort();a,b=intervals[0]
 for c,d in intervals[1:]:
  if abs(c-b)<1e-6:b=d
  else:boundary.append((axis,line,a,b,n));a,b=c,d
 boundary.append((axis,line,a,b,n))
def wall_panel(name,axis,line,a,b,n,z0,z1,openings,group,thick=.3):
 # Orthogonal 2D panel decomposition; internal faces removed by Parts.finish.
 if group=='EXTERIOR':a-=.3;b+=.3
 us=sorted(set([a,b]+[max(a,min(b,o[q])) for o in openings for q in ['lo','hi']]))
 if name.startswith('EXT') and axis=='X' and line==0:
  us=sorted(set(us+[v for v in [21.8,22,23.5,26.5,28,28.2] if a<v<b]))
 zs=sorted(set([z0,z1]+[max(z0,min(z1,o[q])) for o in openings for q in ['z0','z1']]+[v for v in [.6,3.6,3.65,4,4.05,7.6,8,11.6,12] if z0<v<z1]))
 pa=Parts()
 for u,U in zip(us,us[1:]):
  for z,Z in zip(zs,zs[1:]):
   mid=(u+U)/2;midz=(z+Z)/2
   if any(o['lo']-1e-8<mid<o['hi']+1e-8 and o['z0']-1e-8<midz<o['z1']+1e-8 for o in openings):continue
   mat='BAND_REV' if midz%4>3.6 else 'WALL'
   if name.startswith('EXT') and axis=='X' and line==0 and (21.8<=mid<=23.5 or 26.5<=mid<=28.2) and midz<3.6:mat='ENTRY_WOOD'
   if name.startswith('EXT') and axis=='X' and line==0 and 22<=mid<=28 and 3.65<midz<4.05:mat='ENTRY_WOOD'
   l,L=sorted([line,line-n*thick])
   pa.box([u,l,z,U,L,Z] if axis=='X' else [l,u,z,L,U,Z],mat)
 if group=='EXTERIOR':
  EXT_SOLIDS.boxes.extend(pa.boxes);return None
 return pa.finish(name,group)
for idx,(axis,line,a,b,n) in enumerate(boundary):
 ops=[o for o in G['openings'] if o['side']!='INTERIOR' and o['axis']==axis and abs(o['line']-line)<.001 and o['hi']>a and o['lo']<b]
 # Third floor terrace replaces enclosure on its south/west/east edges below its open sky.
 mid=(a+b)/2
 top=12.3
 if (axis=='X' and line in [8,22] and (52<=mid<=64 or 94<=mid<=106)) or (axis=='X' and line==0 and (18<=mid<=38 or 142<=mid<=150)) or (axis=='Y' and line in [18,38,142,150] and b<=4):top=12.12
 if (axis=='X' and line in [0,28] and 64<=mid<=94) or (axis=='Y' and line in [64,94] and a<28):top=12.65
 if axis=='X' and line==0 and a==64 and b==94:
  wall_panel(f'EXT_{idx}_F12',axis,line,a,b,n,0,8,ops,'EXTERIOR')
  wall_panel(f'EXT_{idx}_F3',axis,line,74,b,n,8,12.65,ops,'EXTERIOR')
 else:
  if axis=='Y' and line==64 and a==0:top=8
  wall_panel(f'EXT_{idx}',axis,line,a,b,n,0,top,ops,'EXTERIOR')
# Internal room strips unioned per height. Door cuts extend through full wall thickness.
for f in range(1,4):
 z=(f-1)*4;rects=[];doors=[]
 for r in G['rooms']:
  if r['floor']!=f or r['id'].endswith('_AT'):continue
  x,y,X,Y=r['rect']
  rects += [[x-.2,y,x,Y],[X,y,X+.2,Y],[x-.2,y-.2,X+.2,y],[x-.2,Y,X+.2,Y+.2]]
  dx,dy=r['door'];w=r['door_width']
  if abs(dy-y)<.05:doors.append([dx-w/2,y-.25,dx+w/2,y+.02])
  elif abs(dy-Y)<.05:doors.append([dx-w/2,Y-.02,dx+w/2,Y+.25])
  elif abs(dx-X)<.05:doors.append([X-.02,dy-w/2,X+.25,dy+w/2])
  elif abs(dx-x)<.05:doors.append([x-.25,dy-w/2,x+.02,dy+w/2])
 for st in G['stairs']:
  x,y,X,Y=st['box'];rects += [[x,8.8,X,9.0],[x,0,x+.2,8.8],[X-.2,0,X,8.8]]
  dx,dy=st['door'];doors.append([dx-1.1,8.78,dx+1.1,9.02])
 # Lift shaft walls and 1.2m landing door toward corridor.
 rects += [[79.8,.6,80,3.4],[82.4,.6,82.6,3.4],[80,.6,82.4,.8],[80,3.2,82.4,3.4]]
 doors.append([80.6,3.18,81.8,3.42])
 # Clip partition solids to interior footprint, and keep courtyard/terrace void clear.
 inner=[[r[0]+.3,r[1]+.3,r[2]-.3,r[3]-.3] for r in BODY]
 # Intersections with interiors of union are used instead of filling control rectangle.
 clipped=[]
 for r in rects:
  # Exterior touching strips omitted; outer shell already owns both faces.
  cx,cy=(r[0]+r[2])/2,(r[1]+r[3])/2
  if any((ax=='X' and abs(cy-ln)<.21 and a<cx<b) or (ax=='Y' and abs(cx-ln)<.21 and a<cy<b) for ax,ln,a,b,n in boundary):continue
  clipped.append(r)
 voids=[COURT]+([[64,0,74,6]] if f==3 else [])
 planar_union(f'PARTITIONS_F{f:02}_DOOR_BAND',clipped,z,z+2.6,f'PARTITIONS_F{f:02}','WALL',doors+voids,True)
 planar_union(f'PARTITIONS_F{f:02}_HEAD',clipped,z+2.6,z+3.45,f'PARTITIONS_F{f:02}','WALL',voids,True)
print('Whole architecture slabs and opening walls complete',flush=True)
# Windows and doors: actual reveal, frames, glass, shared materials, fully open sliding leaves at main paths.
opening_log=[]
def opening_mesh(o):
 axis=o['axis'];ln=o['line'];a,b=o['lo'],o['hi'];z,Z=o['z0'],o['z1'];n=o.get('normal',0)
 internal=o['side']=='INTERIOR';isdoor=o['kind'] in ['door','sliding_internal']
 gr=f"INTERIOR_F{min(3,int(z/4)+1):02}" if internal else 'EXTERIOR'
 pa=Parts();frame='ENTRY_FRAME' if o['id']=='C01_MAIN' else 'FRAME'
 # Frame lies entirely outside the prescribed clear opening.
 def part(u,U,d,D,v,V,mat):
  pa.box([u,ln+d,v,U,ln+D,V] if axis=='X' else [ln+d,u,v,ln+D,U,V],mat)
 depth=(-.14,.0) if internal else tuple(sorted([-.16*n,-.05*n]))
 d,D=depth
 for u,U in [(a-.055,a),(b,b+.055)]:part(u,U,d,D,z if isdoor else z-.055,Z+.055,frame)
 part(a,b,d,D,Z,Z+.055,frame)
 if not isdoor:
  part(a,b,d,D,z-.055,z,frame)
  # One 12mm solid pane per window opening, with mullions, no glass/opaque duplicate surfaces.
  part(a+.012,b-.012,(d+D)/2-.006,(d+D)/2+.006,z+.012,Z-.012,'SKYLIGHT' if o['kind']=='link' else 'GLASS')
  count=max(1,round((b-a)/1.1))
  for i in range(1,count):u=a+(b-a)*i/count;part(u-.018,u+.018,d,D,z,Z,frame)
 else:
  # Leaves slide fully out of clear opening and park against wall, no outward obstruction.
  w=(b-a)/2
  leaf=-n*.33 if n else d-.02
  for u in [a-w-.07,b+.07]:
   part(u,u+w,leaf-.01,leaf+.01,z+.025,Z-.025,'GLASS')
   part(u,u+.035,leaf-.02,leaf+.02,z,Z,frame);part(u+w-.035,u+w,leaf-.02,leaf+.02,z,Z,frame)
   part(u,u+w,leaf-.02,leaf+.02,Z-.05,Z,frame)
   part(u,u+w,leaf-.02,leaf+.02,z,z+.05,frame)
 if 'shade_depth' in o and not isdoor:
  dep=o['shade_depth'];start=-n*.01
  # Shade stays within site control at y0/x0 etc; projection into setbacks allowed.
  outward=n*dep
  if (axis=='X' and ln in [0,28]) or (axis=='Y' and ln in [0,150]):outward=-outward
  lo,hi=sorted([start,outward]);part(a-.08,b+.08,lo,hi,Z+.08,Z+.14,'BAND_REV')
 ob=pa.finish('OPEN_'+o['id'],gr);ob['opening_id']=o['id'];ob['clear_width']=b-a;ob['clear_height']=Z-z
 opening_log.append(dict(id=o['id'],axis=axis,line=ln,lo=a,hi=b,z0=z,z1=Z,actual_object=ob.name))
for o in G['openings']:
 # Revision adds WL north opening missing in old row list, existing room door uses same cut.
 opening_mesh(o)
# Additional southern room doors and three stair doors absent from original opening schedule.
ids={o['room'] for o in G['openings'] if o['side']=='INTERIOR'}
for r in G['rooms']:
 if r['id'] in ids or r['id'].endswith('_AT'):continue
 x,y,X,Y=r['rect'];dx,dy=r['door'];w=r['door_width'];z=(r['floor']-1)*4
 ax='X' if abs(dy-y)<.1 or abs(dy-Y)<.1 else 'Y';line=dy+(.1 if abs(dy-Y)<.1 else -.1) if ax=='X' else dx+.1
 mid=dx if ax=='X' else dy
 opening_mesh(dict(id=r['id']+'_TRIAL_D',axis=ax,line=line,lo=mid-w/2,hi=mid+w/2,z0=z,z1=z+2.6,side='INTERIOR',kind='sliding_internal'))
for st in G['stairs']:
 for f in range(3):
  opening_mesh(dict(id=st['id']+f'_F{f+1}_D',axis='X',line=8.9,lo=st['door'][0]-1.1,hi=st['door'][0]+1.1,z0=4*f,z1=4*f+2.6,side='INTERIOR',kind='sliding_internal'))
# Roof: closed continuous sloping prisms, real eaves and ridge, core/skylight holes.
def roof_prism(name,xa,xb,ya,yb,za,zb,mat='ROOF'):
 v=[(xa,ya,za),(xb,ya,za),(xb,yb,zb),(xa,yb,zb),(xa,ya,za-.12),(xb,ya,za-.12),(xb,yb,zb-.12),(xa,yb,zb-.12)]
 return mesh(name,v,[(0,1,2,3),(7,6,5,4),(4,5,1,0),(5,6,2,1),(6,7,3,2),(7,4,0,3)],mat,'ROOF')
for a,b in [(0,52),(106,150)]:
 for ya,yb,za,zb in [(3.4,13,12.247506801884446,13.087397971733317),(13,22.6,13.087397971733317,12.247506801884446)]:
  roof_prism(f'ROOF_GABLE_{a}_{ya}',a,b,ya,yb,za,zb)
 # Gable ends fill the triangular loft without overlapping lower exterior wall.
 for x in [a,b]:
  v=[(x,4,12.3),(x,22,12.3),(x,13,13.087397971733317)]
  # Thin closed triangular prism inward.
  t=.20 if x==a else -.20;vv=v+[(X+t,Y,Z) for X,Y,Z in v]
  mesh(f'GABLE_END_{x}',vv,[(0,2,1),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],'WALL','ROOF')
planar_union('CORE_ROOF',[[64,0,94,28]],12.65,12.9,'ROOF','ROOF',[COURT,[64,0,74,6]])
for a,b in [(52,64),(94,106)]:box(f'LINK_ROOF_{a}',[a,8,12.12,b,22,12.3],'ROOF','ROOF')
for r in [[18,0,38,4],[142,0,150,4]]:box('FRONT_LOW_ROOF_'+str(r[0]),[r[0],r[1],12.12,r[2],r[3],12.3],'ROOF','ROOF')
# Court glazing rises from13.2 edges to13.65 glass/13.68 frame peak.
for ya,yb,za,zb in [(15,19.5,13.2,13.65),(19.5,24,13.65,13.2)]:
 roof_prism('SKYLIGHT_GLASS_'+str(ya),74,86,ya,yb,za,zb,'SKYLIGHT')
 for x in [74+i*1.5 for i in range(9)]:slopebeam((x,ya,za+.015),(x,yb,zb+.015),.055,.03,'SKYLIGHT_FRAME','ROOF','FRAME')
box('SKYLIGHT_RIDGE',[74,19.47,13.65,86,19.53,13.68],'FRAME','ROOF')
for b in [[64,27.8,12.9,94,28,13],[93.8,0,12.9,94,28,13],[64,6,12.9,64.2,28,13]]:
 box('CORE_PARAPET',b,'BAND_REV','ROOF')
# Terrace rear wall/door actual finish; full clear door and 1.20m guard.
ops=[o for o in G['openings'] if o['id']=='TERRACE_ACCESS']
wall_panel('TERRACE_REAR','X',6,64,74,-1,8.03,12.65,ops,'EXTERIOR')
box('TERRACE_FINISH',[64,0,8,74,6,8.03],'FLOOR','SLAB_F03')
def guardline(name,p1,p2,z0,height,group):
 slopebeam((p1[0],p1[1],z0+height-.025),(p2[0],p2[1],z0+height-.025),.05,.05,name+'_TOP',group)
 length=math.dist(p1,p2);n=max(1,math.ceil(length/1.0))
 pa=Parts()
 for i in range(n+1):
  u=i/n;x=p1[0]+(p2[0]-p1[0])*u;y=p1[1]+(p2[1]-p1[1])*u
  pa.box([x-.018,y-.018,z0,x+.018,y+.018,z0+height-.05],'RAIL')
 pa.finish(name+'_POSTS',group)
 # Thin safety infill is solid clear glass and separate from top/posts.
 slopebeam((p1[0],p1[1],z0+.56),(p2[0],p2[1],z0+.56),.012,1.02,name+'_INFILL',group,'GLASS')
for a,b in [((64.04,.04),(73.96,.04)),((64.04,.04),(64.04,5.96)),((73.96,.04),(73.96,5.96))]:
 guardline('TERRACE_GUARD',a,b,8.03,1.2,'EXTERIOR')
box('TERRACE_DRAIN_CHANNEL',[73.55,.15,8.01,73.8,4.7,8.03],'METAL','EXTERIOR')
box('TERRACE_PIPE',[73.64,0,.15,73.72,.08,8.01],'FRAME','EXTERIOR')
# Courtyard open ground entries, upper voids use transparent guards, no continuous infill walls in void.
for f in [2,3]:
 z=(f-1)*4;gr=f'INTERIOR_F{f:02}'
 for a,b in [((74.04,15.04),(85.96,15.04)),((85.96,15.04),(85.96,23.96)),((85.96,23.96),(74.04,23.96)),((74.04,23.96),(74.04,15.04))]:
  guardline(f'COURT_F{f}',a,b,z,1.2,gr)
# Real stair flights: one closed stepped profile extrusion, no boxes stacked to fake risers.
stair_report=[]
def flight(name,x,ystart,yend,zbase,zend,group):
 # 12 rises: first rise at start, 11 goings of.30m, 2.0m rise.
 direction=1 if yend>ystart else -1;run=abs(yend-ystart);rise=(zend-zbase)/12
 end_embedded=yend+direction*.001
 profile=[(ystart,zbase-.18),(ystart,zbase),(ystart,zbase+rise)]
 for i in range(11):
  yy=ystart+direction*run*(i+1)/11 if i<10 else end_embedded
  profile.append((yy,zbase+(i+1)*rise))
  if i<10:profile.append((yy,zbase+(i+2)*rise))
 # Twelfth riser belongs to the receiving landing; never fold a zero-thickness riser back on itself.
 profile.append((end_embedded,zend-rise-.18))
 v=[(xx,y,z) for xx in [x,x+2.2] for y,z in profile];N=len(profile)
 faces=[tuple(range(N-1,-1,-1)),tuple(range(N,2*N))]
 for i in range(N):j=(i+1)%N;faces.append((i,j,j+N,i+N))
 ob=mesh(name,v,faces,'FLOOR',group)
 # Recalculate outside normals for extruded concave profile.
 import bmesh
 bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
 return ob
for st in G['stairs']:
 a,b,A,B=st['opening'];gr='STAIR_CORE_'+st['id']
 for level in [0,4]:
  flight(st['id']+f'_L{level}_UP1',a,6.4,3.1,level,level+2,gr)
  flight(st['id']+f'_L{level}_UP2',a+2.5,3.1,6.4,level+2,level+4,gr)
  box(st['id']+f'_MID_{level}',[a,.9,level+1.82,A,3.1,level+2],'FLOOR',gr)
  # Centre rails outside both 2.2m clear flights: .3 gap, boundary rails in opening reveals.
  for x,y0,y1,z0,z1 in [(a-.045,6.4,3.1,level,level+2),(a+2.245,6.4,3.1,level,level+2),(a+2.455,3.1,6.4,level+2,level+4),(A+.045,3.1,6.4,level+2,level+4)]:
   slopebeam((x,y0,z0+1.10),(x,y1,z1+1.10),.04,.04,'HANDRAIL_'+st['id'],gr)
   for u in [0,.25,.5,.75,1]:
    y=y0+(y1-y0)*u;z=z0+(z1-z0)*u
    box('RAIL_POST_'+st['id'],[x-.015,y-.015,z,x+.015,y+.015,z+1.08],'RAIL',gr)
  guardline('MID_BACK_'+st['id'],(a,.855),(A,.855),level+2,1.10,gr)
  guardline('MID_W_'+st['id'],(a-.045,.855),(a-.045,3.1),level+2,1.10,gr)
  guardline('MID_E_'+st['id'],(A+.045,.855),(A+.045,3.1),level+2,1.10,gr)
 for z in [4,8]:
  # Upper opening guard excludes arrival edge of upper flight.
  guardline('TOP_EDGE_'+st['id'],(a,6.45),(a+2.25,6.45),z,1.1,gr)
 stair_report.append(dict(id=st['id'],opening=st['opening'],clear_run=2.2,risers_per_floor=24,going=.3,rise=4/24,mid_depth=2.2,
  headroom_parallel_flight=3.82,top_landing_depth=8.8-6.4,headroom_status='analytic repeated-flight underside; sampled mesh check required'))
# High-frequency public furniture, actual open legs.
for it in G['furniture']:
 b=it['bounds'][:]
 if it['id']=='P1_CHANGE_W':b[3]=21.85
 if it['id']=='P1_WAIT':b[0]=28.15;b[3]=29.3
 x,y,z,X,Y,Z=b;gr='INTERIOR_F%02d'%(min(3,int(z/4)+1));pa=Parts()
 if it['kind'] in ['bench','table','reception']:
  pa.box([x,y,Z-.045,X,Y,Z],'WOOD')
  for xx in [x+.08,X-.12]:
   for yy in [y+.06,Y-.10]:pa.box([xx,yy,z,xx+.04,yy+.04,Z-.045],'FRAME')
 elif it['kind']=='notice':
  pa.box([x,y,Z-.65,X,Y,Z],'BOARD')
  pa.box([x,y,z,x+.035,Y,Z-.65],'FRAME');pa.box([X-.035,y,z,X,Y,Z-.65],'FRAME')
 pa.finish(it['id'],gr)
# Low-depth support rooms get intended use props, never fill main route.
for r in G['rooms']:
 if r['kind']!='support':continue
 x,y,X,Y=r['rect'];z=(r['floor']-1)*4;gr=f"INTERIOR_F{r['floor']:02}"
 if 'WC' in r['id']:
  pa=Parts()
  for i in range(3):
   xx=x+.5+i*.95
   pa.box([xx,y+.4,z+.70,xx+.6,y+.9,z+.83],'WALL')
   pa.box([xx,y+.4,z,xx+.07,y+.9,z+.7],'METAL')
  pa.finish(r['id']+'_SINK_BLOCKS',gr)
 else:
  pa=Parts()
  for xx in [x+.2,x+1.4]:
   pa.box([xx,y+.2,z,xx+1,y+.6,z+1.2],'WOOD')
   for zz in [.4,.8]:pa.box([xx,y+.18,z+zz,xx+1,y+.2,z+zz+.025],'FRAME')
  pa.finish(r['id']+'_STORAGE',gr)
# Entrance recognition is structural material ownership, blank sign, no school name.
EXT_SOLIDS.box([21.8,0,3.3,28.2,2,3.6],'ENTRY_WOOD')
EXT_SOLIDS.finish('EXT_WHOLE_UNION','EXTERIOR')
# Rainwater downpipes on solid corner piers; simple bent rectangular metal sections.
for x,y in [(0.34,3.97),(51.66,3.97),(106.34,3.97),(149.66,22.03),(64.34,27.96),(93.66,27.96)]:
 box('RAINPIPE',[x-.035,y-.035,.12,x+.035,y+.035,12.25],'FRAME','EXTERIOR')
# Origin is an EMPTY common reference; coordinates are baked in geometry, linked instances retain placements.
root=bpy.data.objects.new(P+'_ROOT',None);whole.objects.link(root);root['units']='metres';root['front']='south -Y'
root['world_xy']=G['origin_world_xy'];root['engineering_xy_offset']=[0,51];root['engineering_z_offset']=8
for ob in list(whole.all_objects):
 if ob!=root:ob.parent=root
# Context is excluded from FBX and source stats.
box('GROUND',[-40,-30,-.32,190,60,-.27],'FLOOR',context)
box('ENTRY_PAVING',[17,-9,-.27,39,0,-.251],'BAND_REV',context)
# All texture images pack; paths remain relative on save.
for im in bpy.data.images:
 if im.source=='FILE':im.pack()
for c in scene.collection.children:
 if c==checks:c.hide_render=True;c.hide_viewport=True
for f in range(1,4):
 groups[f'CEILING_F{f:02}'].hide_render=False
scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=True
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB'
scene.render.resolution_x=2560;scene.render.resolution_y=1440;scene.render.resolution_percentage=100
scene.world.color=(.6,.6,.6);scene.world.use_nodes=True
bg=scene.world.node_tree.nodes.get('Background');bg.inputs[0].default_value=(.72,.82,1,1);bg.inputs[1].default_value=.6
sun=bpy.data.lights.new('EARLY_SUMMER_SUN','SUN');sun.energy=2.5;sun.angle=math.radians(5)
ob=bpy.data.objects.new('EARLY_SUMMER_SUN',sun);context.objects.link(ob);ob.rotation_euler=[math.radians(x) for x in (30,-20,-35)]
scene.view_settings.view_transform='AgX'
camdata=bpy.data.cameras.new('CAMERA');cam=bpy.data.objects.new('CAMERA',camdata);context.objects.link(cam);scene.camera=cam
camdata.type='ORTHO';camdata.lens=50
def camera(target,az,el,scale):
 t=Vector(target);a=math.radians(az);e=math.radians(el)
 cam.location=t+Vector((math.cos(a)*math.cos(e),math.sin(a)*math.cos(e),math.sin(e)))*200
 cam.rotation_euler=(t-cam.location).to_track_quat('-Z','Y').to_euler();camdata.ortho_scale=scale
camera((75,14,5.5),225,30,150)
bpy.ops.object.select_all(action='DESELECT')
architecture=[o for o in whole.all_objects if o.type=='MESH']
# Only used material slots. In particular linked furniture must share identical compact layouts.
for me in set(o.data for o in architecture):
 used=sorted(set(p.material_index for p in me.polygons));old=list(me.materials)
 indices=[used.index(p.material_index) for p in me.polygons]
 me.materials.clear()
 for i in used:me.materials.append(old[i])
 for poly,i in zip(me.polygons,indices):poly.material_index=i
for o in architecture:o.select_set(True)
bpy.context.view_layer.objects.active=architecture[0]
scene['reference_sha256']=hashlib.sha256((OUT.parent/'Reference/Revision01/SL_BLD_C01_MAIN_01_REFERENCE_01_REV_01_GEOMETRY.json').read_bytes()).hexdigest()
scene['trial_build']='new architectural mesh construction; no reference blend imported'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/(P+'.blend')),compress=True)
# FBX expands linked placements into independent export meshes to avoid Blender 5.2 linked-slot exporter warnings.
original_meshes={o:o.data for o in architecture}
for o in architecture:
 if o.data.users>1:o.data=o.data.copy()
bpy.context.view_layer.update()
bpy.ops.export_scene.fbx(filepath=str(OUT/(P+'.fbx')),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,
 axis_forward='-Y',axis_up='Z',add_leaf_bones=False,mesh_smooth_type='FACE',path_mode='RELATIVE',use_mesh_modifiers=True,use_custom_props=True)
for o,me in original_meshes.items():o.data=me
def bbox(objects):
 coords=[o.matrix_world@Vector(v) for o in objects for v in o.bound_box]
 return [[min(v[i] for v in coords) for i in range(3)],[max(v[i] for v in coords) for i in range(3)]]
meshes=set(o.data for o in architecture)
stats=dict(mesh_objects=len(architecture),unique_mesh_sources=len(meshes),linked_placements=len(architecture)-len(meshes),
 source_vertices=sum(len(m.vertices) for m in meshes),source_triangles=sum(len(p.vertices)-2 for m in meshes for p in m.polygons),
 placed_vertices=sum(len(o.data.vertices) for o in architecture),placed_triangles=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in architecture),
 materials=len(mats),texture_pngs=len(list((OUT/'Textures').glob('*.png'))),architectural_bbox=bbox(architecture),classrooms=classcounts,locker_nominal=sum(b['nominal'] for b in banks),
 groups={n:len(c.objects) for n,c in groups.items()},reference_imported=False)
data={k:G[k] for k in ['control','segments','body_rects','origin_world_xy','engineering_origin_world_xy','ground_engineering_z','floors','court','terrace','rt01','roof','player_interface','character','routes']}
data.update(asset=P,source_geometry='new mesh generation in build_trial.py',entrances=G['entrances'],rooms=G['rooms'],openings=opening_log,lockers=banks,stairs=stair_report,
 authorized_internal_adjustments=['Player paired column pitch .90 ->1.06; Y13.47,14.53,16.67,17.73,19.87,20.93; original30 seats/room/door/business fixed','Player actual approach y18.70 ->18.80 and seat y19.625 ->19.870; recovery(45,18.7) remains candidate unchanged','Shared desk legs y+/-.26 ->+/-.29 within original .65m desktop to clear finite knee proxy','Main locker double depth .60 -> .66; capacity/room/positions unchanged','Actual cabinet boards and two-panel vertical sliding front candidate','All background classrooms use linked 30-seat desk/chair sources','Sliding door panels park on interior face, not embedded in solid wall; opening widths unchanged','Main left changing bench shortened .15m to x21.85; right waiting bench moved to x28.15..29.30 to clear parked glass leaves'],
 player_layout=dict(desk_x=[42.625,43.575,45.775,46.725,47.675],desk_y=[13.47,14.53,16.67,17.73,19.87,20.93],pair_pitch=1.06,conservative_art_width=1.039655172413793,seated_pair_gap=1.06-1.039655172413793,occupied_cross_aisle=2.14-1.039655172413793),
 stats=stats,uv=dict(name='UV_METRIC_64',method='face planar metric tile',px_m=64,tile_px=256,tile_m=4,overlap='intentional repeated materials'))
for name,obj in [('GEOMETRY.json',data),('STATISTICS.json',stats)]:
 (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('TRIAL_BUILD_DONE',json.dumps(stats),flush=True)
