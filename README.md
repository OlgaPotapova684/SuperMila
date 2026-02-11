# Бот SuperMila (Мила Алова)

Telegram-бот: приветствие, проверка подписки на канал, выдача бесплатных подарков, отложенное сообщение про закрытый канал и оплату (имитация / Продамус).

## Быстрый старт на Mac

1. **Предварительные шаги** — см. [PRELIMINARY_STEPS.md](PRELIMINARY_STEPS.md).
2. Установка и запуск:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   # Заполни .env (токен, канал, ссылки)
   python run_bot.py
   ```

## Структура проекта

```
SuperMila/
├── .env                 # не в git; создаётся из .env.example
├── .env.example
├── config/
│   └── settings.py     # загрузка настроек из .env
├── bot/
│   ├── main.py         # точка входа, регистрация handlers
│   ├── messages.py     # тексты сообщений
│   ├── keyboards.py    # inline-кнопки
│   ├── handlers/
│   │   ├── start.py    # /start — фото + приветствие
│   │   ├── subscription.py  # проверка подписки, отложенное сообщение
│   │   └── payment.py  # кнопки оплаты, выдача ссылки на закрытый канал
│   └── services/
│       └── subscription_check.py  # проверка подписки через API Telegram
├── assets/
│   └── expert_photo.jpg   # фото для /start (путь в .env)
├── requirements.txt
├── run_bot.py
├── PRELIMINARY_STEPS.md
└── README.md
```

## Логика сценария

1. **/start** — отправляется фото эксперта (если файл есть) и приветствие с кнопками: «Я уже подписан/а», «Подписаться на канал».
2. **«Подписаться на канал»** — открывается ссылка на канал (пользователь подписывается в Telegram).
3. **«Я уже подписан/а»** — бот проверяет подписку. Если да — отправляет блок «Видео-тренировка» и текст с подарками; запускается таймер на второе сообщение.
4. **Через DELAY_SECONDS (по умолчанию 2 мин)** — отправляется сообщение про закрытый канал за 490₽ и две кнопки: «По картам РФ», «С любой точки мира».
5. **Оплата (имитация)** — по нажатию кнопки бот сразу отправляет ссылку на закрытый канал. Реальная оплата через Продамус: в .env добавляются ссылки на оплату и при необходимости webhook.

## Переменные окружения (.env)

| Переменная | Описание |
|------------|----------|
| `BOT_TOKEN` | Токен от @BotFather |
| `CHANNEL_USERNAME` | Username канала для проверки подписки (без @) |
| `CHANNEL_ID` | Числовой ID канала (например -1001234567890) |
| `CHANNEL_INVITE_LINK` | Ссылка на канал для кнопки «Подписаться» |
| `CLOSED_CHANNEL_LINK` | Ссылка на закрытый канал после оплаты |
| `EXPERT_PHOTO_PATH` | Имя файла в `assets/` или полный путь к фото |
| `DELAY_SECONDS` | Задержка второго сообщения в секундах (120 = 2 мин) |
| `PAYMENT_SIMULATION` | `True` — имитация оплаты; `False` — реальные ссылки на Продамус |
| `SELLAMUS_PAYMENT_LINK_RF` | Ссылка на оплату по картам РФ (когда будет) |
| `SELLAMUS_PAYMENT_LINK_WORLD` | Ссылка на оплату с любой точки мира |

## Где разместить бота

Бот должен работать 24/7. Варианты:

| Вариант | Плюсы | Минусы |
|--------|--------|--------|
| **VPS (Timeweb, Selectel, Reg.ru, Beget, зарубежные)** | Полный контроль, можно держать и сайт alova-team.ru, и бота на одном сервере или разделить | Нужна настройка Linux, SSL при необходимости |
| **Railway / Render / Fly.io** | Быстрый деплой по git, не нужен свой сервер | Ограниченный бесплатный тир, потом платно |
| **Heroku** | Привычный PaaS | Платный после отмены free tier |
| **Хостинг сайта alova-team.ru** | Всё в одном месте | Зависит от хостинга: если только PHP/статик — бота туда не поставить; если есть Python или Docker — можно запускать бота через cron или фоновый процесс (не идеально для long-running) |
| **Oracle Cloud (Free Tier)** | Бесплатный VPS | Нужна карта, ограничения по региону |

**Рекомендация:** для стабильной работы лучше отдельный VPS или PaaS (Railway/Render). Сайт [alova-team.ru](https://alova-team.ru) оставить для лендинга и кнопки «Написать в бота» (t.me/username_bot), а бота держать на отдельном сервере.

### Деплой на VPS (кратко)

- Установить Python 3.10+, склонировать репозиторий, создать `.env`, установить зависимости.
- Запускать через systemd или screen/tmux: `python run_bot.py`. Или использовать process manager (supervisor, pm2 для Node не подойдёт — у нас Python).

Пример unit для systemd (`/etc/systemd/system/supermila-bot.service`):

```ini
[Unit]
Description=SuperMila Telegram Bot
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/SuperMila
Environment=PATH=/path/to/SuperMila/venv/bin
ExecStart=/path/to/SuperMila/venv/bin/python run_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Дальше: `sudo systemctl enable supermila-bot && sudo systemctl start supermila-bot`.

## Продамус (реальная оплата)

- В личном кабинете Продамус создать товар/подписку на 490₽, настроить приём по картам РФ и с любой точки мира.
- Взять ссылки на оплату и прописать в .env: `SELLAMUS_PAYMENT_LINK_RF`, `SELLAMUS_PAYMENT_LINK_WORLD`.
- Поставить `PAYMENT_SIMULATION=False`.
- При необходимости доработать бота: после оплаты Продамус может вызывать webhook на твой сервер — по нему отправлять пользователю ссылку на закрытый канал (нужен HTTPS и отдельный endpoint).

## Лицензия

Частный проект.
