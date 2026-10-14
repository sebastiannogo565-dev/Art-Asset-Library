"""C01 planning diagrams only: no 3D assets or game writes."""
from pathlib import Path
import json, math, hashlib, base64, html
ROOT=Path('D:/Art Asset Library')
OUT=ROOT/'ArtSource/Buildings/SL_BLD_C01_MAIN_01/Planning'
DOC=ROOT/'Docs/AssetPlanning/BuildingProduction/C01'
OUT.mkdir(parents=True,exist_ok=True); DOC.mkdir(parents=True,exist_ok=True)
world_path=ROOT/'ArtSource/MapDesign/V13/SL_WORLD_V13_LAYOUT_01.json'
world=json.loads(world_path.read_text(encoding='utf-8'))
base=next(b for b in world['buildings'] if b['id']=='C01')
origin=base['footprint'][0]
sources=[world_path,ROOT/'ArtSource/MapDesign/V13/SL_WORLD_V13_PLAN_01.svg',ROOT/'Docs/MapDesign/V13/building-use-phase-index.md',Path('D:/UE project/SchoolLife/Docs/LifeCoreBlockout-Phase4A-Step1-Plan.md'),Path('D:/UE project/SchoolLife/Docs/Validation/LifeCoreBlockout/Step4/Observations.md'),Path('D:/UE project/SchoolLife/Docs/Validation/LifeCoreBlockout/Step2/ActorRecipe.json'),Path('D:/UE project/SchoolLife/ArtSource/Characters/StudentChibi/FrontIdle/StudentChibi_Front_Idle.png')]
sources+=list((ROOT/'ArtSource/Buildings/SL_BLD_B01_HOME_01/Reference').glob('*'))
sources += [ROOT/'Docs/AssetPlanning/BuildingProduction/TaskCards/SL_BLD_B01_HOME_01.md',ROOT/'Docs/AssetPlanning/BuildingProduction/review-B01-reference-01.md']
protected=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sources if p.is_file()]
rect_area=lambda r:(r[2]-r[0])*(r[3]-r[1])
body=[[0,4,52,22],[52,8,64,22],[64,0,94,28],[94,8,106,22],[106,4,150,22],[18,0,30,4],[30,0,38,4],[142,0,150,4]]
segments=[dict(id='WEST',range=[0,52],name='西教学段'),dict(id='LINK_W',range=[52,64],name='连接/鞋柜分区'),dict(id='CORE',range=[64,94],name='学习交流核心'),dict(id='LINK_E',range=[94,106],name='连接/年级停留'),dict(id='EAST',range=[106,150],name='东教学段')]
atrium=[74,15,86,24]; terrace=[64,0,74,6]; shaft=[80,.8,82.4,3.2]
stairs=[dict(id='S1',box=[30,0,38,8.8],opening=[31.6,.9,36.3,6.4],door=[34,8.8]),dict(id='S2',box=[86,0,94,8.8],opening=[87.6,.9,92.3,6.4],door=[90,8.8]),dict(id='S3',box=[142,0,150,8.8],opening=[143.6,.9,148.3,6.4],door=[146,8.8])]
entrances=[dict(id='C01_MAIN',local=[25,0],world=base['world_entry'],width=3,height=3.2),dict(id='C01_N',local=[90,28],world=base['secondary_entries'][0]['at'],width=3,height=3),dict(id='C01_E',local=[150,14],world=base['secondary_entries'][1]['at'],width=3,height=3)]
rooms=[]
def room(f,id,name,rect,kind='support',access='student',phase='background',door=None):
    if door is None: door=[(rect[0]+rect[2])/2,rect[1] if rect[1]>=12.7 else rect[3]]
    rooms.append(dict(id=f'F{f}_{id}',floor=f,name=name,rect=rect,net_area=round(rect_area(rect),4),kind=kind,access=access,door=door,door_width=1.6 if kind=='classroom' else 1.4,door_height=2.6,production_depth=phase))
