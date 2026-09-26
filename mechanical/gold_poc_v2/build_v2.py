import cadquery as cq, numpy as np, math,json
from pathlib import Path
P=Path(__file__).parent
INS=5.6
parts={}; printparts={}; colors={}
def cyl(r,h,z=0,x=0,y=0):return cq.Workplane('XY').workplane(offset=z).center(x,y).circle(r).extrude(h)
def ring(ro,ri,h,z):return cyl(ro,h,z).cut(cyl(ri,h+2,z-1))
def box(x,y,h,z=0):return cq.Workplane('XY').box(x,y,h,centered=(True,True,False)).translate((0,0,z))
def radial(r,n=4,phase=45):return [(r*math.cos(math.radians(phase+360*i/n)),r*math.sin(math.radians(phase+360*i/n))) for i in range(n)]
def holes(s,pts,d,z,h):
 for x,y in pts:s=s.cut(cyl(d/2,h,z,x,y))
 return s
posts=radial(36,4,0); mounts=radial(47)
# P01 - base: rounded feet, open motor bay, no broad support overhang
s=cyl(42,4)
for x,y in posts:s=s.union(cyl(4.5,42,4,x,y))
s=holes(s,posts,INS,39.5,7)
s=holes(s,radial(36,4,45),4.5,-1,6)
# two tie slots, available for cable strain relief
for x in [-8,8]:s=s.cut(box(3,7,6,-1).translate((x,30,0)))
parts['P01_base']=s
# P02 - motor deck with central closed support and underside pilot recess
s=cyl(42,4,46)
for x,y in mounts:s=s.union(cyl(7,10,40,x,y))
s=holes(s,mounts,INS,41.5,9)
s=holes(s,posts,4.5,45,6)
s=holes(s,[(x,y) for x in [-15.5,15.5] for y in [-15.5,15.5]],3.4,45,6)
s=s.cut(cyl(11.3,2.2,45.9)).cut(cyl(2.8,8,45))
s=s.union(ring(6.5,2.8,2,50))
parts['P02_motor_deck']=s
# P03 repeated standoffs atop deck, support catcher external dry tabs
parts['P03_spacer_x4']=ring(6,2.25,12,50)
# P04 - catcher. Sloped planar wet floor z=67+0.03*y. No floor fasteners.
s=cyl(42,39,62)
# cut cavity above sloping floor. Rotate bottom of cutting box about X.
slope=math.degrees(math.atan(.03))
above=box(120,120,110,0).rotate((0,0,0),(1,0,0),slope).translate((0,0,67))
cavity=cyl(39,90,45).intersect(above)
s=s.cut(cavity).cut(cyl(18.7,100,30))
s=s.union(ring(21.7,18.7,11,62))
# drain centerline exactly follows floor slope; flat-bottomed D-bore prevents a sill
outer=cq.Workplane('XZ').circle(9).extrude(26).rotate((0,0,0),(1,0,0),slope).translate((0,-35,70.95))
# floor at y=-35 is65.95; D-bore lower edge center-5=65.95
s=s.union(outer)
prof=cq.Workplane('XZ').moveTo(4,-5).lineTo(-4,-5).lineTo(-4,-3).threePointArc((-5,0),(0,5)).threePointArc((5,0),(4,-3)).close()
drain=prof.extrude(30).rotate((0,0,0),(1,0,0),slope).translate((0,-34,70.98))
s=s.cut(drain)
for x,y in mounts:
 s=s.union(cyl(7,5,62,x,y))
 s=s.cut(cyl(2.25,7,61,x,y))
 s=s.union(cyl(7,8,93,x,y))
 s=s.cut(cyl(INS/2,6.6,94.5,x,y))
parts['P04_catcher']=s
# P05 - small directly driven hub with opposed shaft screws and 3 balanced bowl bolts
s=ring(5,2.55,2,56).union(ring(11,2.55,8,58)).union(ring(18,2.55,4,62))
rotorbolt=radial(14.5,3,90)
s=holes(s,rotorbolt,4.5,61,6)
for a in [0,180]:
 full=cq.Workplane('YZ').workplane(offset=2).center(0,61).circle(2.25).extrude(10)
 ins=cq.Workplane('YZ').workplane(offset=5).center(0,61).circle(INS/2).extrude(8)
 s=s.cut(full.rotate((0,0,0),(0,0,1),a)).cut(ins.rotate((0,0,0),(0,0,1),a))
