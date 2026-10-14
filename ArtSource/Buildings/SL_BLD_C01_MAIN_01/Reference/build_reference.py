"""C01 REFERENCE only. One metre geometry feeds vector sheets and Blender source.
Does not write Planning, SchoolLife, B01 or approved SchoolGate assets.
Run with bundled Python; run render_reference.py in fresh background Blender next.
"""
from pathlib import Path
import json,math,hashlib,base64,html
ROOT=Path('D:/Art Asset Library')
OUT=Path(__file__).parent
PREFIX='SL_BLD_C01_MAIN_01_REFERENCE_01'
PLAN=ROOT/'ArtSource/Buildings/SL_BLD_C01_MAIN_01/Planning/SL_BLD_C01_MAIN_01_PLAN_01.json'
P=json.loads(PLAN.read_text(encoding='utf-8-sig'))
G={'asset':P['asset_id'],'revision':'REFERENCE_01','date':'2026-10-15','scope':'design/reference geometry, not formal asset or UE acceptance',
   'units':'m','plan_source':str(PLAN),'plan_sha256':hashlib.sha256(PLAN.read_bytes()).hexdigest(),
   'control':P['candidate']['control'],'segments':P['candidate']['segments'],'body_rects':P['candidate']['body_rects'],
   'rooms':P['rooms'],'entrances':P['entrances'],'areas':P['areas'],'routes':P['routes'],
   'origin_world_xy':P['shared_origin_world_xy'],'engineering_origin_world_xy':P['engineering_origin_world_xy'],
   'ground_engineering_z':8,'floors':[0,4,8],'slab_depth':.25,'ceiling_relative':3.45,
   'character':P['character'],'court':[74,15,86,24],'terrace':[64,0,74,6],
   'rt01':{'rect':[38,3,66,24],'area':588,'source_level_m_candidate':12,'level_semantics':'source does not disambiguate local roof height vs engineering absolute; planning review required',
           'stair_core':[41,9,49,19],'entry':[49,14],'status':'independent historical candidate; not relocated'},
   'roof':P['candidate']['roof_geometry'],'stairs':P['candidate']['stairs'],
   'materials':{'WALL':'#DDD9CB','PLINTH':'#989E98','FRAME':'#53686B','GLASS':'#779CA4','ROOF':'#687D80',
                'WOOD':'#AC875A','FLOOR':'#D4CEC0','METAL':'#7D8B89','BOARD':'#38625A','CHAIR':'#B39365',
                'GROUND':'#9DAF94','PAVE':'#CAC8BB','RAIL':'#768A89','SKYLIGHT':'#A2C3C8'},
   'openings':[],'primitives':[],'furniture':[],'classroom_variants':{},'lockers':[],
   'groups':{},'protected_inputs':json.loads((ROOT/'.cache/c01_reference/protected.json').read_text(encoding='utf-8'))}
def box(name,b,mat,group):
    if any(b[i+3]<=b[i] for i in range(3)):raise ValueError((name,b))
    G['primitives'].append({'id':name,'type':'box','bounds':b,'material':mat,'group':group})
def mesh(name,verts,faces,mat,group):
    G['primitives'].append({'id':name,'type':'mesh','vertices':verts,'faces':faces,'material':mat,'group':group})
def inside(x,y,rects):
    return any(a<=x<=c and b<=y<=d for a,b,c,d in rects)
def tiles(rects,holes=()):
    xs=sorted(set(v for r in rects+list(holes) for v in (r[0],r[2])))
    ys=sorted(set(v for r in rects+list(holes) for v in (r[1],r[3])))
    return [[a,b,c,d] for a,c in zip(xs,xs[1:]) for b,d in zip(ys,ys[1:])
            if inside((a+c)/2,(b+d)/2,rects) and not inside((a+c)/2,(b+d)/2,holes)]
def boundary(rects,holes=()):
    ts=tiles(rects,holes);raw=[]
    for a,b,c,d in ts:
        for axis,line,lo,hi,n in [('X',b,a,c,-1),('X',d,a,c,1),('Y',a,b,d,-1),('Y',c,b,d,1)]:
            mx,my=((lo+hi)/2,line+n*.001) if axis=='X' else (line+n*.001,(lo+hi)/2)
            if not inside(mx,my,rects) or inside(mx,my,holes):raw.append((axis,line,lo,hi,n))
    merged=[]
    for key in sorted(set((e[0],e[1],e[4]) for e in raw)):
        segs=sorted((e[2],e[3]) for e in raw if (e[0],e[1],e[4])==key)
        for lo,hi in segs:
            if merged and merged[-1][:2]==key[:2] and merged[-1][4]==key[2] and abs(merged[-1][3]-lo)<1e-6:
                e=merged.pop();merged.append((key[0],key[1],e[2],hi,key[2]))
            else:merged.append((key[0],key[1],lo,hi,key[2]))
    return merged
def wallbox(name,axis,line,lo,hi,z0,z1,mat,grp,th=.30,n=0):
    # Exterior wall lies inward from fixed outer boundary; room openings are through it.
    ctr=line-n*th/2
    b=[lo,ctr-th/2,z0,hi,ctr+th/2,z1] if axis=='X' else [ctr-th/2,lo,z0,ctr+th/2,hi,z1]
    box(name,b,mat,grp)
def opening(oid,axis,line,lo,hi,z0,z1,kind,room,side,n):
    o=dict(id=oid,axis=axis,line=line,lo=lo,hi=hi,z0=z0,z1=z1,kind=kind,room=room,side=side,normal=n)
    G['openings'].append(o);return o
def facade_windows(axis,line,lo,hi,n,floor):
    z=(floor-1)*4;os=[]
    # Original three entry points only on first level. F03 terrace controlled access separate.
    for e in G['entrances']:
        ex,ey=e['local'];q=ex if axis=='X' else ey
        if floor==1 and abs((ey if axis=='X' else ex)-line)<1e-6 and lo<=q-1.5 and hi>=q+1.5:
            os.append(opening(e['id'],axis,line,q-1.5,q+1.5,z,z+e['height'],'door',e['id'],'S' if axis=='X' and n<0 else ('N' if axis=='X' else 'E'),n))
    if floor==3 and axis=='X' and line==6 and lo<=69<=hi:
        os.append(opening('TERRACE_ACCESS',axis,line,68.2,69.8,8,10.6,'door','F3_CW','S',n))
    relevant=[]
    for r in G['rooms']:
        if r['floor']!=floor:continue
        a,b,c,d=r['rect']
        edge=(b if n<0 else d) if axis=='X' else (a if n<0 else c)
        if abs(edge-line)>.31:continue
        rrlo,rrhi=(a,c) if axis=='X' else (b,d)
        aa=max(lo+.35,rrlo+.25);bb=min(hi-.35,rrhi-.25)
        if bb-aa<1.3:continue
        relevant.append((r,aa,bb))
    side=('S' if n<0 else 'N') if axis=='X' else ('W' if n<0 else 'E')
    if axis=='X' and line==8 and lo in (52,94):
        for j in range(4):
            aa=lo+.6+j*2.8
            os.append(opening(f'LINK_{int(lo)}_F{floor}_S_{j+1}',axis,line,aa,aa+2.3,z+.6,z+3.2,'link',f'F{floor}_L'+('W' if lo==52 else 'E'),'S',n))
    for r,a,b in relevant:
        typ='teaching' if r['kind']=='classroom' else ('privacy' if 'WC' in r['id'] else
            ('link' if r['id'].endswith(('LW','LE')) else ('public' if r['kind']=='public' else 'support')))
        sill=1.6 if typ=='privacy' else (.45 if typ in ('link','public') else .9)
        height=1.25 if typ=='privacy' else (2.8 if typ in ('link','public') else 2.1)
        # Individual room bays, 3 north classroom openings / room, differing support rhythms.
        num=3 if typ=='teaching' else max(1,int((b-a)/3.0))
        step=(b-a)/num;ww=min(2.35 if typ=='teaching' else 2.2,step-.35)
        for j in range(num):
            mid=a+(j+.5)*step;ll=mid-ww/2;hh=mid+ww/2
            if any(ll<o['hi']+.2 and hh>o['lo']-.2 for o in os):continue
            os.append(opening(f"{r['id']}_{side}_{j+1:02}",axis,line,ll,hh,z+sill,z+sill+height,typ,r['id'],side,n))
    # Stair/end-corridor glazing with fixed bays, where no room touches the outside edge.
    for s in G['stairs']:
        a,b,c,d=s['box']
        if axis=='X' and line==0 and lo<=a+.6 and hi>=c-.6:
            os.append(opening(f"{s['id']}_F{floor}_S",axis,line,a+1,c-1,z+1,z+3.25,'stair',s['id'],'S',n))
    if axis=='Y' and line in (0,150):
        for mid in [10.9]:
            if lo+.6<=mid-1.25 and hi-.6>=mid+1.25 and not any(mid-1.25<o['hi'] and mid+1.25>o['lo'] for o in os):
                os.append(opening(f'END_{int(line)}_F{floor}',axis,line,mid-1.25,mid+1.25,z+.5,z+3.3,'end',None,side,n))
    return os
