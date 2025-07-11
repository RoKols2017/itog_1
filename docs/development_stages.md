# Этапы разработки LinguaTrack (выполненные этапы — в начале)

Этот файл предназначен для отслеживания выполнения ключевых этапов разработки проекта. Отмечайте галочкой выполненные этапы.

---

**Важно: все шаблоны (HTML) размещать в каталоге templates/<имя_приложения> в корне проекта, а не внутри папок приложений. Например: templates/cards/card_list.html**

**UI/UX: Все страницы должны быть стилизованы в едином мягком стиле (полутона, светлый фон, тени, скругления, плавные эффекты, без кричащих цветов). Формы, списки, кнопки и главная страница — адаптивные, современные, удобные для мобильных.**

- [x] **1. Проектирование и базовая архитектура**
    - Инициализация Django-проекта, настройка окружения, создание базовых приложений (users, cards, core).
    - Проработка структуры моделей и связей.
    - Настройка системы контроля версий, базовых тестов, CI (по необходимости).

- [x] **2. Аутентификация и пользовательская модель**
    - [x] Реализация регистрации, входа, профиля пользователя (с поддержкой Telegram ID).
    - [x] Генерация magic-ссылки и QR-кода для привязки Telegram из сайта.
    - [x] Отображение статуса привязки Telegram в профиле.
    - [ ] Реализация endpoint для обработки magic-ссылки (бот привязывает пользователя).
    - [ ] Генерация magic-ссылки для привязки сайта из бота (будет реализовано при интеграции с ботом).
    - [x] **Протестировано:**
        - Регистрацию и вход пользователя
        - Генерацию magic-ссылки и QR-кода
        - Отображение статуса привязки в профиле

- [x] **3. CRUD карточек и базовый интерфейс**
    - Модели, формы, представления и шаблоны для карточек.
    - Список, создание, редактирование, удаление, фильтрация по уровню.
    - Минимальная адаптивность интерфейса (Tailwind).

- [x] **4. Интервальное повторение (ядро продукта)**
    - [x] Имплементация алгоритма SM-2 или собственной логики.
    - [x] Учёт успешных/неуспешных ответов.
    - [x] Интерфейс для режима повторения.
    - [x] Возможность ручного изменения даты следующего повторения.

- [x] **5. UI/UX: Единый дизайн форм**
    - [x] Стилизация всех форм под единый дизайн (вход, регистрация, карточки, профиль)
    - [x] Единообразные кнопки и поля ввода
    - [x] Адаптация главной страницы (скрытие кнопок для неавторизованных)
    - [x] Кнопка выхода на странице повторения
    - [x] Правильные редиректы после регистрации/входа

[x] **Докстринги и комментарии**
    - Во всех файлах проекта добавлены докстринги и пояснения по best practices Python/Django (PEP 257, Django style guide). 

[x] **Массовая загрузка карточек (импорт из CSV)**
    - Кнопка “Импорт из CSV” на странице карточек
    - Форма загрузки файла, инструкция и пример формата
    - Поддержка формата: CSV, UTF-8, word, translation, example, comment, level
    - Валидация, сообщения об успехе/ошибках
    - Импортируются только для текущего пользователя 

[x] **UI/UX: Адаптация интерфейса**
    - Все формы и страницы приведены к единому мягкому стилю (полутона, светлый фон, тени, скругления, плавные эффекты, адаптивность)
    - Форма редактирования карточки: уменьшены поля для примера и комментария, лейблы компактны и центрированы
    - Поля ввода визуально выделены (фон, рамка, тень), не сливаются с текстом карточки
    - Исправлены ошибки шаблонов (убран несуществующий фильтр as_widget)
    - CardForm перенесена в правильное приложение (cards), импорт и стилизация через widgets
    - Сервер перезапущен, все изменения протестированы

---

**Текущие и предстоящие этапы:**

- [ ] **6. Интеграция с Yandex SpeechKit (озвучка)**
    - Реализация API-запросов к Yandex SpeechKit.
    - Кнопка озвучки на карточке, кэширование аудиофайлов.
    - Обработка ошибок и лимитов API.

- [ ] **7. Telegram-бот: базовая интеграция**
    - Настройка aiogram-бота, привязка Telegram ID.
    - Реализация команд: /start, /cards, /say (озвучка через бота).
    - Проверка стабильности интеграции с основным приложением.

- [ ] **8. Фоновые задачи (Celery + Redis)**
    - Настройка Celery для фоновых задач (генерация озвучки, напоминания).
    - Реализация отправки напоминаний через Telegram-бота.
    - Проверка работы на вашей ОС (особенности Windows).

- [ ] **9. Прогресс и статистика**
    - Сбор и отображение статистики (количество слов, ошибок, повторений).
    - Визуализация прогресса (графики).

- [ ] **10. Тестирование и улучшение UX**
    - Покрытие ключевых модулей тестами (unit, интеграционные).
    - Ручное тестирование пользовательских сценариев.
    - Улучшение интерфейса, добавление подсказок, обработка ошибок.

- [ ] **11. Документация и финализация**
    - Описание установки, запуска, основных сценариев использования.
    - Инструкции для деплоя (если требуется).

---

**Следующие шаги:**
- Завершить интеграцию с Yandex SpeechKit (озвучка, кэширование, обработка ошибок)
- Реализовать Telegram-бота (привязка, команды, интеграция с озвучкой)
- После этого: экспорт карточек (CSV/Excel), предпросмотр перед импортом, статистика и графики, фоновая генерация озвучки и напоминания 