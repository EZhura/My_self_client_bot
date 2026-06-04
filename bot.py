import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# ===== НАСТРОЙКИ =====
# Обязательные переменные окружения для Render:
# TELEGRAM_BOT_TOKEN — токен бота от BotFather
# PUBLIC_URL — публичный URL Render, например https://your-app.onrender.com
# PORT — Render обычно задаёт сам

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
PUBLIC_URL = os.environ.get("PUBLIC_URL", "").rstrip("/")
PORT = int(os.environ.get("PORT", "10000"))

# Необязательные ссылки. Их можно добавить в Render Environment Variables.
ADMIN_TELEGRAM_URL = os.environ.get("ADMIN_TELEGRAM_URL", "https://t.me/your_username")
WHATSAPP_URL = os.environ.get("WHATSAPP_URL", "https://wa.me/your_number")
CHANNEL_URL = os.environ.get("CHANNEL_URL", "https://t.me/your_channel")

DEMO_ADMIN_BOT_URL = os.environ.get("DEMO_ADMIN_BOT_URL", "https://t.me/your_admin_demo_bot")
DEMO_CLIENT_BOT_URL = os.environ.get("DEMO_CLIENT_BOT_URL", "https://t.me/your_client_demo_bot")
DEMO_AI_BOT_URL = os.environ.get("DEMO_AI_BOT_URL", "https://t.me/your_ai_demo_bot")


# ===== ТЕКСТЫ ЭКРАНОВ =====