def build_wall(axis,line,lo,hi,n,floor,os,index,court=False):
    z=(floor-1)*4;zs=sorted(set([z,z+4]+[o[k] for o in os for k in ('z0','z1')]))
    us=sorted(set([lo,hi]+[o[k] for o in os for k in ('lo','hi')]))
    grp=f'EXTERIOR_{("N" if n>0 else "S") if axis=="X" else ("E" if n>0 else "W")}'
    if court:grp=f'INTERIOR_F{floor:02}_COURT'
    for a,b in zip(us,us[1:]):
        for c,d in zip(zs,zs[1:]):
            if not any(o['lo']<(a+b)/2<o['hi'] and o['z0']<(c+d)/2<o['z1'] for o in os):
                wallbox(f'W_{floor}_{index}_{a:.3f}_{c:.3f}',axis,line,a,b,c,d,'WALL',grp,n=n)
    for o in os:
        a,b,c,d=o['lo'],o['hi'],o['z0'],o['z1'];t=.075
        wallbox(o['id']+'_glass',axis,line,a,b,c,d,'GLASS',grp,th=.045,n=n)
        for q,(u,v,e,f) in enumerate([(a,a+t,c,d),(b-t,b,c,d),(a,b,c,c+t),(a,b,d-t,d)]):
            wallbox(o['id']+f'_frame{q}',axis,line,u,v,e,f,'FRAME',grp,th=.12,n=n)
        for j in range(1,max(2,round((b-a)/.85))):
            mid=a+(b-a)*j/max(2,round((b-a)/.85))
            wallbox(o['id']+f'_mullion{j}',axis,line,mid-.025,mid+.025,c,d,'FRAME',grp,th=.07,n=n)
        if o['kind'] in ('support','privacy','teaching','public','link') and not court:
            depth=.75 if o['side']=='S' else .35
            at_control_edge=(axis=='X' and line in (0,28)) or (axis=='Y' and line in (0,150))
            ctr=line+(-n if at_control_edge else n)*depth/2
            bounds=[a-.1,ctr-depth/2,d+.10,b+.1,ctr+depth/2,d+.19] if axis=='X' else [ctr-depth/2,a-.1,d+.10,ctr+depth/2,b+.1,d+.19]
            box(o['id']+'_shade',bounds,'ROOF','EXTERIOR_SHADE')
            o['shade_depth']=depth
            o['shade_mode']='inside control / inward hood' if at_control_edge else 'projected canopy'
    # thin darker floor fascia; not a thick curtain-wall stripe
    wallbox(f'BAND_{floor}_{index}',axis,line,lo,hi,z+3.85,z+4,'PLINTH',grp,th=.32,n=n)
for f in (1,2,3):
    holes=[G['court']]+([G['terrace']] if f==3 else [])
    for i,e in enumerate(boundary(G['body_rects'],[G['terrace']] if f==3 else [])):
        os=facade_windows(*e,f);build_wall(*e,f,os,i)
    # Atrium glass rail/frame is interior; no closed slab or ceiling over the court.
    if f>1:
        for axis,line,lo,hi,n in [('X',15,74,86,1),('X',24,74,86,-1),('Y',74,15,24,1),('Y',86,15,24,-1)]:
            wallbox(f'COURT_GUARD_F{f}_{axis}_{line}',axis,line,lo,hi,(f-1)*4,(f-1)*4+1.2,'RAIL',f'INTERIOR_F{f:02}_COURT',th=.08)
    floorholes=[] if f==1 else [G['court']]+[s['opening'] for s in G['stairs']]
    # Terrace is a slab at FL8, not an extra raised platform; finish sheet .03 only.
    for i,r in enumerate(tiles(G['body_rects'],floorholes)):
        box(f'SLAB_F{f:02}_{i}',[r[0],r[1],(f-1)*4-.25,r[2],r[3],(f-1)*4],'FLOOR',f'SLAB_F{f:02}')
    ceilholes=[G['court']]+[s['opening'] for s in G['stairs']]
    if f==2:ceilholes+=[G['terrace']]
    if f==3:ceilholes+=[G['terrace']]
    for i,r in enumerate(tiles(G['body_rects'],ceilholes)):
        box(f'CEILING_F{f:02}_{i}',[r[0],r[1],(f-1)*4+3.45,r[2],r[3],(f-1)*4+3.49],'WALL',f'INTERIOR_F{f:02}_CEILING')
    # Partition surfaces on net room boundaries; door cutouts, shared walls owned once.
    for r in [r for r in G['rooms'] if r['floor']==f and r['id']!='F1_AT']:
        a,b,c,d=r['rect'];dx,dy=r['door'];wd=r['door_width'];z=(f-1)*4
        for side,axis,line,lo,hi in [('S','X',b,a,c),('N','X',d,a,c),('W','Y',a,b,d),('E','Y',c,b,d)]:
            # Exterior inward face already owned by exterior. Shared divider placed in room gap.
            if any(e[0]==axis and abs(e[1]-line)<=.31 and e[2]<=lo+.01 and e[3]>=hi-.01 for e in boundary(G['body_rects'],holes if f==3 else [])):continue
            q=dx if axis=='X' else dy
            ondoor=abs((dy if axis=='X' else dx)-line)<1e-6
            # Room perimeter is guide only on N/E to avoid duplicates; S/W actual partitions.
            if side in ('N','E'):continue
            grp=f'INTERIOR_F{f:02}_WALLS'
            ctr=line-.10
            if ondoor:
                for j,(aa,bb,cc,dd) in enumerate([(lo,q-wd/2,z,z+3.45),(q+wd/2,hi,z,z+3.45),(q-wd/2,q+wd/2,z+r['door_height'],z+3.45)]):
                    if bb>aa:wallbox(f'{r["id"]}_{side}_{j}',axis,ctr,aa,bb,cc,dd,'WALL',grp,th=.2)
            else:wallbox(f'{r["id"]}_{side}',axis,ctr,lo,hi,z,z+3.45,'WALL',grp,th=.2)
            if ondoor:
                opening(r['id']+'_D',axis,ctr,q-wd/2,q+wd/2,z,z+r['door_height'],'sliding_internal',r['id'],'INTERIOR',0)
# Roofs: actual 5 degree surfaces with ridge from original span; .60 eaves lower along same slope.
pitch=math.tan(math.radians(5))
for name,a,c in [('WEST',0,52),('EAST',106,150)]:
    ridge=G['roof']['ridge_top'];edge=12.3-.6*pitch
    v=[[a,3.4,edge],[c,3.4,edge],[c,13,ridge],[a,13,ridge],
       [a,22.6,edge],[c,22.6,edge]]
    mesh(name+'_SHALLOW_ROOF',v,[[0,1,2,3],[3,2,5,4]],'ROOF','ROOF')
    for j,y in enumerate([3.4,22.6]):
        box(name+f'_GUTTER{j}',[a,y-.08,edge-.12,c,y+.08,edge+.03],'FRAME','ROOF')
    for x in [a+.6,c-.6]:
        for y in [4.0,22.0]:
            box(f'DRAIN_{name}_{x}_{y}',[x-.07,y-.07,.2,x+.07,y+.07,12.2],'METAL','EXTERIOR_DRAIN')
    # Gable triangles close shells on actual end X; no floating roof over open wall.
    for x in [a,c]:
        mesh(f'{name}_GABLE_{x}',[[x,4,12],[x,22,12],[x,22,12.3],[x,13,ridge],[x,4,12.3]],[[0,1,2,3,4]],'WALL','EXTERIOR_GABLE')
for i,r in enumerate(tiles([[64,0,94,28]],[G['court'],G['terrace']])):
    box(f'CORE_ROOF_{i}',[r[0],r[1],12.65,r[2],r[3],12.9],'ROOF','ROOF')
for name,r in [('LINK_W',[52,8,64,22]),('LINK_E',[94,8,106,22]),('WEST_STAIR',[30,0,38,4]),('PORCH',[18,0,30,4]),('EAST_STAIR',[142,0,150,4])]:
    box(name+'_ROOF',[r[0],r[1],12.12,r[2],r[3],12.3],'ROOF','ROOF')
