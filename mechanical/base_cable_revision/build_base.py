"""Straight P01 corner supports; drill four new holes in existing P02. All dimensions mm."""
from pathlib import Path
import math,json
import cadquery as cq
import numpy as np
from render_support import render,stlmesh
P=Path(__file__).parent
REF=P.parent/'gold_poc_v2'/'STEP'
BASE_R=42; BASE_T=4; POST_CIRCLE=35.5; POST_R=6; FOOT_R=8
INSERT_D=5.6; INSERT_BOTTOM=39.5

def cyl(r,h,z=0,x=0,y=0):return cq.Workplane('XY').workplane(offset=z).center(x,y).circle(r).extrude(h)
def box(x,y,h,z):return cq.Workplane('XY').box(x,y,h,centered=(True,True,False)).translate((0,0,z))
base=cyl(BASE_R,BASE_T);tops=[]
for angle in [45,135,225,315]:
 a=math.radians(angle);x,y=POST_CIRCLE*math.cos(a),POST_CIRCLE*math.sin(a);tops.append((x,y))
 base=base.union(cyl(FOOT_R,4,0,x,y))
 base=base.union(cq.Workplane('XY').newObject([cq.Solid.makeCone(FOOT_R,POST_R,8,cq.Vector(x,y,4),cq.Vector(0,0,1))]))
 base=base.union(cyl(POST_R,34,12,x,y))
 base=base.cut(cyl(INSERT_D/2,7,INSERT_BOTTOM,x,y))
 # Relief around the existing upper plate's outer underside bosses.
 bx,by=47*math.cos(a),47*math.sin(a)
 base=base.cut(cyl(7.3,7,39.8,bx,by))
# Keep 1 mm nominal clearance around the assumed 42 mm square motor.
# This clips only the inward sides of the corner feet/posts, leaving straight axes.
base=base.cut(box(44,44,42,5))
# No unused plate holes or cable-tie slots.
# Reusable top-side template: four old R36 holes locate it; four diagonal holes mark new screws.
template=cyl(40,3).cut(cyl(14,5,-1))
for a in [0,90,180,270]:
 x,y=36*math.cos(math.radians(a)),36*math.sin(math.radians(a))
 template=template.cut(cyl(2.25,5,-1,x,y))
for x,y in tops:template=template.cut(cyl(2.25,5,-1,x,y))
cq.exporters.export(template,str(P/'P02_drill_template.stl'),tolerance=.015,angularTolerance=.06)
cq.exporters.export(template,str(P/'P02_drill_template.step'))
assert base.val().isValid() and len(base.solids().vals())==1
cq.exporters.export(base,str(P/'P01_BASE_STRAIGHT_VERTICAL_R3.stl'),tolerance=.015,angularTolerance=.06)
cq.exporters.export(base,str(P/'P01_BASE_STRAIGHT_VERTICAL_R3.step'))
motor=cq.importers.importStep(str(REF/'H_motor.step'));deck=cq.importers.importStep(str(REF/'P02_motor_deck.step'))
for x,y in tops:deck=deck.cut(cyl(2.25,6,45,x,y))
cq.exporters.export(deck,str(P/'P02_drilled_reference.step'))
# Deliberately explicit unmeasured plug/cable insertion envelope on each motor face.
# It is swept straight outward, open to the exterior, including a modest hand-fit allowance.
corridor=box(45,24,16,6).translate((43.5,0,0)) # x21..66, y+-12, z6..22
checks={}
for name,sh in [('motor',motor),('P02_with_new_holes',deck)]+[(f'connector_corridor_{a}',corridor.rotate((0,0,0),(0,0,1),a)) for a in [0,90,180,270]]:
 v=base.intersect(sh).val().Volume();checks[name]=round(v,8);assert v<.005,(name,v)
# Original deck fastener axes remain open; check nominal M4 screws over thread engagement.
for x,y in tops:
 screw=cyl(2,8,42,x,y)
 assert base.intersect(screw).val().Volume()<.005
v,f=stlmesh(P/'P01_BASE_STRAIGHT_VERTICAL_R3.stl');_,ix=np.unique(np.round(v,5),axis=0,return_inverse=True);ff=ix.reshape(-1,3)
e=np.concatenate([ff[:,[0,1]],ff[:,[1,2]],ff[:,[2,0]]]);_,back,cnt=np.unique(np.sort(e,axis=1),axis=0,return_inverse=True,return_counts=True)
assert np.all(cnt==2) and np.all(np.bincount(back,weights=np.where(e[:,0]<e[:,1],1,-1))==0)
tr=v[f];vol=np.einsum('ij,ij->i',tr[:,0],np.cross(tr[:,1],tr[:,2])).sum()/6;assert vol>0
bb=base.val().BoundingBox()
report={'valid_single_solid':True,'closed_oriented_stl':True,'triangles':len(f),'volume_mm3':float(vol),'bounding_box_mm':[bb.xlen,bb.ylen,bb.zlen],'post_diameter_mm':12,'foot_diameter_mm':16,'post_axes_radius_mm':35.5,'post_angles_deg':[45,135,225,315],'post_axes_vertical':True,'top_z_mm':46,'insert_pilot_mm':5.6,'insert_depth_mm':6.5,'motor_relief_mm':[44,44],'deck_boss_relief_radius_mm':7.3,'new_deck_holes':{'diameter_mm':4.5,'centers_xy_mm':tops,'action':'DRILL EXISTING P02; no reprint required'},'connector_assumption':{'width_mm':24,'z_range_mm':[6,22],'radial_range_mm':[21,66],'status':'unmeasured allowance'},'intersection_volumes_mm3':checks,'validation_limit':'CAD only; requires drilling existing P02 and physical fit check.'}

for i,view in enumerate([(1,-1.6,1.25),(-1,1,1.2),(1,0,.15),(0,0,1),(1,-1,-1)]):render([(v,f,'#4c91a8')],P/f'review_{i}.png',view,(1000,800))
def obj(sh,col):
 vv,ff=sh.val().tessellate(.035,.08);return np.array([q.toTuple() for q in vv]),np.array(ff),col
render([obj(base,'#4c91a8'),obj(motor,'#53565c'),obj(deck,'#bcc5ca'),obj(corridor,'#e0a53a')],P/'assembly_clearance.png',(1,-1.4,.7),(1100,850))
render([obj(base,'#4c91a8'),obj(motor,'#53565c'),obj(corridor,'#e0a53a')],P/'connector_front.png',(1,0,.1),(1100,850))
a=cq.Assembly();a.add(base,name='revised_base');a.add(motor,name='reference_motor');a.add(deck,name='P02_with_new_holes');a.save(str(P/'base_motor_deck_reference.step'))
(P/'checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)
