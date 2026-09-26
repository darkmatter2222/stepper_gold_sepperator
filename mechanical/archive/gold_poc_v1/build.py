import cadquery as cq, math, json
from pathlib import Path
P=Path(__file__).parent
INS=5.6 # trial bore for M4 heat-set inserts, must coupon-test
parts={}
def cyl(r,h,z=0,x=0,y=0): return cq.Workplane('XY').workplane(offset=z).center(x,y).circle(r).extrude(h)
def box(x,y,h,z=0): return cq.Workplane('XY').box(x,y,h,centered=(True,True,False)).translate((0,0,z))
def holes(s,xy,d,z,h):
 for x,y in xy:s=s.cut(cyl(d/2,h,z,x,y))
 return s
def ring(ro,ri,h,z):return cyl(ro,h,z).cut(cyl(ri,h+2,z-1))
def rev(points):return cq.Workplane('XZ').polyline(points).close().revolve(360,(0,0),(0,1))
def radial(r,n=4,phase=45):return [(r*math.cos(math.radians(phase+i*360/n)),r*math.sin(math.radians(phase+i*360/n))) for i in range(n)]
frame_xy=[(-43,-43),(-43,43),(43,-43),(43,43)]
# Base and open motor bridge. Standard NEMA17 mounting is M3, not M4.
s=box(116,116,6)
for x,y in frame_xy:s=s.union(box(14,14,48,6).translate((x,y,0)))
s=s.union(box(100,100,6,54));s=s.cut(cyl(11.3,8,53))
s=holes(s,[(x,y) for x in [-15.5,15.5] for y in [-15.5,15.5]],3.4,53,8)
s=holes(s,frame_xy,INS,47.5,13)
# open bridge sides are wire egress; mount holes in base
s=holes(s,[(-50,0),(50,0),(0,-50),(0,50)],4.5,-1,8)
parts['01_motor_base']=s
# Bearing support with four legs bolted from underside into blind inserts
s=box(100,100,8,92).cut(cyl(7,10,91))
for x,y in frame_xy:
 leg=box(14,14,32,60).translate((x,y,0));leg=leg.cut(cyl(2.25,35,59,x,y));s=s.union(leg)
 # screw counterbore in top deck for M4x50 to reach base inserts
 s=s.cut(cyl(4.1,6,95,x,y))
s=s.union(cyl(18,27,100)).cut(cyl(6,42,91))
# top installed bearing lower pocket needs pass through upper bore; intermediate relief radius 11.2
s=s.cut(cyl(11.1,32,100))
# lower 608 seat 100..107; upper120..127; top relief127..131
s=s.cut(cyl(11.1,8,120))
# catcher mounts on stand posts
for x,y in radial(58):
 s=s.union(cyl(6,31,100,x,y));s=s.cut(cyl(INS/2,8,123,x,y))
s=holes(s,radial(15,3,0),INS,119,12)
parts['02_bearing_stand']=s
parts['09_bearing_spacer']=ring(6,4.3,13,107)
parts['10_bearing_retainer']=holes(ring(18,9,3,127),radial(15,3,0),4.5,126,5)
# Splash catcher seamless, floor136..140; center dry chimney r34, rim150
s=ring(83,30.8,4,136).union(ring(83,79,60,140)).union(ring(34,30.8,10,140))
# drain spout in Y direction, 12mm bore, OD18. at z147 points outward
sp=cq.Workplane('XZ').center(0,147).circle(9).extrude(26).translate((0,-76,0))
# XZ normal -y extrusion => from -76 to-102
s=s.union(sp)
cut=cq.Workplane('XZ').center(0,147).circle(6).extrude(30).translate((0,-75,0));s=s.cut(cut)
# mounts OUTSIDE wet floor, dry lugs at r90
for x,y in radial(58):
 # post coords r58 lie under floor => no penetration: underside blind inserts not needed; screw through upper floor would leak
 pass
# use 4 mounting bores through floor, raised sealed dry wells to above operating level; separated from rotor r64
# instead external tabs, separate riser brackets from stand
for x,y in radial(89):
 s=s.union(cyl(7,5,136,x,y));s=s.union(box(16,16,5,136).translate((x*.94,y*.94,0)))
 s=s.cut(cyl(2.25,7,135,x,y))
for x,y in radial(89):
 s=s.union(cyl(7,8,192,x,y)).union(box(16,16,8,192).translate((x*.94,y*.94,0)))
 s=s.cut(cyl(INS/2,6.5,193.5,x,y))
parts['03_splash_catcher']=s
lid=ring(85,28,3,200)
for x,y in radial(89):
 lid=lid.union(cyl(7,3,200,x,y)).union(box(16,16,3,200).translate((x*.94,y*.94,0)))
lid=holes(lid,radial(89),4.5,199,5)
lid=holes(lid,[(40,0),(-40,0)],6.3,199,5)
parts['11_splash_lid']=lid
# individual radial brackets stand at r58 to catcher r89, horizontal strap z131..136
s=box(43,14,5,131).translate((73.5,0,0));s=s.cut(cyl(2.25,7,130,58,0))
# catcher M4x8 screws enter shallow insert 3mm length; use through nut instead better hex captive nut
s=s.cut(cq.Workplane('XY').workplane(offset=131).center(89,0).polygon(6,8.3).extrude(3.4));s=s.cut(cyl(2.25,7,130,89,0))
parts['04_catcher_bracket_print4']=s
# sealed bowl, flat flange and overhanging dry labyrinth skirt
s=rev([(0,147),(30,147),(30,151),(18,151),(18,171),(22,171),(64,187),(64,195),(60,195),(60,191),(18,175),(14,175),(14,155),(0,155)])
# thicker underside flange for blind heat inserts:143..151
s=s.union(cyl(30,8,143)).union(ring(38,35.5,8,145)).union(ring(38,18,4,151))
s=holes(s,radial(23),INS,142.9,6.1)
# top collar fastening bosses r21 3 symmetric, blind inserts, entirely within solid
for x,y in radial(21,3,0):
 s=s.union(cyl(5,12,168,x,y));s=s.cut(cyl(INS/2,9.5,170.5,x,y))
