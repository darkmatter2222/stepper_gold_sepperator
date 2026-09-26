from pathlib import Path
import json,struct,math,numpy as np
P=Path(__file__).parent
checks={}
for p in sorted((P/'STL').glob('*.stl')):
 raw=p.read_bytes();n=struct.unpack('<I',raw[80:84])[0];dt=np.dtype([('n','<f4',(3,)),('v','<f4',(3,3)),('a','<u2')]);tr=np.frombuffer(raw,dt,n,84)['v'].astype(float)
 v,inv=np.unique(np.round(tr.reshape(-1,3),5),axis=0,return_inverse=True);f=inv.reshape(-1,3)
 ed=np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]);sort=np.sort(ed,axis=1);unique,back,cnt=np.unique(sort,axis=0,return_inverse=True,return_counts=True)
 orient=np.where(ed[:,0]<ed[:,1],1,-1);balance=np.bincount(back,weights=orient)
 vol=np.sum(np.einsum('ij,ij->i',tr[:,0],np.cross(tr[:,1],tr[:,2])))/6
 valid=bool(np.all(cnt==2) and np.all(balance==0) and vol>0)
 assert valid,p.name
 checks[p.name]={'triangles':n,'closed_manifold':valid,'oriented_edges':bool(np.all(balance==0)),'positive_volume_mm3':round(vol,3)}
(P/'mesh_checks.json').write_text(json.dumps(checks,indent=2))
geom=json.loads((P/'geometry_checks.json').read_text());assert not geom['interferences'];assert not geom['rotation_interferences']
# transparent analytical screening calculations, not CFD or recovery simulation
beta=math.atan(7/19);r=.029
fr=[]
for mu in [0,.1,.2,.3,.4]:
 lim=(math.tan(beta)-mu)/(1+mu*math.tan(beta));rpm=math.sqrt(9.81*lim/r)*60/(2*math.pi) if lim>0 else None
 fr.append({'friction_coefficient':mu,'inward_sliding_limit_rpm':None if rpm is None else round(rpm,1)})
sett=[]
for d in [10,20]:
 for visc in [1,5]:
  v=(19300-1000)*9.81*(d*1e-6)**2/(18*visc*.001)
  sett.append({'gold_diameter_um':d,'viscosity_mPa_s':visc,'settling_mm_per_s':round(v*1000,3),'time_for_5mm_s':round(.005/v,2)})
(P/'mechanics_screening.json').write_text(json.dumps({'model':'Analytical screening only; no CFD, no measured recovery','slope_degrees':round(math.degrees(beta),3),'friction_cases':fr,'ideal_gold_settling':sett,'oscillatory_boundary_layer_mm_at_1Hz':round(math.sqrt(1e-6/math.pi)*1000,3),'radial_g_at_30rpm_r29mm':round((math.pi**2*.029)/9.81,4),'drain_floor':'z=67+0.03*y mm; outlet follows same slope; flat bore invert matches floor within 0.003 mm'},indent=2))
print('PASS: closed/oriented STL meshes; no assembly or sampled rotational interference.');print(fr)
