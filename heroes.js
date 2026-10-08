// Карточки исторических героев: портрет, звёзды значимости, ранг, характеристики и достижения.
// Факты взяты из учебника «Всеобщая история. История Нового времени», 7 класс (Мединский, Торкунов),
// спорные детали сверены с открытыми источниками. Оценки характеристик придуманы для игры.

const STAT_KINDS = {
  explorer: [["Мореходство", "ship"], ["Смелость", "sword"], ["Упорство", "mountain"], ["Знания", "book"], ["Везение", "star"], ["Слава", "crown"]],
  conq: [["Смелость", "sword"], ["Хитрость", "scales"], ["Власть", "crown"], ["Упорство", "mountain"], ["Везение", "star"], ["Слава", "flag"]],
  ruler: [["Власть", "crown"], ["Дипломатия", "scales"], ["Богатство", "coin"], ["Армия", "shield"], ["Культура", "palette"], ["Влияние", "flag"]],
  thinker: [["Знания", "book"], ["Харизма", "star"], ["Упорство", "mountain"], ["Влияние", "flag"], ["Смелость", "sword"], ["Наследие", "scroll"]],
  maker: [["Знания", "book"], ["Мастерство", "hammer"], ["Упорство", "mountain"], ["Идеи", "star"], ["Влияние", "flag"], ["Наследие", "scroll"]]
};
const TIERS = { 5: "S", 4: "A", 3: "B" };