parts['05_sealed_bowl']=s
# removable collar 16mm throat over 28mm wide sump. slope sheds particles toward hole
s=rev([(8,176),(17.7,175.3),(17.7,177),(8,180)])
for x,y in radial(21,3,0):
 s=s.union(cyl(5,3,180,x,y)).union(box(12,8,3,180).translate((17,0,0)).rotate((0,0,0),(0,0,1),math.degrees(math.atan2(y,x)))) if False else s
# spokes radially laid, plate180..183 connects collar at top edge via overlap add rim
s=s.union(ring(18,8,3,177))
for a in [0,120,240]:
 tab=box(13,9,3,180).translate((19,0,0)).rotate((0,0,0),(0,0,1),a)
 s=s.union(tab)
s=holes(s,radial(21,3,0),4.5,176,8)
# bosses need contact bottom collar177; trim bowl bosses180 to177 in bowl
b=parts['05_sealed_bowl']
# collar bosses remain at z180
parts['05_sealed_bowl']=b
parts['06_trap_collar']=s.cut(parts['05_sealed_bowl'])
# hub shaft8.1, four flange bolts and opposed grub inserts, lower nose contacts inner bearing ring
s=ring(6,4.05,4,127).union(ring(13,4.05,8,131)).union(ring(30,4.05,4,139))
s=holes(s,radial(23),4.5,138,6)
for a in [0,180]:
 cutter=cq.Workplane('YZ').workplane(offset=6).center(0,135).circle(INS/2).extrude(8).rotate((0,0,0),(0,0,1),a)
 screw=cq.Workplane('YZ').workplane(offset=3).center(0,135).circle(2.25).extrude(12).rotate((0,0,0),(0,0,1),a)
 s=s.cut(cutter).cut(screw)
parts['07_drive_hub']=s
# bearing top cap around journal, stops outer race upward,3 screws need boss attachment omitted snug seats retained hub weight; cap not needed
# coupons
s=box(65,24,10)
for i,d in enumerate([5.2,5.4,5.6,5.8,6.0]):s=s.cut(cyl(d/2,7,3,-24+i*12,0))
parts['08_insert_coupon']=s
report={}
for name,s in parts.items():
 assert s.val().isValid(),name
 assert len(s.solids().vals())==1,(name,len(s.solids().vals()))
 bb=s.val().BoundingBox(); pr=s.translate((0,0,-bb.zmin))
 cq.exporters.export(pr,str(P/(name+'.stl')),tolerance=.035,angularTolerance=.12)
 cq.exporters.export(s,str(P/(name+'.step')))
 report[name]={'valid':True,'solids':len(s.solids().vals()),'bbox_mm':[round(bb.xlen,2),round(bb.ylen,2),round(bb.zlen,2)],'volume_mm3':round(s.val().Volume(),1)}
 print(name,report[name],flush=True)
(P/'geometry_checks.json').write_text(json.dumps(report,indent=2))
# assembly with 4 brackets in place
assy=cq.Assembly()
for name,s in parts.items():
 if name.startswith('08'):continue
 if name.startswith('04'):
  for a in [45,135,225,315]:assy.add(s.rotate((0,0,0),(0,0,1),a),name='bracket'+str(a))
 else:assy.add(s,name=name)
assy.save(str(P/'assembly.step'))
# quantify rigid-body interference between assembly parts
checks=[]
items=[(n,o) for n,o in parts.items() if not n.startswith(('04','08'))]
items += [('bracket'+str(a),parts['04_catcher_bracket_print4'].rotate((0,0,0),(0,0,1),a)) for a in [45,135,225,315]]
for i,(n,a) in enumerate(items):
 for m,b in items[i+1:]:
  v=a.intersect(b).val().Volume()
  if v>0.01: checks.append([n,m,round(v,3)])
(P/'interference_checks.json').write_text(json.dumps(checks,indent=2))
print('INTERFERENCES',checks,flush=True)
# render CAD meshes, half cut section and overview
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
fig=plt.figure(figsize=(14,8),facecolor='#f5f7fa')
for j,section in enumerate([False,True]):
 ax=fig.add_subplot(1,2,j+1,projection='3d');ax.set_facecolor('#f5f7fa')
 for idx,(name,s) in enumerate(parts.items()):
  if name.startswith(('04','08')):continue
  if section:s=s.intersect(box(250,125,230).translate((0,62.5,0)))
  vs,fs=s.val().tessellate(.2);v=np.array([x.toTuple() for x in vs]);f=np.array(fs)
  if len(f):ax.add_collection3d(Poly3DCollection(v[f],facecolor=['#65758a','#859ab2','#60b4bf','#999','#e6b44e','#e8d8aa','#526375'][idx%7],edgecolor='none',alpha=1))
 ax.set(xlim=(-100,100),ylim=(-105,95),zlim=(0,210));ax.set_box_aspect((1,1,1.05));ax.view_init(25,-90);ax.set_axis_off();ax.set_title('Assembled prototype' if not section else 'Section: central sump and dry drive',fontsize=14)
fig.suptitle('CENTRAL-TRAP GOLD CONCENTRATOR | POC v1\n128 mm bowl • experimental low-speed oscillation',fontsize=18)
plt.tight_layout();plt.savefig(P/'preview.png',dpi=160)
