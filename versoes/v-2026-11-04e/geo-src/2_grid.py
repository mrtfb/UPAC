import math,json,zlib,base64,numpy as np
from PIL import Image
from shapely.geometry import shape
from shapely.ops import transform, unary_union
from shapely import contains_xy
import pyproj
T={}
def img(z,x,y):
    k=(z,x,y)
    if k not in T:
        a=np.asarray(Image.open(f"t/{z}_{x}_{y}.png").convert("RGB")).astype(float)
        T[k]=a[:,:,0]*256+a[:,:,1]+a[:,:,2]/256-32768
    return T[k]
def elev(lat,lon,z):
    n=2**z; fx=(lon+180)/360*n; fy=(1-math.asinh(math.tan(math.radians(lat)))/math.pi)/2*n
    px=fx*256-0.5; py=fy*256-0.5
    x0=math.floor(px); y0=math.floor(py); dx=px-x0; dy=py-y0
    def g(px,py):
        return img(z,px//256,py//256)[py%256,px%256]
    return (g(x0,y0)*(1-dx)*(1-dy)+g(x0+1,y0)*dx*(1-dy)+g(x0,y0+1)*(1-dx)*dy+g(x0+1,y0+1)*dx*dy)
tr=pyproj.Transformer.from_crs(3763,4326,always_xy=True).transform
C=json.load(open('conc.geojson',encoding='utf-8-sig'))
polys=[]
for f in C['features']:
    g=transform(tr,shape(f['geometry'])); polys.append((f['properties'],g))
PT=unary_union([g for _,g in polys]).buffer(0.003)
out={}
def grid(name,la0,la1,lo0,lo1,d,z,step,mask):
    lats=np.arange(la1,la0-1e-9,-d); lons=np.arange(lo0,lo1+1e-9,d)
    H=len(lats);W=len(lons); a=np.zeros((H,W),np.uint8)
    LO,LA=np.meshgrid(lons,lats)
    inpt=contains_xy(mask,LO,LA) if mask is not None else np.ones((H,W),bool)
    for i,la in enumerate(lats):
        for j,lo in enumerate(lons):
            e=elev(la,lo,z)
            if e<=0.5: a[i,j]=0
            elif not inpt[i,j]: a[i,j]=1
            else: a[i,j]=min(255,2+int(round(e/step)))
    print(name,H,W,a.max(),(a.max()-2)*step)
    raw=a.tobytes(); comp=zlib.compress(raw,9)
    import gzip; gz=gzip.compress(raw,9)
    out[name]={"la1":round(la1,4),"lo0":round(lo0,4),"d":d,"w":W,"h":H,"step":step,"b64":base64.b64encode(gz).decode()}
    print(len(raw),len(gz))
grid("c",36.9,42.2,-9.6,-6.15,0.01,8,8,PT)
grid("m",32.35,33.15,-17.35,-16.2,0.005,10,8,None)
grid("a",36.9,39.8,-31.35,-24.95,0.01,9,10,None)
json.dump(out,open('dem.json','w'))
# concelhos simplificados
CC=[]
for p,g in polys:
    s=g.simplify(0.0015,preserve_topology=True)
    rings=[]
    gs=[s] if s.geom_type=='Polygon' else list(s.geoms)
    for pg in gs:
        for r in [pg.exterior]+list(pg.interiors):
            pts=[(round(x*1e4),round(y*1e4)) for x,y in r.coords]
            flat=[pts[0][0],pts[0][1]]
            for k in range(1,len(pts)): flat+= [pts[k][0]-pts[k-1][0],pts[k][1]-pts[k-1][1]]
            rings.append(flat)
    CC.append([p['Concelho'],p['Distrito'],rings])
js=json.dumps(CC,ensure_ascii=False,separators=(',',':'))
print('conc',len(js),sum(len(r) for c in CC for r in c[2])//2)
open('conc_s.json','w').write(js)
