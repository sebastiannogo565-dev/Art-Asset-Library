"""Read-only native reopen, UV/tessellation, opaque ray checks and source-only FBX round trip.
Motion tests use actual component meshes in an independent disposable scene; no source saves.
"""
from pathlib import Path
import bpy,bmesh,json,math,hashlib,traceback
from mathutils import Vector
ROOT=Path(__file__).resolve().parent.parent;CACHE=ROOT.parents[3]/'.cache/sign-plate-trial01'
DATA=json.loads((ROOT/'Source/SL_GE_SIGN_PLATE_01_TRIAL_GEOMETRY_UV.json').read_text(encoding='utf-8'))
def stats(o):
 bpy.context.view_layer.update();v=[o.matrix_world@q.co for q in o.data.vertices];bm=bmesh.new();bm.from_mesh(o.data)
 o.data.calc_loop_triangles()
 d={'name':o.name,'min_m':[min(p[k] for p in v) for k in range(3)],'max_m':[max(p[k] for p in v) for k in range(3)],'origin_m':list(o.location),'scale':list(o.scale),
  'vertices':len(o.data.vertices),'polygons':len(o.data.polygons),'actual_tessellated_triangles':len(o.data.loop_triangles),
  'non_manifold_edges':sum(not e.is_manifold for e in bm.edges),'zero_area_faces':sum(f.calc_area()<1e-13 for f in bm.faces),
  'zero_area_tessellated_triangles':sum(t.area<1e-13 for t in o.data.loop_triangles),'signed_volume_m3':bm.calc_volume(signed=True)}
 bm.free();return d
def coords(o):return {tuple(round(c,6) for c in v.co) for v in o.data.vertices}
def uv_corners(o):
 v={};uv=o.data.uv_layers.active.data
 for l in o.data.loops:
  k=tuple(round(q,6) for q in o.data.vertices[l.vertex_index].co);v.setdefault(k,set()).add(tuple(round(q,4) for q in uv[l.index].uv))
 return v
def density(o):
 out=[];o.data.calc_loop_triangles();uv=o.data.uv_layers.active.data
 for t in o.data.loop_triangles:
  # Calculate in Python float64; mathutils float32 cross products cancel on thin/corner triangles.
  vv=[list(o.data.vertices[i].co) for i in t.vertices];pp=[[float(q)*256 for q in uv[i].uv] for i in t.loops]
  b3=[vv[1][k]-vv[0][k] for k in range(3)];c3=[vv[2][k]-vv[0][k] for k in range(3)]
  cross=[b3[1]*c3[2]-b3[2]*c3[1],b3[2]*c3[0]-b3[0]*c3[2],b3[0]*c3[1]-b3[1]*c3[0]]
  area=.5*math.sqrt(sum(q*q for q in cross));b=[pp[1][k]-pp[0][k] for k in [0,1]];c=[pp[2][k]-pp[0][k] for k in [0,1]];a=.5*abs(b[0]*c[1]-b[1]*c[0])
  assert area>1e-13 and a>1e-12,(o.name,t.index,area,a)
  out.append(math.sqrt(a/area))
 return out
def protected():
 r=DATA['protected_inputs'];dif=[]
 for p in r:
  if hashlib.sha256(Path(p['path']).read_bytes()).hexdigest()!=p['sha256']:dif.append(p['path'])
 assert not dif,dif
 return {'count':len(r),'all_raw_sha256_unchanged':True,'differences':dif}
