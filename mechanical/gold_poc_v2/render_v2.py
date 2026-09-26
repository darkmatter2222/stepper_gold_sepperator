import numpy as np,json,math,struct
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from scipy.ndimage import maximum_filter,minimum_filter
P=Path(__file__).parent
COL={'P01_base':'#587184','P02_motor_deck':'#6c899b','P03_spacer_x4':'#9dafbb','P04_catcher':'#2394a0','P05_drive_hub':'#5f707b','P06_bowl':'#e1a329','P07_optional_trap_insert':'#b67a1b','P08_lid':'#66bdc1','P09_insert_coupon':'#9caeb9'}
DATA=json.loads((P/'assets/meshes.json').read_text()) if (P/'assets/meshes.json').exists() else {}
def mesh(n,group='parts'):
 d=DATA[group+'__'+n];return np.array(d['v']),np.array(d['f'])
def stlmesh(p):
 raw=p.read_bytes();n=struct.unpack('<I',raw[80:84])[0];dt=np.dtype([('n','<f4',(3,)),('v','<f4',(3,3)),('a','<u2')]);v=np.frombuffer(raw,dt,n,84)['v'].reshape(-1,3).astype(float)
 return v,np.arange(len(v)).reshape(-1,3)
def rgb(c):return np.array([int(c[i:i+2],16) for i in [1,3,5]])
def render(objs,path,view=(1,-1.6,1.25),size=(1100,850),margin=.12):
 # objects (vertices, faces, color); true triangle z-buffer with orthographic camera
 cam=np.array(view,dtype=float);cam/=np.linalg.norm(cam);up=np.array([0.,0.,1.])
 if abs(cam[2])>.98:up=np.array([0.,1.,0.])
 right=np.cross(up,cam);right/=np.linalg.norm(right);up=np.cross(cam,right)
 M=np.array([right,up,cam]);vs=np.concatenate([o[0] for o in objs]);proj=vs@M.T
 lo=proj[:,:2].min(0);hi=proj[:,:2].max(0);mid=(lo+hi)/2
 W,H=size;scale=min(W*(1-2*margin)/max(hi[0]-lo[0],1),H*(1-2*margin)/max(hi[1]-lo[1],1))
 im=np.full((H,W,3),250,np.uint8);depth=np.full((H,W),-np.inf);light=cam*.5+np.array([-.4,-.3,.8]);light/=np.linalg.norm(light)
 for v,f,col in objs:
  q=v@M.T;q[:,:2]=(q[:,:2]-mid)*scale;q[:,0]+=W/2;q[:,1]=H/2-q[:,1]
  tr=v[f];norm=np.cross(tr[:,1]-tr[:,0],tr[:,2]-tr[:,0]);ln=np.linalg.norm(norm,axis=1);norm/=np.maximum(ln[:,None],1e-10)
  shade=.42+.58*np.maximum(norm@light,0)
  shade=np.clip(shade,.3,1);colors=rgb(col)[None,:]*shade[:,None]
  for i,ids in enumerate(f):
   a,b,c=q[ids];xmin=max(0,int(np.floor(min(a[0],b[0],c[0]))));xmax=min(W-1,int(np.ceil(max(a[0],b[0],c[0]))));ymin=max(0,int(np.floor(min(a[1],b[1],c[1]))));ymax=min(H-1,int(np.ceil(max(a[1],b[1],c[1]))))
   if xmin>xmax or ymin>ymax:continue
   den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
   if abs(den)<1e-10:continue
   yy,xx=np.mgrid[ymin:ymax+1,xmin:xmax+1];xx=xx+.5;yy=yy+.5
   l1=((b[1]-c[1])*(xx-c[0])+(c[0]-b[0])*(yy-c[1]))/den;l2=((c[1]-a[1])*(xx-c[0])+(a[0]-c[0])*(yy-c[1]))/den;l3=1-l1-l2
   z=l1*a[2]+l2*b[2]+l3*c[2];dd=depth[ymin:ymax+1,xmin:xmax+1];mask=(l1>=-1e-6)&(l2>=-1e-6)&(l3>=-1e-6)&(z>dd)
   dd[mask]=z[mask];im[ymin:ymax+1,xmin:xmax+1][mask]=colors[i].astype(np.uint8)
 # subtle silhouette and depth discontinuity edges, not triangulation artifacts
 occupied=np.isfinite(depth);dd=np.where(occupied,depth,-1e4);edges=occupied&((maximum_filter(dd,3)-minimum_filter(dd,3))>2.3)
 im[edges]=(im[edges]*.72).astype(np.uint8)
 Image.fromarray(im).save(path)
def obj(n,shift=(0,0,0),color=None,group='parts'):
 v,f=mesh(n,group);return(v+np.array(shift),f,color or COL.get(n,'#aab3ba'))
