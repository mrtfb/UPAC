# Versão 2026-11-10b (v39) — revisão final

- Strings: deixa de preferir strings curtas em todos os MPPT (ex. 3 kWp: 1×6 em vez de 2×(1×3), cabo DC 4 mm² em vez de 10 mm²). Penaliza MPPT com Vmpp (STC) < metade da tensão nominal DC do inversor.
- Modo «kW AC»: a potência AC pedida passa a contar na ordenação (pedir 5 kW já não propõe 6 kW).
- Cabos AC monofásicos no Unifilar: corrente admissível com 2 condutores carregados (3G = L+N+PE), como o texto já dizia (antes usava a coluna de 3).
- Dois ou mais inversores: a queda de tensão AC é repartida entre inversor → quadro FV e quadro FV → Q.G.E. quando a soma passava o limite.
- Memória descritiva: sem o código interno (S2, S5b…) no tipo de ligação; texto da corrente de cálculo DC certo com strings em paralelo e fusíveis.
- Telemóvel: separador 1 com o nome «Painéis» na barra de baixo (o «Fotovoltaico» ficava cortado).
Antes: versoes/v-2026-11-10 (v38).
