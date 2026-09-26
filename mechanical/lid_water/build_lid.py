"""P08 replacement: rigid socket for 4 mm OD / 3 mm ID brass tube. mm."""
from pathlib import Path
import cadquery as cq
import numpy as np,json,math,struct
from render_support import render,stlmesh
P=Path(__file__).parent
TUBE_BORE=4.2
INSERT_BORE=4.0 # Assumes M3 heat-set insert about 4.5 OD x 4 long.
def cyl(r,h,z,x=0,y=0):return cq.Workplane('XY').workplane(offset=z).center(x,y).circle(r).extrude(h)
def radial(r,x,h,z=113):return cq.Workplane('YZ').workplane(offset=x).center(0,z).circle(r).extrude(h)
lid=cyl(43,3,101)
for a in [45,135,225,315]:
 x,y=47*math.cos(math.radians(a)),47*math.sin(math.radians(a))
 lid=lid.union(cyl(7,3,101,x,y)).cut(cyl(2.25,5,100,x,y))
# A tapered foot strengthens the collar without reducing the 26 mm central opening.
foot=cq.Workplane('XY').newObject([cq.Solid.makeCone(8,6,6,cq.Vector(22,0,104),cq.Vector(0,0,1))])
lid=lid.union(foot).union(cyl(6,10,110,22))
# Radial insert boss, with a printable inclined rib supporting its overhang.
lid=lid.union(radial(4,25,7))
rib=cq.Workplane('XZ').polyline([(25,104),(28,104),(32,109),(32,113),(25,113)]).close().extrude(2,both=True)
lid=lid.union(rib)
lid=lid.cut(cyl(13,30,100)) # preserve full center feed opening
# 18 mm engagement with a positive seating shoulder at z=102.
lid=lid.cut(cyl(TUBE_BORE/2,19,102,22)).cut(cyl(1.6,3,100,22))
lid=lid.cut(radial(1.6,23.7,8.5)).cut(radial(INSERT_BORE/2,27.5,4.6))
lead=cq.Solid.makeCone(INSERT_BORE/2,INSERT_BORE/2+.3,.3,cq.Vector(31.7,0,113),cq.Vector(1,0,0))
lid=lid.cut(lead)
assert lid.val().isValid() and len(lid.solids().vals())==1
pr=lid.translate((0,0,-101))
cq.exporters.export(pr,str(P/'P08_lid_brass_4mm.stl'),tolerance=.01,angularTolerance=.05)
cq.exporters.export(lid,str(P/'P08_lid_brass_4mm.step'))
v,f=stlmesh(P/'P08_lid_brass_4mm.stl');vv,ix=np.unique(np.round(v,5),axis=0,return_inverse=True);ff=ix.reshape(-1,3)
e=np.concatenate([ff[:,[0,1]],ff[:,[1,2]],ff[:,[2,0]]]);_,back,cnt=np.unique(np.sort(e,axis=1),axis=0,return_inverse=True,return_counts=True)
assert np.all(cnt==2) and np.all(np.bincount(back,weights=np.where(e[:,0]<e[:,1],1,-1))==0)
tr=v[f];volume=np.einsum('ij,ij->i',tr[:,0],np.cross(tr[:,1],tr[:,2])).sum()/6;assert volume>0
report={'valid_single_solid':True,'closed_oriented_stl':True,'triangles':len(f),'volume_mm3':float(volume),'lid_body_diameter_mm':86,'feed_opening_mm':26,'tube_socket_mm':TUBE_BORE,'tube_support_length_mm':18,'flow_passage_mm':3.2,'tube_bottom_above_lid_underside_mm':1,'overall_print_height_mm':19,'collision_check':'pending'}
# Original assembly references supplied via CLI; geometry above is standalone.
import sys
if len(sys.argv)>1:
 ref=Path(sys.argv[1]);collisions=[]
 tube=cyl(2,35,102,22).cut(cyl(1.5,37,101,22))
 # M3 x 8 cap screw: tip at tube outside x=24, head at x32..35.
 screw=radial(1.5,24,8).union(radial(2.75,32,3))
 for name in ['P04_catcher','P06_bowl']:
  sh=cq.importers.importStep(str(ref/(name+'.step')))
  for label,s in [('lid',lid),('brass',tube),('screw',screw)]:
   vol=s.intersect(sh).val().Volume()
   if vol>.005:collisions.append([label,name,vol])
 assert not collisions
 report['collision_check']={'intersections':collisions,'references':str(ref),'note':'Bowl exterior is rotationally symmetric; no inward projecting lid features.'}
for i,view in enumerate([(1.5,-1.5,1.6),(-1,1,1.4),(1,-1,-1.4),(1,0,0)]):render([(v,f,'#409aa5')],P/f'review_{i}.png',view,(950,750))
def obj(sh,color):
 vv,ff=sh.val().tessellate(.025,.06);return np.array([x.toTuple() for x in vv]),np.array(ff),color
section=lid.intersect(cq.Workplane('XY').box(150,100,180,centered=(True,False,False)))
tube=cyl(2,35,102,22).cut(cyl(1.5,37,101,22))
render([obj(section,'#409aa5'),obj(tube,'#c89538')],P/'section.png',(1,-2,1.3),(1000,800))
render([obj(lid,'#409aa5'),obj(tube,'#c89538')],P/'assembly.png',(1.5,-1.5,1.6),(1000,800))
(P/'checks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
