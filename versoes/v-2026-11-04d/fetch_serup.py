# Descarrega a bolsa de inversores certificados do SERUP (DGEG) para serup-inversores.json: python3 fetch_serup.py
# Página: https://apps.dgeg.gov.pt/DGEG/serup/inversoresConsulta.jsp (grelha jqGrid, 50 linhas por página)
import json,os,datetime,urllib.request,http.cookiejar
S=os.path.dirname(os.path.abspath(__file__))+'/'
PAGE='https://apps.dgeg.gov.pt/DGEG/serup/inversoresConsulta.jsp'
op=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
op.addheaders=[('Referer',PAGE),('User-Agent','Mozilla/5.0')]
op.open(PAGE).read()  # abre sessão (JSESSIONID)
get=lambda p:json.load(op.open('https://apps.dgeg.gov.pt/DGEG/jqGridAjaxPublica?aca=12&rows=50&page=%d'%p))
first=get(1); rows=first['rows'] or []
for p in range(2,int(first['total'])+1): rows+=get(p)['rows'] or []
assert len(rows)==int(first['records']),(len(rows),first['records'])
# c2 marca, c3 modelo, c4 potência kW, c6 regime (1 sinc., 2 ilha, 3 ambos), c7 bateria, c8 kWh bateria
REG={'1':'Sincronizado','2':'Ilha','3':'Sincronizado e ilha'}
num=lambda s:float(s) if s not in (None,'') else 0
out=[[r['c2'].strip(),r['c3'].strip(),num(r['c4']),REG.get(r['c6'],r['c6']),int(r['c7']=='1'),num(r['c8'])] for r in rows]
json.dump({'fetched':datetime.date.today().strftime('%d-%m-%Y'),'page':PAGE,'rows':out},
          open(S+'serup-inversores.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
print(len(out),'inversores')
