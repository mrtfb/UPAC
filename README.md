# UPAC — app de dimensionamento fotovoltaico e canalizações

App numa só página (`canalizacoes.html`) para projectos UPAC: dimensionamento de strings e inversores, unifilar e protecções, produção e poupança, processo DGEG (memória descritiva, PDF/Word) e cálculo de canalizações segundo as RTIEBT.

## Como montar

```
python3 build.py
```

Junta `app.html`, `pv_part.html`, `sys_part.html`, `doc_part.html`, `map_part.html`, `mobile_part.html`, `data.js`, `locs.js`, `geo.js`, `modules.json`, `inverters.json` e `serup-inversores.json` em `canalizacoes.html`.

## Pastas

- `fichas/` — fichas técnicas (PDF) de painéis e inversores usadas nos dados.
- `geo-src/` — scripts que geram `geo.js` (mapa offline).
- `versoes/` — versões guardadas (fontes + html montado), cada uma com `LEIA-ME.md`.
- `site/fv.zip` — versão offline (`index.html` + `xlsx.full.min.js`) para alojar num domínio próprio.
- `Calculo_Canaliz.xls` — folha original das canalizações.

Outros scripts: `fetch_serup.py` (actualiza a lista de inversores certificados da DGEG/SERUP), `iac_fichas.py` e `fichas_pdf.py` (dados das fichas).
