"""Native read-only reopen of the freshly generated reference .blend, no save."""
from pathlib import Path
import bpy,json,hashlib
O=Path(__file__).parent;P='SL_BLD_C01_MAIN_01_REFERENCE_01'
bpy.ops.wm.open_mainfile(filepath=str(O/(P+'_REFERENCE_ONLY.blend')),load_ui=False)
g=json.loads((O/(P+'_GEOMETRY.json')).read_text(encoding='utf-8'))
expected=hashlib.sha256((O/(P+'_GEOMETRY.json')).read_bytes()).hexdigest()
ids=[]
for ob in bpy.data.objects:
 if ob.name.startswith('WHOLE_'):ids+=json.loads(ob['source_ids'])
ok=len(ids)==len(g['primitives']) and set(ids)==set(p['id'] for p in g['primitives']) and bpy.context.scene['geometry_sha256']==expected
report={'reopen_passed':ok,'blender_version':bpy.app.version_string,'geometry_sha256':bpy.context.scene['geometry_sha256'],
 'whole_source_ids':len(ids),'collections':len(bpy.data.collections),'no_UV_layers':all(len(o.data.uv_layers)==0 for o in bpy.data.objects if o.type=='MESH'),
 'render_resolution':[bpy.context.scene.render.resolution_x,bpy.context.scene.render.resolution_y],
 'schoollife_writes':0,'source_saved_again':False}
(O/'NATIVE_REOPEN_REPORT.json').write_text(json.dumps(report,indent=2),encoding='utf-8',newline='\n')
print(json.dumps(report),flush=True)
if not ok:raise RuntimeError('reference source does not match JSON')
