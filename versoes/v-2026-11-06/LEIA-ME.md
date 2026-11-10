# Versão 2026-11-06 — app a funcionar fora do claude.ai e offline

- canalizacoes.html é agora um documento completo (doctype, UTF-8, viewport): abre num domínio próprio ou como ficheiro local.
- Descargas (PDF unifilar, PDF do processo, Word, projecto .json) funcionam fora do claude.ai, sem internet.
- Excel (SheetJS) deixou de vir no ficheiro: só é carregado ao importar .xlsx/.xls, primeiro de xlsx.full.min.js na mesma pasta, senão do cdnjs. CSV lê-se sempre sem biblioteca.
- Fontes Google carregam sem bloquear; offline usa as fontes do sistema.
- Para tudo offline: pôr canalizacoes.html e xlsx.full.min.js na mesma pasta. A leitura de fichas PDF (pdf.js) continua a precisar de internet.