for f in (1,2,3):
    for i,x in enumerate([15.2,23.8,32.4,41]):
        room(f,f'W{i+1}',f'{f}年级 {i+1}班'+(' / 玩家' if f==2 and i==3 else ''),[x,12.7,x+8.4,21.7],'classroom',phase='frequent' if f==2 and i==3 else 'background',door=[x+4,12.7])
    for i,x in enumerate([107,115.6,124.2,132.8]):
        room(f,f'E{i+1}',f'{f}年级 {i+5}班',[x,12.7,x+8.4,21.7],'classroom',door=[x+4,12.7])
    room(f,'WG','年级窗边交流',[.3,13,14.9,21.7],'public',phase='medium')
    room(f,'WWC','西侧卫生间套间',[.3,4.3,7.7,8.8],access='student')
    room(f,'WH',['保健/咨询套间','年级事务/小讨论','升学咨询'][f-1],[8,4.3,17.7,8.8],access='staff_controlled',phase='medium')
    room(f,'WL',['鞋柜/入口缓冲','二年级交流厅','安静讨论厅'][f-1],[18.3,.3,29.7,8.8],'public',phase='frequent' if f<3 else 'medium',door=[25,8.8])
    room(f,'WO',['职员工作/来访接待','玩家班侧年级休息厅','导师/小组讨论'][f-1],[38.3,4.3,51.7,8.8],'public' if f==2 else 'support',access='staff_controlled' if f==1 else ('student' if f==2 else 'student_authorized'),phase='medium')
    room(f,'LW',['补充鞋柜/等候','连接交流窗','连接安静角'][f-1],[52.3,13,63.7,21.7],'public',phase='medium')
    room(f,'LE','东连接休息角',[94.3,13,105.7,21.7],'public',phase='medium')
    room(f,'CW',['教务管理','学生会/讨论套间','露台入口缓冲'][f-1],[64.3,6.3 if f==3 else .3,73.7,8.8],access='staff_controlled' if f==1 else 'student_authorized',phase='medium')
    room(f,'CS','储藏/维护套间',[74.3,.3,79.7,8.8],access='maintenance')
    room(f,'CE',['打印/服务柜','广播/器材','指导资料'][f-1],[82.7,.3,85.7,8.8],access='staff_controlled')
    room(f,'CL',['交流厅窗边','共享学习步台','安静讨论步台'][f-1],[64.3,13,73.7,27.7],'public',phase='medium')
    room(f,'CB','采光庭北侧观察廊',[74.3,24.3,85.7,27.7],'public',phase='medium',door=[85.7,26])
    room(f,'CN','北门/后廊前厅' if f==1 else '北侧窗厅',[86.3,13,93.7,27.7],'public',phase='frequent' if f==1 else 'medium',door=[90,13])
    room(f,'EG','东年级交流',[106.3,4.3,118.5,8.8],'public',phase='medium')
    room(f,'EWC','东侧卫生间套间',[118.8,4.3,129,8.8])
    room(f,'ES','储物/维护/备课',[129.3,4.3,141.5,8.8],access='staff_controlled')
    if f==1: room(f,'AT','交流厅底层',[74,15,86,24],'public',phase='medium',door=[86,19.5])
gross=sum(map(rect_area,body)); holes=sum(rect_area(s['opening']) for s in stairs)
areas=[]
for f in (1,2,3):
    enclosed=gross-(60 if f==3 else 0)
    alloc=enclosed-(108 if f>1 else 0)-(holes if f>1 else 0)-rect_area(shaft)
    rp=sum(r['net_area'] for r in rooms if r['floor']==f)
    areas.append(dict(floor=f,control_area=4200,enclosed_plan_envelope=enclosed,atrium_void=108 if f>1 else 0,stair_void=holes if f>1 else 0,elevator_use_exclusion=rect_area(shaft),allocatable_horizontal_area=round(alloc,4),room_public_net_sum=round(rp,4),main_corridor_net=540,other_circulation_structure_reserve=round(alloc-rp-540,4),classrooms=8,classroom_net=604.8,uncovered_terrace=60 if f==3 else 0))
def S(s,z,up=True):
    x=s['door'][0]; p=[[x,8.8,z],[x-1.3,6.4,z],[x-1.3,3.1,z+2],[x-1.3,2,z+2],[x+1.2,2,z+2],[x+1.2,3.1,z+2],[x+1.2,6.4,z+4],[x,8.8,z+4]]
    return p if up else list(reversed(p))
def to_local(points,z=0):return [[p[0]-origin[0],p[1]-origin[1],z] for p in points]
gate=next(p for p in world['campus_paths'] if p['id']=='C_gate')
lib=next(p for p in world['campus_paths'] if p['id']=='C_library')
sport=next(p for p in world['campus_paths'] if p['id']=='C_sport')
routes=[dict(id='DAILY_01',name='校门→鞋柜→二层玩家教室',points=to_local(gate['world_points'])+[[25,5,0],[25,10.9,0],[34,10.9,0]]+S(stairs[0],0)+[[34,10.9,4],[45,10.9,4],[45,12.7,4],[45,19.5,4]]),dict(id='DAILY_02',name='玩家教室→北门→独立图书翼',points=[[45,19.5,4],[45,12.7,4],[45,10.9,4],[90,10.9,4]]+S(stairs[1],0,False)+[[90,10.9,0]]+to_local(lib['world_points'])),dict(id='DAILY_03',name='玩家教室→东口→体育馆方向',points=[[45,19.5,4],[45,12.7,4],[45,10.9,4],[146,10.9,4]]+S(stairs[2],0,False)+[[146,10.9,0],[146,14,0]]+to_local(sport['world_points']))]
for r in routes:
    p=r['points'];r['length_xy_m']=sum(math.dist(a[:2],b[:2]) for a,b in zip(p,p[1:]));r['length_3d_candidate_m']=sum(math.dist(a,b) for a,b in zip(p,p[1:]));r['world_points']=[[origin[0]+x,origin[1]+y,8+z] for x,y,z in p];r['status']='paper polyline, stair centreline candidate; not UE/time verification'