for axis,line,lo,hi,n in boundary([[64,0,94,28]],[G['terrace']]):
    wallbox(f'CORE_PARAPET_{axis}_{line}_{lo}',axis,line,lo,hi,12.9,13,'ROOF','ROOF',th=.25,n=n)
# Court skylight: ring raised13.2, low ridge13.65, no room floor/ceiling over 108m².
mesh('COURT_SKYLIGHT',[[74,15,13.2],[86,15,13.2],[86,19.5,13.65],[74,19.5,13.65],[74,24,13.2],[86,24,13.2]],
     [[0,1,2,3],[3,2,5,4]],'SKYLIGHT','ROOF')
for x in [74,77,80,83,86]:
    for k,(a,b) in enumerate([(15,19.5),(19.5,24)]):
        za=13.2 if a==15 else 13.65;zb=13.65 if b==19.5 else 13.2
        mesh(f'SKY_FRAME_{x}_{k}',[[x-.035,a,za+.03],[x+.035,a,za+.03],[x+.035,b,zb+.03],[x-.035,b,zb+.03]],[[0,1,2,3]],'FRAME','ROOF')
# Main portal over original threshold, roof within control: 2m internal soffit.
box('MAIN_WOOD_PORTAL_L',[21.8,0,0,23.5,.3,3.6],'WOOD','EXTERIOR_ENTRY')
box('MAIN_WOOD_PORTAL_R',[26.5,0,0,28.2,.3,3.6],'WOOD','EXTERIOR_ENTRY')
box('MAIN_SHORT_CANOPY',[21.8,0,3.3,28.2,2.0,3.6],'ROOF','EXTERIOR_ENTRY')
box('MAIN_BLANK_NAME_STRIP',[22.0,0,3.65,28,.05,4.05],'WOOD','EXTERIOR_ENTRY')
for axis,line,lo,hi in [('X',0,64,74),('Y',64,0,6),('Y',74,0,6)]:
    wallbox(f'TERRACE_GUARD_{axis}_{line}',axis,line,lo,hi,8,9.2,'RAIL','INTERIOR_F03_TERRACE',th=.08,n=1 if line==74 else -1)
box('TERRACE_FINISH',[64,0,8,74,6,8.03],'PAVE','INTERIOR_F03_TERRACE')
G['roof']['terrace_finish_top']=8.03
G['roof']['terrace_previous_planning_cap']=8.25
G['roof']['skylight_peak']=13.65
G['roof']['teaching_eave_overhang_y']=.6
G['roof']['eave_outer_edge_z']=12.3-.6*pitch
# Stair identical S1/S2/S3, two storeys; 12 risers/flight, 11 going, platform .9..3.1.
for s in G['stairs']:
    a,b,c,d=s['opening']
    for f,z in [(1,0),(2,4)]:
        grp='STAIR_CORE_'+s['id']
        for run in (0,1):
            xl=a+run*2.5
            for k in range(12):
                y0=6.4-(k+1)*.3 if run==0 else 3.1+k*.3
                y1=6.4-k*.3 if run==0 else 3.1+(k+1)*.3
                # Last riser joins platform/floor; eleven visible treads, twelfth landing surface.
                if k==11:continue
                top=z+(k+1)/6 if run==0 else z+2+(k+1)/6
                box(f'{s["id"]}_F{f}_R{run}_{k}',[xl,y0,top-.16,xl+2.2,y1,top],'FLOOR',grp)
        box(f'{s["id"]}_F{f}_MID',[a,.9,z+1.8,c,3.1,z+2],'FLOOR',grp)
        # finite-width handrail top strips follow true flight rise, distinct centre gap .3.
        for run in (0,1):
            for x in [a+run*2.5-.045,a+run*2.5+2.245]:
                ys=[6.4,3.1] if run==0 else [3.1,6.4]
                zz=[z+1.1,z+3.1] if run==0 else [z+3.1,z+5.1]
                mesh(f'{s["id"]}_F{f}_RAIL{run}_{x}',[[x-.035,ys[0],zz[0]],[x+.035,ys[0],zz[0]],[x+.035,ys[1],zz[1]],[x-.035,ys[1],zz[1]]],[[0,1,2,3]],'FRAME',grp)
    G['groups']['STAIR_CORE_'+s['id']]={'opening':s['opening'],'landings':[0,2,4,6,8],'riser_count_per_floor':24,'clear_flight':2.2,'headroom':'open to matching slab/ceiling holes; finite actor check pending'}
# Player desks point west (-X); same room, door and north windows, different Y column pitch.
for count,cols in [(30,5),(36,6)]:
    items=[];ys=[13.8+j*1.7 for j in range(5)] if cols==5 else [13.55+j*1.44 for j in range(6)]
    for row in range(6):
        for col,y in enumerate(ys):
            x=42.7+row*1.0
            items.append({'id':f'C{count}_DESK_{row+1}_{col+1}','kind':'desk','bounds':[x-.225,y-.325,4+.69,x+.225,y+.325,4+.72],'seat':[x+.4,y,4+.43]})
    G['classroom_variants'][str(count)]={'room':'F2_W4','rect':[41,12.7,49.4,21.7],'front':'west -X','columns':cols,'rows':6,'desks':items,
        'desk_size':[.45,.65,.72],'chair_size':[.45,.45,.43],
        'front_clear':1.475,'rear_static_clear':1.075,
        'between_columns':1.05 if cols==5 else .79,
        'side_clear_min':.775 if cols==5 else .525,
        'chair_pullback_allowance':.25,
        'note':'30 recommended: 1.05 cross-column lanes only 10mm wider than original visible sprite. 36 .79 fits .68 capsule geometrically but not1.04 visible width. Chair pullback and side/rear movement not accepted.'}
for i in G['classroom_variants']['30']['desks']:
    b=i['bounds'];box(i['id'],b,'WOOD','INTERIOR_F02_PLAYER')
    x=(b[0]+b[3])/2;y=(b[1]+b[4])/2
    for lx in [x-.18,x+.18]:
        for ly in [y-.26,y+.26]:box(i['id']+f'_leg{lx}_{ly}',[lx-.02,ly-.02,4,lx+.02,ly+.02,4.69],'FRAME','INTERIOR_F02_PLAYER')
    sx,sy,sz=i['seat'];box(i['id']+'_CHAIR',[sx-.225,sy-.225,sz-.035,sx+.225,sy+.225,sz],'CHAIR','INTERIOR_F02_PLAYER')
    box(i['id']+'_CHAIR_BACK',[sx+.16,sy-.225,sz,sx+.22,sy+.225,4.84],'CHAIR','INTERIOR_F02_PLAYER')
    for lx in [sx-.18,sx+.18]:
        for ly in [sy-.18,sy+.18]:box(i['id']+f'_CHAIRLEG_{lx}_{ly}',[lx-.018,ly-.018,4,lx+.018,ly+.018,sz-.035],'FRAME','INTERIOR_F02_PLAYER')
box('PLAYER_BOARD',[41.05,15,5,41.12,19,6.25],'BOARD','INTERIOR_F02_PLAYER')
box('PLAYER_TEACHER_DESK',[41.45,16.4,4.72,42.05,17.6,4.75],'WOOD','INTERIOR_F02_PLAYER')
for y in [16.45,17.45]:box(f'TEACHER_SUPPORT_{y}',[41.5,y,4,42,y+.1,4.72],'FRAME','INTERIOR_F02_PLAYER')
# shoe banks: main 600 + supplemental300; exact 5 rows × .3 cell height, .3 column pitch.
for row,y in enumerate([2.3,4.9,7.5]):
    for side,x,length in [('W',18.7,3.6),('E',26.9,2.4)]:
        G['lockers'].append({'id':f'MAIN_{side}{row+1}','room':'F1_WL','bounds':[x,y-.35,0,x+length,y+.35,1.5],'columns':round(length/.3),'rows':5,'faces':2,'cell_pitch':[.3,.3],'depth_each':.35})
for j,y in enumerate([16.5,19.5]):
    G['lockers'].append({'id':f'LINK_{j+1}','room':'F1_LW','bounds':[54.8,y-.35,0,59.3,y+.35,1.5],'columns':15,'rows':5,'faces':2,'cell_pitch':[.3,.3],'depth_each':.35})
