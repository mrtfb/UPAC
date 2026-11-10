# Inversores confirmados com a ficha técnica oficial em PDF (pasta fichas/) + estado dos dados de cada inversor (campo "gaps").
# Correr depois de iac_fichas.py:  python3 iac_fichas.py && python3 fichas_pdf.py && python3 build.py
import json,os,re
pt=lambda x:f'{x:g}'.replace('.',',')
S=os.path.dirname(os.path.abspath(__file__))+'/'
inv=json.load(open(S+'inverters.json',encoding='utf-8'))
idx={(i['brand'],i['model']):k for k,i in enumerate(inv)}
def put(e,after=None):
  k=idx.get((e['brand'],e['model']))
  if k is None:
    pos=(idx[after]+1) if after in idx else len(inv)
    inv.insert(pos,e)
  else: inv[k]=e
  idx.clear(); idx.update({(i['brand'],i['model']):k for k,i in enumerate(inv)})

# --- Fox ESS H1-G2 (ficha EN-H1-G2-Datasheet V1.9, 2025-04-11) ---------------------------------------------
FOX='FoxESS_H1-G2_AC1-G2_datasheet_V1.9.pdf'
prev=('Fox ESS','H1-6.0-E')
for m,pac,pdc,arr,iac,ibk,dg in [('3.0',3.0,4.5,6,15.0,13.6,'H1-3.0'),('3.7',3.68,5.5,7.4,18.4,16.7,'H1-3.7'),('4.6',4.6,6.9,9.2,23.0,20.9,'H1-4.6'),
                                ('5.0',5.0,7.5,10,25.0,22.7,'H1-5'),('6.0',6.0,9.0,12,30.0,27.3,'H1-6')]:
  e={"brand":"Fox ESS","model":f"H1-{m}-E-G2","phases":1,"hybrid":True,"pac_kw":pac,"pdc_max_kw":pdc,"vdc_max":600,"v_start":75,"mppt_min":80,"mppt_max":550,"v_nom":360,
     "mppt":2,"strings_per_mppt":[1,1],"imax_mppt":[16,16],"isc_mppt":[20,20],"battery":"HV 80–480 V (LFP, Fox HV)","source":"",
     "note":f"2.ª geração (G2). P DC = potência máx. de entrada ({pt(pdc)} kW); a ficha admite campo FV até {pt(arr)} kWp. Saída EPS {pt(ibk)} A. Na lista DGEG surge como {dg}.",
     "dgeg":dg,"iac_max":iac,"ibk_max":ibk,"iac_src":"ficha H1-G2 V1.9 (máx. corrente de saída; backup = corrente máx. EPS)","ficha":FOX}
  put(e,prev); prev=("Fox ESS",e["model"])
for m in ['3.0','3.7','4.6','5.0','6.0']:
  k=idx.get(('Fox ESS',f'H1-{m}-E'))
  if k is not None: inv[k]['note']=f"1.ª geração (H1-E, ficha DE V3.7): 13,5 A por MPPT. A geração actual é a G2 (16 A por MPPT): escolha H1-{m}-E-G2."

# --- Solis S6-EH1P(3-10)K-L-PLUS(21A) (ficha 2025-11) ---------------------------------------------------------
SOL='Solis_S6-EH1P(3-10)K-L-PLUS(21A).pdf'
prev=('Solis','S6-EH1P6K-L-PLUS')
for m,pac,pdc,arr,iac,ipass,spm,im,isc,dg in [('3K',3.0,4.8,6,13.7,35,1,21,24,'S6-EH1P3K-PLUS'),('3.6K',3.6,5.76,7.2,16.4,35,1,21,24,'S6-EH1P3.6K-PLUS'),
    ('4.6K',4.6,7.36,9.2,20.9,40,1,21,24,'S6-EH1P4.6K-PLUS'),('5K',5.0,8.0,10,22.8,40,1,21,24,'S6-EH1P5K-PLUS'),('6K',6.0,9.6,12,27.3,40,1,21,24,'S6-EH1P6K-PLUS'),
    ('8K',8.0,12.8,16,36.4,50,2,42,48,'S6-EH1P8K-PLUS'),('9K',9.0,14.4,18,40.9,60,2,42,48,None),('10K',10.0,16.0,20,45.5,65,2,42,48,None)]:
  e={"brand":"Solis","model":f"S6-EH1P{m}-L-PLUS","phases":1,"hybrid":True,"pac_kw":pac,"pdc_max_kw":pdc,"vdc_max":500,"v_start":90,"mppt_min":90,"mppt_max":435,"v_nom":330,
     "mppt":2,"strings_per_mppt":[spm,spm],"imax_mppt":[im,im],"isc_mppt":[isc,isc],"battery":"LV 40–60 V (Li-ion / chumbo-ácido)","source":"",
     "note":(f"versão «21A» (ficha 2025): {im} A / {isc} A por MPPT, {spm} entrada{'s' if spm>1 else ''} por MPPT. Unidades mais antigas têm 16 A / 20 A por MPPT: confirme a etiqueta. "
             f"P DC = potência FV máx. utilizável ({pt(pdc)} kW); campo recomendado até {pt(arr)} kWp. Corrente de passagem (bypass) {ipass} A."+(f" Na lista DGEG surge sem o «-L»." if dg else "")),
     "iac_max":iac,"ibk_max":ipass,"iac_src":"ficha S6-EH1P(3-10)K-L-PLUS(21A) (corrente máx. a 220 V; backup = corrente de passagem AC)","ficha":SOL}
  if dg: e["dgeg"]=dg
  put(e,prev); prev=("Solis",e["model"])

# --- estado dos dados: o que não está confirmado numa ficha do próprio modelo ------------------------------
unc=re.compile(r'confirmar|distribuidor|família|estimad|revisão|revisões|conforme leitura|assumid|inferido|como o |de outro modelo',re.I)
for i in inv:
  g=[]
  if i.get('ficha'): i.pop('gaps',None); continue
  if i.get('note') and unc.search(i['note']): g.append("valores da série ou de distribuidor, não confirmados na ficha deste modelo")
  if i['brand']=='Fox ESS' and re.fullmatch(r'H1-[\d.]+-E',i['model']): g.append("ficha da 1.ª geração; confirme se o equipamento não é o G2")
  if not i.get('iac_max'): g.append("corrente AC máxima (estimada pela potência)")
  if not i.get('isc_mppt'): g.append("Isc máx. por MPPT")
  if i.get('hybrid') and not i.get('ibk_max'): g.append("corrente da saída backup / de passagem (usa a corrente AC)")
  if g: i['gaps']=g
  else: i.pop('gaps',None)
json.dump(inv,open(S+'inverters.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(len(inv),'inversores ·',sum(1 for i in inv if i.get('ficha')),'com ficha PDF ·',sum(1 for i in inv if i.get('gaps')),'com dados a confirmar')