stops=[dict(id='P1',name='入口历届照片凹廊',floor=1,at=[28,3],use='集合/等同伴，不堵x25入口主线'),dict(id='P2',name='玩家班旁年级厅',floor=2,at=[45,6.2],use='课间近处折返/放包/公告'),dict(id='P3',name='西连接窗边',floor=2,at=[58,17],use='午休短停，主廊在下方独立'),dict(id='P4',name='交流厅边缘',floor=1,at=[75,19],use='日常讨论/小展示；中央通路留6m'),dict(id='P5',name='北门旁等候边',floor=1,at=[92.5,25],use='图书往返等同伴，不挡北门'),dict(id='P6',name='三层可控小露台',floor=3,at=[69,3],use='60㎡候选，不替代既有RT01，不自动开放')]
data=dict(asset_id='SL_BLD_C01_MAIN_01',revision='PLAN_01',date='2026-10-15',status='whole-building proposal awaiting review; not approved footprint change',units='m',authority=base,shared_origin_world_xy=origin,engineering_origin_world_xy=world['campus']['world_gate'],campus_ground_z_candidate=8,coordinate='local x east,y north,z relative first-floor finish; all collections share SW control origin',candidate=dict(control=[0,0,150,28],segments=segments,body_rects=body,floor_tops=[0,4,8],floor_slab_depth=.25,ceiling_relative=3.45,roof='teaching shallow blue-gray slope5deg / core flat skylight; roof12.4-13.0 candidate',capacity_classes=24,pupils_per_class=[30,36],pupils_total=[720,864],classroom_net=[8.4,9],classroom_door=[1.6,2.6],main_corridor=[0,9.1,150,12.7],stairs=stairs,stair_flight_width=2.2,stair_risers_per_floor=24,stair_riser=4/24,stair_going=.3,stair_landing_depth=2.2,elevator_shaft=shaft,elevator_cabin_candidate=[1.6,1.8],elevator_door=1.2,atrium=atrium,terrace=terrace,shoe_capacity_target=900,shoe_capacity_status='main+west connector combined196.08sqm allowance; detailed banks not verified'),entrances=entrances,rooms=rooms,areas=areas,routes=routes,stops=stops,character=dict(source=str(sources[6]),visible_height=1.8,visible_front_width=67/116*1.8,capsule_height=1.92,capsule_diameter=.68,unchanged=True),graybox_difference=dict(formal_classroom_projection=[45,14],gray_anchor_projection=[45,19.5],gray_ground=8,proposed_classroom_ground=12,old_hall_y=14,new_hall_y=10.9,old_door_width=2.4,new_door_width=1.6,not_time_validated=True),roof_RT01_note='V13 original candidate28x21 roof access polygon partially lies outside setback mass; preserve as historical layer, not silently migrate/approve. Third-floor60sqm terrace is separate candidate.',protected_inputs=protected,production_counts=dict(formal_images_generated=0,models=0,UV=0,UE=0,B01_changes=0))
ridge=12.3+9*math.tan(math.radians(5))
data['candidate']['roof']='teaching shallow gable5deg, eave12.3/ridge13.0874; core flat13; links12.3; terrace slab8.25'
data['candidate']['roof_geometry']=dict(teaching_pitch_deg=5,eave_top=12.3,ridge_top=ridge,ridge_axis='east-west',teaching_span=18,core_top=13,links_top=12.3,terrace_top=8.25)
OUT.joinpath('SL_BLD_C01_MAIN_01_PLAN_01.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')

# Diagram primitives; all dimensions derive from data above.
E=lambda x:html.escape(str(x))
def text(x,y,t,size=23,color='#30464a',anchor='start'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}">{E(t)}</text>'
def rect(x,y,w,h,fill='#f8faf7',stroke='#8b9b98',sw=2):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def line(x,y,X,Y,color='#7a8d88',sw=3,dash=''):return f'<path d="M{x},{y} L{X},{Y}" fill="none" stroke="{color}" stroke-width="{sw}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'
def poly(pts,fill='none',stroke='#387d89',sw=4):return f'<polyline points="'+ ' '.join(f'{x},{y}' for x,y in pts)+f'" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def page(title,sub):return '<svg xmlns="http://www.w3.org/2000/svg" width="3200" height="2400" viewBox="0 0 3200 2400"><rect width="3200" height="2400" fill="#f0f3ef"/><g font-family="Microsoft YaHei, Noto Sans CJK SC, sans-serif">'+text(80,90,title,46)+text(80,145,sub,25)+text(80,195,'北向：平面N=+Y；立面朝向见图名 | 米制：平面比例尺，剖面按尺寸标注，体量不定尺 | 蓝=教学 / 黄=公共 / 棕=管理 / 橙=门',20)+text(80,2350,'SL_BLD_C01_MAIN_01 / PLAN_01 / 2026-10-15 · 米制候选规划；非模型/工程/UE验收；B01状态保持',22)
def finish(s,n):OUT.joinpath(f'SL_BLD_C01_MAIN_01_PLAN_01_P{n:02d}.svg').write_text(s+'</g></svg>',encoding='utf-8')
def caption(s,x,y,lines):
    for i,t in enumerate(lines):s+=text(x,y+i*43,t,25)
    return s