def get_screen_texts() -> dict:
    return {
        "start_screen": (
            "Здравствуйте 👋\n\n"
            "Я создаю Telegram-ботов для малого бизнеса и салонов красоты.\n\n"
            "Бот может помочь клиентам быстро найти услуги, цены, адрес, условия записи, "
            "ответы на частые вопросы и перейти к администратору, если нужен живой ответ.\n\n"
            "Здесь можно посмотреть:\n"
            "— какие форматы ботов бывают;\n"
            "— что умеет бот;\n"
            "— примерную стоимость;\n"
            "— как проходит работа;\n"
            "— что входит в поддержку;\n"
            "— демо-примеры.\n\n"
            "Выберите интересующий раздел ниже."
        ),

        "about_service_screen": (
            "Что я делаю\n\n"
            "Я создаю Telegram-ботов под задачи малого бизнеса.\n\n"
            "Чаще всего бот нужен, чтобы:\n"
            "— отвечать на повторяющиеся вопросы клиентов;\n"
            "— показывать услуги и цены;\n"
            "— объяснять условия записи;\n"
            "— разгружать администратора;\n"
            "— давать клиенту понятную структуру до живой переписки;\n"
            "— переводить сложные вопросы человеку.\n\n"
            "Основной фокус — салоны красоты, студии маникюра, бровей, ресниц, массажные кабинеты, "
            "косметология и другой малый сервисный бизнес."
        ),

        "formats_screen": (
            "Форматы ботов\n\n"
            "Я делаю несколько форматов, в зависимости от задачи бизнеса:\n\n"
            "1. Бот для администратора\n"
            "Внутренний помощник с готовыми ответами для переписки.\n\n"
            "2. Клиентский бот\n"
            "Бот, который сам показывает клиенту услуги, цены, FAQ, адрес и помогает перейти к записи.\n\n"
            "3. Бот с AI-модулем\n"
            "Более гибкий вариант: клиент может задавать часть вопросов своими словами, "
            "а бот отвечает по базе знаний бизнеса и передаёт сложные вопросы администратору."
        ),

        "admin_bot_screen": (
            "Бот для администратора\n\n"
            "Это внутренний бот-помощник для сотрудника или владельца бизнеса.\n\n"
            "Он не общается с клиентом сам. Его задача — хранить готовые ответы и помогать быстрее отвечать "
            "на типовые вопросы.\n\n"
            "Подходит, если:\n"
            "— администратор часто пишет одно и то же;\n"
            "— нужно ускорить ответы;\n"
            "— хочется навести порядок в шаблонах сообщений;\n"
            "— пока не хочется запускать клиентского бота наружу.\n\n"
            "Примеры разделов:\n"
            "— цены;\n"
            "— запись;\n"
            "— перенос записи;\n"
            "— подготовка к процедурам;\n"
            "— ответы на возражения;\n"
            "— повторное касание клиента."
        ),

        "client_bot_screen": (
            "Клиентский бот\n\n"
            "Это бот, с которым взаимодействует сам клиент.\n\n"
            "Он может:\n"
            "— показать услуги;\n"
            "— показать цены;\n"
            "— ответить на частые вопросы;\n"
            "— дать адрес и контакты;\n"
            "— объяснить условия записи;\n"
            "— рассказать, как подготовиться к процедуре;\n"
            "— перевести клиента к администратору.\n\n"
            "Такой бот особенно полезен, если клиенты часто задают одинаковые вопросы "
            "перед записью."
        ),

        "ai_bot_screen": (
            "Бот с AI-модулем\n\n"
            "AI-модуль нужен, если обычных кнопок уже недостаточно и клиенты часто задают вопросы своими словами.\n\n"
            "Такой бот может отвечать по базе знаний бизнеса:\n"
            "— про услуги;\n"
            "— цены;\n"
            "— подготовку;\n"
            "— условия записи;\n"
            "— общие правила;\n"
            "— частые вопросы.\n\n"
            "Важно: AI не должен отвечать на всё подряд. Для сложных, индивидуальных или спорных вопросов "
            "бот переводит клиента к администратору.\n\n"
            "Для косметологии и процедур с противопоказаниями AI лучше использовать особенно осторожно."
        ),

        "what_bot_can_do_screen": (
            "Что может бот\n\n"
            "В зависимости от формата бот может:\n\n"
            "— показывать услуги и цены;\n"
            "— отвечать на частые вопросы;\n"
            "— объяснять условия записи и отмены;\n"
            "— давать адрес, контакты и график;\n"
            "— помогать выбрать нужный раздел;\n"
            "— переводить клиента к администратору;\n"
            "— хранить готовые ответы для сотрудника;\n"
            "— работать с AI-модулем по базе знаний;\n"
            "— помогать сделать общение с клиентом более понятным и быстрым.\n\n"
            "Бот не заменяет продвижение и не гарантирует продажи сам по себе. "
            "Его задача — улучшить обработку входящих обращений."
        ),

        "beauty_examples_screen": (
            "Примеры для салона красоты\n\n"
            "Для салона красоты бот может содержать разделы:\n\n"
            "— услуги;\n"
            "— цены;\n"
            "— мастера;\n"
            "— запись;\n"
            "— адрес и карта;\n"
            "— акции;\n"
            "— подарочные сертификаты;\n"
            "— подготовка к процедурам;\n"
            "— противопоказания и ограничения;\n"
            "— частые вопросы;\n"
            "— связь с администратором.\n\n"
            "Например, клиент может открыть бот, выбрать услугу, посмотреть цену, узнать условия записи "
            "и только потом написать администратору уже с более понятным запросом."
        ),

        "pricing_screen": (
            "Стоимость\n\n"
            "Стоимость зависит от формата, количества разделов, сценариев и глубины настройки.\n\n"
            "Ориентиры:\n\n"
            "Бот для администратора:\n"
            "— базовая версия — от 7 000 ₽;\n"
            "— рабочий формат — от 12 000 ₽;\n"
            "— расширенный вариант — от 18 000 ₽.\n\n"
            "Клиентский бот:\n"
            "— базовая версия — от 10 000 ₽;\n"
            "— рабочий формат — от 16 000 ₽;\n"
            "— расширенный вариант — от 24 000 ₽.\n\n"
            "AI-модуль:\n"
            "— базовое подключение — от 8 000 ₽;\n"
            "— более глубокая настройка — от 15 000 ₽.\n\n"
            "Точная стоимость рассчитывается после короткого уточнения задачи."
        ),

        "support_screen": (
            "Поддержка\n\n"
            "После запуска бот может остаться на сопровождении.\n\n"
            "В поддержку обычно входит:\n"
            "— размещение бота на хостинге;\n"
            "— контроль работоспособности;\n"
            "— мелкие правки;\n"
            "— небольшие изменения текстов;\n"
            "— базовое техническое сопровождение.\n\n"
            "Ориентиры по ежемесячной поддержке:\n"
            "— внутренний бот — от 2 000 ₽/мес.;\n"
            "— клиентский бот — от 2 500 ₽/мес.;\n"
            "— AI-версия — от 4 000 ₽/мес.\n\n"
            "Крупные изменения, новые разделы и интеграции считаются отдельно."
        ),

        "ai_packages_screen": (
            "AI-пакеты\n\n"
            "AI оплачивается отдельно, потому что у него есть расход ресурса и требуется сопровождение.\n\n"
            "Ориентиры:\n\n"
            "AI до 500 ответов в месяц — 3 000 ₽/мес.\n"
            "Подходит для теста или небольшого потока обращений.\n\n"
            "AI до 1000 ответов в месяц — 5 000 ₽/мес.\n"
            "Подходит для регулярного использования.\n\n"
            "AI до 3000 ответов в месяц — 10 000 ₽/мес.\n"
            "Подходит для более активного потока.\n\n"
            "Большие объёмы рассчитываются отдельно."
        ),

        "process_screen": (
            "Как проходит работа\n\n"
            "Обычно работа строится так:\n\n"
            "1. Вы коротко описываете задачу.\n"
            "2. Мы выбираем подходящий формат бота.\n"
            "3. Фиксируем стоимость, сроки и объём.\n"
            "4. После предоплаты я собираю первую версию.\n"
            "5. Вы смотрите бот и даёте согласованные правки.\n"
            "6. После правок бот запускается.\n"
            "7. При необходимости подключается ежемесячная поддержка.\n\n"
            "Базовые версии обычно делаются за 2–3 дня.\n"
            "Рабочие форматы — за 3–5 дней.\n"
            "Расширенные варианты — от 5–7 дней."
        ),

        "what_needed_screen": (
            "Что нужно для старта\n\n"
            "Для старта обычно нужны:\n\n"
            "— список услуг;\n"
            "— цены;\n"
            "— адрес и контакты;\n"
            "— график работы;\n"
            "— условия записи и отмены;\n"
            "— частые вопросы клиентов;\n"
            "— ссылки на сайт, соцсети или онлайн-запись;\n"
            "— пожелания по стилю общения.\n\n"
            "Если у вас пока нет готовой структуры, я могу помочь собрать её в более понятный вид."
        ),

        "included_screen": (
            "Что входит в проект\n\n"
            "Обычно в проект входит:\n\n"
            "— структура бота;\n"
            "— кнопки и разделы;\n"
            "— тексты экранов;\n"
            "— логика переходов;\n"
            "— запуск;\n"
            "— базовое тестирование;\n"
            "— согласованные правки в рамках пакета;\n"
            "— короткая инструкция по использованию.\n\n"
            "Объём зависит от выбранного пакета и заранее согласуется."
        ),

        "not_included_screen": (
            "Что не входит в базовую стоимость\n\n"
            "Обычно отдельно считаются:\n\n"
            "— сложные интеграции с CRM;\n"
            "— онлайн-оплата;\n"
            "— нестандартные AI-сценарии;\n"
            "— большой объём копирайтинга с нуля;\n"
            "— постоянное ведение переписок;\n"
            "— продвижение и реклама;\n"
            "— новые разделы после согласования структуры;\n"
            "— крупная переработка логики после запуска.\n\n"
            "Это помогает заранее избежать недопонимания по объёму работ."
        ),

        "limitations_screen": (
            "Ограничения\n\n"
            "Бот — это рабочий инструмент, но у него есть границы.\n\n"
            "Бот не заменяет администратора полностью.\n"
            "Бот не гарантирует продажи сам по себе.\n"
            "Бот не заменяет рекламу и поток клиентов.\n"
            "AI не должен отвечать на медицинские или индивидуальные вопросы без участия специалиста.\n\n"
            "Хороший бот помогает быстрее давать информацию, снижать количество повторяющихся вопросов "
            "и переводить сложные ситуации человеку."
        ),

        "yclients_screen": (
            "Если уже есть онлайн-запись\n\n"
            "Если у вас уже есть YCLIENTS, DIKIDI, Altegio или другая система онлайн-записи, бот не обязательно её заменяет.\n\n"
            "Он может работать до записи:\n"
            "— объяснять услуги;\n"
            "— показывать цены;\n"
            "— отвечать на частые вопросы;\n"
            "— давать подготовку к процедурам;\n"
            "— помогать клиенту выбрать нужный раздел.\n\n"
            "А на этапе записи бот может переводить клиента в вашу текущую систему или к администратору."
        ),

        "messengers_screen": (
            "Telegram, WhatsApp, VK, Instagram\n\n"
            "Мой основной продукт сейчас — Telegram-боты.\n\n"
            "Telegram удобен для:\n"
            "— меню;\n"
            "— кнопок;\n"
            "— FAQ;\n"
            "— клиентских сценариев;\n"
            "— демо;\n"
            "— AI-модуля;\n"
            "— передачи клиента администратору.\n\n"
            "Если основной поток клиентов у вас идёт из WhatsApp, VK или Instagram, можно отдельно обсудить, "
            "как встроить Telegram-бота в вашу текущую схему общения.\n\n"
            "Сложные интеграции с другими платформами оцениваются отдельно."
        ),

        "demo_screen": (
            "Демо-примеры\n\n"
            "Можно посмотреть несколько форматов:\n\n"
            f"1. Бот для администратора:\n{DEMO_ADMIN_BOT_URL}\n\n"
            f"2. Клиентский бот:\n{DEMO_CLIENT_BOT_URL}\n\n"
            f"3. Бот с AI-модулем:\n{DEMO_AI_BOT_URL}\n\n"
            "Это демонстрационные примеры. Под конкретный бизнес структура, тексты, разделы и логика адаптируются отдельно."
        ),

        "contact_screen": (
            "Связаться\n\n"
            "Если хотите обсудить бота для своего бизнеса, можно написать мне:\n\n"
            f"Telegram:\n@ElenaBotHelper\n\n"
            f"WhatsApp:\n{https://wa.me/84796715140}\n\n"
            f"Канал / витрина:\n{https://t.me/business_bots_elena}\n\n"
            "Лучше всего написать коротко:\n"
            "— какой у вас бизнес;\n"
            "— где сейчас пишут клиенты;\n"
            "— какие вопросы повторяются чаще всего;\n"
            "— нужен бот для администратора, для клиентов или пока не знаете."
        ),

        "quick_request_screen": (
            "Быстрая заявка\n\n"
            "Можно скопировать и отправить мне такой текст:\n\n"
            "Здравствуйте! Хочу обсудить Telegram-бота для бизнеса.\n\n"
            "1. Сфера бизнеса:\n"
            "2. Где сейчас пишут клиенты:\n"
            "3. Какие вопросы повторяются чаще всего:\n"
            "4. Есть ли онлайн-запись / сайт / соцсети:\n"
            "5. Какой формат интересен: админ-бот, клиентский бот, AI или пока не знаю:\n\n"
            f"Написать в Telegram:\n@ElenaBotHelper\n\n"
            f"Написать в WhatsApp:\n{https://wa.me/84796715140}"
        ),

        "faq_screen": (
            "Частые вопросы\n\n"
            "Можно ли начать без AI?\n"
            "Да. Часто лучше сначала запустить обычного бота, а AI подключить позже.\n\n"
            "Можно ли сделать небольшой бот для теста?\n"
            "Да. Можно начать с компактной версии и расширять её постепенно.\n\n"
            "Нужна ли поддержка после запуска?\n"
            "Если клиент не хочет заниматься технической частью, поддержку лучше оставить.\n\n"
            "Бот заменит администратора?\n"
            "Полностью — нет. Но он может заметно снизить количество повторяющихся вопросов.\n\n"
            "Можно ли сделать под другой бизнес, не салон красоты?\n"
            "Да, если задача подходит под формат Telegram-бота."
        ),
    }


