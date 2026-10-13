"""Blender background build, source-only FBX, two real daylight renders, five mesh views.
Run Blender --background --factory-startup --disable-autoexec --python this_file.
This script operates only in its fresh process and never opens a SchoolLife file.
"""
from pathlib import Path
import bpy, bmesh, hashlib, json, math, time, traceback
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

ROOT=Path(__file__).resolve().parent.parent
LIB=ROOT.parents[3]
CACHE=LIB/'.cache/gate-pier-trial01'
CACHE.mkdir(parents=True,exist_ok=True)
PROGRESS=CACHE/'build_progress.json'
DATA=json.loads((ROOT/'Source/SL_GE_GATE_PIER_01_TRIAL_GEOMETRY_UV.json').read_text(encoding='utf-8'))

def progress(stage,**kw):
 PROGRESS.write_text(json.dumps({'stage':stage,'time':time.time(),**kw},indent=2),encoding='utf-8')

def make_material(name,color,roughness=.85):
 m=bpy.data.materials.new(name);m.use_nodes=True;m.diffuse_color=(*color,1)
 bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=roughness
 return m

def target_camera(scene,col,name,position,target,ortho_scale):
 c=bpy.data.cameras.new(name);c.type='ORTHO';c.ortho_scale=ortho_scale;c.clip_start=.05;c.clip_end=100
 o=bpy.data.objects.new(name,c);col.objects.link(o);o.location=position
 o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
 return o

def update_billboard(mesh,az):
 a=math.radians(az);r=Vector((-math.sin(a),math.cos(a),0));anchor=Vector((-1.6,0,0))
 full=1.8*128/116
 corners=[(-64.5/128*full,-8/128*full),(63.5/128*full,-8/128*full),
          (63.5/128*full,120/128*full),(-64.5/128*full,120/128*full)]
 for v,(u,z) in zip(mesh.vertices,corners):v.co=anchor+r*u+Vector((0,0,z))
 mesh.update()

def projected(scene,cam,p):
 q=world_to_camera_view(scene,cam,Vector(p));r=scene.render
 return [q.x*r.resolution_x,(1-q.y)*r.resolution_y]

def measure(obj):
 bpy.context.view_layer.update()
 pts=[obj.matrix_world@v.co for v in obj.data.vertices]
 mins=[min(p[k] for p in pts) for k in range(3)];maxs=[max(p[k] for p in pts) for k in range(3)]
 bm=bmesh.new();bm.from_mesh(obj.data)
 info={'bounds_m':{'min':mins,'max':maxs},'dimensions_m':[maxs[k]-mins[k] for k in range(3)],'origin_m':list(obj.location),
       'scale':list(obj.scale),'rotation_euler_rad':list(obj.rotation_euler),'vertices':len(obj.data.vertices),'edges':len(obj.data.edges),
       'polygons':len(obj.data.polygons),'triangles':sum(len(p.vertices)-2 for p in obj.data.polygons),
       'non_manifold_edges':sum(not e.is_manifold for e in bm.edges),'signed_volume_m3':bm.calc_volume(signed=True),
       'zero_area_faces':sum(f.calc_area()<1e-10 for f in bm.faces),'material_slots':len(obj.data.materials)}
 bm.free();return info

