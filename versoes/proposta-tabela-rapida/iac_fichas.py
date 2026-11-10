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

# --- 2.ª ronda (2026-11-02, tarde): fichas via pesquisa web (sites dos fabricantes continuam bloqueados ao contentor) ---
def _m(dst,src):
  for b,mm in src.items(): dst.setdefault(b,{}).update(mm)
def _g(src,pairs,bk=None): return {m:(v,(bk or {}).get(m),src) for m,v in pairs}
_m(D,{
 'Huawei':{**_g('ficha SUN2000-30/36/40KTL-M3 (Smáx/3×230 V)',[('SUN2000-30KTL-M3',47.9),('SUN2000-36KTL-M3',58.0),('SUN2000-40KTL-M3',63.8)]),
           'SUN2000-50KTL-M3':(79.8,None,'ficha Huawei SUN2000-50KTL-M3 (a 400 V)'),'SUN2000-100KTL-M2':(160.4,None,'ficha Huawei SUN2000-100KTL-M2 (a 400 V)'),
           **_g('ficha Huawei SUN2000-8-10K-LC0',[('SUN2000-8K-LC0',40.0),('SUN2000-10K-LC0',45.5)])},
 'SMA':{**_g('ficha SB1.5-2.5-1VL-40',[('Sunny Boy 1.5 (SB1.5-1VL-40)',7),('Sunny Boy 2.0 (SB2.0-1VL-40)',9),('Sunny Boy 2.5 (SB2.5-1VL-40)',11)]),
        **_g('manual STP5.0/6.0-3AV-40',[('Sunny Tripower 5.0 (STP5.0-3AV-40)',7.6),('Sunny Tripower 6.0 (STP6.0-3AV-40)',9.1)]),
        **_g('manual STP xx-50 (Tripower X)',[('Sunny Tripower X 15 (STP 15-50)',25),('Sunny Tripower X 20 (STP 20-50)',36.6),('Sunny Tripower X 25 (STP 25-50)',36.6)]),
        'Sunny Tripower CORE1 (STP 50-41)':(72.5,None,'ficha STP 50-41 CORE1'),
        **_g('ficha STPxx-3SE-40 (backup = corrente máx. cargas backup em rede)',[('Sunny Tripower Smart Energy 5.0 (STP5.0-3SE-40)',7.6),('Sunny Tripower Smart Energy 10.0 (STP10.0-3SE-40)',15.2)],
             {'Sunny Tripower Smart Energy 5.0 (STP5.0-3SE-40)':20,'Sunny Tripower Smart Energy 10.0 (STP10.0-3SE-40)':20})},
 'Fronius':{**_g('ficha Fronius Primo GEN24 Plus (corrente a 220 V)',[('Primo GEN24 3.0 Plus',13.6),('Primo GEN24 3.6 Plus',16.7),('Primo GEN24 4.0 Plus',18.2),('Primo GEN24 4.6 Plus',20.9),('Primo GEN24 6.0 Plus',27.3),('Primo GEN24 10.0 Plus',45.45)]),
            'Primo GEN24 5.0 Plus':(27.5,None,'página técnica Fronius Primo GEN24 5.0 Plus (27,5 A; outras fontes 22,7 A — usado o maior)'),
            'Symo GEN24 10.0 Plus':(16.4,None,'ficha Fronius Symo GEN24 6.0-10.0 Plus'),
            'Tauro 50-3-D':(75.8,None,'ficha Fronius Tauro 50-3-D (a 220 V)')},
 'GoodWe':{**_g('ficha ET 5-10 kW (corrente máx. para a rede)',[('GW5K-ET',8.5),('GW8K-ET',13.5),('GW10K-ET',16.5)],{'GW5K-ET':8.5,'GW8K-ET':13.5,'GW10K-ET':16.5}),
           **_g('ficha SDT G3 (Smáx/3×220 V)',[('GW10K-SDT-30',16.7),('GW12K-SDT-30',20.0),('GW15K-SDT-30',25.0),('GW17K-SDT-30',28.3),('GW20K-SDT-30',33.3)]),
           **_g('ficha GoodWe SMT/MT',[('GW25K-MT',40),('GW30K-MT',48),('GW50KN-MT',80)]),
           **_g('ficha DNS G3 (maior valor entre mercados, versão AU)',[('GW3000-DNS-30',14.4),('GW3600-DNS-30',17.3),('GW5000-DNS-30',24.0),('GW6000-DNS-30',28.8)])},
 'Sungrow':{**_g('ficha SG5.0-12RT',[('SG10RT',16.7),('SG12RT',20)]),**_g('ficha SG15/17/20RT',[('SG15RT',25),('SG17RT',28.3),('SG20RT',31.9)]),
            **_g('ficha SG33/40/50CX',[('SG33CX',55.2),('SG40CX',66.9),('SG50CX',83.6)]),'SG110CX':(158.8,None,'ficha SG110CX V1.1')},
 'Growatt':{**_g('ficha MOD 10-15KTL3-X (15K: Smáx 16,5 kVA ÷ 3×220 V)',[('MOD 10KTL3-X',16.7),('MOD 12KTL3-X',20.0),('MOD 15KTL3-X',25.0)]),
            **_g('ficha MID 15-25KTL3-X',[('MID 15KTL3-X',24.2),('MID 20KTL3-X',31.9),('MID 25KTL3-X',40.2)]),'MOD 10KTL3-XH':(16.7,None,'ficha MOD 3-10KTL3-XH')},
 'Solis':{**_g('ficha S6-GR1P(2.5-6)K V2.0 2024',[('S6-GR1P2.5K',11.4),('S6-GR1P3K',13.6),('S6-GR1P3.6K',16),('S6-GR1P4K',18.2),('S6-GR1P4.6K',20.9),('S6-GR1P5K',22.7),('S6-GR1P6K',27.3)]),
          **_g('ficha S5-GR3P(5-25)K (Smáx a 230 V)',[('S5-GR3P5K',7.9),('S5-GR3P6K',9.5),('S5-GR3P8K',12.7),('S5-GR3P10K',15.9),('S5-GR3P12K',19.1),('S5-GR3P15K',23.8),('S5-GR3P17K',27.0),('S5-GR3P20K',31.8)]),
          'S5-GC30K':(50.2,None,'ficha S5-GC(25-50)K'),'RHI-3P10K-HVES-5G':(16.7,16.7,'ficha RHI-3P(5-10)K-HVES-5G (backup = saída backup)')},
 'Deye':{'SUN-12K-SG04LP3-EU':(20,None,'ficha SUN-5-12K-SG04LP3'),'SUN-6K-SG04LP3-EU':(10,None,'ficha SUN-5-12K-SG04LP3')},
 'Fox ESS':{**_g('declaração CEI 0-21 H3 (+ ficha 5.0-E: 8,8 A)',[('H3-5.0-E',8.8),('H3-6.0-E',10.6),('H3-8.0-E',14.1),('H3-10.0-E',17.6),('H3-12.0-E',21.2)]),
            'KH8':(38.3,None,'ficha Fox KH (KH8)')},
 'SolaX':{**_g('ficha X1-Hybrid G4 (corrente contínua máx.)',[('X1-Hybrid-3.0-D G4',14.4),('X1-Hybrid-3.7-D G4',16),('X1-Hybrid-5.0-D G4',23.9),('X1-Hybrid-6.0-D G4',28.6),('X1-Hybrid-7.5-D G4',32.6)]),
          **_g('ficha X3-Hybrid G4',[('X3-Hybrid-5.0-D G4',8.1),('X3-Hybrid-6.0-D G4',9.7)])},
 'Sofar':_g('ficha HYD 3000-6000-EP',[('HYD3000-EP',13.6),('HYD4000-EP',18.2),('HYD5000-EP',22.7)]),
 'ZCS Azzurro':{**_g('ficha ZCS 1PH HYD 3000-6000 ZSS (HP)',[('1PH HYD3000 ZSS',15),('1PH HYD3680 ZSS',16),('1PH HYD4000 ZSS',20),('1PH HYD4600 ZSS',20.9),('1PH HYD5000 ZSS',25),('1PH HYD6000 ZSS',27.3)]),
                **_g('ficha ZCS 3PH HYD 5000-20000 ZSS',[('3PH HYD5000 ZSS',8),('3PH HYD6000 ZSS',10),('3PH HYD8000 ZSS',13),('3PH HYD10000 ZSS',16),('3PH HYD15000 ZSS',24),('3PH HYD20000 ZSS',32)])},
})
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
