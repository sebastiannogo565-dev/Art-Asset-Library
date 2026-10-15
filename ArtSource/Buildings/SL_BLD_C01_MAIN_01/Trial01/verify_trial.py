"""Native reopen and independent actual FBX reimport; finite static checks, never a UE claim."""
import bpy,bmesh,json,math,hashlib
from pathlib import Path
from mathutils import Vector
OUT=Path(__file__).parent;P='SL_BLD_C01_MAIN_01_TRIAL_01'
G=json.loads((OUT/'GEOMETRY.json').read_text(encoding='utf-8'))
def write(n,v):(OUT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
bpy.ops.wm.open_mainfile(filepath=str(OUT/(P+'.blend')))
obs=[o for o in bpy.data.collections['WHOLE'].all_objects if o.type=='MESH']
def bbox(obs):
 co=[o.matrix_world@Vector(v) for o in obs for v in o.bound_box]
 return [[min(v[i] for v in co) for i in range(3)],[max(v[i] for v in co) for i in range(3)]]
def vertical_hit(ob,x,y,z):
 p=ob.matrix_world.inverted()@Vector((x,y,z))
 hit,loc,n,idx=ob.ray_cast(p,Vector((0,0,-1)),distance=.8)
 return bool(hit)
holes=[]
for f in [2,3]:
 ob=bpy.data.objects[f'SLAB_F{f:02}_ACTUAL']
 for label,r in [('COURT',[74,15,86,24]),('LIFT',[80,.8,82.4,3.2])]+[(s['id'],s['opening']) for s in G['stairs']]:
  x,y=(r[0]+r[2])/2,(r[1]+r[3])/2
  slabclear=not vertical_hit(ob,x,y,(f-1)*4+.1)
  ceiling=bpy.data.objects[f'CEILING_F{f-1:02}']
  ceilingclear=not vertical_hit(ceiling,x,y,(f-2)*4+3.6)
  holes.append(dict(floor=f,opening=label,slab_clear=slabclear,lower_ceiling_clear=ceilingclear))
bad=[];density=[];topology=[];faces={};duplicates=[];micro_faces=0;all_density=[]
for me in set(o.data for o in obs):
 uv=me.uv_layers.active
 if not uv or len(uv.data)!=len(me.loops):bad.append(me.name)
 bm=bmesh.new();bm.from_mesh(me)
 deg=sum(1 for f in bm.faces if f.calc_area()<1e-10)
 boundary=sum(1 for e in bm.edges if e.is_boundary);nonman=sum(1 for e in bm.edges if not e.is_manifold)
 topology.append(dict(mesh=me.name,degenerate_faces=deg,boundary_edges=boundary,nonmanifold_edges=nonman))
 bm.free()
 if uv:
  ratios=[]
  for poly in me.polygons:
   if poly.area<1e-10:continue
   # UV triangle area / actual polygon area, square root converts to texel/m.
   pts=[uv.data[i].uv.copy() for i in poly.loop_indices]
   area=abs(sum(pts[i].x*pts[(i+1)%len(pts)].y-pts[(i+1)%len(pts)].x*pts[i].y for i in range(len(pts)))/2)
   value=256*math.sqrt(area/poly.area);all_density.append(value)
   if poly.area>=.0001:ratios.append(value)
   else:micro_faces+=1
  density += [dict(mesh=me.name,min=min(ratios),max=max(ratios))] if ratios else []
source=dict(blend_sha256=hashlib.sha256((OUT/(P+'.blend')).read_bytes()).hexdigest(),bbox=bbox(obs),
 objects=len(obs),unique_meshes=len(set(o.data for o in obs)),missing_uv=bad,density_min=min(x['min'] for x in density),density_max=max(x['max'] for x in density),
 images=[dict(name=im.name,packed=bool(im.packed_file),size=list(im.size)) for im in bpy.data.images if im.source=='FILE'],
 holes=holes,topology=topology,default_visible_groups=[c.name for c in bpy.data.collections['WHOLE'].children if not c.hide_render])
source['density_measurement']={'area_threshold_m2':.0001,'excluded_sub_cm2_faces':micro_faces,'unfiltered_range':[min(all_density),max(all_density)],
 'reason':'Subpixel contact faces near global UV coordinates suffer float cancellation; full UV presence and topology still checked for all faces.'}
def material_area(objects):
 result={}
 for ob in objects:
  for p in ob.data.polygons:
   name=ob.data.materials[p.material_index].name if p.material_index<len(ob.data.materials) else 'MISSING'
   result[name]=result.get(name,0)+p.area
 return result
source_areas=material_area(obs);source['material_area_m2']=source_areas
slots={}
for ob in obs:
 if ob.data.name in slots:continue
 slots[ob.data.name]=dict(materials=[m.name if m else None for m in ob.data.materials],placements=sum(o.data==ob.data for o in obs))
write('MATERIAL_SLOTS.json',slots)
for im in bpy.data.images:
 if im.name.startswith('StudentChibi_Front_Idle'):
  source['character_packed_sha256']=hashlib.sha256(im.packed_file.data).hexdigest() if im.packed_file else None
source['character_disk_sha256']=hashlib.sha256(Path(G['character']['source']).read_bytes()).hexdigest()
source['entry_ray_clearances']=[]
for o in G['openings']:
 if o['id'] not in ['C01_MAIN','C01_N','C01_E','F1_WL_D_REV','F2_W4_D','TERRACE_ACCESS']:continue
 normal=next((x.get('normal',0) for x in json.loads((OUT.parent/'Reference/Revision01/SL_BLD_C01_MAIN_01_REFERENCE_01_REV_01_GEOMETRY.json').read_text(encoding='utf-8'))['openings'] if x['id']==o['id']),0)
 axis=0 if o['axis']=='X' else 1;pt=[0,0,o['z0']+1];pt[axis]=(o['lo']+o['hi'])/2;pt[1-axis]=o['line']-normal*.15
 distances=[]
 for sign in [-1,1]:
  direction=Vector((sign,0,0) if axis==0 else (0,sign,0));hits=[]
  for ob in obs:
   inv=ob.matrix_world.inverted();hit,loc,n,idx=ob.ray_cast(inv@Vector(pt),(inv.to_3x3()@direction).normalized(),distance=5)
   if hit:hits.append(((ob.matrix_world@loc)-Vector(pt)).length)
  distances.append(min(hits) if hits else None)
 source['entry_ray_clearances'].append(dict(id=o['id'],distances=distances,actual_clear=sum(distances) if all(x is not None for x in distances) else None))
write('NATIVE_REOPEN.json',source)
# Analytic finite envelopes use actual desk/chair object bounds; no reference rectangle substitutions.
def rect(ob,pull=False):
 b=bbox([ob]);return [b[0][0]+(.25 if pull else 0),b[0][1],b[1][0]+(.25 if pull else 0),b[1][1]]
def pdist(p,r):return math.hypot(max(r[0]-p[0],0,p[0]-r[2]),max(r[1]-p[1],0,p[1]-r[3]))
def sdist(a,b,r):
 # exact segment-to-AABB distance via vertices, projection and edge intersection.
 dx,dy=b[0]-a[0],b[1]-a[1];l=dx*dx+dy*dy
 def dp(q):
  t=max(0,min(1,((q[0]-a[0])*dx+(q[1]-a[1])*dy)/l)) if l else 0
  return math.hypot(q[0]-a[0]-t*dx,q[1]-a[1]-t*dy)
 lo,hi=0.,1.
 for aa,dd,mn,mx in [(a[0],dx,r[0],r[2]),(a[1],dy,r[1],r[3])]:
  if abs(dd)<1e-10:
   if not mn<=aa<=mx:lo=2;break
  else:
   t0,t1=sorted([(mn-aa)/dd,(mx-aa)/dd]);lo=max(lo,t0);hi=min(hi,t1)
 if lo<=hi and hi>=0 and lo<=1:return 0.
 return min(pdist(a,r),pdist(b,r),*(dp(q) for q in [(r[0],r[1]),(r[2],r[1]),(r[2],r[3]),(r[0],r[3])]))
player=[o for o in obs if o.name.startswith('F2_W4_') and ('DESK_' in o.name or 'CHAIR_' in o.name)]
routes=G['player_interface'];states=[]
for pulled in [False,True]:
 rs=[rect(o,pulled and 'CHAIR_' in o.name) for o in player]
 paths=routes['route_to_approach']+routes['route_return_via_teaching']
 clearance=min(sdist(a,b,r) for a,b in zip(paths,paths[1:]) for r in rs)
 bus=min(pdist([45,19.5],r) for r in rs);rec=min(pdist([45,18.7],r) for r in rs)
 states.append(dict(chairs='pulled .25m' if pulled else 'rest',main_route_center_clearance=clearance,full_width=2*clearance,
  main_width_1_10_pass=clearance>=.55-2e-6,business_distance=bus,business_055_pass=bus>=.55-2e-6,recovery_distance=rec))
shoe=dict(nominal=sum(x['nominal'] for x in G['lockers']),main=600,link=300,
 shoe_assumption=dict(length=.29,width=.105,height=.115,pair_width=.235,depth_allowance=.01),
 previous_gross=.60,previous_effective_depth=(.60-.012)/2-.020,new_gross=.66,new_effective_depth=(.66-.012)/2-.020,
 min_cavity_width=.288,min_cavity_height=.263,door_open_height=.138,depth_margin=.004,
 aisle=2.6-.66,one_operation_strip=.70,one_active_free=2.6-.66-.70,two_active_free=2.6-.66-1.4,
 two_active_pass=False,top_row_bottom=1.2,top_row_reach='door handle1.328m; reach/actual shoe handling not validated',
 closed_front_track_in_cabinet=True,hardware='candidate half-height vertical lift; no tested fastener/tool tolerances')
limits=[
 dict(id='SEAT_TRANSITION',status='NOT_PASSED',detail='Own chair occupies endpoint. Static lateral sit candidate only; continuous body/joint motion and full-size seated character art unavailable. Standing capsule cannot be swept through chair.'),
 dict(id='PAIRED_OCCUPANTS',status='STATIC_ENVELOPE_CANDIDATE',detail='Trial-only pair pitch1.06m vs conservative unchanged art width1.039655m: no static shoulder overlap, only .020345m pair margin. Occupied inter-pair aisle1.100345m. Sitting/motion not approved.',gap=.020344827586207),
 dict(id='LOCKER_TWO_ACTIVE',status='NOT_PASSED',detail='Two .70m operating envelopes leave .54m, below .68m capsule and1.039655m art width.'),
 dict(id='FRONT_CROSSING',status='NOT_PASSED',detail='Arrival and departure paths cross near y1.375; simultaneous finite envelopes collide.'),
 dict(id='UPPER_BANK_QUEUE',status='NOT_PASSED',detail='Queue at22.9/6.2 and22.9/7.9 consumes1.2m cabinet-end branch; .68m capsule leaves.52m, character1.039655 leaves.160345m.'),
 dict(id='RT01',status='NOT_OPEN',detail='Original588m2 retained only as metadata. No support, door, access route or export geometry created.'),
 dict(id='TERRACE',status='CANDIDATE',detail='Geometry finish8.03/guard9.23 synchronized. Waterproofing, slope, real drainage, anchoring not certified.')]
write('HIGH_FREQUENCY_CHECKS.json',dict(player_states=states,shoe=shoe,limits=limits,
 stairs=G['stairs'],scope='finite static geometry/analytic; no navigation or gameplay',baseline_tolerance_m=2e-6))
# Save source summary, then a true empty-scene FBX reimport.
expected_names={o.name for o in obs};expected_groups={o.name:o.get('group') for o in obs}
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=str(OUT/(P+'.fbx')),use_custom_props=True)
imp=[o for o in bpy.context.scene.objects if o.type=='MESH']
gotnames={o.name for o in imp}
re=dict(fbx_sha256=hashlib.sha256((OUT/(P+'.fbx')).read_bytes()).hexdigest(),bbox=bbox(imp),
 mesh_objects=len(imp),expected_objects=len(expected_names),missing_names=sorted(expected_names-gotnames),extra_names=sorted(gotnames-expected_names),
 missing_group_properties=[o.name for o in imp if not o.get('group')],unexpected_check_objects=[o.name for o in imp if 'CHECK' in o.name or 'CHAR' in o.name],
 uv_missing=[o.name for o in imp if not o.data.uv_layers],empty_materials=[o.name for o in imp if any(m is None for m in o.data.materials)],
 measured_entries=[dict(id=o.name,width=o.get('clear_width'),height=o.get('clear_height')) for o in imp if o.get('opening_id') in ['C01_MAIN','C01_N','C01_E','TERRACE_ACCESS','F2_W4_D','F1_WL_D_REV']],
 axis='FBX -Y forward / Z up; reimport same metre coordinates',unit_scale=bpy.context.scene.unit_settings.scale_length,
 import_images=[dict(name=im.name,size=list(im.size),path=im.filepath,exists=Path(bpy.path.abspath(im.filepath)).exists()) for im in bpy.data.images if im.source=='FILE'])
