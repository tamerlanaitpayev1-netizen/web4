# Результаты проверки форм

Браузер: Chromium 145.0.7632.6. Проверено: 88/88.

Проверки выполняют ввод с клавиатуры, смену фокуса и нажатие кнопки отправки. У невалидной формы событие submit не возникает. Обработчик, который отменяет отправку валидной формы, добавляется только тестом и отсутствует в HTML проекта.

| Проверка | Результат |
|---|---|
| HTML attributes: full-name | PASS |
| HTML attributes: university-email | PASS |
| HTML attributes: age | PASS |
| HTML attributes: team-size | PASS |
| HTML attributes: track | PASS |
| HTML attributes: arrival-date | PASS |
| HTML attributes: checkin-time | PASS |
| HTML attributes: entry-fee | PASS |
| HTML attributes: github-url | PASS |
| HTML attributes: password | PASS |
| HTML attributes: motivation | PASS |
| HTML attributes: agreement | PASS |
| Task 2 contains no script, pattern or novalidate | PASS |
| Track offers exactly Web, Mobile, AI and GameDev | PASS |
| Three experience radios form one required group | PASS |
| No error feedback on initial page load | PASS |
| PDF example: Full name: Anna-Maria Lee | PASS |
| PDF example: Full name: A | PASS |
| PDF example: Email: a.fedenko@astanait.edu.kz | PASS |
| PDF example: Email: a.fedenko | PASS |
| PDF example: Email: a.fedenko@ | PASS |
| PDF example: Age: 18 | PASS |
| PDF example: Age: 15 | PASS |
| PDF example: Age: 31 | PASS |
| PDF example: Team size: 4 | PASS |
| PDF example: Team size: 5 | PASS |
| PDF example: Team size: 2.5 | PASS |
| PDF example: Track: Web | PASS |
| PDF example: Track: Choose... | PASS |
| PDF example: Arrival: 2026-11-21 | PASS |
| PDF example: Arrival: 2026-11-25 | PASS |
| PDF example: Check-in: 10:30 | PASS |
| PDF example: Check-in: 10:15 | PASS |
| PDF example: Check-in: 19:00 | PASS |
| PDF example: Entry fee: 1500 | PASS |
| PDF example: Entry fee: 1250 | PASS |
| PDF example: Entry fee: 6000 | PASS |
| PDF example: Experience: Beginner | PASS |
| PDF example: Experience: none | PASS |
| PDF example: GitHub: empty | PASS |
| PDF example: GitHub: full HTTPS URL | PASS |
| PDF example: GitHub: no protocol | PASS |
| PDF example: Password: Astana2026 | PASS |
| PDF example: Password: short | PASS |
| PDF example: Motivation: 120 characters | PASS |
| PDF example: Motivation: 49 characters | PASS |
| PDF example: Agreement: checked | PASS |
| PDF example: Agreement: unchecked | PASS |
| Boundary: Full name lower bound: 2 | PASS |
| Boundary: Full name upper bound: 40 | PASS |
| Boundary: Age lower bound: 16 | PASS |
| Boundary: Age upper bound: 30 | PASS |
| Boundary: Age fraction: 18.5 | PASS |
| Boundary: Team size lower bound: 1 | PASS |
| Boundary: Team size below range: 0 | PASS |
| Boundary: Arrival lower bound: 2026-11-20 | PASS |
| Boundary: Arrival upper bound: 2026-11-22 | PASS |
| Boundary: Arrival before range: 2026-11-19 | PASS |
| Boundary: Check-in lower bound: 09:00 | PASS |
| Boundary: Check-in upper bound: 18:00 | PASS |
| Boundary: Check-in below range: 08:30 | PASS |
| Boundary: Entry fee lower bound: 0 | PASS |
| Boundary: Entry fee upper bound: 5000 | PASS |
| Boundary: Entry fee below range: -500 | PASS |
| Boundary: Password lower bound: 8 | PASS |
| Boundary: Password upper bound: 20 | PASS |
| Boundary: Motivation lower bound: 50 | PASS |
| Boundary: Motivation upper bound: 300 | PASS |
| Boundary: Track: Mobile | PASS |
| Boundary: Track: AI | PASS |
| Boundary: Track: GameDev | PASS |
| maxlength prevents typing past 40: full-name | PASS |
| maxlength prevents typing past 20: password | PASS |
| maxlength prevents typing past 300: motivation | PASS |
| Changed invalid field shows feedback after blur | PASS |
| No horizontal overflow: index.html at 375px | PASS |
| No horizontal overflow: index.html at 1280px | PASS |
| No horizontal overflow: task1.html at 375px | PASS |
| No horizontal overflow: task1.html at 1280px | PASS |
| No JavaScript or novalidate: task1.html | PASS |
| No horizontal overflow: task2.html at 375px | PASS |
| No horizontal overflow: task2.html at 1280px | PASS |
| No JavaScript or novalidate: task2.html | PASS |
| No horizontal overflow: task3.html at 375px | PASS |
| No horizontal overflow: task3.html at 1280px | PASS |
| No JavaScript or novalidate: task3.html | PASS |
| No horizontal overflow: completed.html at 375px | PASS |
| No horizontal overflow: completed.html at 1280px | PASS |
