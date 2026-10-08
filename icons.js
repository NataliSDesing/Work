// Нарисованные иконки (viewBox 48×48): тёмный контур, золото, пергамент.
// ico("ship", 40) → строка с <svg>; icoAt("ship", x, y, size) → вложенный <svg> для карты.

const ICON_PATHS = {
  ship: `<path d="M5 31h38l-6 10H11z" fill="#8a5d2b"/><path d="M24 7v24"/><path d="M25 9l14 17H25z" fill="#f6e9c8"/><path d="M23 13L10 27h13z" fill="#f6e9c8"/><path d="M24 7l7 2-7 2z" fill="#b4452f"/><path d="M3 44q5-3 10 0t10 0 10 0 10 0" fill="none" stroke="#2f7f86"/>`,
  anchor: `<circle cx="24" cy="9" r="3.5" fill="none"/><path d="M24 12.5V40M16 18h16" fill="none"/><path d="M8 28q3 12 16 12t16-12" fill="none"/><path d="M8 28l-3 5 7-1zM40 28l3 5-7-1z" fill="#e3b04b"/>`,
  compass: `<circle cx="24" cy="24" r="17" fill="#f6e9c8"/><circle cx="24" cy="24" r="13" fill="none" stroke-width="1.2"/><path d="M24 9l6 15H18z" fill="#b4452f"/><path d="M18 24h12l-6 15z" fill="#b8c0c8"/><circle cx="24" cy="24" r="2.6" fill="#e3b04b"/>`,
  scroll: `<rect x="11" y="8" width="26" height="30" rx="2" fill="#f6e9c8"/><path d="M16 18h16M16 24h16M16 30h10" stroke-width="1.6"/><rect x="8" y="5" width="32" height="6" rx="3" fill="#e3b04b"/><rect x="8" y="35" width="32" height="6" rx="3" fill="#e3b04b"/>`,
  book: `<path d="M24 12q-8-4-17-2v27q9-2 17 2 8-4 17-2V10q-9-2-17 2z" fill="#f6e9c8"/><path d="M24 12v27"/><path d="M12 18q5-1 9 1M12 24q5-1 9 1M27 19q4-2 9-1M27 25q4-2 9-1" fill="none" stroke-width="1.4"/>`,
  crown: `<path d="M7 36L9 14l10 10 5-14 5 14 10-10 2 22z" fill="#e3b04b"/><rect x="7" y="36" width="34" height="6" rx="1.5" fill="#c28f1f"/><circle cx="9" cy="13" r="2.6" fill="#b4452f"/><circle cx="24" cy="9" r="2.6" fill="#b4452f"/><circle cx="39" cy="13" r="2.6" fill="#b4452f"/>`,
  sword: `<g transform="rotate(45 24 24)"><path d="M24 2l4.5 7v21h-9V9z" fill="#b8c0c8"/><rect x="13" y="30" width="22" height="4.5" rx="2.2" fill="#e3b04b"/><rect x="21.5" y="34.5" width="5" height="8" fill="#8a5d2b"/><circle cx="24" cy="44" r="2.6" fill="#e3b04b"/></g>`,
  shield: `<path d="M24 5l16 5v13q0 13-16 20Q8 36 8 23V10z" fill="#3a4290"/><path d="M24 12v24M15 21h18" stroke="#e3b04b" stroke-width="4"/>`,
  castle: `<rect x="10" y="22" width="28" height="20" fill="#c9b99a"/><rect x="5" y="14" width="11" height="28" fill="#d9ccae"/><rect x="32" y="14" width="11" height="28" fill="#d9ccae"/><path d="M5 14h3v-3h2v3h2v-3h2v3h2M32 14h3v-3h2v3h2v-3h2v3h2" fill="none" stroke-width="1.8"/><path d="M19 42V33a5 5 0 0110 0v9z" fill="#5b4630"/><path d="M10 8v6" /><path d="M10 8l6 2-6 2z" fill="#b4452f"/>`,
  coin: `<circle cx="24" cy="24" r="17" fill="#e3b04b"/><circle cx="24" cy="24" r="12" fill="none" stroke-width="1.5"/><path d="M24 15l2.6 6 6.4.4-5 4.2 1.7 6.3-5.7-3.5-5.7 3.5 1.7-6.3-5-4.2 6.4-.4z" fill="#f6e9c8" stroke-width="1.4"/>`,
  flag: `<path d="M11 6v38"/><path d="M11 8q8-5 15 0t13 0v16q-6 5-13 0t-15 0z" fill="#b4452f"/>`,
  globe: `<circle cx="24" cy="22" r="16" fill="#3a8fa6"/><path d="M14 14q6-4 9 1t-3 8-7-1zM28 24q6-3 8 3t-4 8-5-5z" fill="#4f8a3e" stroke-width="1.4"/><path d="M14 43h20M24 38v5"/>`,
  map: `<path d="M5 12l12-4 14 4 12-4v28l-12 4-14-4-12 4z" fill="#f6e9c8"/><path d="M17 8v28M31 12v28" stroke-width="1.4"/><path d="M10 28q6-8 12-2t14-8" fill="none" stroke="#b4452f" stroke-dasharray="3 3" stroke-width="1.8"/><path d="M34 21l5 5m0-5l-5 5" stroke="#b4452f"/>`,
  quill: `<path d="M41 5C27 7 17 18 14 34l6-6c6-1 14-8 21-23z" fill="#f6e9c8"/><path d="M14 34L8 43"/><path d="M20 28L33 14" stroke-width="1.2"/>`,
  wheat: `<path d="M24 44V14"/><path d="M24 14c-5-2-6-6-5-9 5 1 6 5 5 9zM24 14c5-2 6-6 5-9-5 1-6 5-5 9zM24 24c-6-1-8-5-7-8 6 0 8 4 7 8zM24 24c6-1 8-5 7-8-6 0-8 4-7 8zM24 34c-6-1-8-5-7-8 6 0 8 4 7 8zM24 34c6-1 8-5 7-8-6 0-8 4-7 8z" fill="#e3b04b"/>`,
  sack: `<path d="M17 12h14l-3 5c8 3 12 10 12 17 0 7-6 10-16 10S8 41 8 34c0-7 4-14 12-17z" fill="#c9a36a"/><path d="M17 12q7 4 14 0"/><circle cx="19" cy="32" r="2.2" fill="#b4452f"/><circle cx="28" cy="35" r="2.2" fill="#b4452f"/><circle cx="27" cy="27" r="2.2" fill="#e3b04b"/>`,
  cross: `<path d="M20 6h8v12h12v8H28v18h-8V26H8v-8h12z" fill="#e3b04b"/>`,
  mountain: `<path d="M3 41L17 14l8 14 6-8 14 21z" fill="#8a97a6"/><path d="M13 22l4-8 4 8-4-2z" fill="#f6e9c8"/><path d="M31 20v-9"/><path d="M31 11l7 2-7 2z" fill="#b4452f"/>`,
  skull: `<path d="M6 5v39"/><rect x="6" y="8" width="35" height="24" rx="2" fill="#2b1d12"/><circle cx="24" cy="18" r="7" fill="#f6e9c8" stroke="none"/><rect x="20.5" y="23" width="7" height="5" fill="#f6e9c8" stroke="none"/><circle cx="21" cy="18" r="2" fill="#2b1d12" stroke="none"/><circle cx="27" cy="18" r="2" fill="#2b1d12" stroke="none"/>`,
  tree: `<path d="M21 44l1-14h4l1 14z" fill="#8a5d2b"/><circle cx="24" cy="18" r="9" fill="#4f8a3e"/><circle cx="16" cy="25" r="7" fill="#4f8a3e"/><circle cx="32" cy="25" r="7" fill="#4f8a3e"/>`,
  leaf: `<path d="M24 5l3 8 7-3-2 9 8-2-5 8 4 3-9 3 1 9-7-5-7 5 1-9-9-3 4-3-5-8 8 2-2-9 7 3z" fill="#b4452f" transform="translate(0 -2) scale(1 .95)"/><path d="M24 30v13"/>`,
  potato: `<path d="M8 28c0-9 8-15 18-15 9 0 15 6 14 14-1 9-9 13-19 12C14 38 8 34 8 28z" fill="#c9a36a"/><circle cx="19" cy="24" r="1.6" fill="#8a5d2b" stroke="none"/><circle cx="29" cy="20" r="1.6" fill="#8a5d2b" stroke="none"/><circle cx="31" cy="30" r="1.6" fill="#8a5d2b" stroke="none"/><circle cx="21" cy="33" r="1.6" fill="#8a5d2b" stroke="none"/>`,
  gear: `<g fill="#b8c0c8"><rect x="21" y="4" width="6" height="9" rx="1"/><rect x="21" y="4" width="6" height="9" rx="1" transform="rotate(45 24 24)"/><rect x="21" y="4" width="6" height="9" rx="1" transform="rotate(90 24 24)"/><rect x="21" y="4" width="6" height="9" rx="1" transform="rotate(135 24 24)"/><rect x="21" y="4" width="6" height="9" rx="1" transform="rotate(180 24 24)"/><rect x="21" y="4" width="6" height="9" rx="1" transform="rotate(225 24 24)"/><rect x="21" y="4" width="6" height="9" rx="1" transform="rotate(270 24 24)"/><rect x="21" y="4" width="6" height="9" rx="1" transform="rotate(315 24 24)"/><circle cx="24" cy="24" r="14"/></g><circle cx="24" cy="24" r="5.5" fill="#5b4630"/>`,
  bank: `<path d="M4 18L24 6l20 12z" fill="#e3b04b"/><rect x="8" y="20" width="5" height="16" fill="#f6e9c8"/><rect x="17" y="20" width="5" height="16" fill="#f6e9c8"/><rect x="26" y="20" width="5" height="16" fill="#f6e9c8"/><rect x="35" y="20" width="5" height="16" fill="#f6e9c8"/><rect x="5" y="37" width="38" height="5" fill="#d9ccae"/>`,
  chains: `<g fill="none"><rect x="6" y="14" width="24" height="14" rx="7" stroke="#2b1d12" stroke-width="6"/><rect x="18" y="22" width="24" height="14" rx="7" stroke="#2b1d12" stroke-width="6"/><rect x="6" y="14" width="24" height="14" rx="7" stroke="#b8c0c8" stroke-width="2.4"/><rect x="18" y="22" width="24" height="14" rx="7" stroke="#b8c0c8" stroke-width="2.4"/></g>`,
  scales: `<path d="M24 8v32M12 41h24"/><path d="M8 14h32"/><path d="M8 14l-5 13q5 5 10 0zM40 14l-5 13q5 5 10 0z" fill="#e3b04b"/><circle cx="24" cy="8" r="2.6" fill="#e3b04b"/>`,
  hat: `<path d="M3 31L13 13h22l10 18-21 8z" fill="#2f3566"/><path d="M13 13l11 26M35 13L24 39" stroke-width="1.2"/><circle cx="24" cy="28" r="3.2" fill="#e3b04b"/>`,
  calendar: `<rect x="7" y="9" width="34" height="33" rx="4" fill="#f6e9c8"/><path d="M7 21h34"/><path d="M7 13a4 4 0 014-4h26a4 4 0 014 4v8H7z" fill="#b4452f"/><path d="M16 5v7M32 5v7"/><text x="24" y="37" text-anchor="middle" font-size="14" font-weight="800" fill="#2b1d12" stroke="none" font-family="Nunito,sans-serif">15</text>`,
  eagle: `<path d="M21 22L3 14l5 10-3 7 13-3zM27 22l18-8-5 10 3 7-13-3z" fill="#e3b04b"/><path d="M24 20l6 6-3 13h-6l-3-13z" fill="#2f3566"/><circle cx="19" cy="14" r="3.6" fill="#e3b04b"/><circle cx="29" cy="14" r="3.6" fill="#e3b04b"/><path d="M15 14l-4-1 4 3zM33 14l4-1-4 3z" fill="#b4452f"/><path d="M20 17l2.5 5M28 17l-2.5 5"/><path d="M21 9l1.5 2 1.5-3 1.5 3 1.5-2v3h-6z" fill="#e3b04b" stroke-width="1.4"/>`,
  palette: `<path d="M24 6C12 6 5 14 5 24c0 9 7 16 16 16 4 0 4-3 2-5-2-3 0-6 4-6h7c5 0 9-3 9-8C43 12 35 6 24 6z" fill="#e5d1a1"/><circle cx="14" cy="22" r="3" fill="#b4452f"/><circle cx="21" cy="14" r="3" fill="#e3b04b"/><circle cx="31" cy="14" r="3" fill="#2f7f86"/><circle cx="36" cy="22" r="3" fill="#4f8a3e"/>`,
  fork: `<path d="M24 44V20" stroke-width="3.4"/><path d="M12 8v12q0 6 12 6t12-6V8M24 8v18" fill="none" stroke-width="3.2"/>`,
  dome: `<path d="M8 38v-8a16 16 0 0132 0v8z" fill="#e3b04b"/><path d="M24 6v8"/><path d="M24 6l4 2-4 2z" fill="#b4452f"/><rect x="5" y="38" width="38" height="5" fill="#f6e9c8"/><rect x="1.5" y="18" width="5" height="24" fill="#f6e9c8"/><rect x="41.5" y="18" width="5" height="24" fill="#f6e9c8"/><path d="M1.5 18L4 11l2.5 7zM41.5 18l2.5-7 2.5 7z" fill="#e3b04b"/>`,
  barrel: `<path d="M12 7h24q5 17 0 34H12q-5-17 0-34z" fill="#a8743a"/><path d="M12.5 15h23M12.5 33h23M11.5 24h25" fill="none"/>`,
  chart: `<path d="M6 6v36h36" fill="none"/><path d="M10 34l10-10 7 6 13-16" fill="none" stroke="#b4452f" stroke-width="3.4"/><path d="M32 14h8v8" fill="none" stroke="#b4452f" stroke-width="3.4"/>`,
  flame: `<path d="M24 4c3 8 12 12 12 24a12 12 0 01-24 0c0-6 3-9 6-12 0 4 2 5 4 5-2-6 0-12 2-17z" fill="#e8883a"/><path d="M24 25c2 4 6 6 6 10a6 6 0 01-12 0c0-3 2-5 4-6z" fill="#f4d37a" stroke="none"/>`,
  star: `<path d="M24 4l6 13 14 1.5-10.5 9.5 3 14L24 34.5 11.5 42l3-14L4 18.5 18 17z" fill="#e3b04b"/>`,
  lock: `<rect x="10" y="21" width="28" height="21" rx="4" fill="#c9a36a"/><path d="M16 21v-6a8 8 0 0116 0v6" fill="none"/><circle cx="24" cy="31" r="3" fill="#2b1d12"/>`,
  hammer: `<path d="M24 20v23" stroke-width="5.5"/><path d="M24 20v23" stroke="#a8743a" stroke-width="2.6"/><rect x="8" y="7" width="26" height="12" rx="2.5" fill="#8a97a6"/><path d="M34 9l6 3-6 5z" fill="#8a97a6"/>`,
  lighthouse: `<path d="M17 43l3-27h8l3 27z" fill="#f6e9c8"/><path d="M18.4 30h11.2l.9 8H17.5zM19.7 18.5h8.6l.5 5H19.2z" fill="#b4452f" stroke="none"/><rect x="17" y="10" width="14" height="7" fill="#e3b04b"/><path d="M15 10h18L24 4z" fill="#8a97a6"/><path d="M4 43h40"/>`,
  stall: `<path d="M7 20h34l-3-9H10z" fill="#b4452f"/><path d="M7 20q4 5 8.5 0 4 5 8.5 0 4 5 8.5 0 4 5 8.5 0" fill="#f6e9c8"/><path d="M10 24v18M38 24v18"/><rect x="10" y="32" width="28" height="5" fill="#a8743a"/><circle cx="18" cy="29" r="3" fill="#e3b04b"/><circle cx="26" cy="29" r="3" fill="#b4452f"/><circle cx="33" cy="29" r="3" fill="#4f8a3e"/>`,
  seal: `<circle cx="24" cy="24" r="16" fill="#b4452f"/><circle cx="24" cy="24" r="11" fill="none" stroke-width="1.6"/><path d="M24 14v20M14 24h20" stroke-width="1.6"/>`,
  help: `<circle cx="24" cy="24" r="17" fill="#e3b04b"/><path d="M18 19q0-6 6-6t6 5q0 4-6 7v3" fill="none" stroke-width="3"/><circle cx="24" cy="36" r="2" fill="#2b1d12"/>`
};