parts['P05_drive_hub']=s
# P06 - sealed bowl, smooth filleted sump entry, no wet screw bosses or raised collar
w=cq.Workplane('XZ').moveTo(0,66).lineTo(18,66).lineTo(18,74).lineTo(13,74).lineTo(13,82).lineTo(32,90.5).lineTo(32,97).lineTo(30,97).lineTo(30,95.4).threePointArc((29.8,94.5),(29,94)).lineTo(10,87).threePointArc((8.5,86),(8,84.5)).lineTo(8,77).threePointArc((7.7,76.3),(7,76)).lineTo(0,76).close()
s=w.revolve(360,(0,0),(0,1))
s=s.union(ring(26,23,7,70)).union(ring(26,12,3,74))
s=holes(s,rotorbolt,INS,65.9,6.6)
# dry shaft relief accommodates protrusion up to26mm above motor face, 3mm minimum to wet floor
s=s.cut(cyl(3,7,65.9))
parts['P06_bowl']=s
# P07 optional gravity-seated recessed cone: no protruding lip above bowl inlet
s=cq.Workplane('XZ').polyline([(7.9,84.2),(5,82.5),(5,81),(7.9,82.7)]).close().revolve(360,(0,0),(0,1))
for x,y in radial(5.9,3,0):s=s.union(cyl(.8,7,76,x,y))
limit=cq.Workplane('XZ').polyline([(0,75),(8,75),(8,84.2),(5,82.5),(0,82.5)]).close().revolve(360,(0,0),(0,1))
s=s.intersect(limit)
parts['P07_optional_trap_insert']=s
# P08 - cover with two water ports over working slope and 26mm central feed opening
s=ring(43,13,3,101)
for x,y in mounts:s=s.union(cyl(7,3,101,x,y))
s=holes(s,mounts,4.5,100,5)
s=holes(s,[(22,0),(-22,0)],4.3,100,5)
parts['P08_lid']=s
# P09 fit coupon with labelled diameters in guide; shaft fit and insert holes
s=box(62,18,9)
try:s=s.edges('|Z').fillet(2)
except:pass
for x,d in zip([-24,-12,0,12,24],[5.2,5.4,5.6,5.8,6.0]):s=s.cut(cyl(d/2,6.6,2.5,x,0))
parts['P09_insert_coupon']=s
colors={'P01_base':'#587184','P02_motor_deck':'#6c899b','P03_spacer_x4':'#9dafbb','P04_catcher':'#2394a0','P05_drive_hub':'#5f707b','P06_bowl':'#e1a329','P07_optional_trap_insert':'#b67a1b','P08_lid':'#66bdc1','P09_insert_coupon':'#9caeb9'}
report={}
for n,s in parts.items():
 assert s.val().isValid(),n
 assert len(s.solids().vals())==1,(n,len(s.solids().vals()))
 # flip these onto largest plane for export: deck, hub, insert. All delivered STLs print-oriented.
 pr=s
 if n in ['P02_motor_deck','P05_drive_hub','P07_optional_trap_insert']:pr=pr.rotate((0,0,0),(1,0,0),180)
 bb=pr.val().BoundingBox();pr=pr.translate((0,0,-bb.zmin));printparts[n]=pr
 cq.exporters.export(pr,str(P/'STL'/(n+'.stl')),tolerance=.015,angularTolerance=.06)
 cq.exporters.export(s,str(P/'STEP'/(n+'.step')))
 bb=s.val().BoundingBox()
 report[n]={'valid_solid':True,'dimensions_mm':[round(bb.xlen,3),round(bb.ylen,3),round(bb.zlen,3)],'volume_mm3':round(s.val().Volume(),3)}
 print(n,report[n],flush=True)
# assembled solids and specified hardware
assembled={n:s for n,s in parts.items() if n not in ['P03_spacer_x4','P09_insert_coupon','P07_optional_trap_insert']}
for i,(x,y) in enumerate(mounts):assembled['spacer'+str(i)]=parts['P03_spacer_x4'].translate((x,y,0))
hardware={}
hardware['motor']=box(42,42,40,6).union(cyl(11,2,46)).union(cyl(2.5,24,46))
hardware['thrust_lower']=ring(5,2.6,1.2,52)
hardware['thrust_cage']=ring(4.8,2.7,1.6,53.2)
hardware['thrust_upper']=ring(4.9,2.5,1.2,54.8)
# rounded motor body is not needed for clearance: conservative square envelope used
for n,s in hardware.items():cq.exporters.export(s,str(P/'STEP'/('H_'+n+'.step')))
assy=cq.Assembly()
for n,s in {**assembled,**hardware}.items():assy.add(s,name=n,color=cq.Color(colors.get(n,'#a5adb4')))
assy.save(str(P/'assembly.step'))
inter=[]
items=list(assembled.items())+list(hardware.items())
for i,(n,a) in enumerate(items):
 for m,b in items[i+1:]:
  v=a.intersect(b).val().Volume()
  if v>.005:inter.append([n,m,round(v,4)])
report['interferences']=inter
# Verify rotational envelope by rotating full rotor through discrete angles; axisymmetric bowl except blind holes
rotor=parts['P05_drive_hub'].union(parts['P06_bowl'])
rot_inter=[]
for angle in range(0,360,15):
 rr=rotor.rotate((0,0,0),(0,0,1),angle)
 for n in ['P04_catcher','P08_lid','P02_motor_deck']:
  v=rr.intersect(parts[n]).val().Volume()
  if v>.005:rot_inter.append([angle,n,v])
report['rotation_interferences']=rot_inter
(P/'geometry_checks.json').write_text(json.dumps(report,indent=2))
print('INTERFERENCES',inter,rot_inter,flush=True)
# Save tessellations, assembly coordinates, for deterministic software rendering
payload={}
for group,objects in [('parts',parts),('hardware',hardware),('print',printparts)]:
 for n,s in objects.items():
  v,f=s.val().tessellate(.05,.10)
  payload[group+'__'+n]={'v':[q.toTuple() for q in v],'f':f}
(P/'assets'/'meshes.json').write_text(json.dumps(payload))