for bank in G['lockers']:
    b=bank['bounds'];box('LOCKER_'+bank['id'],b,'WOOD','INTERIOR_F01_SHOES')
    for face,y in enumerate([b[1]-.005,b[4]+.005]):
        for col in range(bank['columns']):
            for row in range(5):
                box(f'CELL_{bank["id"]}_{face}_{col}_{row}',[b[0]+col*.3+.015,y-.007,row*.3+.015,b[0]+(col+1)*.3-.015,y+.007,(row+1)*.3-.015],'PLINTH','INTERIOR_F01_SHOES')
G['shoe_capacity']={'main':600,'supplement':300,'total_cells':900,'target':900,'basis':'8 double-sided banks, .30x.30 pitch, 5rows, 2faces each; nominal grid not运营/消防 capacity',
                   'main_center_lane':[23.5,.3,26.5,8.8],'main_bank_gap':1.9,'supplement_bank_gap':2.3,'main_clearances':'west bank end to central lane1.2m; east .4m cabinet-side buffer not pedestrian passage; east cells approached from north/south'}
def furnishing(oid,room,rect,kind='bench',facing='centre',height=.45):
    r=next(r for r in G['rooms'] if r['id']==room);z=(r['floor']-1)*4
    b=[rect[0],rect[1],z,rect[2],rect[3],z+height]
    G['furniture'].append(dict(id=oid,room=room,bounds=b,kind=kind,facing=facing))
    box(oid,b,'WOOD' if kind not in ('notice','reception') else 'FRAME',f'INTERIOR_F{r["floor"]:02}_PUBLIC')
for item in [('P1_CHANGE_W','F1_WL',[18.8,.65,22,.95],'bench','north',.45),
             ('P1_WAIT','F1_WL',[27, .65,29.1,1.1],'bench','north',.45),
             ('P1_PHOTOS','F1_WL',[29.45,1.2,29.7,1.9],'notice','west',1.6),
             ('VISITOR_DESK','F1_WO',[39,7.1,40.6,7.8],'reception','north',.75),
             ('LINK_CHANGE','F1_LW',[60,14,62.7,14.45],'bench','north',.45),
             ('P2_A','F2_WO',[39,4.6,42,5.2],'bench','north',.45),
             ('P2_B','F2_WO',[48,4.6,51,5.2],'bench','north',.45),
             ('P2_TABLE','F2_WO',[44,5.7,46.2,6.6],'table','centre',.72),
             ('P2_NOTICE','F2_WO',[48,8.4,51,8.65],'notice','south',1.6),
             ('P3_WINDOW','F2_LW',[54,21,59,21.6],'bench','south',.45),
             ('P3_TABLE','F2_LW',[55.5,18.8,57.5,19.7],'table','north',.72),
             ('P3_LOW_RETURN','F2_LW',[53,19.5,53.6,21.6],'bench','east',.45),
             ('P4_W','F1_AT',[74.5,16,75.1,22],'bench','east',.45),
             ('P4_E','F1_AT',[84.9,16,85.5,22],'bench','west',.45),
             ('P4_SHORT_TABLE_W','F1_AT',[75.8,18.5,77,19.5],'table','west',.65),
             ('P4_SHORT_TABLE_E','F1_AT',[83,18.5,84.2,19.5],'table','east',.65),
             ('P5_EDGE','F1_CN',[92.8,23.5,93.4,26.8],'bench','west',.45),
             ('P5_NOTICE','F1_CN',[86.6,26.9,88,27.3],'notice','south',1.6),
             ('P6_BUFFER','F3_CW',[64.7,7.7,67.5,8.2],'bench','south',.45)]:
    furnishing(*item)
for j,rect in enumerate([[65,1,68,1.5],[72.4,2,73,5]]):
    G['furniture'].append({'id':f'P6_TERRACE_{j}','room':'TERRACE','bounds':[rect[0],rect[1],8.03,rect[2],rect[3],8.48],'kind':'bench','facing':'centre'})
    box(f'P6_TERRACE_{j}',G['furniture'][-1]['bounds'],'WOOD','INTERIOR_F03_TERRACE')
for group in sorted(set(o['group'] for o in G['primitives'])):
    G['groups'].setdefault(group,{'scope':'reference geometry only','shared_origin':[0,0,0]})
G['groups']['contract']={'ROOF':'removable incl skylight/gutters; roof removal does not remove outer wall/gables',
 'EXTERIOR':'one inward-facing exterior ownership, S/N/E/W independently hideable, shade/entry/drain children',
 'SLAB_F01_F03':'solid tiles subtract matching 108m² court on F02,F03 and 3×25.85m² stair openings; no elevator structural excavation assumed',
 'INTERIOR_F01_F03':'walls / ceilings / player / shoes / public / court / terrace separable; ceiling same holes as upper slab',
 'STAIR_CORE':'each S1/2/3 independent, leave all supports/treads active when floor shell hidden',
 'NAV':'S1/2/3 lower landing y6.4..8.8 at0/4/8, mid y.9..3.1 at2/6, upper exit same y6.4..8.8; author finite capsules later',
 'OCCLUSION':'hide south exterior + current floor south partitions + ceiling together; no code implemented; rotate25–40deg check pending'}
G['cameras']={'A':{'azimuth_from_east':225,'elevation':30,'target':[75,14,5.5]},
              'B':{'azimuth_from_east':45,'elevation':30,'target':[75,14,5.5]},
              'ENTRY':{'azimuth_from_east':240,'elevation':18,'target':[25,3,2],'ortho_scale':22},
              'CLASS':{'azimuth_from_east':45,'elevation':42,'target':[45.2,17.2,4.8],'ortho_scale':13}}
G['annotations']={'court_section_x':80,'stair_section_x':32.7,'entry_section_x':25,
 'material_density_candidates_px_per_m':[32,64],'material_scope':'procedural/flat design indication only; no final UV or base-color baked solar shadows',
 'confirmed':'150x28,52/12/30/12/44,3floors,24classes,3entrances,court108,terrace60,player30main',
 'not_verified':['finite actor movement','36seats sprite clearance','locker operating capacity','structural/fire design','RT01 access/support','UV/LOD/collision/budgets','UE/NPC/time/occlusion']}
