"""Independent Blender reopen and FBX round trip. Read-only for delivered source.
Run in a fresh Blender background process after build_trial.py finishes.
"""
from pathlib import Path
import bpy, bmesh, hashlib, json, math, traceback
from mathutils import Vector

ROOT=Path(__file__).resolve().parent.parent
PROGRESS=ROOT.parents[3]/'.cache/gate-pier-trial01/verify_progress.json'

def stats(o):
 bpy.context.view_layer.update();v=[o.matrix_world@q.co for q in o.data.vertices]
 bm=bmesh.new();bm.from_mesh(o.data)
 a={'dimensions_m':[max(q[k] for q in v)-min(q[k] for q in v) for k in range(3)],'min_m':[min(q[k] for q in v) for k in range(3)],
    'max_m':[max(q[k] for q in v) for k in range(3)],'origin_m':list(o.location),'scale':list(o.scale),
    'vertices':len(o.data.vertices),'polygons':len(o.data.polygons),'triangles':sum(len(p.vertices)-2 for p in o.data.polygons),
    'non_manifold_edges':sum(not e.is_manifold for e in bm.edges),'zero_area_faces':sum(f.calc_area()<1e-10 for f in bm.faces),
    'signed_volume_m3':bm.calc_volume(signed=True)}
 bm.free();return a

def geometry(o):return {tuple(round(c,6) for c in v.co) for v in o.data.vertices}

def uv_corners(o):
 values={};uv=o.data.uv_layers.active.data
 for loop in o.data.loops:
  key=tuple(round(c,6) for c in o.data.vertices[loop.vertex_index].co)
  values.setdefault(key,set()).add(tuple(round(c,5) for c in uv[loop.index].uv))
 return values

