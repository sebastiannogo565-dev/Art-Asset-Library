from pathlib import Path
import bpy,json,hashlib,sys
O=Path(__file__).parent;PR='SL_BLD_C01_MAIN_01_REFERENCE_01_REV_01'
bpy.ops.wm.open_mainfile(filepath=str(O/(PR+'_REFERENCE_ONLY.blend')),load_ui=False)
g=json.loads((O/(PR+'_GEOMETRY.json')).read_text(encoding='utf-8'))
ids=[]
for ob in bpy.data.objects:
 if ob.name.startswith('WHOLE_'):ids+=json.loads(ob['source_ids'])
expected=hashlib.sha256((O/(PR+'_GEOMETRY.json')).read_bytes()).hexdigest()
zmax=max((o.matrix_world@v.co).z for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('WHOLE_') for v in o.data.vertices)
ok=set(ids)==set(p['id'] for p in g['primitives']) and len(ids)==len(g['primitives']) and bpy.context.scene['geometry_sha256']==expected and abs(zmax-13.68)<.00002
finalize='--finalize-display' in sys.argv
if finalize:
 for ob in bpy.data.objects:
  if ob.type=='MESH':ob.hide_viewport=not ob.name.startswith(('WHOLE_','CONTEXT_'))
 bpy.ops.wm.save_as_mainfile(filepath=str(O/(PR+'_REFERENCE_ONLY.blend')))
report={'passed':ok,'geometry_sha256':bpy.context.scene['geometry_sha256'],'whole_source_ids':len(ids),'highest_mesh_z':zmax,
 'no_UV_layers':all(len(o.data.uv_layers)==0 for o in bpy.data.objects if o.type=='MESH'),'blender':bpy.app.version_string,'parent_not_saved':True,
 'display_only_finalize_saved_revision':finalize}
(O/'NATIVE_REOPEN_REPORT.json').write_text(json.dumps(report,indent=2),encoding='utf-8',newline='\n')
print(report)
if not ok:raise RuntimeError('native revision mismatch')
