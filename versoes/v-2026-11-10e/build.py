# Monta canalizacoes.html a partir das fontes nesta pasta: python3 build.py
import re,json,os
S=os.path.dirname(os.path.abspath(__file__))+'/'
rd=lambda f:open(S+f,encoding='utf-8').read()
app=rd('app.html').replace('/*DATA*/',rd('data.js'))
pv=rd('pv_part.html')
style=re.search(r'<style>(.*?)</style>',pv,re.S).group(1)
sect=re.search(r'(<section id="view-pv".*?</section>)',pv,re.S).group(1)
script=re.search(r'<script>(.*)</script>',pv,re.S).group(1)
mods=json.load(open(S+'modules.json')); invs=json.load(open(S+'inverters.json'))

# Bolsa de inversores certificados do SERUP (DGEG), descarregada por fetch_serup.py
# linhas: [marca, modelo, potência kW, regime, indicador bateria, bateria kWh]
sj=json.load(open(S+'serup-inversores.json',encoding='utf-8'))
dg=sorted(sj['rows'],key=lambda r:(r[0].upper(),r[1].upper()))
info={'url':sj['page'],'fetched':sj['fetched']}

data=(rd('locs.js')+'\nconst MODULES='+json.dumps(mods,ensure_ascii=False)+';\nconst INVERTERS='+json.dumps(invs,ensure_ascii=False)+
      ';\nconst DGEG_INFO='+json.dumps(info,ensure_ascii=False)+';\nconst DGEG_LIST='+json.dumps(dg,ensure_ascii=False,separators=(',',':'))+';\n')
script=script.replace('/*PVDATA*/',data)
app=app.replace('</style>',style+'</style>',1)
app=app.replace('  <section id="view-ref" hidden>',sect+'\n  <section id="view-ref" hidden>',1)
# SheetJS (Excel) já não vem no ficheiro: é carregado só quando se importa um .xlsx (ver xlsxLoad em app.html)
# separador Unifilar e protecções (sys_part.html), usa a configuração escolhida no separador Fotovoltaico
sp=rd('sys_part.html')
app=app.replace('</style>',re.search(r'<style>(.*?)</style>',sp,re.S).group(1)+'</style>',1)
app=app.replace('  <section id="view-ref" hidden>',re.search(r'(<section id="view-sys".*?</section>)',sp,re.S).group(1)+'\n  <section id="view-ref" hidden>',1)
app=app.rstrip()+'\n<script>'+script+'</script>\n<script>'+re.search(r'<script>(.*)</script>',sp,re.S).group(1)+'</script>\n'
# separadores Produção e poupança e Processo DGEG, e barra do projecto (doc_part.html); usa pv.edit, sysCalc() e o PDF do sys_part
dp=rd('doc_part.html')
app=app.replace('</style>',re.search(r'<style>(.*?)</style>',dp,re.S).group(1)+'</style>',1)
for sid in ('view-prod','view-doc'):
    app=app.replace('  <section id="view-ref" hidden>',re.search(r'(<section id="%s".*?</section>)'%sid,dp,re.S).group(1)+'\n  <section id="view-ref" hidden>',1)
app=app.rstrip()+'\n<script>'+re.search(r'<script>(.*)</script>',dp,re.S).group(1)+'</script>\n'
# mapa de localização (map_part.html + geo.js e pvgis.js, gerados por geo-src/*.py); usa pv, LOCS e GEO dos separadores anteriores
mp=rd('map_part.html')
app=app.replace('</style>',re.search(r'<style>(.*?)</style>',mp,re.S).group(1)+'</style>',1)
app=app.replace('  <section id="view-ref" hidden>',re.search(r'(<dialog id="mp-dlg".*?</dialog>)',mp,re.S).group(1)+'\n  <section id="view-ref" hidden>',1)
app=app.rstrip()+'\n<script>'+re.search(r'<script>(.*)</script>',mp,re.S).group(1).replace('/*GEODATA*/',rd('geo.js')+(rd('pvgis.js') if os.path.exists(S+'pvgis.js') else ''))+'</script>\n'
# adaptação ao telemóvel (mobile_part.html): estilos ≤ 640 px e script; vem no fim porque usa os separadores todos
mo=rd('mobile_part.html')
app=app.replace('</style>',re.search(r'<style>(.*?)</style>',mo,re.S).group(1)+'</style>',1)
app=app.rstrip()+'\n<script>'+re.search(r'<script>(.*)</script>',mo,re.S).group(1)+'</script>\n'
# documento completo (codificação UTF-8 e viewport) para abrir fora do claude.ai: domínio próprio ou ficheiro local
app='<!doctype html>\n<html lang="pt-PT">\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'+app
open(S+'canalizacoes.html','w',encoding='utf-8').write(app)
print(len(app),'bytes ·',len(dg),'inversores DGEG')
