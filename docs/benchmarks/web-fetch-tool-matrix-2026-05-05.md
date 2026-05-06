# Benchmark URL readers: web_fetch vs SNITCHMD vs CloakBrowser

## Что сделано:

Обновлён и расширен практический benchmark выбора URL-reader для Клевера: `web_fetch`, SNITCHMD и прямой CloakBrowser. Артефакт лежит здесь: `docs/benchmarks/web-fetch-tool-matrix-2026-05-05.md`.

В этот раз отчёт не ограничивается общей рекомендацией: добавлены конкретные URL из `MyBookmarks`, наблюдаемые результаты, где `web_fetch` достаточен, где SNITCHMD даёт заметно больше текста, и когда нужно эскалировать до прямого браузера.

## Зачем это нужно / как влияет на UX Вадима:

Вадим часто приносит конкретную ссылку из Telegram/bookmarks и ждёт, что агент прочитает именно её, а не уйдёт в общий web search. Эта матрица уменьшает три раздражающих сценария:

1. агент получает от `web_fetch` короткий/шумный/обёрнутый markdown и делает слабой глубины вывод;
2. агент сразу запускает тяжёлый браузер там, где хватало дешёвого fetch/markdown extraction;
3. агент не понимает, когда надо признать блокировку/интерактивность и попросить выбор или ручной шаг.

Практический UX-эффект: для обычных статей и README Клевер быстрее отвечает; для длинных статей, Substack/лендингов и JS-heavy страниц он по умолчанию берёт SNITCHMD; для Cloudflare/CAPTCHA/login/click-flow он не притворяется, что `web_fetch` всё прочитал, а эскалирует к CloakBrowser или просит Вадима.

## Выборка

Источник: локальный Telegram archive `MyBookmarks`, команда:

```bash
/home/clever/.openclaw/workspace/skills/telegram-user-search/scripts/tg_user_search.sh recent --chat MyBookmarks --days 30 --limit 80
```

Из выборки взяты типовые классы ссылок:

- Habr: `https://habr.com/ru/articles/1030832/`
- SPA/landing: `https://getdesign.md/`
- GitHub README: `https://github.com/syabro/SNITCHMD`
- Substack/blog: `https://blog.kilo.ai/p/bentoboard?...`
- HTTP landing: `http://lazypi.org/`
- Browser/anti-bot tooling repo: `https://github.com/CloakHQ/CloakBrowser`
- API/JSON endpoint from bookmark: `https://www.reddit.com/r/webscraping/comments/1gdx19g/best_methods_for_scraping_reddit_data.json`
- Corporate article: `https://block.xyz/inside/from-hierarchy-to-intelligence`

## Наблюдения по инструментам

### `web_fetch`

Плюсы:

- Быстро: на smoke set ответы были примерно 1.1–1.9 секунды.
- Хорош для quick skim: Habr/GitHub/Substack возвращают заголовок и начало основного текста.
- Не требует отдельного браузерного рантайма.

Минусы:

- В выдачу добавляется security wrapper, который раздувает контекст. Например, при `maxChars=2000` полезный `rawLength` у Habr/GitHub был около 1229 символов, остальное — служебная обёртка.
- На длинных материалах 2k chars дают только начало статьи; для исследования этого мало.
- На `getdesign.md` вернул только короткий landing-фрагмент: `rawLength=185`, тогда как SNITCHMD извлёк 6295 символов.

Когда использовать первым:

- быстрый sanity check URL;
- короткий ответ “что это за ссылка?”;
- статический HTML, где глубина не нужна;
- проверка статуса/заголовка перед более дорогим чтением.

### SNITCHMD

Плюсы:

- Даёт существенно более полный markdown для “серьёзного чтения”.
- Закрывает большинство кейсов из bookmarks без отдельного решения “какой браузер запускать”.
- В текущей выборке успешно отработал на 8/8 URL, включая Habr, GitHub, Substack, лендинги и корпоративную статью.

Smoke results:

| URL class | URL / label | SNITCHMD result | Вывод |
|---|---|---:|---|
| Habr long article | `habr1030832` | `chars=25763`, `quality=0.9`, cached | Для анализа статьи SNITCHMD лучше `web_fetch`, потому что достаёт полный текст, а не первый экран. |
| Design landing / SPA-ish | `getdesign.md` | `chars=6295`, `quality=1.0`, cached | Сильный пример: `web_fetch` увидел 185 raw chars, SNITCHMD достал полноценное содержимое. |
| GitHub README | `syabro/SNITCHMD` | `chars=5441`, `quality=0.95` | Достаточно для README/обзора; для проверки кода всё равно нужен checkout/API. |
| Substack/blog | `blog.kilo.ai/p/bentoboard` | `chars=11553`, `quality=1.0` | Для longform лучше SNITCHMD, иначе `web_fetch` отдаёт только начало. |
| HTTP landing | `lazypi.org` | `chars=4706`, `quality=1.0` | Нормально читает простой лендинг. |
| Browser tooling repo | `CloakHQ/CloakBrowser` | `chars=51913`, `quality=1.0` | README большой; SNITCHMD пригоден для глубокого обзора. |
| Reddit JSON endpoint | `reddit_data.json` | `chars=220`, `quality=0.3` | Для JSON/API лучше не SNITCHMD, а raw/API-aware чтение; extractor честно даёт низкое качество. |
| Corporate article | `block.xyz/inside/...` | `chars=16569`, `quality=1.0` | Хороший default для статей на современных сайтах. |