SCREEN_BUTTONS = {
    "start_screen": [
        [("Что я делаю", "about_service_screen")],
        [("Форматы ботов", "formats_screen"), ("Что может бот", "what_bot_can_do_screen")],
        [("Для салона красоты", "beauty_examples_screen"), ("Стоимость", "pricing_screen")],
        [("Как проходит работа", "process_screen"), ("Что нужно для старта", "what_needed_screen")],
        [("Поддержка", "support_screen"), ("AI-пакеты", "ai_packages_screen")],
        [("Что входит", "included_screen"), ("Ограничения", "limitations_screen")],
        [("Демо-примеры", "demo_screen"), ("Связаться", "contact_screen")],
        [("FAQ", "faq_screen")],
    ],

    "formats_screen": [
        [("Бот для администратора", "admin_bot_screen")],
        [("Клиентский бот", "client_bot_screen")],
        [("Бот с AI-модулем", "ai_bot_screen")],
        [("В меню", "start_screen")],
    ],

    "what_bot_can_do_screen": [
        [("YCLIENTS / онлайн-запись", "yclients_screen")],
        [("Telegram / WhatsApp / VK", "messengers_screen")],
        [("В меню", "start_screen")],
    ],

    "pricing_screen": [
        [("Поддержка", "support_screen")],
        [("AI-пакеты", "ai_packages_screen")],
        [("Что входит", "included_screen")],
        [("Что не входит", "not_included_screen")],
        [("В меню", "start_screen")],
    ],

    "process_screen": [
        [("Что нужно для старта", "what_needed_screen")],
        [("Быстрая заявка", "quick_request_screen")],
        [("Связаться", "contact_screen")],
        [("В меню", "start_screen")],
    ],

    "included_screen": [
        [("Что не входит", "not_included_screen")],
        [("Ограничения", "limitations_screen")],
        [("В меню", "start_screen")],
    ],

    "limitations_screen": [
        [("Что не входит", "not_included_screen")],
        [("AI-модуль", "ai_bot_screen")],
        [("В меню", "start_screen")],
    ],

    "demo_screen": [
        [("Связаться", "contact_screen")],
        [("Быстрая заявка", "quick_request_screen")],
        [("В меню", "start_screen")],
    ],

    "contact_screen": [
        [("Быстрая заявка", "quick_request_screen")],
        [("Демо-примеры", "demo_screen")],
        [("В меню", "start_screen")],
    ],

    "faq_screen": [
        [("Форматы ботов", "formats_screen")],
        [("Стоимость", "pricing_screen")],
        [("Связаться", "contact_screen")],
        [("В меню", "start_screen")],
    ],
}


