import json,csv,glob,base64,gzip,unicodedata
def nk(s): return ''.join(c for c in unicodedata.normalize('NFD',s) if unicodedata.category(c)!='Mn').upper().replace('-',' ')
small={'De','Da','Do','Dos','Das','E'}
def tw(w,i): return '-'.join(x.lower() if ((x.capitalize() in small or x=='a') and (i or k)) else x.capitalize() for k,x in enumerate(w.split('-')))
def tc(s): return ' '.join(tw(w,i) for i,w in enumerate(s.lower().split()))
CC=json.load(open('conc_s.json'))
acc={nk(c[0]):tc(c[0]) for c in CC}
P=[]
for r in csv.DictReader(open(glob.glob('rg/*/reverse_geocoder/rg_cities1000.csv')[0],encoding='utf-8')):
    if r['cc']!='PT': continue
    n=r['name']; n={'Lisbon':'Lisboa','Fatima':'Fátima'}.get(n,n)
    if nk(n) in acc: n=acc[nk(n)]
    elif n.isascii():
        # nomes GeoNames sem acentos: terminações portuguesas mais comuns
        W={'Sao':'São','Joao':'João','Antonio':'António','Jose':'José','Bras':'Brás','Vitoria':'Vitória','Gloria':'Glória','Mae':'Mãe','Agua':'Água','Aguas':'Águas','Pedrogao':'Pedrógão','Odivelas':'Odivelas'}
        def fw(w):
            if w in W: return W[w]
            for e,r2 in (('cao','ção'),('coes','ções'),('ao','ão'),('aes','ães'),('oes','ões')):
                if w.endswith(e) and len(w)>len(e)+1: return w[:-len(e)]+r2
            return w
        n=' '.join(fw(w) for w in n.split(' '))
    P.append([n,round(float(r['lat']),4),round(float(r['lon']),4)])
print(len(P))
for c in CC: c[0]=tc(c[0]); c[1]=tc(c[1])
dem=json.load(open('dem.json'))
s='// Gerado por fetch_geo.py: relevo (Terrarium/Mapzen, AWS), concelhos (CAOP via nmota/caop_GeoJSON), localidades (GeoNames cities1000)\n'
s+='const GEO_DEM='+json.dumps(dem,separators=(',',':'))+';\n'
s+='const GEO_CONC="'+base64.b64encode(gzip.compress(json.dumps(CC,ensure_ascii=False,separators=(',',':')).encode(),9)).decode()+'";\n'
s+='const GEO_PLACES='+json.dumps(P,ensure_ascii=False,separators=(',',':'))+';\n'
open('/mnt/project-files/app-fv/geo.js','w',encoding='utf-8').write(s); print(len(s))
