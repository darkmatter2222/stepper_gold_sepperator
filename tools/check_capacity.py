"""Static P06 cavity volumes from build_v2.py wet profile. No flow/recovery model.
Run with CadQuery 2.7: python tools/check_capacity.py
No optional P07 insert, print tolerances, grains or meniscus included.
"""
import json, math
from pathlib import Path
import cadquery as cq
cavity = (cq.Workplane('XZ').moveTo(0,76).lineTo(7,76)
 .threePointArc((7.7,76.3),(8,77)).lineTo(8,84.5)
 .threePointArc((8.5,86),(10,87)).lineTo(29,94)
 .threePointArc((29.8,94.5),(30,95.4)).lineTo(30,97)
 .lineTo(0,97).close().revolve(360,(0,0),(0,1)))
rows=[]
for height in [2.5,5,8.5,11,18,21]:
 cut=cq.Workplane('XY').box(100,100,height,centered=(True,True,False)).translate((0,0,76))
 rows.append(dict(depth_from_sump_floor_mm=height,assembly_z_mm=76+height,
                  static_void_ml=round(cavity.intersect(cut).val().Volume()/1000,4)))
result={'scope':'Static empty P06 void, no P07. Not operational retained-solids capacity or a safe fill limit.',
        'fill_volumes':rows,
        'spin_screening':[dict(rpm=n,radial_g_at_29mm=round((n*math.pi/30)**2*.029/9.81,4),
                              ideal_water_rise_mm=round((n*math.pi/30)**2*.029**2/(2*9.81)*1000,3))
                          for n in [90,135,180,195,210,225]]}
Path('docs/CAPACITY_SCREENING.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
