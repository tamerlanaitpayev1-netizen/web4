# Assignment 4 — Forms and Validation

**Aitpayev Tamerlan · IT-2510**

Исходный код: https://github.com/tamerlanaitpayev1-netizen/web4

Три задания по HTML, Bootstrap и CSS. В страницах нет JavaScript, атрибутов `novalidate` или `pattern`. Bootstrap 5.3.8 и Montserrat хранятся локально, поэтому после скачивания проект не зависит от CDN.

## Запуск

Из папки проекта выполните:

```powershell
python serve.py
```

Откройте **http://127.0.0.1:8000/**. Если порт занят, используйте `python serve.py --port 8001`.

Страницы можно просматривать и непосредственно из файлов. Для демонстрации отправки POST нужен `serve.py`: он принимает данные, сразу отбрасывает их и перенаправляет на страницу завершения. Он ничего не сохраняет и не создаёт реальные билеты, регистрации или бронирования. Это локальный учебный просмотр, не рабочий сервис.

## Страницы

| Файл | Задание |
| --- | --- |
| `index.html` | Навигация по работе |
| `task1.html` | Покупка билета: сетка Bootstrap, переключатель направления, даты, пассажиры, класс вагона, контакты, SMS и согласие |
| `task2.html` | AITU Hack 2026: 13 полей, ограничения HTML и сообщения после взаимодействия |
| `task3.html` | Исправленная форма кафе: все исходные поля, подписи, корректная отправка и доступность |
| `completed.html` | Завершение локальной демонстрации |

В первом задании текстовые поля и варианты изначально пусты. Для скриншотов выбраны примеры из макета. Кнопка `Clear` имеет `type="reset"`, поэтому очищает введённые данные, выбор пассажиров, радиокнопки и флажки. Код страны +7 остаётся постоянной частью телефона. В HTML порядок кнопок — Clear, Find trains; `flex-column-reverse flex-md-row` меняет только их расположение на телефоне.

Во втором задании только GitHub необязателен. Название University email не добавляет запрет на другие домены: по таблице требуется корректный адрес электронной почты. Для времени `step="1800"` задаёт 30 минут в секундах. Ошибки оформлены через `:user-invalid`, а не через начальное `:invalid`. Ограничения `minlength` проверяются при пользовательском вводе; `maxlength` не даёт ввести лишние символы.

## Отчёт и доказательства

- `docs/Assignment4_Aitpayev_Tamerlan.docx` — редактируемый отчёт для сдачи.
- `docs/Assignment4_Aitpayev_Tamerlan.pdf` — PDF-версия отчёта.
- `screenshots/` — снимки настоящих страниц в браузере.
- `docs/task2-results.*` — результаты проверки значений, включая границы диапазонов.
- `docs/task3-audit.md` — таблица проблем исходной формы и альтернативные решения.
- `docs/defense.md` — объяснения кода и подготовка к защите.
- `reference/task3-original.txt` — точная транскрипция исходного фрагмента, нумерация строк для аудита.

## Повторение проверок

Для просмотра страниц сторонние Python-пакеты не нужны. Для вспомогательных проверок установите зависимости и Chromium:

```powershell
python -m pip install -r tools/requirements.txt
python -m playwright install chromium
python tools/check_forms.py
python tools/check_keyboard.py
python tools/validate_html.py
python tools/build_report.py
```

Во время браузерных проверок сервер должен работать на порту 8000. Проверка W3C требует интернет-соединения. Python-скрипты в `tools/` предназначены для проверки и подготовки отчёта; они не подключены к веб-страницам.

## Использованные материалы

- [Bootstrap: формы](https://getbootstrap.com/docs/5.3/forms/overview/)
- [MDN: time](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input/time)
- [MDN: :user-invalid](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/:user-invalid)
- [W3C Nu HTML Checker](https://validator.w3.org/nu/)

Лицензии сторонних ресурсов включены: Bootstrap — MIT (`assets/vendor/bootstrap-LICENSE.txt`), Montserrat — SIL Open Font License (`assets/fonts/OFL.txt`). Дизайн задания 1 и исходный фрагмент задания 3 взяты из выданного Assignment 4.pdf; изображения в `reference/` сохранены для сравнения в отчёте.