const HEROES = [
  { id: "gutenberg", m: "m0", name: "Иоганн Гутенберг", tags: "изобретатель · печатник · Майнц", years: "ок. 1400 — 1468", country: "Германия", cls: "Изобретатель", era: "XV век", kind: "maker", stars: 5,
    s: [80, 95, 85, 95, 95, 100],
    ach: [{ i: "book", h: "Печатный станок", t: "Около 1450 года начал печатать книги подвижными литерами." }, { i: "scroll", h: "Дешёвые книги", t: "Книги стали делать быстрее и дешевле." }, { i: "flag", h: "Идеи без границ", t: "Новые идеи быстро разошлись по Европе." }],
    line: "Майнц, около 1450 года: начало эпохи печатной книги.",
    face: { skin: "#f0c9a0", hair: "#8a7a62", hs: "long", beard: ["long"], hat: "cap", hatc: "#6b4a2b", robe: "#6b4a2b", collar: "plain", bg: "workshop" } },

  { id: "henry", m: "m1", name: "Энрике Мореплаватель", tags: "принц Португалии · организатор плаваний", years: "1394 — 1460", country: "Португалия", cls: "Организатор", era: "XV век", kind: "explorer", stars: 4,
    s: [40, 60, 95, 85, 80, 85],
    ach: [{ i: "ship", h: "Корабли на юг", t: "Отправлял корабли вдоль берегов Африки." }, { i: "coin", h: "Золото и слоновая кость", t: "Португальцы торговали с землями к югу от Сахары." }, { i: "compass", h: "Страх побеждён", t: "Его капитаны шли на юг вопреки суевериям." }],
    line: "Он отправлял корабли вдоль Африки, и путь на Восток стал короче.",
    face: { skin: "#f0c9a0", hair: "#3b2a1b", hs: "short", beard: [], hat: "cap", hatc: "#7a2a2a", robe: "#7a2a2a", collar: "chain", bg: "sea" } },

  { id: "dias", m: "m1", name: "Бартоломеу Диаш", tags: "мореплаватель · мыс Доброй Надежды", years: "ок. 1450 — 1500", country: "Португалия", cls: "Первооткрыватель", era: "XV век", kind: "explorer", stars: 3,
    s: [90, 85, 80, 70, 60, 65],
    ach: [{ i: "mountain", h: "Южный край Африки", t: "В 1488 году достиг южной оконечности материка." }, { i: "compass", h: "Мыс Доброй Надежды", t: "Название дали в надежде на путь в Индию." }, { i: "ship", h: "Дорога открыта", t: "Его плавание подготовило экспедицию Васко да Гамы." }],
    line: "В 1488 году европейцы впервые обогнули Африку с юга.",
    face: { skin: "#e8b98a", hair: "#3b2a1b", hs: "short", beard: ["mustache"], hat: "cap", hatc: "#262b66", robe: "#3b5a7a", collar: "plain", bg: "sea" } },

  { id: "gama", m: "m1", name: "Васко да Гама", tags: "мореплаватель · путь в Индию", years: "умер в 1524", country: "Португалия", cls: "Первооткрыватель", era: "XV–XVI века", kind: "explorer", stars: 4,
    s: [95, 90, 90, 70, 75, 90],
    ach: [{ i: "sack", h: "Путь в Индию", t: "В 1498 году корабли пришли к берегам Индии." }, { i: "ship", h: "Три плавания", t: "Побывал в Индии в 1497–98, 1502 и 1524 годах." }, { i: "coin", h: "Пряности", t: "Привёз их образцы, и его встречали как героя." }],
    line: "Почти четыре века торговля с Азией шла его путём.",
    face: { skin: "#e8b98a", hair: "#2b1d12", hs: "short", beard: ["goatee", "mustache"], hat: "beret", hatc: "#8e3220", robe: "#8e3220", collar: "cross", bg: "ship" } },

  { id: "columbus", m: "m1", name: "Христофор Колумб", tags: "мореплаватель · адмирал · Новый Свет", years: "1451 — 1506", country: "Испания (родом из Генуи)", cls: "Первооткрыватель", era: "XV век", kind: "explorer", stars: 5,
    s: [85, 95, 95, 60, 70, 100],
    ach: [{ i: "ship", h: "Через Атлантику", t: "12 октября 1492 года достиг Багамских островов." }, { i: "map", h: "Куба и Гаити", t: "В первом плавании открыл эти острова." }, { i: "compass", h: "Четыре плавания", t: "Ещё трижды плавал за океан, открыл Антильские острова." }],
    line: "Искал Индию, а открыл для Европы Новый Свет.",
    face: { skin: "#f3d2b0", hair: "#d8d0c0", hs: "long", beard: [], hat: "none", robe: "#5b3f8f", collar: "chain", bg: "ship" } },

  { id: "vespucci", m: "m1", name: "Америго Веспуччи", tags: "мореплаватель · учёный · Италия", years: "1454 — 1512", country: "Италия", cls: "Первооткрыватель", era: "XV–XVI века", kind: "explorer", stars: 3,
    s: [80, 70, 80, 90, 75, 85],
    ach: [{ i: "globe", h: "Новый Свет", t: "Первым прямо заявил, что это новая часть света." }, { i: "scroll", h: "Яркие письма", t: "Его письма были очень популярны в Европе." }, { i: "map", h: "Имя на карте", t: "В его честь назвали Америку." }],
    line: "Материк назвали Америкой, а не Колумбией.",
    face: { skin: "#e8b98a", hair: "#3b2a1b", hs: "curly", beard: ["mustache"], hat: "none", robe: "#2f7f86", collar: "plain", bg: "map" } },

  { id: "magellan", m: "m1", name: "Фернан Магеллан", tags: "мореплаватель · первое кругосветное плавание", years: "ок. 1480 — 1521", country: "Португалия, на службе Испании", cls: "Первооткрыватель", era: "XVI век", kind: "explorer", stars: 5,
    s: [100, 95, 100, 75, 40, 95],
    ach: [{ i: "globe", h: "Пролив Магеллана", t: "Нашёл проход в Южное море." }, { i: "ship", h: "Тихий океан", t: "Пересёк океан и дал ему это имя." }, { i: "flag", h: "Вокруг Земли", t: "Его экспедиция впервые обогнула планету (1519–1522)." }],
    line: "Сам погиб на Филиппинах, но «Виктория» вернулась домой.",
    face: { skin: "#e8b98a", hair: "#2b1d12", hs: "short", beard: ["short"], hat: "beret", hatc: "#262b66", robe: "#262b66", collar: "plain", bg: "sea" } },

  { id: "barents", m: "m1", name: "Виллем Баренц", tags: "мореплаватель · Арктика · Нидерланды", years: "ок. 1550 — 1597", country: "Нидерланды", cls: "Первооткрыватель", era: "XVI век", kind: "explorer", stars: 3,
    s: [85, 90, 100, 70, 35, 65],
    ach: [{ i: "mountain", h: "Три экспедиции", t: "В 1594–1596 годах искал северо-восточный путь в Азию." }, { i: "flame", h: "Зимовка на Новой Земле", t: "Пережил первую в истории полярную зимовку." }, { i: "ship", h: "Помощь поморов", t: "Русские поморы помогли его спутникам вернуться домой." }],
    line: "Его зимовье нашли только в 1871 году.",
    face: { skin: "#f0c9a0", hair: "#b08c55", hs: "long", beard: ["short"], hat: "cap", hatc: "#8a8a8a", robe: "#4a6a7a", collar: "fur", bg: "ice" } },

  { id: "isabella", m: "m1", name: "Изабелла I Кастильская", tags: "королева · Католические короли", years: "1451 — 1504", country: "Испания", cls: "Правитель", era: "XV век", kind: "ruler", stars: 5, female: true,
    s: [90, 90, 70, 85, 75, 95],
    ach: [{ i: "crown", h: "Единая Испания", t: "Вместе с Фернандо объединила страну." }, { i: "sword", h: "Конец Реконкисты", t: "Вместе с мужем завершила изгнание мавров с полуострова." }, { i: "ship", h: "Корабли для Колумба", t: "Согласилась снарядить его экспедицию." }],
    line: "Папа дал ей и Фернандо титул Католических королей.",
    face: { skin: "#f3d2b0", hair: "#8a4a1a", hs: "long", beard: [], hat: "crown", robe: "#b4452f", collar: "chain", bg: "court", f: true } },

  { id: "albuquerque", m: "m2", name: "Афонсу д’Албукерке", tags: "вице-король · Португальская Индия", years: "ок. 1453 — 1515", country: "Португалия", cls: "Вице-король", era: "XVI век", kind: "conq", stars: 3,
    s: [90, 85, 90, 85, 70, 80],
    ach: [{ i: "flag", h: "Вице-король", t: "Управлял португальскими владениями на Востоке в 1509–1515 годах." }, { i: "castle", h: "Гоа", t: "Захватил город и сделал его своей резиденцией." }, { i: "ship", h: "Контроль над морем", t: "Строил мощные крепости на морских путях." }],
    line: "Главная опора могущества Португалии на Востоке.",
    face: { skin: "#dcae80", hair: "#2b1d12", hs: "short", beard: ["long"], hat: "beret", hatc: "#3b3a46", robe: "#3b3a46", collar: "cross", bg: "fort" } },

  { id: "cortes", m: "m2", name: "Эрнан Кортес", tags: "конкистадор · Мексика", years: "1485 — 1547", country: "Испания", cls: "Конкистадор", era: "XVI век", kind: "conq", stars: 4,
    s: [90, 90, 85, 80, 75, 85],
    ach: [{ i: "sword", h: "Небольшой отряд", t: "В 1519 году высадился примерно с 500 людьми." }, { i: "castle", h: "Теночтитлан", t: "В 1521 году взял столицу ацтеков." }, { i: "scales", h: "Союзники", t: "Использовал вражду племён, ненавидевших ацтеков." }],
    line: "На месте Теночтитлана вырос Мехико.",
    face: { skin: "#e8b98a", hair: "#2b1d12", hs: "short", beard: ["mustache", "short"], hat: "morion", robe: "#5b5b66", collar: "plain", bg: "fort" } },

  { id: "pizarro", m: "m2", name: "Франсиско Писарро", tags: "конкистадор · держава инков", years: "ок. 1475 — 1541", country: "Испания", cls: "Конкистадор", era: "XVI век", kind: "conq", stars: 4,
    s: [85, 85, 80, 85, 70, 80],
    ach: [{ i: "mountain", h: "Держава инков", t: "В 1532–1535 годах завоевал её." }, { i: "coin", h: "Огромный выкуп", t: "За правителя Атауальпу получил свыше 6 тонн золота и серебра." }, { i: "castle", h: "Лима", t: "Основал город Лиму." }],
    line: "«Это стóит Перу!» — говорили в Испании.",
    face: { skin: "#dcae80", hair: "#8a8a8a", hs: "short", beard: ["long"], hat: "morion", robe: "#6b4a2b", collar: "plain", bg: "fort" } },

  { id: "lascasas", m: "m2", name: "Бартоломе де Лас Касас", tags: "монах · защитник индейцев", years: "1484 — 1566", country: "Испания", cls: "Защитник", era: "XVI век", kind: "thinker", stars: 4,
    s: [85, 85, 95, 80, 90, 90],
    ach: [{ i: "cross", h: "«Апостол индейцев»", t: "Прозван так за защиту их прав." }, { i: "book", h: "Способны к вере", t: "Доказывал, что индейцы способны принять христианство." }, { i: "scroll", h: "Закон короля", t: "Под его влиянием король запретил делать индейцев рабами." }],
    line: "Он спорил с конкистадорами и добился защиты для индейцев.",
    face: { skin: "#f0c9a0", hair: "#d0d0d0", hs: "bald", beard: [], hat: "none", robe: "#f0e6d0", collar: "cross", bg: "church" } },

  { id: "drake", m: "m2", name: "Фрэнсис Дрейк", tags: "корсар · Англия · кругосветное плавание", years: "ок. 1540 — 1596", country: "Англия", cls: "Корсар", era: "XVI век", kind: "explorer", stars: 4,
    s: [90, 95, 85, 75, 80, 90],
    ach: [{ i: "globe", h: "Кругосветка 1577–1580", t: "Второе после Магеллана кругосветное плавание." }, { i: "coin", h: "Сокровища Перу", t: "Захватил корабль, нагруженный сокровищами." }, { i: "sword", h: "Рыцарь на палубе", t: "Елизавета I посвятила его в рыцари на борту корабля." }],
    line: "Самый удачливый корсар своего времени.",
    face: { skin: "#f0c9a0", hair: "#b4693a", hs: "short", beard: ["goatee", "mustache"], hat: "beret", hatc: "#262b66", feather: true, robe: "#8e3220", collar: "ruff", bg: "ship" } },

  { id: "champlain", m: "m2b", name: "Самюэль де Шамплен", tags: "путешественник · учёный · Канада", years: "ок. 1574 — 1635", country: "Франция", cls: "Первооткрыватель", era: "XVII век", kind: "explorer", stars: 3,
    s: [80, 80, 90, 90, 70, 75],
    ach: [{ i: "leaf", h: "Квебек", t: "Основал город в 1608 году." }, { i: "map", h: "Точные карты", t: "Составил описания и карты открытых земель." }, { i: "flag", h: "Друзья среди племён", t: "Подружился с частью индейских племён." }],
    line: "Квебек стал столицей французской Канады.",
    face: { skin: "#f0c9a0", hair: "#6b4a2b", hs: "long", beard: ["goatee", "mustache"], hat: "beret", hatc: "#2f5a8a", robe: "#2f5a8a", collar: "plain", bg: "forest" } },

  { id: "elizabeth", m: "m2b", name: "Елизавета I", tags: "королева Англии · «королева-дева»", years: "1533 — 1603", country: "Англия", cls: "Правитель", era: "XVI век", kind: "ruler", stars: 5, female: true,
    s: [90, 90, 80, 80, 85, 95],
    ach: [{ i: "tree", h: "Виргиния", t: "Колонию назвали в её честь." }, { i: "skull", h: "Доля добычи", t: "Получила немалую часть добычи Дрейка." }, { i: "crown", h: "Рыцарь Дрейк", t: "Сама посвятила его в рыцари." }],
    line: "Виргиния названа в честь «королевы-девы».",
    face: { skin: "#fffaf0", hair: "#c4561f", hs: "long", beard: [], hat: "crown", robe: "#d9a62c", collar: "ruff", bg: "court", f: true } },

  { id: "comenius", m: "m3b", name: "Ян Амос Коменский", tags: "педагог · мыслитель · Чехия", years: "1592 — 1670", country: "Чехия", cls: "Просветитель", era: "XVII век", kind: "thinker", stars: 4,
    s: [100, 80, 90, 85, 70, 100],
    ach: [{ i: "book", h: "Основатель педагогики", t: "Его считают основателем современной педагогики." }, { i: "calendar", h: "Уроки", t: "Предложил поурочное обучение." }, { i: "palette", h: "Наглядность", t: "Выступал за повозрастной и наглядный методы." }],
    line: "Школьная программа и классы по возрасту появились при нём.",
    face: { skin: "#f0c9a0", hair: "#b0b0b0", hs: "long", beard: ["short"], hat: "cap", hatc: "#1d1611", robe: "#3b3a46", collar: "plain", bg: "workshop" } },

  { id: "luther", m: "m4", name: "Мартин Лютер", tags: "реформатор · священник · Виттенберг", years: "1483 — 1546", country: "Германия", cls: "Реформатор", era: "XVI век", kind: "thinker", stars: 5,
    s: [90, 95, 95, 100, 95, 100],
    ach: [{ i: "scroll", h: "Против индульгенций", t: "В 1517 году выступил против их продажи." }, { i: "book", h: "Библия по-немецки", t: "Перевёл Священное Писание на немецкий язык." }, { i: "shield", h: "«На том я стою»", t: "В Вормсе в 1521 году отказался отречься." }],
    line: "Его выступление положило начало Реформации.",
    face: { skin: "#f0c9a0", hair: "#4a3a28", hs: "short", beard: [], hat: "beret", hatc: "#1d1611", robe: "#1d1611", collar: "plain", bg: "church" } },

  { id: "calvin", m: "m4", name: "Жан Кальвин", tags: "реформатор · Женева", years: "1509 — 1564", country: "Франция, жил в Женеве", cls: "Реформатор", era: "XVI век", kind: "thinker", stars: 4,
    s: [90, 85, 95, 90, 70, 95],
    ach: [{ i: "book", h: "Наставление в вере", t: "В 1536 году издал главный труд." }, { i: "scales", h: "Призвание в труде", t: "Учил, что успех в делах — знак избранности." }, { i: "flag", h: "Гугеноты и пуритане", t: "Его идеи разошлись по многим странам." }],
    line: "Идеи кальвинизма помогали деловой активности.",
    face: { skin: "#e8d5b8", hair: "#3b2a1b", hs: "short", beard: ["long"], hat: "biretta", robe: "#1d1611", collar: "plain", bg: "church" } },

  { id: "loyola", m: "m4", name: "Игнатий Лойола", tags: "основатель иезуитов · бывший воин", years: "1491 — 1556", country: "Испания", cls: "Основатель ордена", era: "XVI век", kind: "thinker", stars: 4,
    s: [85, 80, 95, 90, 85, 90],
    ach: [{ i: "shield", h: "Орден иезуитов", t: "Основал в 1534 году, папа утвердил в 1540-м." }, { i: "book", h: "Лучшие школы", t: "Иезуиты создавали лучшие по тем временам школы." }, { i: "globe", h: "Миссии", t: "Они проповедовали в Азии, Африке и Америке." }],
    line: "После тяжёлого ранения он посвятил жизнь церкви.",
    face: { skin: "#e8d5b8", hair: "#e0d8c8", hs: "bald", beard: ["short"], hat: "none", robe: "#1d1611", collar: "cross", bg: "church" } },

  { id: "rudolf2", m: "m5", name: "Рудольф II", tags: "император · собиратель редкостей", years: "правил 1576 — 1611", country: "Священная Римская империя", cls: "Правитель", era: "XVI–XVII века", kind: "ruler", stars: 3,
    s: [60, 70, 80, 55, 100, 70],
    ach: [{ i: "castle", h: "Столица в Праге", t: "Перенёс столицу из Вены в Прагу." }, { i: "palette", h: "Коллекции", t: "Собирал книги, картины и диковины." }, { i: "scroll", h: "Свобода веры", t: "В 1609 году дал протестантам в Чехии свободу вероисповедания." }],
    line: "При его дворе работали учёные и мыслители.",
    face: { skin: "#f3d2b0", hair: "#8a6a3a", hs: "curly", beard: ["goatee", "mustache"], hat: "crown", robe: "#5b3f8f", collar: "ruff", bg: "court" } },

  { id: "elector", m: "m5", name: "Фридрих Вильгельм", tags: "Великий курфюрст Бранденбурга", years: "правил 1640 — 1688", country: "Бранденбург", cls: "Правитель", era: "XVII век", kind: "ruler", stars: 3,
    s: [80, 90, 70, 80, 50, 75],
    ach: [{ i: "castle", h: "Централизация", t: "Проводил реформы, чтобы укрепить государство." }, { i: "scales", h: "Умный союзник", t: "Умело лавировал между сильными державами." }, { i: "ship", h: "Выход к Балтике", t: "По итогам Тридцатилетней войны получил выход к морю." }],
    line: "Его сын в 1701 году стал королём Пруссии.",
    face: { skin: "#f0c9a0", hair: "#4a3a28", hs: "long", beard: ["mustache"], hat: "none", robe: "#262b66", collar: "chain", bg: "fort" } },

  { id: "sobieski", m: "m5", name: "Ян III Собеский", tags: "король Польши · победитель под Веной", years: "1629 — 1696", country: "Речь Посполитая", cls: "Полководец", era: "XVII век", kind: "conq", stars: 4,
    s: [95, 70, 80, 85, 70, 95],
    ach: [{ i: "sword", h: "Битва под Веной", t: "В 1683 году разгромил турок." }, { i: "castle", h: "Спасённая Вена", t: "Осаждённый город был спасён." }, { i: "flag", h: "Священная лига", t: "Речь Посполитая стала одной из главных сил лиги против турок." }],
    line: "Армией, разбившей турок, командовал польский король.",
    face: { skin: "#e8b98a", hair: "#4a3a28", hs: "short", beard: ["mustache"], hat: "cap", hatc: "#b4452f", feather: true, robe: "#b4452f", collar: "fur", bg: "fort" } },

  { id: "charles5", m: "m6", name: "Карл V Габсбург", tags: "император · король Испании", years: "1500 — 1558", country: "Испания, Священная Римская империя", cls: "Правитель", era: "XVI век", kind: "ruler", stars: 5,
    s: [95, 80, 90, 90, 75, 95],
    ach: [{ i: "globe", h: "Империя без заката", t: "В его владениях никогда не заходило солнце." }, { i: "scroll", h: "Почти 40 лет", t: "Правил, ведя тяжёлые войны с Францией, протестантами и турками." }, { i: "castle", h: "Уход в монастырь", t: "В 1556 году отрёкся от трона." }],
    line: "Редчайший случай: император сам оставил власть.",
    face: { skin: "#f3d2b0", hair: "#b08c55", hs: "short", beard: ["short"], hat: "crown", robe: "#1d1611", collar: "chain", bg: "court" } },

  { id: "philip2", m: "m6", name: "Филипп II", tags: "король Испании · «король деловых бумаг»", years: "1527 — 1598", country: "Испания", cls: "Правитель", era: "XVI век", kind: "ruler", stars: 4,
    s: [90, 75, 85, 90, 85, 90],
    ach: [{ i: "castle", h: "Эскориал", t: "Построил дворец-монастырь, «восьмое чудо света»." }, { i: "map", h: "Мадрид — столица", t: "С 1561 года Мадрид стал столицей." }, { i: "flag", h: "Португалия", t: "В 1580 году присоединил её с колониями." }],
    line: "Огромный флот «Непобедимой армады» разгромили в 1588 году.",
    face: { skin: "#f3d2b0", hair: "#b08c55", hs: "short", beard: ["goatee", "mustache"], hat: "none", robe: "#1d1611", collar: "ruff", bg: "court" } }
];