function ico(key, size = 40, cls = "") {
  const p = ICON_PATHS[key] || ICON_PATHS.star;
  return `<svg class="ico ${cls}" viewBox="0 0 48 48" width="${size}" height="${size}" aria-hidden="true"><g stroke="#2b1d12" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round" fill="none">${p}</g></svg>`;
}
function icoAt(key, x, y, size) {
  const p = ICON_PATHS[key] || ICON_PATHS.star;
  return `<svg x="${x}" y="${y}" width="${size}" height="${size}" viewBox="0 0 48 48" aria-hidden="true"><g stroke="#2b1d12" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round" fill="none">${p}</g></svg>`;
}

// Какой значок у какой миссии и карточки.
const MISSION_ICON = { m0: "dome", m1: "anchor", m2: "sword", m2b: "flag", m3: "coin", m3b: "crown", m4: "scroll", m5: "eagle", m6: "castle" };
const CARD_ICON = {
  constantinople: "dome", gutenberg: "book", renaissance: "palette",
  henry: "compass", dias: "mountain", columbus: "ship", gama: "sack", vespucci: "map", magellan: "globe", caravel: "ship",
  albuquerque: "castle", cortes: "sword", pizarro: "coin", lascasas: "cross", drake: "skull",
  company: "barrel", virginia: "tree", champlain: "leaf", exchange: "potato",
  revprice: "chart", mercantilism: "scales", manufactory: "gear", agrarian: "wheat", serfdom: "chains",
  absolutism: "crown", estates: "scales", comenius: "book", fashion: "hat",
  luther: "scroll", calvin: "book", loyola: "shield", gregorian: "calendar",
  peasantwar: "fork", mohacs: "sword", vienna: "castle", elector: "eagle",
  charles5: "crown", philip2: "quill", escorial: "castle", armada: "ship"
};