(OUT/(PREFIX+'_GEOMETRY.json')).write_text(json.dumps(G,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
print('Geometry',len(G['primitives']),'primitives',len(G['openings']),'openings','900nominalcells')

# SVG drawing helpers. All projections use exact JSON coordinates.
class Sheet:
 def __init__(self,title,subtitle):
  self.a=['<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="3200" height="2400" viewBox="0 0 3200 2400">',
   '<rect width="3200" height="2400" fill="#F4F2EB"/>',
   '<style>text{font-family:Microsoft YaHei,sans-serif;fill:#293F42} .small{font-size:24px}</style>']
  self.text(80,95,title,48);self.text(80,145,subtitle,25)
  self.line(80,185,3120,185,'#9BACAB',2)
 def text(self,x,y,t,size=28,color=None,anchor='start'):
  self.a.append(f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" text-anchor="{anchor}"'+(f' fill="{color}"' if color else '')+'>'+html.escape(str(t))+'</text>')
 def line(self,a,b,c,d,col='#667B7A',w=2,dash=None):
  self.a.append(f'<line x1="{a}" y1="{b}" x2="{c}" y2="{d}" stroke="{col}" stroke-width="{w}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
 def rect(self,x,y,w,h,fill='none',stroke='#607676',sw=2):
  self.a.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
 def poly(self,pts,fill='none',col='#566E70',sw=2):
  self.a.append('<polygon points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in pts)+f'" fill="{fill}" stroke="{col}" stroke-width="{sw}"/>')
 def image(self,name,x,y,w,h):
  path=OUT/name
  if path.exists():
   uri=base64.b64encode(path.read_bytes()).decode()
   self.a.append(f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet" xlink:href="data:image/png;base64,{uri}"/>')
  else:self.rect(x,y,w,h,'#DFE4DE');self.text(x+20,y+50,'渲染将由同JSON参考源补入',25)
 def note(self,x,y,lines,size=27,dy=45):
  for i,t in enumerate(lines):self.text(x,y+i*dy,t,size)
 def save(self,id):
  self.text(80,2335,'C01 REFERENCE_01 · 2026-10-15 · 单位m · 设计参考 / 共享简模预览；非最终贴图 / 非实际游戏效果',23)
  self.text(3100,2335,id,27,anchor='end');self.a.append('</svg>')
  (OUT/f'{PREFIX}_{id}.svg').write_text('\n'.join(self.a),encoding='utf-8',newline='\n')
def dim(s,x1,y1,x2,y2,t):
 s.line(x1,y1,x2,y2);s.line(x1,y1-8,x1,y1+8);s.line(x2,y2-8,x2,y2+8);s.text((x1+x2)/2,(y1+y2)/2-12,t,25,anchor='middle')
def plan(s,f,ox,oy,k=18,labels=True,furniture=True,outline=True):
 conv=lambda x,y:(ox+x*k,oy-y*k)
 for r in G['body_rects']:
  x,y=conv(r[0],r[3]);s.rect(x,y,(r[2]-r[0])*k,(r[3]-r[1])*k,'#E1DFD3','#7E9391',2)
 for r in G['rooms']:
  if r['floor']!=f:continue
  a,b,c,d=r['rect'];x,y=conv(a,d);fill='#F1EEE4' if r['kind']=='classroom' else '#E9E4D7'
  s.rect(x,y,(c-a)*k,(d-b)*k,fill,'#879A97',1.5)
  if labels:
   s.text(ox+(a+c)/2*k,oy-(b+d)/2*k,r['id'],20,anchor='middle')
   if k>=18:s.text(ox+(a+c)/2*k,oy-(b+d)/2*k+27,'玩家班 30' if r['id']=='F2_W4' else ('75.6㎡' if r['kind']=='classroom' else r['name'][:7]),18,anchor='middle')
  dx,dy=r['door'];s.line(ox+(dx-.8)*k,oy-dy*k,ox+(dx+.8)*k,oy-dy*k,'#B3734F',5)
 # clear central corridor
 x,y=conv(0,12.7);s.rect(x,y,150*k,3.6*k,'#DAE9E5','#899F9C',1)
 s.text(ox+75*k,oy-10.9*k+8,'主廊净3.6 · 中心y10.9 · 维护部分共用，授权/错时',21,anchor='middle')
 a,b,c,d=G['court'];x,y=conv(a,d)
 s.rect(x,y,(c-a)*k,(d-b)*k,'#FFFFFF','#839C98',3)
 s.text(ox+80*k,oy-19.5*k,'108㎡庭 / '+('底层' if f==1 else '通高孔'),21,anchor='middle')
 for st in G['stairs']:
  a,b,c,d=st['opening'];x,y=conv(a,d);s.rect(x,y,(c-a)*k,(d-b)*k,'#C2D3CF')
  s.text(ox+(a+c)/2*k,oy-(b+d)/2*k,st['id'],22,anchor='middle')
 if f==3:
  a,b,c,d=G['terrace'];x,y=conv(a,d);s.rect(x,y,(c-a)*k,(d-b)*k,'#DCE5D4')
  s.text(ox+69*k,oy-3*k,'60㎡受控露台',22,anchor='middle')
 for o in G['openings']:
  if o['side']=='INTERIOR' or int(o['z0']//4)+1!=f:continue
  if o['axis']=='X':
   s.line(ox+o['lo']*k,oy-o['line']*k,ox+o['hi']*k,oy-o['line']*k,'#527A88',4)
  else:s.line(ox+o['line']*k,oy-o['lo']*k,ox+o['line']*k,oy-o['hi']*k,'#527A88',4)
 if furniture:
  for it in G['furniture']+([dict(b,kind='locker') for b in G['lockers']] if f==1 else []):
   b=it['bounds']
   if int(b[2]//4)+1!=f:continue
   x,y=conv(b[0],b[4]);s.rect(x,y,(b[3]-b[0])*k,(b[4]-b[1])*k,'#A58B66','#776E5C',1)
  if f==2:
   for it in G['classroom_variants']['30']['desks']:
    b=it['bounds'];x,y=conv(b[0],b[4]);s.rect(x,y,(b[3]-b[0])*k,(b[4]-b[1])*k,'#A58B66','#776E5C',1)
 if f==1:
  for e in G['entrances']:
   x,y=conv(*e['local']);s.text(x,y+42,e['id']+' ↓' if e['id']=='C01_MAIN' else e['id'],23,anchor='middle')
def class_plan(s,count,ox,oy,k=90):
 v=G['classroom_variants'][str(count)]
 a,b,c,d=v['rect'];s.rect(ox,oy,8.4*k,9*k,'#FBFAF5',sw=4)
 # x horizontal / north up, same geometry in both
 for it in v['desks']:
  q=it['bounds'];x=ox+(q[0]-a)*k;y=oy+(d-q[4])*k
  s.rect(x,y,.45*k,.65*k,'#AC875A',sw=1)
  sx,sy,sz=it['seat'];s.rect(ox+(sx-.225-a)*k,oy+(d-sy-.225)*k,.45*k,.45*k,'#CCC2AA',sw=1)
 s.rect(ox+.05*k,oy+2.7*k,.07*k,4*k,'#38625A')
 s.rect(ox+.45*k,oy+4.1*k,.6*k,1.2*k,'#AC875A')
 s.line(ox+3.2*k,oy+9*k,ox+4.8*k,oy+9*k,'#B3734F',8)
 for o in G['openings']:
  if o['room']=='F2_W4' and o['side']=='N':
   s.line(ox+(o['lo']-a)*k,oy,ox+(o['hi']-a)*k,oy,'#527A88',8)
 s.text(ox+4.2*k,oy-30,f'{count}席 · {v["columns"]}列×6排 · 向西授课 ←',28,anchor='middle')
 dim(s,ox,oy+9*k+40,ox+8.4*k,oy+9*k+40,'8.4m')
 s.note(ox,oy+9*k+90,[f'列间 {v["between_columns"]:.2f}m / 桌0.65×0.45×H0.72',
  '教师前场1.475 / 静态后通道1.075',
  '门1.6×2.6，滑门；人物侧通道仍窄',
  '椅后拉0.25后，后通道0.825待核'],24,38)
def char(s,x,y,k=120):
 f=Path(G['character']['source']);im=base64.b64encode(f.read_bytes()).decode()
 # bbox top4 bottom120; fixed groundy, original image placed with no re-encoding
 size=1.8*128/116*k
 s.a.append(f'<image x="{x}" y="{y-1.8*120/116*k}" width="{size}" height="{size}" style="image-rendering:pixelated" xlink:href="data:image/png;base64,{im}"/>')
 s.line(x+size+20,y,x+size+20,y-1.8*k);s.text(x+size+35,y-.9*k,'可见1.80',24)
 s.rect(x+(size-.68*k)/2,y-1.92*k,.68*k,1.92*k,'none','#BB815E',2)
def projected(s,side,ox,oy,k=17,labels=True):
 # Exact visible union facade; painter depth handles inset portions, fronts and returns.
 axis='X' if side in ('S','N') else 'Y'
 n=-1 if side in ('S','W') else 1
 objs=[]
 for o in G['primitives']:
  if not o['group'].startswith(('EXTERIOR','ROOF')):continue
  if o['type']=='box':
   a,b,c,d,e,f=o['bounds'];v=[[a,b,c],[d,b,c],[d,e,c],[a,e,c],[a,b,f],[d,b,f],[d,e,f],[a,e,f]]
   faces=[[0,1,5,4]] if side=='S' else [[2,3,7,6]] if side=='N' else [[3,0,4,7]] if side=='W' else [[1,2,6,5]]
  else:v=o['vertices'];faces=o['faces']
  for face in faces:
   pts=[v[i] for i in face];depth=sum(p[1 if axis=='X' else 0] for p in pts)/len(pts)
   xy=[(ox+(p[0] if axis=='X' else p[1])*k,oy-p[2]*k) for p in pts]
   objs.append((depth,xy,G['materials'][o['material']]))
 for depth,pts,col in sorted(objs,key=lambda q:q[0],reverse=n<0):s.poly(pts,col,col,1)
 width=150 if axis=='X' else 28
 s.line(ox,oy,ox+width*k,oy,'#4D6766',3)
 if labels:
  for z in [0,4,8,12]:
   s.line(ox,oy-z*k,ox+width*k,oy-z*k,'#748682',1,'12 8')
  s.text(ox,oy+45,f'{side}立面 · 看'+{'S':'北','N':'南','W':'东','E':'西'}[side]+' · FL0/4/8',24)
  dim(s,ox,oy+85,ox+width*k,oy+85,f'{width}m控制')
def roof_plan(s,ox,oy,k=18):
 for o in G['primitives']:
  if o['group']!='ROOF':continue
  if o['type']=='box':
   a,b,c,d,e,f=o['bounds'];s.rect(ox+a*k,oy-e*k,(d-a)*k,(e-b)*k,G['materials'][o['material']],sw=1)
  else:
   for face in o['faces']:s.poly([(ox+o['vertices'][i][0]*k,oy-o['vertices'][i][1]*k) for i in face],G['materials'][o['material']],sw=1)
 for x1,x2 in [(0,52),(106,150)]:
  s.line(ox+x1*k,oy-13*k,ox+x2*k,oy-13*k,'#E7E3D7',3)
  s.text(ox+(x1+x2)/2*k,oy-16*k,'5° ↓ 南北排水',24,anchor='middle')
 a,b,c,d=G['terrace'];s.rect(ox+a*k,oy-d*k,(c-a)*k,(d-b)*k,'#DCE5D4')
 s.text(ox+69*k,oy-3*k,'60㎡',23,anchor='middle')
 a,b,c,d=G['rt01']['rect'];s.rect(ox+a*k,oy-d*k,(c-a)*k,(d-b)*k,'none','#B46C59',4)
 s.text(ox+52*k,oy-25*k,'原RT01 588㎡ · 原位叠层',25,anchor='middle')
 route=[[34,8.8],[34,10.9],[49,10.9],[49,14]]
 for p,q in zip(route,route[1:]):s.line(ox+p[0]*k,oy-p[1]*k,ox+q[0]*k,oy-q[1]*k,'#DAA176',3,'10 8')
 s.text(ox+30*k,oy-7*k,'S1延伸上屋面待审',22)
 dim(s,ox,oy+45,ox+150*k,oy+45,'150m')
def section(s,kind,ox,oy,k=80):
 # Cut same model along X=80 court, X=25 entrance, or X=32.7 first flight.
 xx={'COURT':80,'ENTRY':25,'STAIR':32.7}[kind]
 for o in G['primitives']:
  if o['type']!='box':continue
  a,b,c,d,e,f=o['bounds']
  if a<=xx<=d and o['group'].startswith(('SLAB','INTERIOR','STAIR','EXTERIOR','ROOF')):
   if kind in ('ENTRY','STAIR'):
    b=max(b,0);e=min(e,9.2)
    if e<=b:continue
   s.rect(ox+b*k,oy-f*k,(e-b)*k,(f-c)*k,G['materials'][o['material']],sw=.6)
 # slopes on roof shown exact in section
 for o in G['primitives']:
  if o['type']!='mesh' or not o['group'].startswith('ROOF'):continue
  for face in o['faces']:
   pts=[o['vertices'][i] for i in face];ints=[]
   for p,q in zip(pts,pts[1:]+pts[:1]):
    if (p[0]-xx)*(q[0]-xx)<0:
     t=(xx-p[0])/(q[0]-p[0]);ints.append([p[j]+t*(q[j]-p[j]) for j in range(3)])
   if len(ints)==2:
    p,q=sorted(ints,key=lambda p:p[1])
    if kind in ('ENTRY','STAIR'):
     if p[1]>=9.2 or q[1]<=0:continue
     for idx,v in enumerate([p,q]):
      target=max(0,min(9.2,v[1]));t=(target-p[1])/(q[1]-p[1]) if q[1]!=p[1] else 0
      if target!=v[1]:ints[idx]=[xx,target,p[2]+t*(q[2]-p[2])]
     p,q=ints
    s.line(ox+p[1]*k,oy-p[2]*k,ox+q[1]*k,oy-q[2]*k,'#536B6D',6)
 s.text(ox,oy+65,{'COURT':'A—A x80：108㎡庭，F02/F03同孔','ENTRY':'C—C x25：原门点不退，短檐向内2m','STAIR':'B—B x32.7：S1第一跑，24级/层'}[kind],26)
 for z in [0,4,8,12]:
  s.text(ox-20,oy-z*k,f'+{z:.0f}',22,anchor='end')
 if kind=='STAIR':
  for z in [2,6]:s.text(ox+.95*k,oy-z*k-12,f'半层＋{z}',23)
def make_sheets():
 s=Sheet('C01 · 整栋外观与偏西主入口','P01 / 已接受150×28控制，52—12—30—12—44，三层 / 整栋共享几何深化')
 s.image('Preview_A.png',80,220,3040,940)
 s.text(100,1195,'A 西南→东北 · 30° · 共享参考简模 / 自然日光，非游戏截图',27)
 s.image('Preview_ENTRY.png',70,1240,1120,840)
 s.note(1210,1280,['主入口仍在(25,0)，暖木门框＋空白校名带',
  '门净3×3.2；短檐覆盖门内2m，檐顶3.60',
  '无新增核心南门。首层核心南面是管理/维护。',
  '教学翼：米白实体窗墙，3窗/75.6㎡教室。',
  '连接：12m短段局部高玻璃、深窗座。',
  '交流核心：采光庭与框架窗，保北门原位。',
  '檐沟青灰、排水管靠端柱；不以纹理画阴影。'],28,53)
 # site relation small fixed origin diagram
 s.text(1210,1740,'到达关系 / 原坐标保持',29)
 plan(s,1,1240,2250,11.8,False,False)
 s.line(1240,2250+20,1240+25*11.8,2250+20,'#A27754',4)
 s.text(1240,1855,'校门(0,−51)→偏西入口；北门→C03，东门→C08 / FIELD另走北路',24)
 s.save('P01')
 s=Sheet('C01 · 三层完整平面与使用边界','P02 / 房间净界与24班继承PLAN_01；家具、窗位与洞口来自REFERENCE_01同JSON')
 for f,oy in [(1,830),(2,1470),(3,2110)]:
  s.text(90,oy-535,f'F0{f} · FL{(f-1)*4} / 工程Z{8+(f-1)*4}',31)
  plan(s,f,120,oy,19)
  s.text(120,oy+100,['来访→主厅接待→职员/管理受控；学生鞋柜→S1/S2/S3；维护东口授权，部分共廊',
   '玩家F2_W4：30主方案；其余班基础壳体。课堂业务XY45/19.5保留，Z从旧8转候选12',
   '8班＋60㎡授权露台；门在(69,6)，无替代RT01；通高庭及梯洞与下层顶面相同'][f-1],25)
 s.save('P02')
 s=Sheet('C01 · 玩家班与鞋柜实排','P02A / 同一75.6㎡：30席主方案 vs 36席 / 柜列实际900名义格，不等于运营容量通过')
 class_plan(s,30,120,300,95);class_plan(s,36,1120,300,95)
 s.note(2120,300,['课堂共同固定：','净8.4×9 / 西面黑板4×1.25',
 '门1.6×2.6，南门x45 / 滑门',
 '北窗3组，每组约2.22×2.1',
 '30席5列×6排，列道1.05m',
 '36席6列×6排，列道0.79m',
 '36可见宽1.04m超出列道0.25',
 '0.68胶囊并不代表人物视觉通过',
 '靠窗/靠廊边道0.525–0.775m',
 '桌椅后拉、相向拥挤留给试作'],27,51)
 # Shoe detailed layouts two panels
 s.text(100,1550,'主鞋柜96.90㎡ · 600格',30)
 s.text(1250,1550,'西连接补充99.18㎡ · 300格',30)
 for room,ox in [('F1_WL',120),('F1_LW',1250)]:
  r=next(r for r in G['rooms'] if r['id']==room);a,b,c,d=r['rect'];k=62
  s.rect(ox,1600,(c-a)*k,(d-b)*k,'#F8F6EF',sw=3)
  for bank in [v for v in G['lockers'] if v['room']==room]:
   q=bank['bounds'];s.rect(ox+(q[0]-a)*k,1600+(d-q[4])*k,(q[3]-q[0])*k,.7*k,'#A98B61')
   s.text(ox+(q[0]-a)*k,1600+(d-q[4])*k-10,bank['id']+f' {bank["columns"]}×5×2',20)
  if room=='F1_WL':
   s.rect(ox+(23.5-a)*k,1600,3*k,(d-b)*k,'none','#64A59B',3)
   s.text(ox+(25-a)*k,1900,'3.0m主线',23,anchor='middle')
 s.note(2150,1590,['8座双面柜 / .30列距×.30行距',
  '主：3×(12＋8)×5×2＝600',
  '补：2×15×5×2＝300',
  '柜高1.5 / 总深0.70',
  '主柜列间净1.90 / 补充2.30',
  '靠东柜端0.40不是通道',
  '排队在柜列两侧，不占中间3m',
  '换鞋凳/等候边退出门口主线',
  '门厅到廊口原1.4m是瓶颈',
  '900格仅名义格数，运作待核'],25,45)
 s.save('P02A')
 s=Sheet('C01 · 公共空间、典型楼梯与原人物','P02B / 实排、朝向、净通路；使用方式与有限人物试作分开')
 # enlarged furniture plan crops
 for room,ox,oy,k in [('F2_WO',110,760,68),('F2_LW',1160,880,70),('F1_AT',2160,870,67)]:
  r=next(r for r in G['rooms'] if r['id']==room);a,b,c,d=r['rect']
  s.text(ox,250,r['name']+' '+room,29);s.rect(ox,300,(c-a)*k,(d-b)*k,'#F8F6EF',sw=3)
  for it in [v for v in G['furniture'] if v['room']==room]:
   q=it['bounds'];x=ox+(q[0]-a)*k;y=300+(d-q[4])*k
   s.rect(x,y,(q[3]-q[0])*k,(q[4]-q[1])*k,'#AD906B',sw=2)
   s.text(x+8,y-8,it['id'],19)
  s.text(ox,950,{'F2_WO':'课间折返：边凳向北，桌旁可停 / 主廊在北','F2_LW':'午休窗座向南，L凳围合 / 通廊不绕家具',
               'F1_AT':'对坐边凳与小桌，中央x77–83净6m'}[room],23)
 s.text(100,1060,'S1典型U梯 / S2、S3同构 · 洞口4.7×5.5，2.2净跑＋0.3间隔＋2.2净跑',30)
 k=135;ox=160;oy=1960
 a,b,c,d=G['stairs'][0]['opening'];s.rect(ox,oy-5.5*k,4.7*k,5.5*k,'#ECE9DE',sw=4)
 s.rect(ox,oy-2.2*k,4.7*k,2.2*k,'#C4D5D0')
 for run in (0,1):
  for j in range(12):s.line(ox+run*2.5*k,oy-(2.2+j*.3)*k,ox+(run*2.5+2.2)*k,oy-(2.2+j*.3)*k)
 s.text(ox+1.1*k,oy-3.7*k,'↑12级',25,anchor='middle')
 s.text(ox+3.6*k,oy-3.7*k,'↓12级',25,anchor='middle')
 dim(s,ox,oy+50,ox+4.7*k,oy+50,'4.7m洞 / 平台2.2m深')
 s.note(880,1230,['层高4 / 24级，级高0.166667',
 '每跑12踢面、11踏步，踏面0.30',
 '中台FL2/6，上下层FL0/4/8',
 '楼板孔与下层顶面孔4.7×5.5同位',
 '扶手1.10，庭与露台护栏1.20候选',
 '平台出口到主廊不穿辅助房间',
 '墙/顶面隐藏，梯核保留独立',
 '防灾、结构、头顶和有限人物待验'],27,52)
 # scale furniture elevation, actual figure
 s.text(1890,1120,'认可人物与真实尺度 / 原字节内嵌',29)
 char(s,1900,1940,160)
 s.rect(2380,1940-2.6*160,1.6*160,2.6*160,'none','#758B86',4)
 s.text(2370,1490,'门1.6×2.6',26)
 s.rect(2800,1940-.72*160,.65*160,.05*160,'#AC875A')
 s.line(2800,1940,2800,1940-.72*160);s.text(2740,2010,'桌H0.72 / 椅座0.43',25)
 s.rect(2940,1940-.43*160,72,6,'#B39365',sw=1)
 for x in [2945,3007]:s.line(x,1940,x,1940-.43*160,'#53686B',3)
 s.line(3007,1940-.43*160,3007,1940-.84*160,'#B39365',6)
 s.line(2670,1940-1.2*160,2740,1940-1.2*160,'#768A89',6)
 for x in [2670,2705,2740]:s.line(x,1940,x,1940-1.2*160,'#768A89',3)
 s.text(2640,1705,'栏杆1.20',23)
 s.note(1890,2100,['可见1.80×约1.04m；胶囊1.92×0.68m',
 '1.6门口静态宽余量：可见0.560 / 胶囊0.920',
 '原图128²、可见116px；环境贴图不统一128²'],25,42)
 s.save('P02B')
 s=Sheet('C01 · 入口集合、北门与受控露台','P02C / 补足P1/P5/P6实际围合；授权边界与门口净界，候选尺寸不代表消防/运营验证')
 def crop(room,ox,oy,k):
  r=next(v for v in G['rooms'] if v['id']==room);a,b,c,d=r['rect']
  s.rect(ox,oy,(c-a)*k,(d-b)*k,'#FAF8F0',sw=3)
  for it in G['furniture']+([dict(v,kind='locker') for v in G['lockers']] if room=='F1_WL' else []):
   if it['room']!=room:continue
   q=it['bounds'];x=ox+(q[0]-a)*k;y=oy+(d-q[4])*k
   s.rect(x,y,(q[3]-q[0])*k,(q[4]-q[1])*k,'#AF946F',sw=2)
  return a,b,c,d
 s.text(110,270,'P1 主入口 / 换鞋 / 等同伴',31);a,b,c,d=crop('F1_WL',110,320,80)
 s.rect(110+(23.5-a)*80,320,3*80,8.5*80,'none','#689C8E',4)
 s.text(110+(25-a)*80,735,'↑ 学生主线3m',27,anchor='middle')
 s.text(110,1080,'主门净3.0，厅北门1.4；侧柜列排队，两侧换鞋凳 / 历届照片在东凹廊',25)
 s.note(110,1140,['来访在接待确认后进职员区，不穿班级作为捷径。',
  '学生先换鞋、沿x25进入主廊；门厅1.4m廊口为集散瓶颈，',
  '保原位置，本轮不扩大接口。集中上学队列、相向行走待试作。'],26,43)
 s.text(1210,270,'P5 原北门 / 图书往返等候边',31);a,b,c,d=crop('F1_CN',1210,320,54)
 s.line(1210+(88.5-a)*54,320,1210+(91.5-a)*54,320,'#AC7352',8)
 s.rect(1210+(88.5-a)*54,320,3*54,14.7*54,'none','#689C8E',3)
 s.text(1210,1160,'3m门线x90，右边凳向西，公告在左，中央集合通路不布家具',24)
 s.text(1920,270,'P6 三层60㎡露台 / 原RT01独立',31)
 ox,oy,k=1930,340,100;s.rect(ox,oy,1000,600,'#E6E8DC',sw=4)
 for it in [it for it in G['furniture'] if it['room']=='TERRACE']:
  q=it['bounds'];s.rect(ox+(q[0]-64)*k,oy+(6-q[4])*k,(q[3]-q[0])*k,(q[4]-q[1])*k,'#AF946F')
 s.line(ox+420,oy,ox+580,oy,'#AC7352',8)
 s.text(ox+500,oy-25,'(69,6)门1.6×2.6 / 授权进入',25,anchor='middle')
 s.note(1930,1010,['完成面FL8＋0.03 / 护栏1.20候选',
  '门口保持2m以上缓冲，边凳向场内，折返可走中央。',
  '60㎡不冒充588㎡RT01；雨天/许可由既有规则另核。',
  '坡向南排水候选，滴水不落入口；节点与出口待验证。'],25,48)
 s.text(100,1400,'实际点位与三路：候选几何线仅供建模接口，旧地面层真实测时不直接套二层',30)
 plan(s,1,130,2080,19,False,True)
 for r in G['routes']:
  points=[p for p in r['points'] if 0<=p[0]<=150 and 0<=p[1]<=28]
  col={'DAILY_01':'#B27D4B','DAILY_02':'#578C85','DAILY_03':'#7A819D'}[r['id']]
  for p,q in zip(points,points[1:]):s.line(130+p[0]*19,2080-p[1]*19,130+q[0]*19,2080-q[1]*19,col,4)
 s.note(120,2200,['橙：主门→鞋柜→S1→F2玩家班；绿：S2下楼→北门图书；蓝：S3下楼→东口体育馆。',
  '维护从东口授权进入储藏，部分共廊并错时；职员/管理与学生授权区域按PLAN_01访问属性保留。'],25,43)
 s.save('P02C')
 s=Sheet('C01 · 四立面与门窗材料','P03 / 相同坐标、窗表与标高；南主门不复制到北背面，端面保持原东入口')
 projected(s,'S',140,650,18.8);projected(s,'N',140,1120,18.8)
 projected(s,'W',130,1660,28);projected(s,'E',1210,1660,28)
 s.note(2220,1410,['北教学面：每班3窗、窗台0.90',
 '南辅助面：卫生间高窗台1.60',
 '公共/连接：窗台0.45、窗高2.80',
 '常规窗高2.10，框宽0.075',
 '南遮阳深0.75；北/端0.35候选',
 '窗编号＝房间ID＋侧＋序号',
 '全量窗表见同JSON与OPENINGS.csv'],27,51)
 s.text(100,1840,'材料 / 克制像素表面建议（示意，与自然光预览、游戏效果分开）',30)
 for j,(mat,label) in enumerate([('WALL','M01 米白砂浆'),('ROOF','M02 青灰金属'),('FRAME','M03 哑光框'),('WOOD','M04 暖木鞋柜'),('GLASS','M05 低镜反玻璃')]):
  s.rect(120+j*600,1890,470,140,G['materials'][mat],sw=1);s.text(120+j*600,2070,label,27)
 s.note(120,2140,['建议32px/m远段 vs64px/m近入口：32较安静，64可表达少量拼缝/雨痕；暂推荐64近处，远段试32。',
  '无照片缩小纹理；基础色无固定阳光阴影。小样见P05；最终UV、通道配置、LOD/预算本轮不冻结。'],27,48)
 s.save('P03')
 s=Sheet('C01 · 统一屋顶、庭剖面与RT01冲突','P04 / 原588㎡RT01原位叠层；F03 60㎡露台独立 / 开孔、标高与屋面接口')
 roof_plan(s,130,820,19)
 s.note(130,960,['教学5°浅切妻：内墙檐12.30 / 脊13.0874；外挑0.60檐边12.2475。核心平屋面12.90 / 女儿墙13.00。',
 '采光庭低脊玻璃顶最高13.65；连接12.30。檐沟南北排水，竖管在教学端柱；实际管径/坡降/排水工法待验。',
 '露台完成面8.03：承载楼板FL8上30mm面层；历史Planning的8.25体块帽改为本次地面细化，门/高度接口须复核。'],26,45)
 section(s,'COURT',155,2120,73)
 s.note(2290,1260,['原RT01 28×21＝588㎡',
 '本次外廓下未承托的范围明确叠图',
 '支持投影462㎡ / 缺126㎡',
 'x38–52教学坡屋面不可直接站立',
 'x52–64连接屋面，结构/护栏未核',
 'x64–66跨核心与露台低位屋面',
 '原level12高程语义待核，不直接套屋面',
 '原梯核x41–49/y9–19与教室冲突',
 '方案A：保独立RT01待整体重设计',
 '接近：F03主廊→S1延伸→原49/14',
 '当前不搭可进入RT01、不移动区域'],26,52)
 s.text(155,2240,'通高庭12×9；F02/F03楼板孔、F01/F02顶面孔同位；F03顶面仍保持庭上无封板',24)
 s.save('P04')
 s=Sheet('C01 · 入口/楼梯剖面与拆分合同','P04A / 用同几何切面解释连接；共享简模只供参考，不冻结结构、碰撞或最终拓扑')
 section(s,'ENTRY',150,1370,75);section(s,'STAIR',1250,1370,85)
 char(s,150+4*75,1370,75);char(s,1250+6.5*85,1370,85)
 s.note(2200,310,['入口原门点(25,0) / Z0',
 '向内短檐2m / 屋顶3.60',
 '门内换鞋，无台阶追加',
 '门厅→主廊1.4m待拥挤检查',
 '上层公共厅有独立楼板/顶面',
 '梯孔与下层顶面开孔完全相同',
 '梯跑头顶不得被隐藏逻辑补板',
 '半层平台2.2深、扶手1.10',
 '采光庭边/露台护栏1.20候选'],26,50)
 s.text(120,1510,'共享原点SW(0,0,0) · worldXY(2190.909091,1969.181818) · 工程原点换算：localY＋51m / Z＋8m',28)
 s.note(130,1630,['ROOF：教学坡面/平屋面/采光顶/檐沟，可单独拆；山墙留在EXTERIOR，拆屋顶后室内不缺边。',
 'EXTERIOR：S/N/E/W、遮阳/雨棚/排水；外墙内外一套所有权，避免复制交叠。门窗ID对照CSV。',
 'SLAB_F01/F02/F03：0/4/8上表面、厚0.25；上两层扣108㎡庭＋三处4.7×5.5梯孔。',
 'INTERIOR_F01/F02/F03：墙、顶面、鞋柜、玩家班、公共家具、庭护栏、露台分别组织；净顶3.45。',
 'STAIR_CORE_S1/S2/S3：楼梯独立；楼层壳体隐藏时不带走梯跑/扶手/半层平台。',
 '遮挡合同：隐藏面向镜头的外墙＋本层对应分隔墙＋顶面，庭边护栏和楼梯核保持；不实现UE代码。',
 '导航落点：FL0/4/8出口y6.4–8.8，半层FL2/6；有限胶囊、上/下楼、门扇、镜头25°–40°待试作。',
 '真实柱网/结构、门消防、电梯、RT01、临时UV/人物碰撞、游戏交互半径/恢复落点/通勤均未验。'],27,67)
 s.save('P04A')
 s=Sheet('C01 · 真实相反两向与生活尺度','P05 / A西南→东北 / B东北→西南；同简模、同日光 / 单体设计预览，不是实际游戏效果')
 s.image('Preview_A.png',80,220,3040,890)
 s.image('Preview_B.png',80,1180,3040,890)
 s.text(100,1130,'A · 225°方位 / 30°俯角：偏西南主门、实体教学翼、局部连接与三层露台',26)
 s.text(100,2110,'B · 45°方位 / 30°俯角：北侧24班窗墙、采光庭与原北门；不是正门镜像',26)
 s.note(100,2180,['主线：偏西主门→900名义鞋格分区→S1→二层玩家班；北门→独立C03，东口→C08；FIELD保北路。',
 '基础色与像素密度仍示意：材色/实际太阳预览单列；字符不烘在墙上，校名留空。游戏/最终UV效果尚未验证。'],26,48)
 s.save('P05')
 s=Sheet('C01 · 玩家班、鞋柜与公共空间预览','P05A / 来自同JSON共享简模；剖透室内明确隐藏墙顶 / 原人物在P02B按原字节对照')
 for name,x,y,lab in [('Preview_CLASS.png',80,220,'F2_W4 30席 / 西面授课，北侧窗'),
                       ('Preview_SHOES.png',1650,220,'主鞋柜与原入口 / 3m中央线'),
                       ('Preview_COURT.png',80,1270,'108㎡庭 / 中央6m净线，双侧讨论'),
                       ('Preview_LINK.png',1650,1270,'西连接窗座 / L形围合，通廊独立')]:
  s.image(name,x,y,1460,880);s.text(x,y+940,lab,29)
 s.save('P05A')
 s=Sheet('C01 · 像素密度比较与近入口尺度','P05B / 表面示意单列；不以像素噪点替代结构，不把自然太阳影写入基础色')
 s.image('Preview_ENTRY.png',80,220,2020,1260)
 s.note(2160,300,['共享几何真实入口局部',
  '温暖木材/青灰金属/米白砂浆',
  '校名留空，标识在后期独立编辑',
  '本图程序材色示意，无最终UV',
  '不对照声称真实游戏镜头通过'],28,56)
 import random
 for j,density in enumerate([32,64]):
  ox=150+j*1430;oy=1600;size=480;pix=size/density
  rng=random.Random(71)
  s.text(ox,1550,f'{density}px/m · 1×1m表面 / 3色，稀疏接缝与雨痕',29)
  s.rect(ox,oy,size,size,'#DDD9CB',sw=1)
  # Sparse stepped water traces, constant lighting-free colors, no dense noise.
  for t in range(7):
   x=rng.randrange(2,density-3);start=rng.randrange(2,density//2);length=rng.randrange(2,density//3)
   for v in range(start,min(start+length,density)):
    s.rect(ox+x*pix,oy+v*pix,pix,pix,'#D2CFC2','#D2CFC2',0)
  for x in range(density):s.rect(ox+x*pix,oy+int(density*.7)*pix,pix,pix,'#C7C8BB','#C7C8BB',0)
  s.note(ox+540,1660,['同1m物理表面，固定低对比色。',
   '32：远翼更安静，纹理细节较少。',
   '64：近入口/鞋柜更可读。',
   '雨痕长度约0.05–0.25m候选。',
   '小样为设计示意，非最终纹理资产。'],26,50)
 s.note(150,2180,['建议近处64、远处试32；正式试作再核屏幕像素与镜头距离。不冻结整栋atlas尺寸、通道、LOD、面数或复杂碰撞。',
  '认可人物仍原128²，不要求建筑环境贴图128²；明暗与太阳投影只来自预览光照。'],26,48)
 s.save('P05B')
make_sheets()
# Machine-readable opening schedule, same source as all views.
import csv
with (OUT/'OPENINGS.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['id','room','side','axis','line','lo','hi','z0','z1','kind','normal','shade_depth','shade_mode'],lineterminator='\n')
 w.writeheader();w.writerows(G['openings'])