def build_parent_map(screen_buttons: dict) -> dict:
    parent_map = {}

    for parent_screen, rows in screen_buttons.items():
        for row in rows:
            for _, target_screen in row:
                if target_screen != "start_screen":
                    parent_map[target_screen] = parent_screen

    return parent_map


def build_full_screen_buttons(screen_texts: dict, screen_buttons: dict) -> dict:
    parent_map = build_parent_map(screen_buttons)
    full_buttons = dict(screen_buttons)

    for screen_id in screen_texts:
        if screen_id not in full_buttons:
            parent_screen = parent_map.get(screen_id, "start_screen")
            full_buttons[screen_id] = [[("Назад", parent_screen), ("В меню", "start_screen")]]

    return full_buttons


def build_button_to_screen(screen_buttons: dict) -> dict:
    button_to_screen = {}

    for _, rows in screen_buttons.items():
        for row in rows:
            for button_text, target_screen in row:
                button_to_screen[button_text] = target_screen

    return button_to_screen


SCREEN_TEXTS = get_screen_texts()
SCREEN_BUTTONS = build_full_screen_buttons(SCREEN_TEXTS, SCREEN_BUTTONS)
BUTTON_TO_SCREEN = build_button_to_screen(SCREEN_BUTTONS)


def build_keyboard(screen_id: str) -> ReplyKeyboardMarkup:
    rows = SCREEN_BUTTONS.get(screen_id, SCREEN_BUTTONS["start_screen"])
    keyboard = []

    for row in rows:
        keyboard.append([KeyboardButton(button_text) for button_text, _ in row])

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        input_field_placeholder="Выберите раздел"
    )


