<?php
// Приём заявок с формы. Замените адрес получателя и проверьте, что на хостинге работает mail().
$TO = 'info@example.com';           // ← ваш адрес
$SUBJECT = 'Заявка с сайта Laserline';
header('Content-Type: application/json; charset=utf-8');
$d = json_decode(file_get_contents('php://input'), true);
if (!is_array($d) || empty($d['name']) || empty($d['email']) || !filter_var($d['email'], FILTER_VALIDATE_EMAIL)) {
  http_response_code(400); echo '{"ok":false}'; exit;
}
$lines = [];
foreach ($d as $k => $v) { $lines[] = $k . ': ' . trim(strip_tags((string)$v)); }
$ok = mail($TO, '=?UTF-8?B?' . base64_encode($SUBJECT) . '?=', implode("\n", $lines),
  "Content-Type: text/plain; charset=utf-8\r\nReply-To: " . $d['email']);
http_response_code($ok ? 200 : 500); echo $ok ? '{"ok":true}' : '{"ok":false}';
