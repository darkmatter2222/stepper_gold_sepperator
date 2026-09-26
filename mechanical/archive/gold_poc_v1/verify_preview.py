from pathlib import Path
import numpy as np,json,struct,cadquery as cq
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
P=Path(__file__).parent
reports={}
for p in sorted(P.glob('*.stl')):
 raw=p.read_bytes();n=struct.unpack('<I',raw[80:84])[0]
 dt=np.dtype([('normal','<f4',(3,)),('v','<f4',(3,3)),('attr','<u2')]);a=np.frombuffer(raw,dt,n,84)
 v=a['v'].reshape(-1,3);uv,inv=np.unique(np.round(v,5),axis=0,return_inverse=True);f=inv.reshape(-1,3)
 edges=np.sort(np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1)
 _,ct=np.unique(edges,axis=0,return_counts=True)
 reports[p.name]={'triangles':n,'closed_two_faces_per_edge':bool(np.all(ct==2))}
 assert np.all(ct==2),p.name
(P/'mesh_checks.json').write_text(json.dumps(reports,indent=2))
fig=plt.figure(figsize=(13,7),facecolor='white')
ax=fig.add_subplot(121)
from matplotlib.patches import Circle
for r,c in [(64,'#bd8928'),(60,'#edcb7c'),(18,'#7d92aa'),(8,'#293b50')]:ax.add_patch(Circle((0,0),r,color=c))
for a in [0,120,240]:
 x=21*np.cos(np.radians(a));y=21*np.sin(np.radians(a));ax.plot([x*.72,x],[y*.72,y],color='#7d92aa',lw=12);ax.add_patch(Circle((x,y),2.25,color='white',zorder=5))
ax.annotate('16 mm entrance',(0,0),(-64,-81),arrowprops={'arrowstyle':'->'},fontsize=11)
ax.annotate('Removable collar',(15,8),(20,77),arrowprops={'arrowstyle':'->'},fontsize=11)
ax.text(0,-99,'28 mm sump beneath collar\nSmooth sloped working surface',ha='center',fontsize=11)
ax.set_xlim(-85,85);ax.set_ylim(-105,95);ax.set_aspect('equal');ax.axis('off');ax.set_title('Bowl plan • schematic colors',pad=14)
ax=fig.add_subplot(122)
for name,col in [('01_motor_base','#536579'),('02_bearing_stand','#708198'),('03_splash_catcher','#208f9a'),('05_sealed_bowl','#b88422'),('06_trap_collar','#6e859e'),('07_drive_hub','#536579'),('11_splash_lid','#208f9a')]:
 s=cq.importers.importStep(str(P/(name+'.step')))
 sec=cq.Workplane('XZ').newObject([s.val()]).section()
 for e in sec.edges().vals():
  pts=np.array([e.positionAt(float(t)).toTuple() for t in np.linspace(0,1,40)])
  ax.plot(pts[:,0],pts[:,2],color=col,lw=1.5)
# nonprinted components specified, shown as outlines
from matplotlib.patches import Rectangle
for xy,w,h in [((-21,14),42,40),((-2.5,54),5,20),((-12.5,64),25,25),((-4,79),8,62)]:ax.add_patch(Rectangle(xy,w,h,fill=False,edgecolor='#a0a0a0',ls='--',lw=1))
for z in [100,120]:
 for x in [-11,4]:ax.add_patch(Rectangle((x,z),7,7,fill=False,edgecolor='#a0a0a0'))
ax.annotate('Deep sump',(0,163),(-92,179),arrowprops={'arrowstyle':'->'},fontsize=10)
ax.annotate('Dry splash labyrinth',(33,149),(50,166),arrowprops={'arrowstyle':'->'},fontsize=9)
ax.annotate('2 × 608 bearings',(9,119),(43,116),arrowprops={'arrowstyle':'->'},fontsize=9)
ax.annotate('5 → 8 mm coupling',(10,76),(42,80),arrowprops={'arrowstyle':'->'},fontsize=9)
ax.annotate('NEMA17 motor',(17,33),(42,31),arrowprops={'arrowstyle':'->'},fontsize=9)
ax.set_aspect('equal');ax.set_xlim(-100,108);ax.set_ylim(0,212);ax.set_xlabel('mm');ax.set_ylabel('mm');ax.set_title('Actual CAD section • hardware dashed');ax.spines[['top','right']].set_visible(False)
fig.suptitle('CENTRAL-TRAP CONCENTRATOR — PROOF OF CONCEPT\nM4 modular assembly | recovery and leak testing required',fontsize=15)
plt.tight_layout(rect=(0,0,1,.89));plt.savefig(P/'preview.png',dpi=160)
print(json.dumps(reports))
