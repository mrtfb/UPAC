# Produção específica do PVGIS (kWh/kWp·ano, inclinação e azimute óptimos, 14 % de perdas) numa grelha
# sobre terra (continente, Madeira, Açores). Gera ../pvgis.js (const GEO_PVGIS), lido pelo mapa sem internet.
# Uso: python3 geo-src/4_pvgis.py   (a cache pvgis_cache.json evita repetir pedidos)
import json, re, base64, gzip, os, time, urllib.request, concurrent.futures as cf
S = os.path.dirname(os.path.abspath(__file__)) + '/'
geo = open(S + '../geo.js', encoding='utf-8').read()
DEM = json.loads(re.search(r'const GEO_DEM=(\{.*?\});\n', geo).group(1))
CACHE = S + 'pvgis_cache.json'
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
API = 'https://re.jrc.ec.europa.eu/api/v5_3/PVcalc?lat={:.4f}&lon={:.4f}&peakpower=1&loss=14&optimalangles=1&outputformat=json'
GRID = {'c': 0.05, 'm': 0.02, 'a': 0.025}

def land_near(g, a, lat, lon, r):
    """há terra portuguesa (código >= 2) na grelha de relevo a menos de r graus do ponto?"""
    i0 = int((g['la1'] - lat - r) / g['d']); i1 = int((g['la1'] - lat + r) / g['d']) + 1
    j0 = int((lon - r - g['lo0']) / g['d']); j1 = int((lon + r - g['lo0']) / g['d']) + 1
    for i in range(max(0, i0), min(g['h'], i1 + 1)):
        for j in range(max(0, j0), min(g['w'], j1 + 1)):
            if a[i * g['w'] + j] >= 2: return True
    return False

def fetch(k):
    if k in cache: return k, cache[k]
    lat, lon = map(float, k.split(','))
    for t in range(5):
        try:
            with urllib.request.urlopen(API.format(lat, lon), timeout=60) as r:
                d = json.load(r); v = d['outputs']['totals']['fixed']['E_y']
                return k, round(v)
        except urllib.error.HTTPError as e:
            if e.code == 400: return k, 0      # mar
            time.sleep(2 + 3 * t)
        except Exception:
            time.sleep(2 + 3 * t)
    return k, None

out = {}
for reg, d in GRID.items():
    g = DEM[reg]; a = gzip.decompress(base64.b64decode(g['b64']))
    la1 = g['la1'] + g['d'] / 2; lo0 = g['lo0'] - g['d'] / 2
    la0 = g['la1'] - (g['h'] - 0.5) * g['d']; lo1 = g['lo0'] + (g['w'] - 0.5) * g['d']
    # grelha alinhada a múltiplos de d
    la1 = round(int(la1 / d) * d + d, 4); lo0 = round((int(lo0 / d) - 1) * d, 4)
    H = int((la1 - la0) / d) + 2; W = int((lo1 - lo0) / d) + 2
    pts = [(i, j, round(la1 - i * d, 4), round(lo0 + j * d, 4)) for i in range(H) for j in range(W)]
    pts = [p for p in pts if land_near(g, a, p[2], p[3], d * 0.75)]
    keys = {f'{la:.4f},{lo:.4f}': (i, j) for i, j, la, lo in pts}
    print(reg, H, W, len(keys), 'pontos;', sum(k in cache for k in keys), 'em cache', flush=True)
    with cf.ThreadPoolExecutor(8) as ex:
        n = 0
        for k, v in ex.map(fetch, list(keys)):
            if v is not None: cache[k] = v
            n += 1
            if n % 200 == 0:
                print(' ', n, flush=True); json.dump(cache, open(CACHE, 'w'))
    json.dump(cache, open(CACHE, 'w'))
    v = [0] * (H * W)
    for k, (i, j) in keys.items():
        if cache.get(k): v[i * W + j] = cache[k]
    # pontos no mar junto a arribas: o horizonte da arriba baixa muito o valor; retira-os se ficarem
    # abaixo de 92 % da mediana dos vizinhos em terra (a interpolação usa então só os de terra)
    isl = lambda la, lo: land_near(g, a, la, lo, g['d'] * 0.5)
    lnd = {(i, j) for k, (i, j) in keys.items() if isl(la1 - i * d, lo0 + j * d)}
    drop = 0
    for k, (i, j) in keys.items():
        if (i, j) in lnd or not v[i * W + j]: continue
        nb = sorted(v[ii * W + jj] for ii in range(i - 2, i + 3) for jj in range(j - 2, j + 3)
                    if (ii, jj) in lnd and 0 <= ii < H and 0 <= jj < W and v[ii * W + jj])
        if nb and v[i * W + j] < 0.92 * nb[len(nb) // 2]: v[i * W + j] = 0; drop += 1
    print(reg, 'retirados (mar junto a arribas):', drop)
    out[reg] = {'la1': la1, 'lo0': lo0, 'd': d, 'w': W, 'h': H, 'v': v}
    print(reg, 'valores', sum(1 for x in v if x), min(x for x in v if x), max(v))

s = ('// Gerado por geo-src/4_pvgis.py: produção específica do PVGIS 5.3 (JRC, SARAH3/ERA5), kWh/kWp·ano\n'
     '// com inclinação e azimute óptimos, 14 % de perdas, horizonte do relevo incluído. 0 = sem valor (mar).\n'
     '// Descarregado em ' + time.strftime('%Y-%m-%d') + '.\n'
     'const GEO_PVGIS=' + json.dumps(out, separators=(',', ':')) + ';\n')
open(S + '../pvgis.js', 'w', encoding='utf-8').write(s)
print(len(s), 'bytes')
