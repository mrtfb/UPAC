import math,os,subprocess,sys
def tile(lat,lon,z):
    n=2**z; x=int((lon+180)/360*n); y=int((1-math.asinh(math.tan(math.radians(lat)))/math.pi)/2*n); return x,y
boxes=[(36.85,42.25,-9.6,-6.1,8),(32.3,33.2,-17.4,-16.15,10),(36.85,39.85,-31.4,-24.9,9)]
jobs=[]
for la0,la1,lo0,lo1,z in boxes:
    x0,y0=tile(la1,lo0,z); x1,y1=tile(la0,lo1,z)
    for x in range(x0,x1+1):
        for y in range(y0,y1+1): jobs.append((z,x,y))
print(len(jobs))
for z,x,y in jobs:
    f=f"t/{z}_{x}_{y}.png"
    if not os.path.exists(f): subprocess.run(["curl","-s","-m","60","-o",f,f"https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"])
