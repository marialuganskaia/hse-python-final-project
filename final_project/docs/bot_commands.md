# Спецификация команд Telegram-бота

Техническое описание команд в терминах входных данных и возвращаемых доменных сущностей.

---

## Основные команды

### `/start`
**Вход:**
- Команда `/start` (без аргументов)
- Контекст: `telegram_id`, `username`, `first_name`, `last_name` из Telegram

**Выход:**
- Создание или обновление сущности `User`:
  - Если пользователь новый: создается запись `User` с `role='participant'`
  - Если пользователь существующий: обновляются поля `username`, `first_name`, `last_name`
- Определение активного хакатона: поиск `Hackathon` где `is_active=true`
- Установка `User.current_hackathon_id` на найденный активный хакатон
- Возврат `Hackathon` (основная информация)

### `/help`
**Вход:**
- Команда `/help` без аргументов
- Контекст: `User` (определяется по `telegram_id`)

**Выход:**
- Список доступных команд, отфильтрованный по `User.role`
- Текущий контекст: `User.current_hackathon_id`

---

## Информация о хакатоне

### `/hackathon`
**Вход:**
- Команда `/hackathon` без аргументов
- Контекст: `User.current_hackathon_id` (обязательно должен быть установлен)

**Выход:**
- Сущность `Hackathon` по `current_hackathon_id` с полями:
  - `name`, `description`, `start_at`, `end_at`, `code`
- Статус подписки: `ReminderSubscription.enabled` для данного пользователя и хакатона

### `/schedule`
**Вход:**
- Команда `/schedule` без аргументов
- Контекст: `User.current_hackathon_id`

**Выход:**
- Список сущностей `Event[]` где `Event.hackathon_id = User.current_hackathon_id`
- Сортировка по `Event.starts_at` (возрастание)
- Группировка по дням на основе `starts_at`

### `/rules`
**Вход:**
- Команда `/rules` без аргументов
- Контекст: `User.current_hackathon_id`

**Выход:**
- Сущность `Rules` где `Rules.hackathon_id = User.current_hackathon_id`
- Единственное поле: `Rules.content`

### `/faq`
**Вход:**
- Команда `/faq` без аргументов
- Контекст: `User.current_hackathon_id`

**Выход:**
- Список сущностей `FAQItem[]` где `FAQItem.hackathon_id = User.current_hackathon_id`
- Каждый `FAQItem` содержит: `question`, `answer`
- Возможна пагинация или группировка по категориям

---

## Уведомления

### `/notify_on`
**Вход:**
- Команда `/notify_on` без аргументов
- Контекст: `User.id`, `User.current_hackathon_id`

**Выход:**
- Поиск или создание `ReminderSubscription`:
  - Поиск: `user_id = User.id` AND `hackathon_id = User.current_hackathon_id`
  - Если найдено: обновление `ReminderSubscription.enabled = true`
  - Если не найдено: создание новой подписки с `enabled = true`
- Подтверждение успешной активации

### `/notify_off`
**Вход:**
- Команда `/notify_off` без аргументов
- Контекст: `User.id`, `User.current_hackathon_id`

**Выход:**
- Поиск `ReminderSubscription`:
  - `user_id = User.id` AND `hackathon_id = User.current_hackathon_id`
- Обновление `ReminderSubscription.enabled = false`
- Подтверждение успешной деактивации

---

## Административные команды

### `/admin_stats`
**Вход:**
- Команда `/admin_stats` без аргументов
- Контекст: `User` (проверка `User.role == 'organizer'`)
- Дополнительно: `User.current_hackathon_id`

**Выход:**
- Статистика по `User.current_hackathon_id`:
  - Количество `User` с `current_hackathon_id` = текущему хакатону
  - Количество `ReminderSubscription` с `enabled=true` для текущего хакатона
  - Количество `Event` для текущего хакатона
- Статистика активности:
  - Распределение `User` по времени регистрации
  - Популярность команд для данного хакатона

### `/admin_broadcast`
**Вход:**
- Двухэтапная команда:
  1. `/admin_broadcast` (инициализация)
  2. Текстовое сообщение от администратора
- Контекст: `User` (проверка `User.role == 'organizer'`), `User.current_hackathon_id`

**Выход:**
- Поиск всех `User` где `current_hackathon_id = User.current_hackathon_id`
- Асинхронная рассылка сообщения всем найденным пользователям
- Отчет о рассылке:
  - Общее количество получателей
  - Успешно отправлено
  - Ошибки отправки
- Создание лога рассылки в системе

---

## Дополнительные сценарии

### Смена активного хакатона (неявная команда)
**Вход:**
- Команда `/start` с параметром `code` (например, `/start HACK123`)
- Или выбор хакатона через интерактивное меню

**Выход:**
- Поиск `Hackathon` по `code`
- Обновление `User.current_hackathon_id` на найденный хакатон
- Возврат подтверждения смены контекста

### Получение ближайшего события
**Вход:**
- Неявный запрос (например, при запуске бота)
- Контекст: `User.current_hackathon_id`, текущее время

**Выход:**
- Сущность `Event` где:
  - `Event.hackathon_id = User.current_hackathon_id`
  - `Event.starts_at > current_time`
  - Сортировка по `Event.starts_at` (возрастание)
  - Лимит 1 запись
