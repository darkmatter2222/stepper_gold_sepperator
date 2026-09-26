"""Drop-in P05 revision for the 64 mm Central Trap v2. All dimensions mm."""
from pathlib import Path
import cadquery as cq
import math,json,numpy as np,sys
P=Path(__file__).parent
INSERT_BORE=4.0 # starting bore for approximately 4.5 OD x 4 long M3 heat-set insert
INSERT_DEPTH=4.5
SCREW_Z=60.0
def cyl(r,h,z):return cq.Workplane('XY').workplane(offset=z).circle(r).extrude(h)
def ring(ro,ri,h,z):return cyl(ro,h,z).cut(cyl(ri,h+2,z-1))
def radial_cyl(r,x,length,z=SCREW_Z):return cq.Workplane('YZ').workplane(offset=x).center(0,z).circle(r).extrude(length)
# Preserve 36 mm flange, 5.1 mm shaft bore, 10 mm stack and bearing nose.
hub=ring(5,2.55,2,56).union(ring(11,2.55,8,58)).union(ring(18,2.55,4,62))
# Solid round boss, flat external insertion face, material fully surrounding the insert.
hub=hub.union(radial_cyl(4,4.5,6.5))
for a in [90,210,330]:
 x,y=14.5*math.cos(math.radians(a)),14.5*math.sin(math.radians(a))
 hub=hub.cut(cyl(2.25,6,61).translate((x,y,0)))
hub=hub.cut(radial_cyl(1.6,1.8,9.4))
hub=hub.cut(radial_cyl(INSERT_BORE/2,11-INSERT_DEPTH,INSERT_DEPTH+.1))
# 0.3 mm lead-in: the remaining pocket seats a 4 mm long insert, leaving tip clearance.
lead=cq.Solid.makeCone(INSERT_BORE/2,INSERT_BORE/2+.3,.3,cq.Vector(10.7,0,SCREW_Z),cq.Vector(1,0,0))
hub=hub.cut(lead)
assert hub.val().isValid() and len(hub.solids().vals())==1
print_hub=hub.rotate((0,0,0),(1,0,0),180).translate((0,0,66))
cq.exporters.export(print_hub,str(P/'P05_drive_hub_M3.stl'),tolerance=.01,angularTolerance=.05)
cq.exporters.export(hub,str(P/'P05_drive_hub_M3.step'))
# Bounding envelopes for nominal M3 x 10 socket screw and installed brass insert.
# D-flat assumed x=2; shaft itself stays a round clearance bore so different flats fit.
screw=radial_cyl(1.5,2,10).union(radial_cyl(2.75,12,3))
insert=radial_cyl(INSERT_BORE/2,7,4).cut(radial_cyl(1.5,6.9,4.2))
reference=P.parent/'gold_poc_v2'/'STEP'
checks={'valid_single_solid':True,'insert_bore_mm':INSERT_BORE,'insert_depth_mm':INSERT_DEPTH,'screw_axis_z_mm':SCREW_Z,'unchanged_interfaces':{'flange_diameter_mm':36,'shaft_bore_mm':5.1,'bolt_circle_diameter_mm':29,'bolt_holes_mm':4.5,'stack_height_mm':10,'bearing_nose_diameter_mm':10},'interferences':[]}
if reference.exists():
 for a in range(0,360,15):
  moving=hub.union(screw).rotate((0,0,0),(0,0,1),a)
  for name in ['P04_catcher','P02_motor_deck','P08_lid']:
   other=cq.importers.importStep(str(reference/(name+'.step')))
   v=moving.intersect(other).val().Volume()
   if v>.005:checks['interferences'].append([a,name,v])
 assert not checks['interferences']
 # Straight 2.5 mm-across-corners tool envelope reaches socket through under-catcher gap.
 tool=radial_cyl(1.25,15,45)
 checks['tool_interference_mm3']=tool.intersect(cq.importers.importStep(str(reference/'P04_catcher.step'))).val().Volume()
 assert checks['tool_interference_mm3']<.005
# Render actual exported STL from four angles, plus section illustrating insert pocket.
from render_support import render,stlmesh
v,f=stlmesh(P/'P05_drive_hub_M3.stl')
# Check every triangle edge appears exactly twice with opposite orientation.
vv,inv=np.unique(np.round(v,5),axis=0,return_inverse=True);ff=inv.reshape(-1,3)
e=np.concatenate([ff[:,[0,1]],ff[:,[1,2]],ff[:,[2,0]]]);_,back,cnt=np.unique(np.sort(e,axis=1),axis=0,return_inverse=True,return_counts=True)
assert np.all(cnt==2) and np.all(np.bincount(back,weights=np.where(e[:,0]<e[:,1],1,-1))==0)
tr=v[f];vol=np.einsum('ij,ij->i',tr[:,0],np.cross(tr[:,1],tr[:,2])).sum()/6
assert vol>0
checks.update(closed_oriented_stl=True,triangles=len(f),volume_mm3=float(vol))
for j,view in enumerate([(2,-1,1.4),(-2,1,1.2),(2,0,0),(1,-1,-1.3)]):render([(v,f,'#568797')],P/f'review_{j}.png',view,(800,650))
def ob(s,color):
 vv,ff=s.val().tessellate(.03,.08);return np.array([q.toTuple() for q in vv]),np.array(ff),color
render([ob(hub,'#568797'),ob(screw,'#b2bac2'),ob(insert,'#d8a843')],P/'assembled_hub.png',(2,-1,-1.2),(1000,760))
section=hub.intersect(cq.Workplane('XY').box(100,100,100,centered=(True,False,False)))
render([ob(section,'#568797'),ob(insert,'#d8a843')],P/'section.png',(1,-2,1),(1000,760))
(P/'checks.json').write_text(json.dumps(checks,indent=2))
print(json.dumps(checks,indent=2))