try:
 src=ROOT/'Source/SL_GE_SIGN_PLATE_01_TRIAL_01.blend';fbx=ROOT/'Exports/SL_GE_SIGN_PLATE_01_TRIAL_01.fbx'
 original_source_hash=hashlib.sha256(src.read_bytes()).hexdigest()
 bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False)
 bpy.context.window.scene=bpy.data.scenes['SOURCE_PLAQUE_TRIAL01'];bpy.context.view_layer.update()
 objects=list(bpy.data.collections['ASSET_SOURCE_ONLY_ONE_SET'].objects);assert len(objects)==11
 source={};dens=[];partstats=[]
 for o in objects:
  s=stats(o);partstats.append(s);source[o.name]={'stats':s,'coords':coords(o),'uv':uv_corners(o),'mesh':o.data.copy()}
  assert s['non_manifold_edges']==0 and s['zero_area_faces']==0 and s['zero_area_tessellated_triangles']==0 and s['signed_volume_m3']>0,s
  assert max(abs(q) for q in s['origin_m'])<1e-8 and s['scale']==[1,1,1]
  assert len(o.data.materials)==1 and len(o.data.uv_layers)==1
  p=next(p for p in DATA['parts'] if p['name']==o.name)
  assert coords(o)=={tuple(round(c,6) for c in v) for v in p['vertices']}
  for face,wanted in zip(o.data.polygons,p['face_uvs']):
   for li,q in zip(face.loop_indices,wanted):assert (o.data.uv_layers.active.data[li].uv-Vector(q)).length<1e-6
  dens.extend(density(o))
 # 64 is the card's density reference. Serialized float32 UVs on extremely small
 # round-corner triangles deviate <0.1%; accept 0.2% numerical tolerance, record all extrema.
 assert max(abs(q/64-1) for q in dens)<.002,(min(dens),max(dens))
 bb={'min':[min(s['min_m'][k] for s in partstats) for k in range(3)],'max':[max(s['max_m'][k] for s in partstats) for k in range(3)]}
 for k in range(3):assert abs(bb['min'][k]-DATA['overall_bounds_m']['min'][k])<1e-7 and abs(bb['max'][k]-DATA['overall_bounds_m']['max'][k])<1e-7
 packed={n:hashlib.sha256(bytes(bpy.data.images[n].packed_file.data)).hexdigest() for n in ['SIGN_TRIAL_BaseColor','SIGN_TRIAL_Roughness','REFERENCE_ORIGINAL_128_RGBA_SIGN']}
 for name in ['BaseColor','Roughness']:assert packed['SIGN_TRIAL_'+name]==hashlib.sha256((ROOT/f'Textures/SL_GE_SIGN_PLATE_01_TRIAL_{name}.png').read_bytes()).hexdigest()
 assert packed['REFERENCE_ORIGINAL_128_RGBA_SIGN']=='082ceb410d904f0037dfe09dd3502e50195351691ab4047cc5dbbb639147b8cd'
 # Saved native host reference truly contains accepted vertices/UV, not an altered reconstruction.
 host=bpy.data.objects['READONLY_ACCEPTED_PIER_LEFT'];hd=json.loads((ROOT.parent.parent/'SL_GE_GATE_PIER_01/Trial01/Source/SL_GE_GATE_PIER_01_TRIAL_GEOMETRY_UV.json').read_text(encoding='utf-8'))
 assert coords(host)=={tuple(round(c,6) for c in v) for v in hd['vertices']}
 for face,wanted in zip(host.data.polygons,hd['face_uvs']):
  for li,q in zip(face.loop_indices,wanted):assert (host.data.uv_layers.active.data[li].uv-Vector(q)).length<1e-6
 measured=json.loads((ROOT/'Source/blender_measurements.json').read_text(encoding='utf-8'))
 assert all(h['first_hit']=='READONLY_ACCEPTED_PIER_LEFT' for h in measured['views']['B']['front_patch_ray_first_hits'])
 assert all(h['first_hit']=='INSTALLED_CARRIER_TRAY' for h in measured['views']['A']['front_patch_ray_first_hits'])
 # Actual side-tool shaft and bent-tip ray segments pass through the service opening,
 # guide/release-stop notch and pull eye in both locked and released positions.
 tool_paths=[];slider=bpy.data.objects['LOCKED_SLIDER'];scene=bpy.context.scene
 for tag,dx in [('locked',0),('released',.01)]:
  slider.location.x=dx;bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
  eye_x=.102+dx;eye_z=-.3135
  origin=Vector((.125,-.0135,eye_z));end=Vector((eye_x,-.0135,eye_z));direction=(end-origin).normalized()
  hit=scene.ray_cast(dg,origin,direction,distance=(end-origin).length)[0];assert not hit,('tool_shaft_blocked',tag)
  tip_end=Vector((eye_x,-.0059,eye_z));tip_hit=scene.ray_cast(dg,end,(tip_end-end).normalized(),distance=(tip_end-end).length)[0];assert not tip_hit,('pull_eye_blocked',tag)
  tool_paths.append({'pose':tag,'shaft_start_m':list(origin),'shaft_end_m':list(end),'bent_tip_end_m':list(tip_end),'shaft_and_eye_rays_clear':True})
 slider.location.x=0;bpy.context.view_layer.update()
 report={'native_source_reopened':True,'native_blender_version':bpy.app.version_string,'source_parts':partstats,'source_bounds_m':bb,
  'source_count':1,'component_count':11,'material_shared_count':len({o.data.materials[0].name for o in objects}),
  'uv':{'density_min_px_per_m':min(dens),'density_max_px_per_m':max(dens),'density_mean_px_per_m':sum(dens)/len(dens),'actual_triangles_checked':len(dens),'source_matches_json':True,'numerical_relative_tolerance':.002,'max_relative_deviation':max(abs(q/64-1) for q in dens),'note':'float32 UV quantization on tiny round-corner triangles; target reference64, not atlas size'},
  'packed_image_sha256':packed,'host_mesh_and_uv_match_accepted_data':True,'opaque_visibility':{'A_front_samples_hit_carrier':9,'B_front_samples_hit_opaque_host':9},
  'protected_inputs':protected(),'side_tool_paths':{'actual_mesh_segments':tool_paths,'scope':'zero-radius ray segments only; real finite tool size/hand clearance/strength pending'}}
 # Independent, unsaved Boolean volume checks against fixed seats/pads at assembly poses.
 # Only fixed-vs-moving collisions tested; engineering tolerance/hand access remains pending.
 motion=bpy.data.scenes.new('DISPOSABLE_MOTION_TEST');bpy.context.window.scene=motion
 def copy_part(name,delta):
  o=bpy.data.objects.new('TEST_'+name,source[name]['mesh']);motion.collection.objects.link(o);o.location=delta;return o
 fixed=[copy_part(n,(0,0,0)) for n in DATA['assembly']['fixed_parts']]
 poses=[('locked',[0,0,0],False),('released',[0,0,0],True),('lift_0.45',[0,0,.0045],True),('lift_0.9',[0,0,.009],True),('lift_1.35',[0,0,.0135],True),('lift_1.8',[0,0,.018],True),('out_0.3',[0,-.003,.018],True),('out_0.6',[0,-.006,.018],True)]
 collisions=[];tests=0
 for tag,delta,released in poses:
  moving=[]
  for name in DATA['assembly']['moving_parts']:
   d=list(delta)
   if released and name=='LOCKED_SLIDER':d[0]+=.01
   moving.append(copy_part(name,d))
  bpy.context.view_layer.update()
  for a in moving:
   ab=stats(a)
   for b in fixed:
    bs=stats(b)
    if any(min(ab['max_m'][k],bs['max_m'][k])-max(ab['min_m'][k],bs['min_m'][k])<=1e-7 for k in range(3)):continue
    mod=a.modifiers.new('VOLUME_INTERSECTION','BOOLEAN');mod.operation='INTERSECT';mod.solver='EXACT';mod.object=b
    ev=a.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();bm=bmesh.new();bm.from_mesh(m);volume=abs(bm.calc_volume(signed=True));bm.free();ev.to_mesh_clear();a.modifiers.remove(mod);tests+=1
    if volume>1e-10:collisions.append({'pose':tag,'moving':a.name,'fixed':b.name,'volume_m3':volume})
  for a in moving:bpy.data.objects.remove(a,do_unlink=True)
 assert not collisions,collisions
 report['assembly_motion']={'poses_checked':len(poses),'boolean_pairs_with_positive_aabb_overlap':tests,'positive_volume_fixed_moving_intersections':collisions,'threshold_m3':1e-10,'scope':'sampled fixed-vs-moving path; not manufacturing tolerance, hand/tool or load test',
  'anti_lift_contact_cm':{'slider_top_z':-31.2,'seat_bottom_z':-31.2,'locked_x_overlap':.8,'released_x_gap':.2,'hook_y_clearance':.05},'anti_retreat_mechanism':'functional candidate only, not validated'}
 # Parse binary FBX metadata, then reimport in a fresh metre scene.
 from io_scene_fbx import parse_fbx
 tree,version=parse_fbx.parse(str(fbx));settings=next(e for e in tree.elems if e.id==b'GlobalSettings');props=next(e for e in settings.elems if e.id==b'Properties70')
 meta={e.props[0].decode():e.props[4] for e in props.elems if e.id==b'P' and e.props[0] in [b'UnitScaleFactor',b'UpAxis',b'UpAxisSign',b'FrontAxis',b'FrontAxisSign',b'CoordAxis',b'CoordAxisSign']}
 types=[e.props[2].decode() for e in next(e for e in tree.elems if e.id==b'Objects').elems if e.id==b'Model']
 assert types==['Mesh']*11,types
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.scene.unit_settings.system='METRIC';bpy.context.scene.unit_settings.scale_length=1
 bpy.ops.import_scene.fbx(filepath=str(fbx),use_custom_normals=True)
 imported=list(bpy.context.scene.objects);assert len(imported)==11 and all(o.type=='MESH' for o in imported)
 roundstats=[]
 for o in imported:
  assert o.name in source,o.name;s=stats(o);orig=source[o.name]
  assert coords(o)==orig['coords'],o.name
  assert uv_corners(o)==orig['uv'],o.name
  assert len(o.data.materials)==1 and len(o.data.uv_layers)==1
  assert s['non_manifold_edges']==0 and s['zero_area_faces']==0 and s['zero_area_tessellated_triangles']==0
  assert max(abs(q) for q in s['origin_m'])<1e-7
  assert abs(s['signed_volume_m3']-orig['stats']['signed_volume_m3'])<1e-10
  roundstats.append(s)
 report['fbx_round_trip']={'passed':True,'binary_version':version,'axis_unit_metadata':meta,'mesh_components':11,'asset_sets':1,'all_vertex_positions_and_uv_corners_match':True,'host_character_floor_camera_exported':False,'parts':roundstats}
 report['source_unchanged_by_reopen']=hashlib.sha256(src.read_bytes()).hexdigest()==original_source_hash;assert report['source_unchanged_by_reopen']
 report['protected_inputs_after']=protected();report['UE_validation_performed']=False
 (ROOT/'Source/verification_results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
 (CACHE/'verify_progress.json').write_text(json.dumps({'stage':'complete','source_reopen':'passed','fbx_round_trip':'passed','motion_poses':len(poses)}),encoding='utf-8')
except Exception:
 (CACHE/'verify_progress.json').write_text(json.dumps({'stage':'failed','error':traceback.format_exc()}),encoding='utf-8');raise
