# Correntes AC máximas (A, por fase) das fichas técnicas → inverters.json (campos iac_max, ibk_max, iac_src)
# Valores confirmados em 2026-11-02 por pesquisa nas fichas dos fabricantes (duas fontes concordantes sempre que possível).
# Correr: python3 iac_fichas.py && python3 build.py
import json,os
S=os.path.dirname(os.path.abspath(__file__))+'/'
D={ # marca: {modelo: (iac_max, ibk_max ou None, fonte)}
 'Huawei':{**{m:(v,None,'ficha UE SUN2000-2-6KTL-L1 (04-202403)') for m,v in [('SUN2000-2KTL-L1',10),('SUN2000-3KTL-L1',15),('SUN2000-3.68KTL-L1',16),('SUN2000-4KTL-L1',20),('SUN2000-4.6KTL-L1',23),('SUN2000-5KTL-L1',25),('SUN2000-6KTL-L1',27.3)]},
           **{m:(v,None,'ficha UE SUN2000-3-10KTL-M1') for m,v in [('SUN2000-3KTL-M1',5.1),('SUN2000-4KTL-M1',6.8),('SUN2000-5KTL-M1',8.5),('SUN2000-6KTL-M1',10.1),('SUN2000-8KTL-M1',13.5),('SUN2000-10KTL-M1',16.9)]},
           **{m:(v,None,'ficha SUN2000-12-20KTL-M2') for m,v in [('SUN2000-12KTL-M2',20),('SUN2000-15KTL-M2',25.2),('SUN2000-17KTL-M2',28.5),('SUN2000-20KTL-M2',33.5)]}},
 'SMA':{**{m:(v,None,'ficha Sunny Boy 3.0-6.0 AV-41') for m,v in [('Sunny Boy 3.0 (SB3.0-1AV-41)',16),('Sunny Boy 3.6 (SB3.6-1AV-41)',16),('Sunny Boy 4.0 (SB4.0-1AV-41)',22),('Sunny Boy 5.0 (SB5.0-1AV-41)',22),('Sunny Boy 6.0 (SB6.0-1AV-41)',26.1)]},
        'Sunny Tripower 8.0 (STP8.0-3AV-40)':(12.1,None,'ficha STP8-10-3AV-40'),'Sunny Tripower 10.0 (STP10.0-3AV-40)':(14.5,None,'ficha STP8-10-3AV-40')},
 'Growatt':{**{m:(v,None,'ficha e certificado CE MIN 2500-6000TL-X') for m,v in [('MIN 2500TL-X',11.3),('MIN 3000TL-X',13.6),('MIN 3600TL-X',16),('MIN 4200TL-X',19),('MIN 4600TL-X',20.9),('MIN 5000TL-X',22.7),('MIN 6000TL-X',27.2)]},
            **{m:(v,None,'manual MOD 3-15KTL3-X') for m,v in [('MOD 5000TL3-X',8.3),('MOD 6000TL3-X',10.0),('MOD 8000TL3-X',13.3)]}},
 'Sungrow':{**{m:(v,None,'ficha SG3.0-6.0RS') for m,v in [('SG3.0RS',13.7),('SG3.6RS',16),('SG4.0RS',18.2),('SG5.0RS',22.8),('SG6.0RS',27.3)]},
            **{m:(v,None,'ficha SH3.0-6.0RS') for m,v in [('SH3.0RS',13.7),('SH3.6RS',16),('SH4.0RS',18.2),('SH5.0RS',22.8),('SH6.0RS',27.3)]},
            **{m:(v,None,'ficha SH5.0-10RT') for m,v in [('SH5.0RT',7.6),('SH6.0RT',9.1),('SH8.0RT',12.1),('SH10RT',15.2)]}},
 'Fox ESS':{**{m:(v,None,'ficha H1 (geração 1)') for m,v in [('H1-3.0-E',14.3),('H1-3.7-E',17.6),('H1-4.6-E',22),('H1-5.0-E',23.9),('H1-6.0-E',28.7)]},
            **{m:(v,b,'ficha e manual H3 Smart (EPS = saída backup)') for m,v,b in [('H3-5.0-Smart',8.3,7.2),('H3-6.0-Smart',10,8.7),('H3-8.0-Smart',13.3,11.6),('H3-10.0-Smart',16.7,14.5),('H3-12.0-Smart',20,17.4),('H3-15.0-Smart',25,21.7)]}},
 'Solis':{m:(v,None,'ficha S6-EH1P(3-8)K-L-PLUS (valor a 220 V, o maior)') for m,v in [('S6-EH1P3K-L-PLUS',13.7),('S6-EH1P3.6K-L-PLUS',16.4),('S6-EH1P4.6K-L-PLUS',20.9),('S6-EH1P5K-L-PLUS',22.8),('S6-EH1P6K-L-PLUS',27.3),('S6-EH1P8K-L-PLUS',36.4)]},
 'GoodWe':{**{m:(v,b,'ficha EMEA ESA 3-10 kW (corrente para a rede a 230 V; bypass = saída backup)') for m,v,b in [('GW3K-EHA-G20',13.1,27.3),('GW3.6K-EHA-G20',15.7,32.8),('GW5K-EHA-G20',21.8,45.5),('GW6K-EHA-G20',26.1,50),('GW8K-EHA-G20',34.8,63),('GW10K-EHA-G20',43.5,63)]},
           **{m:(None,b,'ficha ET 5-10 kW (corrente da saída backup)') for m,b in [('GW5K-ET',8.5),('GW8K-ET',13.5),('GW10K-ET',16.5)]}},
 'Deye':{m:(v,None,'manual SUN-3.6/5/6K-SG03LP1-EU') for m,v in [('SUN-3.6K-SG03LP1-EU',18),('SUN-5K-SG03LP1-EU',25),('SUN-6K-SG03LP1-EU',30)]},
}
inv=json.load(open(S+'inverters.json')); n=0; miss=[]
for b,mm in D.items():
  for m,(i,k,src) in mm.items():
    x=next((x for x in inv if x['brand']==b and x['model']==m),None)
    if not x: miss.append(b+' '+m); continue
    if i: x['iac_max']=i
    if k: x['ibk_max']=k
    x['iac_src']=src; n+=1
json.dump(inv,open(S+'inverters.json','w'),ensure_ascii=False,indent=1)
print(n,'inversores com valores da ficha; não encontrados:',miss)