async def show_screen(update: Update, screen_id: str) -> None:
    if not update.message:
        return

    text = SCREEN_TEXTS.get(screen_id, "Экран пока не найден.")
    keyboard = build_keyboard(screen_id)

    await update.message.reply_text(
        text,
        reply_markup=keyboard,
        disable_web_page_preview=True
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await show_screen(update, "start_screen")


async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await show_screen(update, "start_screen")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return

    await update.message.reply_text(
        "Команды:\n"
        "/start — открыть главное меню\n"
        "/menu — открыть главное меню\n"
        "/help — помощь\n\n"
        "Выберите нужный раздел кнопками ниже.",
        reply_markup=build_keyboard("start_screen")
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return

    text = update.message.text.strip()

    if text in BUTTON_TO_SCREEN:
        await show_screen(update, BUTTON_TO_SCREEN[text])
        return

    await update.message.reply_text(
        "Выберите нужный раздел кнопками ниже 👇",
        reply_markup=build_keyboard("start_screen")
    )


def validate_settings() -> None:
    missing = []

    if not TOKEN:
        missing.append("TELEGRAM_BOT_TOKEN")

    if not PUBLIC_URL:
        missing.append("PUBLIC_URL")

    if missing:
        raise RuntimeError(
            "Не заданы обязательные переменные окружения: " + ", ".join(missing)
        )


def main() -> None:
    validate_settings()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Client Showcase Bot is running on Render...")

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"{PUBLIC_URL}/{TOKEN}",
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()