def arrow(start,end):
 # shaft + conical tip triangulated analytically
 start=np.array(start,float);end=np.array(end,float);axis=end-start;L=np.linalg.norm(axis);u=axis/L;tmp=np.array([0,0,1.]) if abs(u[2])<.9 else np.array([1.,0,0]);a=np.cross(u,tmp);a/=np.linalg.norm(a);b=np.cross(u,a)
 vs=[];fs=[]
 for pos,r in [(start,1),(end-u*min(6,L*.35),1),(end-u*min(6,L*.35),2.6),(end,0)]:
  for i in range(16):vs.append(pos+r*(math.cos(i*math.pi/8)*a+math.sin(i*math.pi/8)*b))
 for j in range(3):
  for i in range(16):k=(i+1)%16;fs.extend([[j*16+i,j*16+k,(j+1)*16+i],[j*16+k,(j+1)*16+k,(j+1)*16+i]])
 return np.array(vs),np.array(fs),'#157cc1'
def main():
 global DATA;DATA=json.loads((P/'assets/meshes.json').read_text())
 # Every exported STL: top oblique, underside oblique, orthographic front. Actual STL bytes.
 reviews=[]
 for p in sorted((P/'STL').glob('*.stl')):
  v,f=stlmesh(p);n=p.stem
  panes=[]
  for j,view in enumerate([(1,-1.5,1.3),(-1,1,-1.2),(0,-1,0)]):
   out=P/'assets'/f'{n}_view{j}.png';render([(v,f,COL[n])],out,view,(500,420));panes.append(Image.open(out))
  sheet=Image.new('RGB',(1500,475),'white');d=ImageDraw.Draw(sheet);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
  for j,im in enumerate(panes):sheet.paste(im,(500*j,35));d.text((500*j+16,455),['Top oblique','Underside oblique','Front'][j],font=font,fill='#243746')
  d.text((16,8),n+'  |  actual STL, print orientation',font=font,fill='#243746');sheet.save(P/'assets'/f'review_{n}.png');reviews.append(sheet)
  print('review',n,flush=True)
 # Full assembly and exploded assembly with specified hardware.
 def base():return[obj('P01_base')]
 motor=obj('motor',group='hardware')
 deck=obj('P02_motor_deck');bearing=[obj(n,group='hardware') for n in ['thrust_lower','thrust_cage','thrust_upper']]
 posts=[(47*math.cos(math.radians(a)),47*math.sin(math.radians(a)),0) for a in [45,135,225,315]]
 sp=[obj('P03_spacer_x4',p) for p in posts]
 full=base()+[motor,deck]+bearing+sp+[obj(n) for n in ['P04_catcher','P05_drive_hub','P06_bowl','P08_lid']]
 render(full,P/'assets/assembly.png')
 # Stages emphasize each new part; arrows show insertion rather than imaginary moving components.
 stages={
 'step_motor':[obj('P02_motor_deck'),obj('motor',(0,0,-18),group='hardware'),arrow((25,0,25),(25,0,42))],
 'step_base':base()+[obj('motor',(0,0,18),group='hardware'),obj('P02_motor_deck',(0,0,18)),arrow((39,0,65),(39,0,48))],
 'step_bearing':base()+[motor,deck]+[obj(n,(0,0,10+5*i),group='hardware') for i,n in enumerate(['thrust_lower','thrust_cage','thrust_upper'])]+[arrow((11,0,78),(11,0,55))],
 'step_hub':[obj('P05_drive_hub'),obj('P06_bowl',(0,0,18)),arrow((23,0,91),(23,0,73))],
 'step_spacers':base()+[motor,deck]+bearing+[obj('P03_spacer_x4',(p[0],p[1],10)) for p in posts]+[arrow((posts[0][0],posts[0][1],75),(posts[0][0],posts[0][1],60))],
 'step_catcher':base()+[motor,deck]+bearing+sp+[obj('P04_catcher',(0,0,28)),arrow((49,0,111),(49,0,86))],
 'step_bowl':base()+[motor,deck,obj('P04_catcher')]+bearing+sp+[obj('P06_bowl',(0,0,28)),obj('P05_drive_hub',(0,0,28)),arrow((0,0,129),(0,0,105))],
 'step_lid':base()+[motor,deck,obj('P05_drive_hub'),obj('P04_catcher'),obj('P06_bowl')]+bearing+sp+[obj('P08_lid',(0,0,18)),arrow((48,0,123),(48,0,104))],
 'step_insert':[obj('P06_bowl'),obj('P07_optional_trap_insert',(0,0,16)),arrow((0,0,106),(0,0,91))]
 }
 for n,oo in stages.items():render(oo,P/'assets'/f'{n}.png');print(n,flush=True)
 render([obj('P06_bowl')],P/'assets/bowl_detail.png',(1,-1,2),(950,800))
 render([obj('P04_catcher')],P/'assets/drain_detail.png',(1,-2,1.8),(950,800))
 # retain actual solid CAD half-section for drain inspection through centerline
 import cadquery as cq
 for name in ['P04_catcher','P06_bowl']:
  sh=cq.importers.importStep(str(P/'STEP'/(name+'.step')))
  cut=sh.intersect(cq.Workplane('XY').box(100,200,250,centered=(False,True,False)))
  vv,ff=cut.val().tessellate(.05,.1);vv=np.array([q.toTuple() for q in vv]);render([(vv,np.array(ff),COL[name])],P/'assets'/f'section_{name}.png',(-2,-1,1.2),(1000,800))
if __name__=='__main__':main()
