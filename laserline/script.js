// Конфигуратор «Марка → Модель → Серия». Данные — заглушки до получения списка у клиента.
const DATA = {
  "Bystronic": ["ByStar Fiber 3015", "ByStar Fiber 4020", "BySprint Fiber 3015"],
  "Trumpf": ["TruLaser 3030", "TruLaser 5030", "TruLaser 3060"],
  "Bodor": ["Bodor i5 3015", "Bodor P 3015", "Bodor C 3015"],
  "HSG Laser": ["GWEIKE LF3015", "GWEIKE LF4020", "GWEIKE LF6025"],
  "Han's Laser": ["G3015", "G4020", "G6025"]
};
const SERIES = {
  "Econom": "Тонколистовой металл, сухая резка",
  "Optimal": "Средние толщины, интенсивное производство",
  "Laserline Pro": "Толстолистовой металл, тяжёлая резка"
};
const state = {brand: "Bystronic", model: null, series: "Optimal"};
state.model = DATA[state.brand][0];

const $ = s => document.querySelector(s);
function chips(el, items, key, onPick){
  el.innerHTML = "";
  items.forEach(v => {
    const b = document.createElement("button");
    b.type = "button"; b.className = "chip"; b.textContent = v;
    b.setAttribute("aria-pressed", state[key] === v);
    b.onclick = () => { state[key] = v; onPick && onPick(); render(); };
    el.appendChild(b);
  });
}
function render(){
  chips($("#brands"), Object.keys(DATA), "brand", () => { state.model = DATA[state.brand][0]; });
  chips($("#models"), DATA[state.brand], "model");
  chips($("#series"), Object.keys(SERIES), "series");
  $("#r-title").textContent = `${state.brand} ${state.model} · ${state.series}`;
  $("#r-series").textContent = SERIES[state.series];
  const msg = `Комплект: ${state.brand} ${state.model}, серия ${state.series}`;
  $("#r-kp").href = "#request?kit=" + encodeURIComponent(msg);
  $("#r-kp").dataset.kit = msg;
}
$("#r-kp").addEventListener("click", e => {
  const f = $("#f-machine"); if (f) f.value = `${state.brand} ${state.model}`;
  const r = document.querySelector('input[name="kind"][value="calc"]'); if (r) r.checked = true;
  e.preventDefault(); $("#request").scrollIntoView({behavior: "smooth"});
});
render();

// Форма. Отправка пока не подключена к серверу/CRM — показываем подтверждение и пишем в консоль.
$("#lead").addEventListener("submit", e => {
  e.preventDefault();
  const data = Object.fromEntries(new FormData(e.target));
  console.info("Заявка Laserline:", data);
  e.target.style.display = "none";
  $("#ok").style.display = "block";
});
