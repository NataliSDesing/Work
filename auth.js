// Коды входа учеников. Код однозначно кодирует имя ученика, поэтому игре не нужен список класса
// и код работает на любом устройстве. Это не защита от взлома, а способ закрепить имя за учеником.

const NAME_ALPH = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЬЭЮЯ "; // 32 символа: 31 буква и пробел
const CODE_ALPH = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"; // 32 символа без похожих I, L, O, U
const CODE_KEYS = [7, 19, 3, 23, 11, 29, 5, 17, 13, 31, 2, 27, 9, 21, 25];
const NAME_MAX = 14;

function cleanName(s) {
  return String(s || "").toUpperCase().replace(/Ё/g, "Е").replace(/Ъ/g, "Ь").replace(/[.\-_,]/g, " ").replace(/\s+/g, " ").trim();
}
function titleName(clean) {
  return clean.split(" ").map(w => w.length === 1 ? w + "." : w[0] + w.slice(1).toLowerCase()).join(" ");
}
// Проверка имени перед выдачей кода: { ok, clean, name, error }
function checkName(s) {
  const clean = cleanName(s);
  if (!clean) return { ok: false, error: "пустое имя" };
  if (clean.length > NAME_MAX) return { ok: false, error: `длиннее ${NAME_MAX} знаков, сократите (например, «Аня К.»)` };
  for (const ch of clean) if (!NAME_ALPH.includes(ch)) return { ok: false, error: `буква «${ch}» не поддерживается, пишите по-русски` };
  return { ok: true, clean, name: titleName(clean) };
}
function nameToCode(s) {
  const r = checkName(s);
  if (!r.ok) return null;
  let out = "", sum = 0;
  [...r.clean].forEach((ch, i) => {
    const idx = NAME_ALPH.indexOf(ch);
    out += CODE_ALPH[(idx + CODE_KEYS[i] + i * 7) % 32];
    sum += (idx + 1) * (i + 3);
  });
  return out + CODE_ALPH[sum % 32];
}
function normCode(c) {
  return String(c || "").toUpperCase().replace(/O/g, "0").replace(/[IL]/g, "1").replace(/U/g, "V").replace(/[^0-9A-Z]/g, "");
}
// Расшифровка: { ok, id, name } или { ok: false }
function codeToName(c) {
  const code = normCode(c);
  if (code.length < 3 || code.length > NAME_MAX + 1) return { ok: false };
  let clean = "", sum = 0;
  for (let i = 0; i < code.length - 1; i++) {
    const v = CODE_ALPH.indexOf(code[i]);
    if (v < 0) return { ok: false };
    const idx = (((v - CODE_KEYS[i] - i * 7) % 32) + 32) % 32;
    clean += NAME_ALPH[idx];
    sum += (idx + 1) * (i + 3);
  }
  if (code[code.length - 1] !== CODE_ALPH[sum % 32]) return { ok: false };
  if (clean !== clean.trim() || /\s\s/.test(clean) || !/^[^ ]/.test(clean)) return { ok: false };
  return { ok: true, id: code, name: titleName(clean) };
}
function groupCode(code) {
  return normCode(code).replace(/(.{4})(?=.)/g, "$1-");
}