Когда использовать первым:

- Вадим дал конкретную ссылку и нужен нормальный пересказ/анализ;
- `web_fetch` вернул слишком короткий текст, JS-shell или много wrapper/noise;
- Habr/Substack/blog/лендинг/GitHub README надо прочитать целиком;
- задача не требует кликов, логина или состояния.

### Прямой CloakBrowser

В этой smoke-выборке прямой CloakBrowser как отдельный шаг не понадобился: SNITCHMD уже использует CloakBrowser под капотом и успешно извлёк все HTML-страницы. Поэтому прямой browser-run не стоит делать default’ом — это дороже и сложнее.

Когда эскалировать именно к CloakBrowser:

- нужен клик, поиск внутри страницы, раскрытие accordion/modal, переход по tabs;
- сайт отдаёт CAPTCHA/Cloudflare/anti-bot wall, и SNITCHMD не смог извлечь полезный markdown;
- требуется screenshot/визуальная проверка;
- нужно проверить flow, а не просто извлечь текст;
- есть login/private state — тогда сначала нужен явный выбор/разрешение Вадима.

## Итоговая матрица выбора

| Ситуация | Первый инструмент | Если не хватило | Почему так |
|---|---|---|---|
| Быстро понять, что за URL | `web_fetch` | SNITCHMD | Самый быстрый sanity check. |
| Habr / обычная статья / blog longform | SNITCHMD | `web_fetch` только для короткого skim; CloakBrowser при блоке | Полный markdown важнее скорости. |
| GitHub README / repo overview | SNITCHMD или GitHub/API/checkout | checkout, если нужны файлы/tests | README можно прочитать markdown extraction, но код надо проверять локально. |
| SPA/landing/modern marketing page | SNITCHMD | CloakBrowser | На `getdesign.md` SNITCHMD дал 6295 chars против 185 raw chars у `web_fetch`. |
| JSON/API endpoint | raw/API-aware fetch, не readability | curl/python parser | Markdown extractor не показатель качества JSON. |
| Cloudflare/CAPTCHA/anti-bot wall | SNITCHMD first if text-only | CloakBrowser/headful/humanize or ask Vadim | SNITCHMD уже включает Cloak; прямой browser нужен при провале/интерактивности. |
| Login/private/click-flow | спросить/получить выбор, затем CloakBrowser | — | Нужны state/credentials/manual decision; нельзя тихо делать внешние действия. |
| Telegram/MyBookmarks source | local Telegram archive first | fetch only explicit sampled URLs | Сначала берём ссылки локально, не скрейпим лишнее. |

## Правило для Клевера

1. Если запрос Вадима — “прочитай/проанализируй эту ссылку” и это не очевидный quick skim, начинать с SNITCHMD.
2. `web_fetch` использовать для быстрых проверок, коротких страниц и случаев, где достаточно заголовка/первых абзацев.
3. Если `web_fetch` дал короткий wrapper/noise или подозрительно мало текста — не делать вывод, а повторить через SNITCHMD.
4. Если SNITCHMD дал `quality < 0.5`, пустой текст, JSON/API вместо HTML, CAPTCHA, login или требуются клики — выбрать специализированный путь: raw parser/API, CloakBrowser или вопрос Вадиму.
5. Прямой CloakBrowser не является default для чтения; это эскалация для интерактивности, антибота, визуальной проверки и stateful flows.

## Что дальше:

ничего автоматически, задача закрыта.

Если позже Вадим поймает конкретный URL, где это правило ошиблось, тогда нужен follow-up с этим URL и фактическим failure mode: `web_fetch empty`, `SNITCHMD low quality`, `CAPTCHA`, `login`, `JSON/API`, `needs clicks`.

## Доказательства:

- Артефакт: `docs/benchmarks/web-fetch-tool-matrix-2026-05-05.md`.
- Telegram sample command: `/home/clever/.openclaw/workspace/skills/telegram-user-search/scripts/tg_user_search.sh recent --chat MyBookmarks --days 30 --limit 80` — успешно вернул свежие bookmarks, включая Habr/GitHub/Substack/лендинги/CloakBrowser.
- `web_fetch` smoke checks: Habr `tookMs=1168`, GitHub `tookMs=1878`, Substack `tookMs=1803`, `getdesign.md rawLength=185`, `lazypi.org rawLength=828`.
- SNITCHMD smoke command: `/home/clever/.openclaw/workspace/scripts/snitchmd <url> --json --timeout 30`.
- SNITCHMD results: Habr `25763 chars / quality 0.9`; `getdesign.md 6295 / 1.0`; GitHub SNITCHMD `5441 / 0.95`; Substack `11553 / 1.0`; LazyPi `4706 / 1.0`; CloakBrowser repo `51913 / 1.0`; Reddit JSON `220 / 0.3`; Block article `16569 / 1.0`.
