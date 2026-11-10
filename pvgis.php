<?php
// Ponte para a API do PVGIS (Comissão Europeia, JRC). O PVGIS não aceita pedidos directos feitos por
// páginas web (não envia cabeçalhos CORS), por isso a app pede a este ficheiro, no mesmo servidor, e ele
// pede ao PVGIS. Basta copiá-lo para a mesma pasta de canalizacoes.html (precisa de PHP no alojamento).
// Sem este ficheiro a app funciona na mesma, com a grelha do PVGIS incluída (~5 km).
header('Content-Type: application/json; charset=utf-8');
if (isset($_GET['ping'])) { echo '{"ok":1}'; exit; }

$q = ['peakpower' => 1, 'loss' => 14, 'outputformat' => 'json'];
foreach (['lat', 'lon', 'angle', 'aspect', 'loss', 'peakpower'] as $k)
  if (isset($_GET[$k]) && is_numeric($_GET[$k])) $q[$k] = round((float)$_GET[$k], 4);
if (!empty($_GET['optimalangles'])) $q['optimalangles'] = 1;
if (!isset($q['lat'], $q['lon']) || abs($q['lat']) > 90 || abs($q['lon']) > 180 || $q['loss'] < 0 || $q['loss'] > 99) {
  http_response_code(400); echo '{"message":"Parâmetros inválidos"}'; exit;
}
$url = 'https://re.jrc.ec.europa.eu/api/v5_3/PVcalc?' . http_build_query($q);

// cache em ficheiro durante 30 dias (os dados do PVGIS só mudam com nova versão)
$dir = sys_get_temp_dir() . '/pvgis-cache';
$file = $dir . '/' . md5($url) . '.json';
if (is_file($file) && time() - filemtime($file) < 30 * 86400) { header('X-Cache: hit'); readfile($file); exit; }

$code = 0; $body = false;
if (function_exists('curl_init')) {
  $c = curl_init($url);
  curl_setopt_array($c, [CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 40, CURLOPT_FOLLOWLOCATION => true]);
  $body = curl_exec($c); $code = (int)curl_getinfo($c, CURLINFO_HTTP_CODE); curl_close($c);
} else {
  $ctx = stream_context_create(['http' => ['timeout' => 40, 'ignore_errors' => true]]);
  $body = @file_get_contents($url, false, $ctx);
  if (isset($http_response_header[0]) && preg_match('/\s(\d{3})\s/', $http_response_header[0], $m)) $code = (int)$m[1];
}
if ($body === false || $code === 0) { http_response_code(502); echo '{"message":"Sem resposta do PVGIS"}'; exit; }
http_response_code($code);
if ($code === 200) { @mkdir($dir, 0700, true); @file_put_contents($file, $body); }
header('Cache-Control: max-age=86400');
echo $body;
