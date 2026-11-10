# Versão 2026-11-10e (v42) — localização com PVGIS e mapa de satélite

- Produção específica do PVGIS 5.3 numa grelha de ~5 km (continente 0,05°, Madeira 0,02°, Açores 0,025°), incluída na app (`pvgis.js`, gerado por `geo-src/4_pvgis.py`). Ao escolher o ponto no mapa a produção é a do PVGIS para esse local (diferença típica < 1 % face ao PVGIS no ponto, máx. ~3 %).
- Valores das capitais de distrito (`locs.js`) passam a ser os do PVGIS.
- Mapa: com internet, satélite (Esri) com nomes de ruas ou mapa de ruas (OpenStreetMap), zoom até ao telhado; sem internet fica o relevo. Pesquisa por morada (Nominatim) e botão «Onde estou».
- `pvgis.php` (opcional, precisa de PHP): ponte para o PVGIS em linha. Com ele, o mapa usa o valor exacto do ponto e o separador Produção tem o botão «Obter do PVGIS (em linha)» para a inclinação/azimute do telhado.
Antes: versoes/v-2026-11-10d (v41).