def north(x,y):return line(x,y+65,x,y,'#30464a',5)+text(x,y-10,'N / 北',24,anchor='middle')
def scale(x,y,px=18):return line(x,y,x+20*px,y,'#30464a',5)+text(x,y-12,'0',20)+text(x+20*px,y-12,'20m',20,anchor='end')
def plan_floor(f,tx=180,ty=1050,sc=18,labels=True):
    s='';xy=lambda p:(tx+p[0]*sc,ty-p[1]*sc)
    R=lambda r:(tx+r[0]*sc,ty-r[3]*sc,(r[2]-r[0])*sc,(r[3]-r[1])*sc)
    s+=rect(*R([0,0,150,28]),'none','#b1b8ac',2)
    for b in body:s+=rect(*R(b),'#d5ded5','#637b77',3)
    s+=rect(*R([0,9.1,150,12.7]),'#e8ecd7','none')
    for r in rooms:
        if r['floor']!=f:continue
        color={'classroom':'#d9e7ef','public':'#e7e7cd'}.get(r['kind'],'#e0d9cd')
        if r['access']=='maintenance':color='#cbd2ce'
        s+=rect(*R(r['rect']),color,'#8eaaa6',1.5)
        if labels:
            x,y=xy([(r['rect'][0]+r['rect'][2])/2,(r['rect'][1]+r['rect'][3])/2])
            name=r['name']; name=name.replace('年级 ','-').replace(' / 玩家',' 玩家')
            available=(r['rect'][2]-r['rect'][0])*sc-10
            n=max(2,int(available/16)); chunks=[name[i:i+n] for i in range(0,len(name),n)]
            for i,t in enumerate(chunks):s+=text(x,y-12+(i-(len(chunks)-1)/2)*19,t,16,anchor='middle')
            s+=text(x,y+22+(len(chunks)-1)*9,f"{r['id'].split('_')[-1]} {r['net_area']:.1f}㎡",13,anchor='middle')
        d=r['door'];x,y=xy(d);s+=line(x-12,y,x+12,y,'#ae684e',5)
    for st in stairs:
        s+=rect(*R(st['box']),'#c5d1da','#587589',3)
        s+=rect(*R(st['opening']),'#f4f5f1','#628282',2)
        x,y=xy(st['door']);s+=text(x,y-30,st['id']+' 2.2m净梯',17,anchor='middle')+line(x-20,y,x+20,y,'#ae684e',5)
        for k in range(12):
            x,y=xy([st['opening'][0],st['opening'][1]+2.2+k*.3]);X,Y=xy([st['opening'][2],st['opening'][1]+2.2+k*.3]);s+=line(x,y,X,Y,'#829595',1)
    s+=rect(*R(shaft),'#afbec5','#436b80',3)
    x,y=xy([81.2,5.5]);s+=text(x,y,'L1 电梯',17,anchor='middle')
    if f>1:s+=rect(*R(atrium),'#f0f3ef','#a59870',3);x,y=xy([80,19.5]);s+=text(x,y,'采光庭孔108㎡',18,anchor='middle')
    if f==3:s+=rect(*R(terrace),'#b9d2b9','#4b7869',3);x,y=xy([69,3]);s+=text(x,y,'60㎡候选露台',17,anchor='middle')
    if f==1:
        for en in entrances:
            x,y=xy(en['local']);s+=text(x,y+35 if en['local'][1]==0 else y-15,en['id'],21,'#a64e3c',anchor='middle')
            s+=line(x-27,y,x+27,y,'#ae684e',6) if en['id']!='C01_E' else line(x,y-27,x,y+27,'#ae684e',6)
    s+=line(tx,ty+75,tx+150*sc,ty+75)+text(tx+75*sc,ty+115,'150m控制长度 / 52 + 12 + 30 + 12 + 44',27,anchor='middle')
    s+=north(tx+150*sc+100,ty-28*sc)+scale(tx,ty+180,sc)
    return s

# P01 campus context, same original world footprint for neighbours.
s=page('C01主教学楼 · 校园关系与权威边界','控制150×28m/三层；新体量仍为候选；周边建筑和三入口数字保持。')
tx,ty,sc=150,2010,5.0
def campusXY(p):return tx+(p[0]-world['campus']['world_bounds'][0][0])*sc,ty-(p[1]-world['campus']['world_bounds'][0][1])*sc
camp=world['campus']['world_bounds'];s+=rect(tx,ty-320*sc,360*sc,320*sc,'#e4eadf')
for b in world['buildings']:
    if not b['id'].startswith('C'):continue
    pts=[campusXY(p) for p in b['footprint']];s+=poly(pts+[pts[0]],'#dbdacf','#7f938d',3)
    x,y=campusXY(b['center']);s+=text(x,y,b['id']+' '+b['name'],22,anchor='middle')
for p in world['campus_paths']:
    if p['type']=='indoor':continue
    s+=poly([campusXY(q) for q in p['world_points']],stroke='#a9b6a0',sw=4)
fg=next(f for f in world['campus']['features'] if f['id']=='FG')
s+=poly([campusXY(p) for p in fg['polygon']]+[campusXY(fg['polygon'][0])],'none','#b8ac81',3)
x,y=campusXY(world['campus']['world_gate']);s+=text(x,y-25,'校门 / GATE01',24,'#a1513f',anchor='middle')
for b in body:
    pts=[campusXY([origin[0]+x,origin[1]+y]) for x,y in [(b[0],b[1]),(b[2],b[1]),(b[2],b[3]),(b[0],b[3]),(b[0],b[1])]];s+=poly(pts,'#b9d4df','#367789',3)
