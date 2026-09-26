"""P01 only: offset lower supports, original P02 interface. All dimensions mm."""
from pathlib import Path
import math,json
import cadquery as cq
import numpy as np
from render_support import render,stlmesh
P=Path(__file__).parent
REF=P.parent/'gold_poc_v2'/'STEP'
BASE_R=42; BASE_T=4; LOWER_R=41; POST_R=6; FOOT_R=9
TOP_R=36; TOP_Z=46; TRANSITION_START=14; TRANSITION_END=37
INSERT_D=5.6; INSERT_BOTTOM=39.5

def cyl(r,h,z=0,x=0,y=0):return cq.Workplane('XY').workplane(offset=z).center(x,y).circle(r).extrude(h)
def loft(x1,y1,z1,r1,x2,y2,z2,r2):
 w1=cq.Workplane('XY').workplane(offset=z1).center(x1,y1).circle(r1).val()
 w2=cq.Workplane('XY').workplane(offset=z2).center(x2,y2).circle(r2).val()
 return cq.Workplane('XY').newObject([cq.Solid.makeLoft([w1,w2],True)])
def box(x,y,h,z):return cq.Workplane('XY').box(x,y,h,centered=(True,True,False)).translate((0,0,z))
base=cyl(BASE_R,BASE_T);tops=[];bottoms=[]
for angle in [0,90,180,270]:
 a=math.radians(angle);b=math.radians(angle+45)
 tx,ty=TOP_R*math.cos(a),TOP_R*math.sin(a)
 bx,by=LOWER_R*math.cos(b),LOWER_R*math.sin(b)
 tops.append((tx,ty));bottoms.append((bx,by))
 # Rounded feet merge into plate, flare to 12 mm posts above the motor-bottom gap.
 base=base.union(cyl(FOOT_R,BASE_T,0,bx,by))
 base=base.union(loft(bx,by,4,FOOT_R,bx,by,12,POST_R))
 base=base.union(cyl(POST_R,2,12,bx,by))
 base=base.union(loft(bx,by,TRANSITION_START,POST_R,tx,ty,TRANSITION_END,POST_R))
 base=base.union(cyl(POST_R,9,37,tx,ty))
 base=base.cut(cyl(INSERT_D/2,7,INSERT_BOTTOM,tx,ty))
 # Base anchor holes move to the now-open cardinal positions.
 base=base.cut(cyl(2.25,6,-1,tx,ty))
for x in [-8,8]:base=base.cut(box(3,7,6,-1).translate((x,30,0)))
assert base.val().isValid() and len(base.solids().vals())==1
cq.exporters.export(base,str(P/'P01_base_cable_clearance.stl'),tolerance=.015,angularTolerance=.06)
cq.exporters.export(base,str(P/'P01_base_cable_clearance.step'))
motor=cq.importers.importStep(str(REF/'H_motor.step'));deck=cq.importers.importStep(str(REF/'P02_motor_deck.step'))
# Deliberately explicit unmeasured plug/cable insertion envelope on each motor face.
# It is swept straight outward, open to the exterior, including a modest hand-fit allowance.
corridor=box(45,24,16,6).translate((43.5,0,0)) # x21..66, y+-12, z6..22
checks={}
for name,sh in [('motor',motor),('unchanged_P02',deck)]+[(f'connector_corridor_{a}',corridor.rotate((0,0,0),(0,0,1),a)) for a in [0,90,180,270]]:
 v=base.intersect(sh).val().Volume();checks[name]=round(v,8);assert v<.005,(name,v)
# Original deck fastener axes remain open; check nominal M4 screws over thread engagement.
for x,y in tops:
 screw=cyl(2,8,42,x,y)
 assert base.intersect(screw).val().Volume()<.005
v,f=stlmesh(P/'P01_base_cable_clearance.stl');_,ix=np.unique(np.round(v,5),axis=0,return_inverse=True);ff=ix.reshape(-1,3)
e=np.concatenate([ff[:,[0,1]],ff[:,[1,2]],ff[:,[2,0]]]);_,back,cnt=np.unique(np.sort(e,axis=1),axis=0,return_inverse=True,return_counts=True)
assert np.all(cnt==2) and np.all(np.bincount(back,weights=np.where(e[:,0]<e[:,1],1,-1))==0)
tr=v[f];vol=np.einsum('ij,ij->i',tr[:,0],np.cross(tr[:,1],tr[:,2])).sum()/6;assert vol>0
bb=base.val().BoundingBox()
report={'valid_single_solid':True,'closed_oriented_stl':True,'triangles':len(f),'volume_mm3':float(vol),'bounding_box_mm':[bb.xlen,bb.ylen,bb.zlen],'base_plate_thickness_mm':4,'old_post_diameter_mm':9,'new_post_diameter_mm':12,'foot_diameter_mm':18,'lower_support_radius_mm':41,'lower_support_angles_deg':[45,135,225,315],'top_support_radius_mm':36,'top_support_angles_deg':[0,90,180,270],'top_z_mm':46,'insert_pilot_mm':5.6,'insert_depth_mm':6.5,'upper_straight_section_z_mm':[37,46],'connector_assumption':{'width_mm':24,'z_range_mm':[6,22],'radial_range_mm':[21,66],'status':'unmeasured clearance envelope, NOT a connector specification'},'intersection_volumes_mm3':checks,'unchanged_top_hole_alignment':True,'hardware_assumptions':'../gold_poc_v2/STEP/H_motor.step; 42x42x40 mm body at z6..46','validation_limit':'No physical print/load test. Angled braces need slicer support review.'}
for i,view in enumerate([(1,-1.6,1.25),(-1,1,1.2),(1,0,.15),(0,0,1),(1,-1,-1)]):render([(v,f,'#4c91a8')],P/f'review_{i}.png',view,(1000,800))
def obj(sh,col):
 vv,ff=sh.val().tessellate(.035,.08);return np.array([q.toTuple() for q in vv]),np.array(ff),col
render([obj(base,'#4c91a8'),obj(motor,'#53565c'),obj(deck,'#bcc5ca'),obj(corridor,'#e0a53a')],P/'assembly_clearance.png',(1,-1.4,.7),(1100,850))
render([obj(base,'#4c91a8'),obj(motor,'#53565c'),obj(corridor,'#e0a53a')],P/'connector_front.png',(1,0,.1),(1100,850))
a=cq.Assembly();a.add(base,name='revised_base');a.add(motor,name='reference_motor');a.add(deck,name='unchanged_P02');a.save(str(P/'base_motor_deck_reference.step'))
(P/'checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)