try:
 src=ROOT/'Source/SL_GE_GATE_PIER_01_TRIAL_01.blend';fbx=ROOT/'Exports/SL_GE_GATE_PIER_01_TRIAL_01.fbx'
 assert fbx.read_bytes().startswith(b'Kaydara FBX Binary  \x00\x1a\x00')
 bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False)
 source=bpy.data.objects['SM_SL_GE_GATE_PIER_01'];s=stats(source);coords=geometry(source);source_uv_corners=uv_corners(source)
 assert len(source.data.materials)==1 and len(source.data.uv_layers)==1
 assert all(abs(v)<1e-7 for v in s['origin_m']) and s['scale']==[1,1,1]
 assert all(abs(a-b)<2e-6 for a,b in zip(s['dimensions_m'],[.6,.6,2.4]))
 assert s['non_manifold_edges']==0 and s['zero_area_faces']==0 and s['signed_volume_m3']>0
 data=json.loads((ROOT/'Source/SL_GE_GATE_PIER_01_TRIAL_GEOMETRY_UV.json').read_text(encoding='utf-8'))
 assert coords=={tuple(round(c,6) for c in v) for v in data['vertices']}
 density=[]
 uv=source.data.uv_layers.active.data
 for face in source.data.polygons:
  loops=list(face.loop_indices);verts=[source.data.vertices[source.data.loops[k].vertex_index].co for k in loops]
  pp=[uv[k].uv*256 for k in loops]
  for i in range(1,len(loops)-1):
   area3=.5*(verts[i]-verts[0]).cross(verts[i+1]-verts[0]).length
   a=pp[i]-pp[0];b=pp[i+1]-pp[0];area2=.5*abs(a.x*b.y-a.y*b.x)
   assert area3>0 and area2>0
   d=math.sqrt(area2/area3);density.append(d);assert abs(d-64)<.003
 # Actual UV values in the saved editable source match the assigned metre layout.
 for face,expected in zip(source.data.polygons,data['face_uvs']):
  for li,wanted in zip(face.loop_indices,expected): assert (uv[li].uv-Vector(wanted)).length<1e-6
 packed={}
 for name in ['Trial_BaseColor','Trial_Roughness','REFERENCE_ORIGINAL_128_RGBA']:
  im=bpy.data.images[name];assert im.packed_file
  packed[name]=hashlib.sha256(bytes(im.packed_file.data)).hexdigest()
 assert packed['REFERENCE_ORIGINAL_128_RGBA']=='082ceb410d904f0037dfe09dd3502e50195351691ab4047cc5dbbb639147b8cd'
 assert packed['Trial_BaseColor']==hashlib.sha256((ROOT/'Textures/SL_GE_GATE_PIER_01_TRIAL_BaseColor.png').read_bytes()).hexdigest()
 assert packed['Trial_Roughness']==hashlib.sha256((ROOT/'Textures/SL_GE_GATE_PIER_01_TRIAL_Roughness.png').read_bytes()).hexdigest()
 # UV uniqueness by whole-face polygon IDs, no duplicated internal cap faces.
 keys=[tuple(sorted(p.vertices)) for p in source.data.polygons];assert len(keys)==len(set(keys))
 report={'source_reopened':True,'blend_format_confirmed_by_native_blender_open':True,'blend_header_first_12_bytes_hex':src.read_bytes()[:12].hex(),'source':s,
         'uv_density_px_per_m':{'min':min(density),'max':max(density),'mean':sum(density)/len(density),'triangles_checked':len(density)},
         'source_uv_matches_layout':True,'all_three_external_images_packed':True,'packed_image_sha256':packed}
 # Inspect binary FBX metadata and object classes, rather than relying on its extension.
 from io_scene_fbx import parse_fbx
 tree,version=parse_fbx.parse(str(fbx));report['fbx_binary_version']=version
 settings=next(e for e in tree.elems if e.id==b'GlobalSettings')
 props=next(e for e in settings.elems if e.id==b'Properties70')
 report['fbx_axis_unit_metadata']={e.props[0].decode():e.props[4] for e in props.elems
    if e.id==b'P' and e.props[0] in [b'UnitScaleFactor',b'OriginalUnitScaleFactor',b'UpAxis',b'UpAxisSign',b'FrontAxis',b'FrontAxisSign',b'CoordAxis',b'CoordAxisSign']}
 objects=next(e for e in tree.elems if e.id==b'Objects')
 models=[e for e in objects.elems if e.id==b'Model']
 report['fbx_model_types']=[e.props[2].decode() for e in models]
 assert report['fbx_model_types']==['Mesh']
 bpy.ops.wm.read_factory_settings(use_empty=True)
 bpy.context.scene.unit_settings.system='METRIC';bpy.context.scene.unit_settings.scale_length=1
 bpy.ops.import_scene.fbx(filepath=str(fbx),use_custom_normals=True)
 imported=list(bpy.context.scene.objects);assert len(imported)==1 and imported[0].type=='MESH'
 o=imported[0];t=stats(o)
 assert all(abs(a-b)<5e-6 for a,b in zip(t['dimensions_m'],[.6,.6,2.4]))
 assert all(abs(v)<1e-6 for v in t['origin_m'])
 assert geometry(o)==coords
 assert t['non_manifold_edges']==0 and t['zero_area_faces']==0
 assert abs(t['signed_volume_m3']-s['signed_volume_m3'])<5e-6
 assert len(o.data.materials)==1 and len(o.data.uv_layers)==1
 assert uv_corners(o)==source_uv_corners
 report['fbx_round_trip']={'single_mesh_only':True,'matches_source_vertex_positions':True,'stats':t,
                           'material_slots':len(o.data.materials),'uv_layers':len(o.data.uv_layers),'uv_corners_match_source':True}
 report['UE_validation_performed']=False
 (ROOT/'Source/verification_results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
 PROGRESS.write_text(json.dumps({'stage':'complete','source_reopen':'passed','fbx_round_trip':'passed'}),encoding='utf-8')
except Exception:
 PROGRESS.write_text(json.dumps({'stage':'failed','error':traceback.format_exc()}),encoding='utf-8');raise