for e in entrances:
    x,y=campusXY(e['world']);s+=text(x,y+30,e['id'],22,'#a1513f',anchor='middle')
s+=north(1920,430)+scale(150,2190,5)
s=caption(s,2150,340,['C01：普通教学/管理/学生交流','C03：独立图书学习翼','C04：实验/艺术特别教学','C05：文化社团预留','C06：讲堂/校史','C07：食堂/生活服务','C08：体育馆/储物','C02旧校钟继续历史主角','','原主入口西起25m，不居中','北门西起90m，落入64–94核心','东口y14接既有C_sport','','淡色矩形：V13原楼体','蓝色：候选退进体量','灰绿线：既有室外步道','内外所有人流仍校内受控','校外市民不穿C01抄近路'])
finish(s,1)
for f in (1,2,3):
    a=areas[f-1];s=page(f'C01 · F0{f} 平面 / '+['一年级与入口管理','二年级与玩家高频空间','三年级与安静交流'][f-1],f'相对首层完成面 +{(f-1)*4:.2f}m；校园候选地面+8m→工程 +{8+(f-1)*4:.2f}m；橙线为门，蓝为班级，灰蓝为梯。')
    s+=plan_floor(f)
    s=caption(s,180,1390,[f"围护平面基面 {a['enclosed_plan_envelope']:.2f}㎡；减庭孔{a['atrium_void']:.2f} / 梯孔{a['stair_void']:.2f} / 电梯使用扣除5.76㎡",f"可分配水平面积 {a['allocatable_horizontal_area']:.2f}㎡；8班净教室604.80㎡；房间/公共净界合计{a['room_public_net_sum']:.2f}㎡",f"主走廊3.6m净/平面540㎡；余量{a['other_circulation_structure_reserve']:.2f}㎡为墙柱/梯平台/接驳及待细化，不能算可用房间",'教室8.4×9m、门1.6×2.6；楼梯2.2m净；24班×30–36只是容量研究，不增加实际NPC。'])
    s=caption(s,180,1660,['F01：鞋柜与补充区净界196.08㎡，900格只是细排目标；来访在职员/接待侧分流。','F02：玩家班F2_W4保45,14原投影及45,19.5灰盒业务XY，正式位于相对+4m。','F03：露台60㎡需学校许可/天气与维护关闭候选；不自动批准原RT01移位。','所有楼梯孔同时开对应楼板与下层顶面；电梯只安排空间，系统未实现。'])
    finish(s,f+1)

# P05 long facade contours + roof plan, not rendered artwork.
s=page('C01 · 体量节奏 / 四立面轮廓 / 屋顶','52–12–30–12–44为本轮推荐；低对比实体教学翼、通透连接和有用途的交流核心。')
sx,by,k=180,720,18
tops={'WEST':ridge,'LINK_W':12.3,'CORE':13,'LINK_E':12.3,'EAST':ridge}
for seg in segments:
    l,r=seg['range'];h=tops[seg['id']]
    if seg['id']=='CORE':s+=rect(sx+l*k,by-8.25*k,10*k,8.25*k,'#dddccc','#6c8983',3)+rect(sx+(l+10)*k,by-h*k,(r-l-10)*k,h*k,'#dddccc','#6c8983',3)
    else:s+=rect(sx+l*k,by-h*k,(r-l)*k,h*k,'#dddccc','#6c8983',3)
    s+=text(sx+(l+r)/2*k,by+40,seg['name']+f' {r-l}m',22,anchor='middle')
    if 'LINK' in seg['id'] or seg['id']=='CORE':
        if seg['id']=='CORE':s+=rect(sx+(l+1)*k,by-7.7*k,8*k,7.1*k,'#a8c2c7','#6c8983',2)+rect(sx+(l+11)*k,by-11.8*k,18*k,11.2*k,'#a8c2c7','#6c8983',2)
        else:s+=rect(sx+(l+1)*k,by-11.8*k,(r-l-2)*k,11.2*k,'#a8c2c7','#6c8983',2)
    else:
        xs=[15.2,23.8,32.4,41] if seg['id']=='WEST' else [107,115.6,124.2,132.8]
        for floor in range(3):
            for x in xs:s+=rect(sx+(x+.6)*k,by-(floor*4+3.1)*k,7.2*k,2*k,'#89a7ac','#6c8983',2)
    for z in [4,8,12]:s+=line(sx+l*k,by-z*k,sx+r*k,by-z*k,'#829c98',2)
s+=text(180,340,'南立面：偏西入口，核心并非主入口；节奏由分翼、退进和遮阳形成',27)
s+=rect(sx+23.5*k,by-3.2*k,3*k,3.2*k,'#6f9aa1','#a0553f',3)
s+=text(sx+25*k,by+90,'原入口 x25',24,'#a0553f',anchor='middle')
by2=1190
for seg in segments:
    l,r=seg['range'];h=tops[seg['id']];s+=rect(sx+l*k,by2-h*k,(r-l)*k,h*k,'#d4dcd5','#6c8983',3)
    if seg['id'] in ['WEST','EAST']:
        xs=[15.2,23.8,32.4,41] if seg['id']=='WEST' else [107,115.6,124.2,132.8]
        for f in range(3):
            for x in xs:s+=rect(sx+(x+.6)*k,by2-(f*4+3.0)*k,7.2*k,2*k,'#9db6b7','#6c8983',2)