try:
 progress('starting')
 assert not bpy.data.filepath, 'Use a fresh factory process, never an existing file'
 # These are factory defaults only, inside this independent background process.
 for obj in list(bpy.data.objects):bpy.data.objects.remove(obj,do_unlink=True)
 scene=bpy.context.scene;scene.name='TRIAL01_DAYLIGHT'
 scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1;scene.unit_settings.length_unit='METERS'
 asset=bpy.data.collections.new('ASSET_SOURCE_ONLY');scene.collection.children.link(asset)
 refs=bpy.data.collections.new('PREVIEW_ONLY_REFERENCE');scene.collection.children.link(refs)
 rig=bpy.data.collections.new('PREVIEW_ONLY_LIGHT_CAMERA');scene.collection.children.link(rig)
 mesh=bpy.data.meshes.new('SL_GE_GATE_PIER_01_TRIAL_MESH')
 mesh.from_pydata(DATA['vertices'],[],DATA['faces']);mesh.update()
 assert not mesh.validate(verbose=False,clean_customdata=False)
 main=bpy.data.objects.new('SM_SL_GE_GATE_PIER_01',mesh);asset.objects.link(main)
 main['asset_id']='SL_GE_GATE_PIER_01';main['front_direction']='-Y';main['pivot']='bottom_center';main['stage']='TRIAL_01_not_final'
 main['sign_reserve_cm']='annotation only: face -Y, X[-15,15], Z[90,190]; no plate/holes'
 uv=mesh.uv_layers.new(name='UVMap_64px_per_m')
 for face,coords in zip(mesh.polygons,DATA['face_uvs']):
  for loop_index,value in zip(face.loop_indices,coords):uv.data[loop_index].uv=value
 zones=mesh.attributes.new(name='trial_zone_M1_or_M2',type='INT',domain='FACE')
 for i,z in enumerate(DATA['face_zones']): zones.data[i].value=1 if z['material_zone']=='M1' else 2
 bpy.context.view_layer.objects.active=main;main.select_set(True)
 mat=make_material('M_SL_GATE_TRIAL_SHARED_ATLAS',(.62,.60,.55));nodes=mat.node_tree.nodes;links=mat.node_tree.links
 bs=nodes.get('Principled BSDF')
 for name,path,colorspace,socket in [('Trial_BaseColor',ROOT/'Textures/SL_GE_GATE_PIER_01_TRIAL_BaseColor.png','sRGB','Base Color'),
                                   ('Trial_Roughness',ROOT/'Textures/SL_GE_GATE_PIER_01_TRIAL_Roughness.png','Non-Color','Roughness')]:
  im=bpy.data.images.load(str(path),check_existing=True);im.name=name;im.colorspace_settings.name=colorspace
  tex=nodes.new('ShaderNodeTexImage');tex.name=name;tex.image=im;tex.interpolation='Closest';tex.extension='EXTEND';links.new(tex.outputs['Color'],bs.inputs[socket])
 mesh.materials.append(mat)

 floor_mesh=bpy.data.meshes.new('PREVIEW_GROUND_REFERENCE_MESH')
 floor_mesh.from_pydata([(-50,-50,0),(50,-50,0),(50,50,0),(-50,50,0)],[],[(0,1,2,3)]);floor_mesh.update()
 floor=bpy.data.objects.new('PREVIEW_ONLY_NEUTRAL_GROUND',floor_mesh);refs.objects.link(floor)
 floor_mesh.materials.append(make_material('PREVIEW_ONLY_GROUND',(.64,.66,.63),.92))
 floor['not_asset']='lighting/contact reference only; excluded from FBX'

 # Independent byte-exact scale image, not a re-created character or its gameplay model.
 character=Path('D:/UE project/SchoolLife/ArtSource/Characters/StudentChibi/FrontIdle/StudentChibi_Front_Idle.png')
 char_img=bpy.data.images.load(str(character),check_existing=True);char_img.name='REFERENCE_ORIGINAL_128_RGBA'
 assert hashlib.sha256(character.read_bytes()).hexdigest()=='082ceb410d904f0037dfe09dd3502e50195351691ab4047cc5dbbb639147b8cd'
 char_mat=bpy.data.materials.new('PREVIEW_ONLY_ORIGINAL_CHARACTER');char_mat.use_nodes=True
 cn=char_mat.node_tree.nodes;cn.clear();cl=char_mat.node_tree.links
 output=cn.new('ShaderNodeOutputMaterial');mix=cn.new('ShaderNodeMixShader');transparent=cn.new('ShaderNodeBsdfTransparent')
 emission=cn.new('ShaderNodeEmission');emission.inputs['Strength'].default_value=1
 image=cn.new('ShaderNodeTexImage');image.image=char_img;image.interpolation='Closest';image.extension='CLIP'
 cl.new(image.outputs['Color'],emission.inputs['Color']);cl.new(image.outputs['Alpha'],mix.inputs[0]);cl.new(transparent.outputs[0],mix.inputs[1])
 cl.new(emission.outputs[0],mix.inputs[2]);cl.new(mix.outputs[0],output.inputs['Surface'])
 refmesh=bpy.data.meshes.new('PREVIEW_ONLY_CHARACTER_BOARD_MESH');refmesh.from_pydata([(0,0,0)]*4,[],[(0,1,2,3)]);refmesh.update()
 refuv=refmesh.uv_layers.new(name='ORIGINAL_IMAGE_UV')
 for i,q in enumerate([(0,0),(1,0),(1,1),(0,1)]):refuv.data[i].uv=q
 refmesh.materials.append(char_mat);refobj=bpy.data.objects.new('PREVIEW_ONLY_ORIGINAL_CHARACTER_SCALE_BOARD',refmesh);refs.objects.link(refobj)
 refobj.visible_shadow=False;refobj.visible_diffuse=False;refobj.visible_glossy=False
 refobj['reference_only']='Original front PNG; visible 1.8m, not a back-facing eight-direction model; never exported'

 world=bpy.data.worlds.new('TRIAL01_NEUTRAL_DAYLIGHT');world.use_nodes=True
 world.node_tree.nodes['Background'].inputs['Color'].default_value=(.65,.68,.72,1)
 world.node_tree.nodes['Background'].inputs['Strength'].default_value=.45;scene.world=world
 sun_data=bpy.data.lights.new('TRIAL01_SUN','SUN');sun_data.energy=1.8;sun_data.angle=math.radians(5)
 sun=bpy.data.objects.new('TRIAL01_SUN',sun_data);rig.objects.link(sun)
 sun.rotation_euler=Vector((.5,.6,-1)).to_track_quat('-Z','Y').to_euler()
 target=Vector((-.55,0,1.18));cams={}
 for key,az in [('A',225),('B',45)]:
  a=math.radians(az);e=math.radians(30);pos=target+7*Vector((math.cos(e)*math.cos(a),math.cos(e)*math.sin(a),math.sin(e)))
  cams[key]=target_camera(scene,rig,'TRIAL_VIEW_'+key,pos,target,4.6)
 scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=48;scene.cycles.use_denoising=True
 scene.render.resolution_x=1600;scene.render.resolution_y=1400;scene.render.resolution_percentage=100
 scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB';scene.render.film_transparent=False
 scene.view_settings.view_transform='Standard';scene.view_settings.exposure=0;scene.view_settings.gamma=1
 scene.render.use_file_extension=True
 mainstats=measure(main)
 assert all(abs(a-b)<2e-6 for a,b in zip(mainstats['dimensions_m'],[.6,.6,2.4]))
 assert mainstats['non_manifold_edges']==0 and mainstats['zero_area_faces']==0 and mainstats['signed_volume_m3']>0

 # Separate actual placement check scene: linked source twice, one platform proxy, no new asset.
 check=bpy.data.scenes.new('VALIDATION_ONLY_2_INSTANCES')
 check.unit_settings.system='METRIC';check.unit_settings.scale_length=1
 valid=bpy.data.collections.new('VALIDATION_ONLY_DO_NOT_EXPORT');check.collection.children.link(valid)
 instances=[]
 for tag,x in [('LEFT',-3.3),('RIGHT',3.3)]:
  ob=bpy.data.objects.new('CHECK_INSTANCE_'+tag,mesh);ob.location=(x,0,8);valid.objects.link(ob);instances.append(ob)
 pm=bpy.data.meshes.new('VALIDATION_PLATFORM_PROXY')
 pm.from_pydata([(-4,-2.5,-.1),(4,-2.5,-.1),(4,2.5,-.1),(-4,2.5,-.1),(-4,-2.5,.1),(4,-2.5,.1),(4,2.5,.1),(-4,2.5,.1)],[],
               [(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)])
 pm.update();platform=bpy.data.objects.new('CHECK_PLATFORM_8x5x0p2',pm);platform.location=(0,2,7.9);valid.objects.link(platform)
 bpy.context.window.scene=check
 bpy.context.view_layer.update()
 checkstats=[]
 for ob in instances+[platform]:
  # These objects belong to a different scene. Read actual mesh and matrix values, not design predictions.
  checkstats.append({'name':ob.name,**measure(ob)})
 clear=checkstats[1]['bounds_m']['min'][0]-checkstats[0]['bounds_m']['max'][0]
 assert abs(clear-6)<1e-6
 assert all(abs(t['bounds_m']['min'][2]-8)<1e-6 for t in checkstats[:2])
 assert abs(checkstats[2]['bounds_m']['max'][2]-8)<1e-6
 bpy.context.window.scene=scene
 bpy.context.view_layer.update()

 update_billboard(refmesh,225);scene.camera=cams['A']
 for img in [n.image for n in nodes if n.type=='TEX_IMAGE']+[char_img]:img.pack()
 for img in [n.image for n in nodes if n.type=='TEX_IMAGE']:img.filepath='//../Textures/'+Path(img.filepath).name
 bpy.context.view_layer.objects.active=main
 for ob in scene.objects:ob.select_set(False)
 main.select_set(True)
 sourcepath=ROOT/'Source/SL_GE_GATE_PIER_01_TRIAL_01.blend'
 bpy.ops.wm.save_as_mainfile(filepath=str(sourcepath))
 export_opts={'use_selection':True,'object_types':{'MESH'},'global_scale':1.0,'apply_unit_scale':True,
              'apply_scale_options':'FBX_SCALE_UNITS','axis_forward':'-Y','axis_up':'Z','bake_space_transform':False,
              'use_mesh_modifiers':True,'mesh_smooth_type':'OFF','use_triangles':True,'bake_anim':False,
              'path_mode':'RELATIVE','embed_textures':False,'use_custom_props':True}
 bpy.ops.export_scene.fbx(filepath=str(ROOT/'Exports/SL_GE_GATE_PIER_01_TRIAL_01.fbx'),**export_opts)
 progress('source_and_fbx_saved',blender_version=bpy.app.version_string,mesh=mainstats)
 views={}
 for key,az in [('A',225),('B',45)]:
  scene.camera=cams[key];update_billboard(refmesh,az);bpy.context.view_layer.update()
  views[key]={'azimuth_deg':az,'elevation_deg':30,'projection':'ORTHOGRAPHIC','camera_location_m':list(cams[key].location),
              'target_m':list(target),'ortho_scale_m':4.6,'native_px':[1600,1400],
              'reference_anchor_m':[-1.6,0,0],'reference_points_px':{str(h):projected(scene,cams[key],(-1.6,0,h)) for h in [0,1.8,1.92]}}
  progress('rendering_view_'+key)
  (ROOT/'Previews/Renders').mkdir(exist_ok=True)
  scene.render.filepath=str(ROOT/f'Previews/Renders/SL_GE_GATE_PIER_01_TRIAL_VIEW_{key}_RENDER.png')
  bpy.ops.render.render(write_still=True)
  progress('view_'+key+'_rendered')

 # Five real Workbench views of this mesh, combined later into one labelled check board.
 progress('rendering_five_mesh_checks')
 refs.hide_render=True;rig.hide_render=False
 scene.render.engine='BLENDER_WORKBENCH'
 scene.display.shading.light='STUDIO';scene.display.shading.color_type='SINGLE';scene.display.shading.single_color=(.65,.70,.68)
 scene.display.shading.show_shadows=True;scene.display.shading.show_cavity=True
 scene.display.shading.background_type='WORLD';scene.world.color=(.93,.92,.88)
 scene.render.resolution_x=480;scene.render.resolution_y=680
 for key,direction in [('SOUTH',(0,-1,0)),('NORTH',(0,1,0)),('EAST',(1,0,0)),('WEST',(-1,0,0)),('TOP',(0,0,1))]:
  center=Vector((0,0,1.2));pos=center+7*Vector(direction)
  camera=target_camera(scene,rig,'CHECK_'+key,pos,center,3.0 if key!='TOP' else 1.0)
  scene.camera=camera;scene.render.filepath=str(CACHE/('CHECK_'+key+'.png'))
  bpy.ops.render.render(write_still=True)
 refs.hide_render=False;scene.render.engine='CYCLES';scene.camera=cams['A'];update_billboard(refmesh,225)
 scene.render.resolution_x=1600;scene.render.resolution_y=1400;scene.render.filepath='//../Previews/Renders/SL_GE_GATE_PIER_01_TRIAL_VIEW_A_RENDER.png'
 # Saved source opens as the usable daylight scene, while its validation scene remains separate.
 bpy.context.view_layer.objects.active=main
 for ob in scene.objects:ob.select_set(False)
 main.select_set(True)
 bpy.ops.wm.save_as_mainfile(filepath=str(sourcepath))
 info={'blender_version':bpy.app.version_string,'mesh':mainstats,'validation_scene':{'instances':checkstats[:2],'platform':checkstats[2],
       'minimum_opening_m':clear,'road_width_reference_m':5,'source_mesh_shared_by_two_instances':instances[0].data is instances[1].data},
       'views':views,'daylight':{'engine':'CYCLES_CPU','samples':48,'denoise':True,'sun_energy':1.8,'sun_angle_deg':5,
       'incoming_sun_direction':[.5,.6,-1],'world_strength':.45,'view_transform':'Standard','exposure':0,'film_transparent':False},
       'export':{k:sorted(v) if isinstance(v,set) else v for k,v in export_opts.items()},
       'reference_original_packed_sha256':hashlib.sha256(bytes(char_img.packed_file.data)).hexdigest(),
       'detail_decisions':DATA['detail_decisions']}
 (ROOT/'Source/blender_measurements.json').write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
 progress('complete',blender_version=bpy.app.version_string)
except Exception:
 progress('failed',error=traceback.format_exc())
 raise