re['material_area_m2']=material_area(imp)
re['material_area_relative_error']={k:abs(re['material_area_m2'].get(k,0)-v)/max(1e-8,v) for k,v in source_areas.items()}
re['entry_ray_clearances']=[]
for o in G['openings']:
 if o['id'] not in ['C01_MAIN','C01_N','C01_E','F2_W4_D','F1_WL_D_REV','TERRACE_ACCESS']:continue
 normal=next((x.get('normal',0) for x in json.loads((OUT.parent/'Reference/Revision01/SL_BLD_C01_MAIN_01_REFERENCE_01_REV_01_GEOMETRY.json').read_text(encoding='utf-8'))['openings'] if x['id']==o['id']),0)
 axis=0 if o['axis']=='X' else 1;pt=[0,0,o['z0']+1];pt[axis]=(o['lo']+o['hi'])/2;pt[1-axis]=o['line']-normal*.15
 distances=[]
 for sign in [-1,1]:
  direction=Vector((sign,0,0) if axis==0 else (0,sign,0));hits=[]
  for ob in imp:
   inv=ob.matrix_world.inverted();hit,loc,n,idx=ob.ray_cast(inv@Vector(pt),(inv.to_3x3()@direction).normalized(),distance=5)
   if hit:hits.append(((ob.matrix_world@loc)-Vector(pt)).length)
  distances.append(min(hits) if hits else None)
 re['entry_ray_clearances'].append(dict(id=o['id'],distances=distances,actual_clear=sum(distances) if all(x is not None for x in distances) else None))
write('FBX_REIMPORT.json',re)
print('NATIVE',source['bbox'],'UV range',source['density_min'],source['density_max'],'degenerate',sum(x['degenerate_faces'] for x in topology),flush=True)
print('FINITE',json.dumps(states),flush=True)
print('REIMPORT',json.dumps({k:v for k,v in re.items() if k!='import_images'}),flush=True)