// ---------- Портрет ----------
function portrait(c, size = 120) {
  const ink = "#2b1d12", sk = c.skin || "#f0c9a0", hc = c.hair || "#3b2a1b", robe = c.robe || "#262b66", hatc = c.hatc || "#262b66";
  const bgs = {
    sea: `<rect width="120" height="150" fill="#f1c98a"/><rect y="74" width="120" height="76" fill="#2f7f86"/><path d="M0 88q10-6 20 0t20 0 20 0 20 0 20 0 20 0" fill="none" stroke="#6fb3b9" stroke-width="3"/><circle cx="96" cy="34" r="12" fill="#f4d37a"/>`,
    ship: `<rect width="120" height="150" fill="#f4d9a0"/><rect y="104" width="120" height="46" fill="#2f7f86"/><path d="M6 6v100" stroke="${ink}" stroke-width="3"/><path d="M8 12L8 92 56 92Z" fill="#fff4d6" stroke="${ink}" stroke-width="2.4"/><path d="M26 44v28M14 58h24" stroke="#b4452f" stroke-width="5"/>`,
    court: `<rect width="120" height="150" fill="#7a2a2a"/><path d="M0 0h120v22Q60 44 0 22z" fill="#9a3a3a"/><path d="M96 0v72" stroke="#e3b04b" stroke-width="3"/><path d="M96 72l-5 14h10z" fill="#e3b04b"/>`,
    church: `<rect width="120" height="150" fill="#3a4290"/><path d="M20 150V62a40 40 0 0180 0v88z" fill="#5b6bc0"/><path d="M60 20v130M26 72h68" stroke="#e3b04b" stroke-width="3"/><circle cx="60" cy="56" r="10" fill="#e3b04b"/>`,
    fort: `<rect width="120" height="150" fill="#b9b1a0"/><path d="M0 30h120M0 60h120M0 90h120M20 0v30M60 0v30M100 0v30M40 30v30M80 30v30M20 60v30M60 60v30M100 60v30" stroke="#8a8272" stroke-width="2"/><path d="M98 6v36" stroke="${ink}" stroke-width="2.4"/><path d="M98 6l16 5-16 5z" fill="#b4452f"/>`,
    forest: `<rect width="120" height="150" fill="#cfe0b8"/><path d="M-6 110l22-66 22 66zM28 118l26-76 26 76zM72 110l24-68 24 68z" fill="#4f8a3e" stroke="#2f5a28" stroke-width="2"/>`,
    ice: `<rect width="120" height="150" fill="#dbeaf0"/><path d="M0 96l28-50 24 36 18-26 50 40v54H0z" fill="#fff" stroke="#8fb0c0" stroke-width="2.5"/>`,
    workshop: `<rect width="120" height="150" fill="#d9c196"/><path d="M0 40h120M0 82h120" stroke="#8a5d2b" stroke-width="5"/><rect x="8" y="14" width="14" height="26" fill="#a8743a"/><rect x="26" y="20" width="12" height="20" fill="#b4452f"/><rect x="82" y="52" width="16" height="30" fill="#a8743a"/><rect x="100" y="58" width="12" height="24" fill="#2f7f86"/>`,
    map: `<rect width="120" height="150" fill="#ecdcb0"/><circle cx="26" cy="40" r="14" fill="#cfe0b8" stroke="#8f6d38" stroke-width="2"/><path d="M8 124q22-42 52-22t50-52" fill="none" stroke="#b4452f" stroke-width="3" stroke-dasharray="6 5"/><path d="M94 40l10 10m0-10l-10 10" stroke="#b4452f" stroke-width="4"/>`
  };
  const collars = {
    ruff: `<ellipse cx="60" cy="108" rx="25" ry="9" fill="#fffaf0" stroke="${ink}" stroke-width="2.4"/><path d="M38 108q4 5 8 0 4 5 8 0 4 5 8 0 4 5 8 0 4 5 8 0 4 5 8 0" fill="none" stroke="#b08c55" stroke-width="1.6"/>`,
    fur: `<path d="M8 150Q10 112 60 108Q110 112 112 150Q96 128 60 126Q24 128 8 150Z" fill="#cfc2a8" stroke="${ink}" stroke-width="2.4"/>`,
    chain: `<path d="M38 110Q60 136 82 110" fill="none" stroke="${ink}" stroke-width="7"/><path d="M38 110Q60 136 82 110" fill="none" stroke="#e3b04b" stroke-width="4"/><circle cx="60" cy="130" r="5" fill="#e3b04b" stroke="${ink}" stroke-width="2"/>`,
    cross: `<path d="M60 116v26M50 126h20" stroke="${ink}" stroke-width="9"/><path d="M60 116v26M50 126h20" stroke="#e3b04b" stroke-width="5"/>`,
    plain: `<path d="M44 108q16 16 32 0l-4-3q-12 8-24 0z" fill="#e8e0d0" stroke="${ink}" stroke-width="2.2" stroke-linejoin="round"/>`
  };
  const hairBack = c.hs === "long" ? `<path d="M30 60Q24 112 34 120L52 106L68 106L86 120Q96 112 90 60Q60 18 30 60Z" fill="${hc}" stroke="${ink}" stroke-width="2.6" stroke-linejoin="round"/>` : "";
  const hairFront = {
    short: `<path d="M34 64Q34 36 60 34Q86 36 86 64Q76 48 60 48Q44 48 34 64Z" fill="${hc}" stroke="${ink}" stroke-width="2.4" stroke-linejoin="round"/>`,
    long: `<path d="M34 64Q34 34 60 32Q86 34 86 64Q72 46 60 46Q46 46 34 64Z" fill="${hc}" stroke="${ink}" stroke-width="2.4" stroke-linejoin="round"/>`,
    curly: `<g fill="${hc}" stroke="${ink}" stroke-width="2.2"><circle cx="38" cy="50" r="9"/><circle cx="50" cy="40" r="9"/><circle cx="64" cy="38" r="9"/><circle cx="78" cy="44" r="9"/><circle cx="84" cy="56" r="7"/></g>`,
    bald: `<path d="M35 66Q32 54 38 48Q38 60 42 70Z M85 66Q88 54 82 48Q82 60 78 70Z" fill="${hc}" stroke="${ink}" stroke-width="2.2" stroke-linejoin="round"/>`
  }[c.hs || "short"];
  const beards = (c.beard || []).map(b => ({
    short: `<path d="M38 80Q40 104 60 106Q80 104 82 80Q76 94 60 94Q44 94 38 80Z" fill="${hc}" stroke="${ink}" stroke-width="2" stroke-linejoin="round"/>`,
    long: `<path d="M36 76Q34 118 60 128Q86 118 84 76Q76 98 60 98Q44 98 36 76Z" fill="${hc}" stroke="${ink}" stroke-width="2" stroke-linejoin="round"/>`,
    goatee: `<path d="M53 94Q60 110 67 94Q60 99 53 94Z" fill="${hc}" stroke="${ink}" stroke-width="2" stroke-linejoin="round"/>`,
    mustache: ""
  }[b])).join("");
  const mustache = (c.beard || []).includes("mustache") ? `<path d="M43 85Q52 80 60 85Q68 80 77 85Q68 91 60 88Q52 91 43 85Z" fill="${hc}" stroke="${ink}" stroke-width="1.8" stroke-linejoin="round"/>` : "";
  const hats = {
    beret: `<path d="M30 46Q32 22 66 22Q98 24 92 46Q80 34 60 36Q42 36 30 46Z" fill="${hatc}" stroke="${ink}" stroke-width="2.6" stroke-linejoin="round"/>`,
    cap: `<path d="M33 52Q35 28 60 28Q85 28 87 52Q60 42 33 52Z" fill="${hatc}" stroke="${ink}" stroke-width="2.6" stroke-linejoin="round"/>`,
    crown: `<path d="M36 42L38 22L48 32L60 16L72 32L82 22L84 42Z" fill="#e3b04b" stroke="${ink}" stroke-width="2.6" stroke-linejoin="round"/><circle cx="60" cy="17" r="3.2" fill="#b4452f"/>`,
    morion: `<path d="M34 48Q34 24 60 22Q86 24 86 48L100 54L20 54Z" fill="#8a97a6" stroke="${ink}" stroke-width="2.6" stroke-linejoin="round"/><path d="M60 22Q58 8 76 12Q66 18 68 24Z" fill="#8a97a6" stroke="${ink}" stroke-width="2.2" stroke-linejoin="round"/>`,
    biretta: `<path d="M36 46L40 26L80 26L84 46Z" fill="#1d1611" stroke="${ink}" stroke-width="2.4" stroke-linejoin="round"/><path d="M60 26v-7" stroke="${ink}" stroke-width="3"/>`,
    none: ""
  };
  const feather = c.feather ? `<path d="M70 26Q86 8 100 14Q90 24 74 34" fill="#fffaf0" stroke="${ink}" stroke-width="2" stroke-linejoin="round"/>` : "";
  const f = !!c.f;
  return `<svg class="portrait" viewBox="0 0 120 150" width="${size}" height="${Math.round(size * 1.25)}" aria-hidden="true">
    ${bgs[c.bg] || bgs.court}
    ${hairBack}
    <rect x="50" y="88" width="20" height="24" fill="${sk}" stroke="${ink}" stroke-width="2.4"/>
    <path d="M6 150Q10 110 60 106Q110 110 114 150Z" fill="${robe}" stroke="${ink}" stroke-width="3" stroke-linejoin="round"/>
    ${collars[c.collar] || collars.plain}
    <circle cx="35" cy="70" r="5" fill="${sk}" stroke="${ink}" stroke-width="2.2"/><circle cx="85" cy="70" r="5" fill="${sk}" stroke="${ink}" stroke-width="2.2"/>
    <ellipse cx="60" cy="68" rx="25" ry="29" fill="${sk}" stroke="${ink}" stroke-width="3"/>
    ${hairFront}${beards}
    <path d="M43 62q7-4 13 0M64 62q7-4 13 0" stroke="${f ? "#6b3a1a" : hc === "#d8d0c0" || hc === "#d0d0d0" ? "#8a8a8a" : ink}" stroke-width="2.8" fill="none" stroke-linecap="round"/>
    <ellipse cx="50" cy="71" rx="3.6" ry="4.4" fill="${ink}"/><ellipse cx="70" cy="71" rx="3.6" ry="4.4" fill="${ink}"/>
    <circle cx="51.4" cy="69.6" r="1.3" fill="#fff"/><circle cx="71.4" cy="69.6" r="1.3" fill="#fff"/>
    ${f ? `<path d="M45 66l-3-2M75 66l3-2" stroke="${ink}" stroke-width="1.8" stroke-linecap="round"/><circle cx="42" cy="80" r="4.5" fill="#e8836b" opacity=".45"/><circle cx="78" cy="80" r="4.5" fill="#e8836b" opacity=".45"/>` : ""}
    <path d="M60 70q-5 10 0 13h4" fill="none" stroke="#a0724a" stroke-width="2.4" stroke-linecap="round"/>
    <path d="M52 90q8 5 16 0" fill="none" stroke="#8e3220" stroke-width="2.8" stroke-linecap="round"/>
    ${mustache}${hats[c.hat || "none"]}${feather}
  </svg>`;
}

const heroById = id => HEROES.find(h => h.id === id);