s+=rect(sx+88.5*k,by2-3*k,3*k,3*k,'#6f9aa1','#a0553f',3)+text(180,910,'北立面：年级教室窗景、北门与泉院/图书联系；不是南立面镜像',27)
for tx2,label in [(180,'西侧轮廓 / 18m教学进深'),(940,'东侧轮廓 / 体育出口')]:
    s+=rect(tx2+4*18,1550-12.3*18,18*18,12.3*18,'#d5dbd2','#6c8983',3)+text(tx2,1590,label,25)
    s+=poly([(tx2+4*18,1550-12.3*18),(tx2+13*18,1550-ridge*18),(tx2+22*18,1550-12.3*18)],'#91aaa5','#6c8983',3)
    if tx2==940:s+=rect(tx2,1550-12.3*18,4*18,12.3*18,'#d5dbd2','#6c8983',3)
    s+=line(tx2+4*18,1550-4*18,tx2+22*18,1550-4*18)+line(tx2+4*18,1550-8*18,tx2+22*18,1550-8*18)
    if tx2==940:s+=rect(tx2+12.5*18,1550-3*18,3*18,3*18,'#6f9aa1','#a0553f',3)
for b in body:s+=rect(180+b[0]*18,2270-b[3]*18,(b[2]-b[0])*18,(b[3]-b[1])*18,'#95aaa6','#658980',2)
s+=rect(180+74*18,2270-24*18,12*18,9*18,'#bed5db','#658980',3)+text(180+80*18,2270-19*18,'小采光庭',19,anchor='middle')
s+=rect(180+64*18,2270-6*18,10*18,6*18,'#b7d2b1','#658980',3)+text(180+69*18,2270-2.5*18,'三层露台',17,anchor='middle')
s+=scale(2400,1550,18)+north(2970,1750)
s+=text(180,1700,'屋顶：教学5°浅切妻/檐12.3/脊13.087m；核心13m平顶采光；长立面画屋面最高包络，未冻结窗表',25)
finish(s,5)

s=page('C01 · 关键剖面 / 楼梯孔 / 整栋拆分','层高4m，净高3.45m为设计候选；不作为现实施工合规、结构或消防结论。')
# Three-level section through teaching block.
for floor in range(3):
    y=1130-floor*280;s+=rect(160,y-18,1050,18,'#b3c0bc','#607c78',2)+text(170,y+45,f'F0{floor+1} +{floor*4} / 工程+{8+floor*4}m',24)
    s+=line(160,y-242,1210,y-242,'#9db0ac',3)
s+=line(160,1130,160,240,'#607c78',10)+line(1210,1130,1210,240,'#607c78',10)
s+=rect(160,210,1050,25,'#90a3a0','#607c78',2)+text(180,1240,'教学横剖：北9m教室—3.6m走廊—南服务/交流',28)
s=caption(s,1450,300,['采光庭：12×9=108㎡，三层通高','F02/F03楼板各减108㎡','边缘步台有讨论/等候，不放大树池','3层南角露台60㎡，不叠加新地标','','每层3座U梯，净跑2.2m','每层24踢步×0.166667=4m','每跑11踏面×0.3=3.3m','梯洞4.7×5.5=25.85㎡/座','F02/F03各扣77.55㎡','每层下方顶面也同位开孔','电梯井2.4×2.4，操作系统未定'])
# stair schematic expanded section
pts=[(180,2070)]
for i in range(24):pts.extend([(180+(i+1)*30,2070-i*(4/24)*100),(180+(i+1)*30,2070-(i+1)*(4/24)*100)])
s+=poly(pts,stroke='#648a82',sw=5)+text(160,1480,'U梯展开剖面示意 / 实际两跑位置不同；本图不是一条直梯',27)
s+=line(180,1770,480,1770,'#a07d58',3,'10,8')+text(180,1740,'对应顶面必须开洞',23)
# Core section: real plan width, two upper-floor apertures.
for f in range(3):
    yy=1370-f*136
    if f==0:s+=rect(1450,yy,1020,9,'#c5cec5')
    else:s+=rect(1450,yy,340,9,'#c5cec5')+rect(2198,yy,272,9,'#c5cec5')
s+=rect(1450,955,1020,10,'#abc5cb')+line(1450,965,1450,1370)+line(2470,965,2470,1370)
s+=text(1910,925,'核心剖面：两层孔位相同，庭边留学习步台',22,anchor='middle')
s=caption(s,1400,1500,['ROOF：各翼屋面/底面/采光构件','EXTERIOR：四向墙壳/门窗/遮阳/连廊接口','SLAB_F01/F02/F03：楼板独立，孔位共用','INTERIOR_F01/F02/F03：房间内墙/顶面/家具','STAIR_CORE：三梯/电梯空间，共轴分层','OCCLUDER：视线侧墙与顶面可独立隐藏','外壳内外只一套，不造重复共面墙','共同SW原点/层高；不各自重置轴心','分组资产就绪不等于运行隐藏/导航实现'])
finish(s,6)

