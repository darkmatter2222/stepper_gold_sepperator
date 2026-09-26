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