// Талисман: сова-штурман Хроня. Настроения: guide (по умолчанию), happy, cheer, think, sad.
// owl(mood, size) → строка с <svg>; owlAt(mood, x, y, size) → вложенный <svg> для карты.

function owlBody(mood) {
  const ink = "#2b1d12";
  const up = mood === "cheer";
  // Крылья
  const wings = up
    ? `<path d="M30 70Q8 52 14 28Q30 36 38 64Z" fill="#7d5028" stroke="${ink}" stroke-width="3" stroke-linejoin="round"/>
       <path d="M90 70Q112 52 106 28Q90 36 82 64Z" fill="#7d5028" stroke="${ink}" stroke-width="3" stroke-linejoin="round"/>`
    : `<path d="M27 68Q12 90 25 112Q37 104 39 80Z" fill="#7d5028" stroke="${ink}" stroke-width="3" stroke-linejoin="round"/>
       ${mood === "think"
         ? `<path d="M93 68Q104 82 82 96Q74 90 80 76Z" fill="#7d5028" stroke="${ink}" stroke-width="3" stroke-linejoin="round"/>`
         : `<path d="M93 68Q108 90 95 112Q83 104 81 80Z" fill="#7d5028" stroke="${ink}" stroke-width="3" stroke-linejoin="round"/>`}`;
  // Глаза
  let eyes, brows = "", extra = "";
  const eye = (cx, dx, dy) => `<circle cx="${cx}" cy="52" r="10.5" fill="#fffaf0" stroke="${ink}" stroke-width="2.6"/><circle cx="${cx + dx}" cy="${52 + dy}" r="5.2" fill="${ink}"/><circle cx="${cx + dx + 1.8}" cy="${50 + dy}" r="1.7" fill="#fff"/>`;
  const arc = cx => `<path d="M${cx - 9} 54Q${cx} 42 ${cx + 9} 54" fill="none" stroke="${ink}" stroke-width="4" stroke-linecap="round"/>`;
  if (mood === "happy" || mood === "cheer") {
    eyes = arc(46) + arc(74);
    extra = `<circle cx="34" cy="63" r="4.5" fill="#e8836b" opacity=".6"/><circle cx="86" cy="63" r="4.5" fill="#e8836b" opacity=".6"/>`;
    if (mood === "cheer") extra += `<path class="twinkle" d="M10 14l2.4 5.2 5.6.6-4.2 3.8 1.2 5.6-5-2.8-5 2.8 1.2-5.6-4.2-3.8 5.6-.6zM108 10l2 4.4 4.8.5-3.6 3.2 1 4.8-4.2-2.4-4.2 2.4 1-4.8-3.6-3.2 4.8-.5z" fill="#e3b04b" stroke="${ink}" stroke-width="1.6" stroke-linejoin="round"/>`;
  } else if (mood === "think") {
    eyes = `<g class="blink">${eye(46, 3, -3) + eye(74, 3, -3)}</g>`;
    brows = `<path d="M35 38Q46 30 57 37" fill="none" stroke="${ink}" stroke-width="3.2" stroke-linecap="round"/><path d="M63 40Q74 40 85 43" fill="none" stroke="${ink}" stroke-width="3.2" stroke-linecap="round"/>`;
    extra = `<text x="96" y="30" font-size="30" font-weight="800" font-family="Nunito,sans-serif" fill="#e3b04b" stroke="${ink}" stroke-width="1.6" paint-order="stroke">?</text>`;
  } else if (mood === "sad") {
    eyes = `<g class="blink">${eye(46, 0, 3) + eye(74, 0, 3)}</g>`;
    brows = `<path d="M35 42L56 35" fill="none" stroke="${ink}" stroke-width="3.2" stroke-linecap="round"/><path d="M64 35L85 42" fill="none" stroke="${ink}" stroke-width="3.2" stroke-linecap="round"/>`;
    extra = `<path d="M37 64q-3 6 0 9 3-3 0-9z" fill="#6fb3d9" stroke="${ink}" stroke-width="1.4"/>`;
  } else {
    eyes = `<g class="blink">${eye(46, 0, 0) + eye(74, 0, 0)}</g>`;
    // подзорная труба в правом крыле
    extra = `<g transform="rotate(-38 90 92)"><rect x="82" y="84" width="34" height="10" rx="3" fill="#c28f1f" stroke="${ink}" stroke-width="2.4"/><rect x="108" y="82" width="9" height="14" rx="2" fill="#8a5d2b" stroke="${ink}" stroke-width="2.4"/><rect x="92" y="84" width="3" height="10" fill="${ink}" opacity=".5"/></g>`;
  }
  return `
    <ellipse cx="60" cy="124" rx="28" ry="5" fill="rgba(0,0,0,.25)"/>
    <path d="M44 112l-4 8h14zM76 112l4 8H66z" fill="#e3b04b" stroke="${ink}" stroke-width="2.4" stroke-linejoin="round"/>
    <ellipse cx="60" cy="80" rx="34" ry="38" fill="#9a6a38" stroke="${ink}" stroke-width="3"/>
    <ellipse cx="60" cy="90" rx="22" ry="26" fill="#f0dcae"/>
    <path d="M46 78q4 5 8 0 4 5 8 0 4 5 8 0M42 91q4 5 8 0 4 5 8 0 4 5 8 0 4 5 8 0M46 104q4 5 8 0 4 5 8 0 4 5 8 0" fill="none" stroke="#b08c55" stroke-width="2" stroke-linecap="round"/>
    ${wings}
    <path d="M34 74Q60 90 86 74L84 84Q60 100 36 84Z" fill="#b4452f" stroke="${ink}" stroke-width="2.4" stroke-linejoin="round"/>
    <ellipse cx="60" cy="50" rx="35" ry="30" fill="#9a6a38" stroke="${ink}" stroke-width="3"/>
    <circle cx="46" cy="52" r="17" fill="#f0dcae" stroke="${ink}" stroke-width="2.4"/><circle cx="74" cy="52" r="17" fill="#f0dcae" stroke="${ink}" stroke-width="2.4"/>
    ${eyes}${brows}
    <path d="M60 54L53 64l7 8 7-8z" fill="#e3b04b" stroke="${ink}" stroke-width="2.3" stroke-linejoin="round"/>
    <path d="M24 34Q60 4 96 34L88 40Q60 22 32 40Z" fill="#262b66" stroke="${ink}" stroke-width="2.8" stroke-linejoin="round"/>
    <path d="M38 28Q60 -4 82 28Q60 18 38 28Z" fill="#262b66" stroke="${ink}" stroke-width="2.8" stroke-linejoin="round"/>
    <path d="M30 37Q60 21 90 37" fill="none" stroke="#e3b04b" stroke-width="2.4"/><circle cx="60" cy="11" r="3.4" fill="#e3b04b" stroke="${ink}" stroke-width="1.6"/>
    ${extra}`;
}
function owl(mood = "guide", size = 64, cls = "") {
  return `<svg class="owl ${cls}" viewBox="0 0 120 130" width="${size}" height="${Math.round(size * 130 / 120)}" aria-hidden="true">${owlBody(mood)}</svg>`;
}
function owlAt(mood, x, y, size) {
  return `<svg x="${x}" y="${y}" width="${size}" height="${Math.round(size * 130 / 120)}" viewBox="0 0 120 130" aria-hidden="true">${owlBody(mood)}</svg>`;
}