s=page('C01 · 高频通路 / 公共停留 / 人物尺度','青绿上学、橙色图书、蓝色体育；楼梯以竖向模块单列，不沿用旧路线时间。')
s+=plan_floor(2,180,980,18,False)
colors=['#318b80','#c0844d','#4c79ad']
for r,c in zip(routes,colors):
    # Only interior XY shown; endpoints/exterior marked separately below.
    p=[(180+x*18,980-y*18) for x,y,z in r['points'] if 0<=x<=150 and 0<=y<=28]
    s+=poly(p,stroke=c,sw=5)
for p in stops:
    x,y=p['at'];s+=text(180+x*18,980-y*18,p['id']+f"·F{p['floor']}",24,'#844e46',anchor='middle')
s=caption(s,180,1250,[f"{r['id']} {r['name']}：纸面3D折线{r['length_3d_candidate_m']:.2f}m / XY{r['length_xy_m']:.2f}m" for r in routes])
s=caption(s,180,1450,['DAILY_03终点为体育馆门，非FIELD训练站位；后续训练场另沿既有室外路。','来访：主门→接待/职员侧；学生：鞋柜→年级梯→课堂；教职员：管理区与共用廊。','维护：东口授权时段→储物/竖井/设备，不穿教室；完全独立后勤路尚未成立。','P1入口照片、P2玩家年级厅、P3连接窗边、P4庭边、P5北门侧、P6许可露台。'])
char=sources[6].read_bytes();b64=base64.b64encode(char).decode()
s+='<image href="data:image/png;base64,'+b64+'" x="140" y="1810" width="260" height="260" style="image-rendering:pixelated"/>'
s=caption(s,500,1810,['原人物128²只读 / 约1.8m可见，约1.04m正面可见宽','胶囊1.92m高/0.68m直径另核；不缩人物或改镜头掩盖问题','教室门1.6×2.6m，主门3m；走廊3.6m允许停留退出主线','梯跑2.2m不代表拥挤相向/扶栏后一定可通；人物试作待核','桌0.65×0.45m/高0.72，椅高0.43；窗台1m，栏杆1.2m候选','当前是数据/比例规划，未进行真实相机、碰撞或自然光验证'])
finish(s,7)

# P08 schematic massing, desks and original character scaled against an actual doorway.
s=page('C01 · 退进体量与教室容量尺度','同一体块约束的相反观察；纯矢量规划，不是正式美术效果图/模型。')
def mass_view(cx,cy,az):
    a=math.radians(az);e=math.radians(30);k=8
    def project(p):
        x,y,z=p;x-=75;y-=14
        return(cx+(-x*math.sin(a)+y*math.cos(a))*k,cy+((x*math.cos(a)+y*math.sin(a))*math.sin(e)-z*math.cos(e))*k)
    faces=[]
    mass_blocks=[]
    for b in body:
        if b==[64,0,94,28]:mass_blocks.extend([([64,0,74,6],8.25),([64,6,74,28],13),([74,0,94,28],13)])
        else:mass_blocks.append((b,12.3 if b[0] in [18,30,52,94,142] else ridge))
    for b,h in mass_blocks:
        l,v,r,n=b
        p=[[l,v,0],[r,v,0],[r,n,0],[l,n,0],[l,v,h],[r,v,h],[r,n,h],[l,n,h]]
        for idxs,col in [([0,1,5,4],'#d8dbd0'),([1,2,6,5],'#bdccc7'),([2,3,7,6],'#cdd8cf'),([3,0,4,7],'#b4c5c1'),([4,5,6,7],'#829e99')]:
            pts=[p[i] for i in idxs];depth=sum((q[0]*math.cos(a)+q[1]*math.sin(a))*math.cos(e)+q[2]*math.sin(e) for q in pts)/len(pts);faces.append((depth,pts,col))
    pts=[[74,15,13.02],[86,15,13.02],[86,24,13.02],[74,24,13.02]]
    faces.append((sum((q[0]*math.cos(a)+q[1]*math.sin(a))*math.cos(e)+q[2]*math.sin(e) for q in pts)/4,pts,'#b7d8df'))
    ss=''
    for depth,pts,col in sorted(faces,key=lambda t:t[0]):ss+=poly([project(q) for q in pts]+[project(pts[0])],col,'#557d75',2)
    return ss
s+=mass_view(825,670,225)+mass_view(2420,670,45)
s+=text(180,990,'A 西南→东北 / 30°：主入口仍在西段，不把核心门厅居中',25)+text(1810,990,'B 东北→西南 / 30°：北门与退进屋面',25)
s+=text(180,1060,'体块按最高屋面包络示意；真实5°坡面/窗表由后续统一参考细化，不是正式渲染。',24)
s+=text(180,1190,'8.4×9m教室：6×6容量示意，5排可改30席；不增加实际NPC',27)
rx,ry,k=180,1260,70
s+=rect(rx,ry,8.4*k,9*k,'#e4ecec','#75958e',3)
s+=rect(rx+.1*k,ry+2.8*k,.12*k,3.4*k,'#65816f')
for row in range(6):
    for col in range(6):
        x=rx+(1.5+row*1.05)*k;y=ry+(.9+col*1.2)*k
        s+=rect(x,y,.45*k,.65*k,'#c2b799','#8e9d8f',1)+rect(x+.52*k,y+.18*k,.30*k,.30*k,'#b4c4b9','#8e9d8f',1)
s+=text(rx+8.4*k/2,ry+9*k+55,'净教室75.6㎡ / 桌宽0.65、深0.45，高0.72',22,anchor='middle')
s+=text(180,2060,'橙色门净1.6m位于走廊侧；桌列0.45/椅位0.30只是摆位候选',24)
s+=line(180,2160,530,2160,'#30464a',4)+text(180,2135,'教室平面 0—5m',22)
s+=line(rx+3.2*k,ry+9*k,rx+4.8*k,ry+9*k,'#a76d51',6)
scale_px=160;dx,dy=1200,1970
s+=rect(dx,dy-2.6*scale_px,1.6*scale_px,2.6*scale_px,'none','#a76d51',8)
canvas=1.8*scale_px*128/116
s+='<image href="data:image/png;base64,'+b64+f'" x="{dx+1.6*scale_px/2-canvas/2}" y="{dy-1.8*scale_px-4*canvas/128}" width="{canvas}" height="{canvas}" style="image-rendering:pixelated"/>'
s=caption(s,1700,1340,['原128²人物按可见1.8m映射','前向可见宽约1.04m，胶囊Ø0.68另核','门1.6×2.6m：正面余宽约0.56m','走廊3.6m：坐面退出该净主线','楼梯2.2m：并排仅约0.12m可见余量','不能据此称拥挤相向通行已通过','窗台1.0m/栏杆1.2m均候选','桌椅身高/坐姿须实际模型再核','原站立PNG不伪造坐姿或背向人物'])
finish(s,8)

# Generated planning tables.
def table(headers,rows):return '|'+ '|'.join(headers)+'|\n|'+'|'.join(['---']*len(headers))+'|\n'+''.join('|'+ '|'.join(map(str,r))+'|\n' for r in rows)
DOC.joinpath('rooms-areas-depth.md').write_text('# C01房间、面积与制作深度\n\n2026-10-15，净房间矩形为候选；控制4200㎡不直接计作使用面积。\n\n'+table(['层','围护平面基面㎡','庭孔㎡','梯孔㎡','井使用扣㎡','可分配水平㎡','房间公共净界㎡','主廊㎡','结构交通待细化㎡'],[[a[k] for k in ['floor','enclosed_plan_envelope','atrium_void','stair_void','elevator_use_exclusion','allocatable_horizontal_area','room_public_net_sum','main_corridor_net','other_circulation_structure_reserve']] for a in areas])+'\n围护平面基面不扣采光庭孔；三层露台60㎡已在该层封闭基面中扣，不重复扣。F1电梯井5.76㎡为使用口径扣除，不宣称首层底板实体开洞。楼梯包络内平台余量留在交通/结构余量中，不把孔与楼梯房净面积重复加减。房间净界不含墙，露台不算室内。\n\n'+table(['ID','用途','净面积㎡','门净宽×高m','访问','制作深度'],[[r['id'],r['name'],r['net_area'],f"{r['door_width']}×{r['door_height']}",r['access'],r['production_depth']] for r in rooms])+'\n深度：frequent=玩家班/主交通精作，medium=入口/管理/年级公共空间中等，background=完整门窗壳体与基础陈设，不要求各班独立玩法。24班共1814.4㎡净教室；两侧各4班/层，候选720–864学生，不等于NPC数。鞋柜总目标900格，当前只核196.08㎡分区预留，柜列/队列/进出细排未通过。\n',encoding='utf-8')
DOC.joinpath('routes.md').write_text('# C01三条高频通路与人群分流\n\n'+table(['ID','同端点目标','XY折线m','含楼梯候选3D线m','高程变化'],[[r['id'],r['name'],round(r['length_xy_m'],3),round(r['length_3d_candidate_m'],3),'校门到二层+4m' if r['id']=='DAILY_01' else '二层下至校园−4m'] for r in routes])+'\n每条完整三维折线在PLAN_01.json；楼梯中心线只是候选几何路线，长度包含大厅接驳和U转弯。Library终点为既有C03正门，不是灰盒LibraryRoom站位；Sport终点为C08馆门，不是ClubGround，因此不与旧R4/R5换端点比较耗时。所有教学楼公众访问受学校控制，不作市民穿校捷径。\n\n'+table(['点','层','用途'],[[p['id']+' '+p['name'],p['floor'],p['use']] for p in stops])+'\n来访在入口接待分流，进入管理区需允许；学生走鞋柜/年级梯与主廊；教职员走职员区与共廊；维护从东侧授权门到储藏/设备，部分仍共用通路，需错时而非宣称完全独立。课间优先玩家班旁交流厅折返，午休可去连接窗边/庭边，未设游戏活动奖励。\n',encoding='utf-8')
print(json.dumps({'body_area':gross,'stair_void_each':holes/3,'areas':areas,'route_m':[round(r['length_3d_candidate_m'],3) for r in routes],'rooms':len(rooms),'classrooms':24,'protected_inputs':len(protected)},ensure_ascii=False))
