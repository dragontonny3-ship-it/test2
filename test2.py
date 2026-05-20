import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import InputMediaPhoto
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)

TOKEN = "8367043192:AAH4mFb-LFOSKxcPF7ItBGX-qYFXxIHXelc"
ADMIN_ID = 8221357115

STEP = {
    "amount": "amount",
    "city": "city",
    "district": "district",
    "payment": "payment"
}

COUNTRIES_FULL = {
    "rf": "🇷🇺 Россия",
    "rb": "🇧🇾 Беларусь",
    "kz": "🇰🇿 Казахстан",
    "pl": "🇵🇱 Польша"
}

COUNTRIES_SHORT = {
    "rf": "РФ 🇷🇺",
    "rb": "РБ 🇧🇾",
    "kz": "КЗ 🇰🇿",
    "pl": "PL 🇵🇱"
}
DATA_MAP = {

    "rf": {
        "Москва": ["ЦАО", "САО", "ЮАО", "ЗАО", "ВАО"],
        "Санкт-Петербург": ["Центральный", "Приморский", "Выборгский", "Невский"],
        "Казань": ["Вахитовский", "Советский", "Приволжский"],
        "Екатеринбург": ["Ленинский", "Верх-Исетский", "Орджоникидзевский"],
        "Новосибирск": ["Центральный", "Ленинский", "Октябрьский", "Калининский", "Дзержинский", "Советский", "Кировский"],
        "Тольятти": ["Автозаводский", "Центральный", "Комсомольский"],
        "Краснодар": ["Центральный", "Прикубанский", "Карасунский", "Западный"],
        "Казань": ["Вахитовский", "Приволжский", "Советский", "Ново-Савиновский", "Московский", "Кировский", "Авиастроительный"],
        "Нижний Новгород": ["Автозаводский", "Канавинский", "Ленинский", "Московский", "Нижегородский", "Приокский", "Советский", "Сормовский"],
        "Челябинск": ["Калининский", "Курчатовский", "Ленинский", "Металлургический", "Советский", "Тракторозаводский"],
        "Самара": ["Железнодорожный", "Кировский", "Красноглинский", "Куйбышевский", "Ленинский", "Октябрьский", "Промышленный", "Самарский", "Советский"],
        "Ростов-на-Дону": ["Ворошиловский", "Железнодорожный", "Кировский", "Ленинский", "Октябрьский", "Первомайский", "Пролетарский", "Советский"],
        "Уфа": ["Демский", "Калининский", "Кировский", "Ленинский", "Октябрьский", "Орджоникидзевский", "Советский"]
    },

    "rb": {
        "Минск": ["Центральный", "Советский", "Фрунзенский", "Московский"],
        "Гомель": ["Центральный", "Новобелицкий"],
        "Брест": ["Московский", "Ленинский"],
        "Могилёв": ["Ленинский", "Октябрьский"],
        "Витебск": ["Железнодорожный", "Октябрьский", "Первомайский"],
        "Гродно": ["Ленинский", "Октябрьский"],
        "Бобруйск": ["Ленинский", "Первомайский"],
        "Барановичи": ["Восточный", "Текстильный", "Северный", "Южный", "Русино"],
        "Пинск": ["Радужный", "Солнечный", "Западный", "Жилгородок", "Центр"],
        "Орша": ["Черёмушки", "Заднепровье", "Льнокомбинат", "Восточный"],
        "Мозырь": ["Молодёжный", "Железнодорожный", "Заречный", "Нефтестроителей"],
        "Новополоцк": ["Боровуха", "Молодёжный", "Юбилейный", "Василевцы"]
    },

    "kz": {
        "Алматы": ["Алмалинский", "Бостандыкский", "Медеуский", "Ауэзовский", "Жетысуский", "Наурызбайский", "Турксибский"],
        "Астана": ["Алматинский район", "Байконурский район", "Есильский район", "Сарыаркинский район", "Нура район"],
        "Шымкент": ["Абайский район", "Аль-Фарабийский район", "Енбекшинский район", "Каратауский район"],
        "Караганда": ["Казыбек би район", "Октябрьский район"],
        "Актобе": ["Алматы район", "Астана район", "Алтынсарин район"],
        "Тараз": ["Алмалинский", "Жамбылский", "Абайский", "Турксибский"],
        "Павлодар": ["Химгородки", "Усолка", "Северный промышленный", "Дачный"],
        "Усть-Каменогорск": ["КШТ", "Пристань", "Защита", "Аблакетка", "Левый берег"],
        "Семей": ["Центр", "Заря", "Восточный", "Жана-Семей"],
        "Атырау": ["Алмагуль", "Привокзальный", "Жилгородок", "Балыкши"],
        "Костанай": ["КСК", "Юбилейный", "Киевский", "Северо-Запад"],
        "Кызылорда": ["Арай", "Мерей", "Шанхай", "Сырдарья микрорайон"]
    },

    "pl": {
        "Варшава": ["Средместье", "Мокотув", "Воля", "Прага-Пулноц", "Прага-Полудне", "Урсынув", "Бемово"],
        "Краков": ["Старе-Място", "Подгуже", "Нова-Хута", "Кроводжа", "Дебники"],
        "Лодзь": ["Балути", "Гурна", "Полесье", "Видзев", "Средместье"],
        "Вроцлав": ["Старе-Място", "Кшики", "Псе-Поле", "Фабрычна", "Средместье"],
        "Познань": ["Старе-Място", "Ежицы", "Вильда", "Грюнвальд", "Нове-Място"],
        "Гданьск": ["Олива", "Вжещ", "Шрудместье", "Приморье", "Новы-Порт"],
        "Щецин": ["Погодно", "Небушево", "Домбье", "Центр", "Поможаны"],
        "Люблин": ["Чубы", "Чехув", "Фелин", "Калинувщина", "Славинек"],
        "Быдгощ": ["Фордон", "Блоне", "Средместье", "Окенче", "Бартодзее"],
        "Белосток": ["Пясечна", "Слонечны-Сток", "Антонюк", "Бялосточек", "Новы-Свят"]
    }
}

EXCHANGE_RATES = {
    "rf": 1.0,
    "rb": 0.035,
    "kz": 5.2,
    "pl": 0.045
}

CURRENCY_SYMBOL = {
    "rf": "₽",
    "rb": "Br",
    "kz": "₸",
    "pl": "zł"
}

REVIEWS = [
    {
        "photo": "AgACAgIAAxkBAAIFR2oOKzalDZcdvjLzPw04_tm4fua4AAINH2sbB9txSEaqtuVIYo3jAQADAgADeAADOwQ",
        "text": "⭐ Отзыв 1\n\n"
    },

    {
        "photo": "AgACAgIAAxkBAAIFU2oOK37xu2UX2BqnW0uMS9bYEQh_AAISH2sbB9txSJgFxyL5lqTgAQADAgADeAADOwQ",
        "text": "⭐ Отзыв 2\n\n"
    },

    {
        "photo": "AgACAgIAAxkBAAIFV2oOK5FDyaTEvK0TI_LwEoSyOQewAAIUH2sbB9txSFHZGzQIrd3MAQADAgADeAADOwQ",
        "text": "⭐ Отзыв 3\n\n"
    },

    {
        "photo": "AgACAgIAAxkBAAIFS2oOK0cOBZ7_tfCCDg_84WEP8UVOAAIPH2sbB9txSAyyJubUaRnxAQADAgADeAADOwQ",
        "text": "⭐ Отзыв 4\n\n"
    },

    {
        "photo": "AgACAgIAAxkBAAIFTWoOK03lVYrUZsyCb2L9gRDOXmMlAAIQH2sbB9txSP4cOj8-Oas4AQADAgADeQADOwQ",
        "text": "⭐ Отзыв 5\n\n"
    },

    {
        "photo": "AgACAgIAAxkBAAIFT2oOK2cziiDnjV7fd8wfZ5UgRtGcAAIRH2sbB9txSDNp4HWtwg0qAQADAgADeAADOwQ",
        "text": "⭐ Отзыв 6\n\n"
    },

    {
        "photo": "AgACAgIAAxkBAAIFUWoOK3In0EXmSKt9Ohtn7fn3_hDhAALPGmsboAthSDGTBZ2qS_D-AQADAgADeAADOwQ",
        "text": "⭐ Отзыв 7\n\n"
    },

    {
        "photo": "AgACAgIAAxkBAAIFVWoOK4iqINKKs9HfdKe_PGNsUUv9AAITH2sbB9txSB0vn-UbLZfXAQADAgADeAADOwQ",
        "text": "⭐ Отзыв 8\n\n"
    },

    {
        "photo": "AgACAgIAAxkBAAIFWWoOK5z7pTUNghgJxs41SiafAaz2AAIVH2sbB9txSD1Y8Cfexxt3AQADAgADeQADOwQ",
        "text": "⭐ Отзыв 9\n\n"
    },

    {
        "photo": "AgACAgIAAxkBAAIFW2oOK6WC8fMV5urz7CpBVpq84DXrAAIWH2sbB9txSM-2eV4xpQhuAQADAgADeAADOwQ",
        "text": "⭐ Отзыв 10\n\n"
    },

    {
        "photo": "AgACAgIAAxkBAAIFXWoOK6ucDEksbmRXxUlly0lsKTFKAAIXH2sbB9txSHzWFpsm4VQhAQADAgADeAADOwQ",
        "text": "⭐ Отзыв 11\n\n"
    },

    {
        "photo": "AgACAgIAAxkBAAIFX2oOK7J2JM5mGn07Ct_CTmbhnhjIAAIYH2sbB9txSKGg8zYn2iSJAQADAgADeAADOwQ",
        "text": "⭐ Отзыв 12\n\n"
    },

    {
        "photo": "AgACAgIAAxkBAAIFYWoOLHuJpZrFvk2HMaHpQVlySPHWAAIZH2sbB9txSEhF0ar_HenrAQADAgADeQADOwQ",
        "text": "⭐ Отзыв 13\n\n"
    },

    {
        "photo": "AgACAgIAAxkBAAIFY2oOLICdayStuk1mELEDapKXIaWNAAIaH2sbB9txSE-hg1FoetAiAQADAgADeQADOwQ",
        "text": "⭐ Отзыв 14\n\n"
    },

    {
        "photo": "AgACAgIAAxkBAAIFZGoOLIDGVD_NaS79eLjd4ezgsSaQAAIbH2sbB9txSOT9LZAsOhJPAQADAgADeQADOwQ",
        "text": "⭐ Отзыв 15\n\n"
    },
]

def convert_price(price_rub, country):
    rate = EXCHANGE_RATES.get(country, 1)
    return round(price_rub * rate)

CATEGORIES = {

    "protein": {
        "name": "🌈Психоделики",
        "subs": {

            "focus": {
                "name": "⚡ ЛСД",
                "items": [
                    {"name": "LSD 170 VHQ 1шт.", "price": 1300},
                    {"name": "LSD 250 VHQ 1шт.", "price": 1500}
                ]
            },

            "mush": {
                "name": "🍄 Грибы",
                "items": [
                    {"name": "Грибы PENIS ENVY 5гр.", "price": 6000},
                    {"name": "Грибы Psilocybe 3гр.", "price": 3500},
                    {"name": "Грибы NIAGARA 6гр.", "price": 5500},
                    {"name": "Грибы GOLDEN TEACHER 10гр.", "price": 7900}
                ]
            }
        }
    },

    "stim": {
        "name": "🚀 Стимуляторы",
        "subs": {

            "hard": {
                "name": "🔥 Кокаин",
                "items": [
                    {"name": "Кокаин BOSS 1гр.", "price": 9300},
                    {"name": "Кокаин Bentley 0.5гр.", "price": 6500},
                    {"name": "Кокаин Rolex 0.5гр.", "price": 6500},
                    {"name": "Крэк 1гр.", "price": 12500}
                ]
            },

            "amp": {
                "name": "⚙ Амфетамин",
                "items": [
                    {"name": "Амфетамин 1гр.", "price": 2700},
                    {"name": "Амфетамин (мука,порошок) 0.5гр.", "price": 2900}
                ]
            },

            "meta": {
                "name": "🧊 Метамфетамин",
                "items": [
                    {"name": "Метамфетамин 0.5гр.", "price": 2900},
                    {"name": "Метамфетамин (мука,порошок) 1гр.", "price": 5300}
                ]
            },

            "alpha": {
                "name": "⚡ Альфа-PVP",
                "items": [
                    {"name": "Альфа-PVP 0.5гр.", "price": 2600},
                    {"name": "Альфа-PVP (мука,порошок) 1гр.", "price": 2700}
                ]
            }
        }
    },

    "happy": {
        "name": "🎉 Эйфоретики",
        "subs": {

            "boost": {
                "name": "⚡ Мефедрон",
                "items": [
                    {"name": "Мефедрон (кристаллы) 0.5гр.", "price": 2200},
                    {"name": "Мефедрон (мука,порошок) 0.5гр.", "price": 1600}
                ]
            },

            "tabs": {
                "name": "💊 Экстази",
                "items": [
                    {"name": "Экстази MIX 1шт.", "price": 1500}
                ]
            },

            "crystal": {
                "name": "💎 МДМА",
                "items": [
                    {"name": "МДМА ШАМПАНЬ 0.5гр.", "price": 4500},
                    {"name": "МДМА White 1гр.", "price": 8900},
                    {"name": "МДМА Прозрачный кристалл 0.5гр.", "price": 2700}
                ]
            }
        }
    },

    "green": {
        "name": "🌿 Марихуана",
        "subs": {

            "buds": {
                "name": "🍃 Бошки",
                "items": [
                    {"name": "Бошки White widow 1гр.", "price": 2700},
                    {"name": "Бошки Amnesia 1гр.", "price": 2500}
                ]
            },

            "cones": {
                "name": "🌱 Шишки",
                "items": [
                    {"name": "Шишки АК-47 1гр.", "price": 2300},
                    {"name": "Шишки Galosa 1гр.", "price": 2500},
                    {"name": "Шишки Critical Cush 1гр.", "price": 3100}
                ]
            },

            "hash": {
                "name": "🟫 Гашиш",
                "items": [
                    {"name": "Гашиш Spain King 1гр.", "price": 2800},
                    {"name": "Гашиш Liverpool 1гр.", "price": 2700}
                ]
            }
        }
    },

    "recovery": {
        "name": "🖤 Опиаты",
        "subs": {

            "hero": {
                "name": "💉 Опиаты(всё вместе)",
                "items": [
                    {"name": "Героин 0.25гр.", "price": 2600},
                    {"name": "Метадон 0.25гр.", "price": 2700},
                    {"name": "Трамадол 100 мг. органика 20шт.", "price": 7100}
                ]
            }
        }
    },

    "pharma": {
        "name": "⚕️ Аптека",
        "subs": {

            "meds": {
                "name": "💊 Pharma",
                "items": [

                    {"name": "1⚕️ Лирика 300 мг. 4шт.", "price": 2200},
                    {"name": "2🚑 Габапентин 300 мг. 10шт.", "price": 1900},
                    {"name": "3⚕️ Акинетон 1шт.", "price": 1900},
                    {"name": "4🚑 Седалит 300 мг. 1шт.", "price": 1400},
                    {"name": "5⚕️ Кетамин 0.5 гр.", "price": 3100},
                    {"name": "6🚑 Венлафаксин-Алси 1шт.", "price": 3300},
                    {"name": "7⚕️ Фаназепам 2гр.", "price": 1700},
                    {"name": "8🚑 Ксанакс 4шт.", "price": 4300},
                    {"name": "9⚕️ Флуоксетин 20мг. 60шт.", "price": 4100},
                    {"name": "10🚑 Золофт 100мг. 20шт.", "price": 3300},
                    {"name": "11⚕️ Триттико 150мг. 20шт.", "price": 4500},
                    {"name": "12🚑 Атаракс(аналог фаназепам) 25мг. 25шт.", "price": 1400},
                    {"name": "13⚕️ Баклофен\Баклосан 25мг. 50шт.", "price": 6000},
                    {"name": "14🚑 Когниттера 40мг. Атомоксетин 14шт.", "price": 6750},
                    {"name": "15⚕️ Седжаро(Тирзепатид) 2.5мг.", "price": 11800}

                ]
            }
        }
    }
}


def menu(user_data):
    country = user_data.get("country")
    btn = COUNTRIES_SHORT.get(country, "🌍 Страна")

    return InlineKeyboardMarkup([
        [InlineKeyboardButton(btn, callback_data="country_menu")],
        [InlineKeyboardButton("🛒 Каталог", callback_data="shop")],
        [InlineKeyboardButton("⭐ Отзывы", callback_data="reviews")],
        [InlineKeyboardButton("💼 Работа", callback_data="job")],
        [InlineKeyboardButton("💬 Поддержка", callback_data="support")]
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Добро пожаловать",
        reply_markup=menu(context.user_data)
    )


async def country_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    kb = [
        [InlineKeyboardButton("🇷🇺 РФ", callback_data="set_rf")],
        [InlineKeyboardButton("🇧🇾 РБ", callback_data="set_rb")],
        [InlineKeyboardButton("🇰🇿 КЗ", callback_data="set_kz")],
        [InlineKeyboardButton("🇵🇱 PL", callback_data="set_pl")],
        [InlineKeyboardButton("⬅ Назад", callback_data="back_menu")]
    ]

    await q.edit_message_text(
        "🌍 Выберите страну:",
        reply_markup=InlineKeyboardMarkup(kb)
    )


async def set_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    country = q.data.replace("set_", "")
    context.user_data["country"] = country

    await q.edit_message_text(
        f"✅ {COUNTRIES_FULL[country]}",
        reply_markup=menu(context.user_data)
    )


async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    # Проверка страны
    if not context.user_data.get("country"):
        await q.edit_message_text(
            "❌ Ошибка\n\nСначала выберите страну",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🌍 Выбрать страну", callback_data="country_menu")],
                [InlineKeyboardButton("⬅ Назад", callback_data="back_menu")]
            ])
        )
        return

    kb = []

    for cat_id, cat in CATEGORIES.items():
        kb.append([
            InlineKeyboardButton(cat["name"], callback_data=f"cat_{cat_id}")
        ])

    kb.append([InlineKeyboardButton("⬅ Назад", callback_data="back_menu")])

    await q.edit_message_text(
        "🛒 Категории:",
        reply_markup=InlineKeyboardMarkup(kb)
    )


async def select_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    cat_id = q.data.replace("cat_", "")
    context.user_data["category"] = cat_id

    kb = []

    subs = CATEGORIES[cat_id]["subs"]

    for sub_id, sub in subs.items():
        kb.append([
            InlineKeyboardButton(sub["name"], callback_data=f"sub_{sub_id}")
        ])

    kb.append([
        InlineKeyboardButton("⬅ Назад", callback_data="shop")
    ])

    await q.edit_message_text(
        "📂 Разделы:",
        reply_markup=InlineKeyboardMarkup(kb)
    )


async def select_sub(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    sub_id = q.data.replace("sub_", "")
    context.user_data["sub"] = sub_id

    cat_id = context.user_data["category"]

    items = CATEGORIES[cat_id]["subs"][sub_id]["items"]

    kb = []

    for i, item in enumerate(items):
        country = context.user_data.get("country", "rf")
        price = convert_price(item["price"], country)
        symbol = CURRENCY_SYMBOL.get(country, "₽")

        text = f'{item["name"]} - {price}{symbol}'

        kb.append([
            InlineKeyboardButton(
                text,
                callback_data=f"item_{i}"
            )
        ])

    kb.append([
        InlineKeyboardButton("⬅ Назад", callback_data=f"cat_{cat_id}")
    ])

    await q.edit_message_text(
        "📦 Товары:",
        reply_markup=InlineKeyboardMarkup(kb)
    )


async def select_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    i = int(q.data.replace("item_", ""))

    cat_id = context.user_data["category"]
    sub_id = context.user_data["sub"]

    item = CATEGORIES[cat_id]["subs"][sub_id]["items"][i]

    context.user_data["product"] = item
    context.user_data["step"] = "amount"
    context.user_data["product"] = item

    # минимальное количество (по умолчанию 1)
    name = item["name"].lower()

    if "0.25" in name:
        context.user_data["min_qty"] = 0.25
    elif "0.5" in name:
        context.user_data["min_qty"] = 0.5
    else:
        context.user_data["min_qty"] = 1

    await q.edit_message_text(
        f"⚖ Введите количество\n\n"
        f"Цена за 1: {item['price']} ₽\n\n"
        f"Минимум: 0.5 или 1 (зависит от товара)"
    )
    return


async def select_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    city = q.data.replace("city_", "")
    context.user_data["city"] = city
    context.user_data["step"] = "district"

    country = context.user_data["country"]
    districts = DATA_MAP[country][city]

    kb = [
        [InlineKeyboardButton(d, callback_data=f"dist_{d}")]
        for d in districts
    ]

    await q.edit_message_text(
        "🏘 Выберите район:",
        reply_markup=InlineKeyboardMarkup(kb)
    )


async def select_district(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    district = q.data.replace("dist_", "")
    context.user_data["district"] = district
    context.user_data["step"] = "payment"

    product = context.user_data["product"]

    country = context.user_data.get("country", "rf")
    price = convert_price(product["price"], country)

    qty = context.user_data.get("amount", 1)

    name = product["name"].lower()

    if "0.25" in name:
        item_qty = 0.25
    elif "0.5" in name:
        item_qty = 0.5
    else:
        item_qty = 1

    total = (qty / item_qty) * price

    symbol = CURRENCY_SYMBOL.get(country, "₽")
    context.user_data["total_price"] = total

    if country == "pl":
        text = (
            f"💳 ВЫБЕРИТЕ ОПЛАТУ\n\n"
            f"💰 СУММА: {total} {symbol}\n\n"
            "1 - 💳 BLIK\n"
            "2 - 🏦 Перевод\n"
            "3 - ₿ USDT"
        )
    else:
        text = (
            f"💳 ВЫБЕРИТЕ ОПЛАТУ\n\n"
            f"💰 СУММА: {total} ₽\n\n"
            "1 - 💳 СБП\n"
            "2 - 🏦 Перевод\n"
            "3 - ₿ USDT"
        )

    await q.edit_message_text(text)


async def all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if context.user_data.get("step") == "amount":

        try:
            qty = float(text.replace(",", ".").replace("гр", "").strip())
        except:
            await update.message.reply_text("❌ Введите число (например 1 или 0.5)")
            return

        min_qty = context.user_data.get("min_qty", 1)

        if qty < min_qty:
            await update.message.reply_text(
                f"❌ Минимальное количество: {min_qty}"
            )
            return

        product = context.user_data["product"]
        country = context.user_data.get("country", "rf")
        price = convert_price(product["price"], country)

        name = product["name"].lower()

# сколько грамм указано в товаре
        if "0.25" in name:
            item_qty = 0.25
        elif "0.5" in name:
            item_qty = 0.5
        else:
            item_qty = 1

# правильный расчёт
        total = (qty / item_qty) * price

        context.user_data["amount"] = qty
        context.user_data["total_price"] = total

    # 🔥 ПЕРЕХОД НА ГОРОД
        context.user_data["step"] = "city"

        cities = DATA_MAP[country].keys()

        kb = [
            [InlineKeyboardButton(city, callback_data=f"city_{city}")]
            for city in cities
        ]

        await update.message.reply_text(
            f"💰 К оплате: {total} ₽\n\n🌍 Выберите город (❗️❗️Если вашего города\ПГТ\Посёлка нету из перечисленых тогда напишите менеджеру❗️❗️):",
            reply_markup=InlineKeyboardMarkup(kb)
        )

        return

    if context.user_data.get("step") == "payment":

        if text not in ["1", "2", "3"]:
            await update.message.reply_text("❌ Введите 1, 2 или 3")
            return

        country = context.user_data.get("country", "не указана")
        city = context.user_data.get("city", "не указан")
        district = context.user_data.get("district", "не указан")

        if country == "pl":
            methods = {
                "1": "💳 BLIK",
                "2": "🏦 Перевод",
                "3": "₿ USDT"
            }
        else:
            methods = {
                "1": "💳 СБП",
                "2": "🏦 Перевод",
                "3": "₿ USDT"
            }

        method = methods[text]
        user = update.message.from_user

        symbol = CURRENCY_SYMBOL.get(country, "₽")

        order_msg = (
            f"🛒 НОВЫЙ ЗАКАЗ\n\n"
            f"👤 @{user.username or 'no_username'}\n"
            f"🆔 {user.id}\n\n"
            f"🌍 {COUNTRIES_FULL.get(country, country)}\n"
            f"🏙 {city}\n"
            f"🏘 {district}\n\n"
            f"📦 {context.user_data['product']['name']}\n"
            f"💰 {context.user_data['total_price']} {symbol}\n"
            f"💳 {method}"
        )

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=order_msg
        )

        await update.message.reply_text(
            f"✅ Вы выбрали: {method}\n\n"
            f"💰 К оплате: {context.user_data['total_price']} ₽\n\n"
            "📤 Реквизиты отправит администратор"
        )

        context.user_data["step"] = None
        return

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message or not update.message.text:
        return

    # если идёт оформление заказа
    if context.user_data.get("step") in ["amount", "payment"]:
        await all_messages(update, context)
        return

    # обычные сообщения → оператору
    await user_to_admin(update, context)


async def reviews(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    index = 0
    context.user_data["review_index"] = index

    review = REVIEWS[index]

    kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⬅", callback_data="review_-1"),
            InlineKeyboardButton("➡", callback_data="review_1")
        ],
        [
            InlineKeyboardButton("⬅ Назад", callback_data="back_menu")
        ]
    ])

    await q.message.edit_media(
        media=InputMediaPhoto(
            media=review["photo"],
            caption=review["text"]
        ),
        reply_markup=kb
    )

async def review_pages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    index = int(q.data.replace("review_", ""))

    if index < 0:
        index = len(REVIEWS) - 1
    if index >= len(REVIEWS):
        index = 0

    review = REVIEWS[index]

    kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⬅", callback_data=f"review_{index - 1}"),
            InlineKeyboardButton("➡", callback_data=f"review_{index + 1}")
        ],
        [
            InlineKeyboardButton("⬅ Назад", callback_data="back_menu")
        ]
    ])

    await q.message.edit_media(
        media=InputMediaPhoto(
            media=review["photo"],
            caption=review["text"]
        ),
        reply_markup=kb
    )

async def job(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    text = (
        "💼 ВАКАНСИЯ\n\n"

        "📢 Открыт набор в ПИАР-команду.\n\n"

        "📍 Местоположение не имеет значения\n"
        "🕒 Свободный график\n"
        "💰 Доход: 150–300$ на первых 2 неделях\n"
        "📈 Возможность долгосрочного сотрудничества\n\n"

        "📩 По поводу вакансии обращайтесь к менеджеру:\n"
        "@manager_junko"
    )

    await q.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "💬 Написать менеджеру",
                    url="https://t.me/manager_junko"
                )
            ],
            [
                InlineKeyboardButton("⬅ Назад", callback_data="back_menu")
            ]
        ])
    )

async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    await q.edit_message_text(
        "💬 Напишите менеджеру: @manager_junko",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅ Назад", callback_data="back_menu")]
        ])
    )


async def user_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    msg = (
        f"📩 СООБЩЕНИЕ ОТ ПОЛЬЗОВАТЕЛЯ\n\n"
        f"👤 @{user.username or 'no_username'}\n"
        f"🆔 {user.id}\n\n"
        f"💬 {text}"
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=msg
    )


async def relay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    if len(context.args) < 2:
        await update.message.reply_text("❌ Формат: /relay user_id текст")
        return

    user_id = int(context.args[0])
    text = " ".join(context.args[1:])

    try:
        await context.bot.send_message(
            chat_id=user_id,
            text=f"💬 Ответ оператора:\n\n{text}"
        )

        await update.message.reply_text("✅ Отправлено")

    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка отправки: {e}")


async def back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    msg = q.message

if msg.text:
    await msg.edit_text("ТВОЙ ТЕКСТ НАЗАД")
elif msg.caption:
    await msg.edit_caption("ТВОЙ ТЕКСТ НАЗАД")
else:
    await msg.reply_text("ТВОЙ ТЕКСТ НАЗАД")
        reply_markup=menu(context.user_data)
    )

async def relay_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.from_user.id != ADMIN_ID:
        return

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "❌ Ответьте на сообщение пользователя фото"
        )
        return

    # получаем user_id из сообщения
    text = update.message.reply_to_message.text

    try:
        user_id = int(text.split("🆔 ")[1].split("\n")[0])
    except:
        await update.message.reply_text("❌ Не удалось получить ID")
        return

    photo = update.message.photo[-1].file_id

    caption = update.message.caption or ""

    try:
        await context.bot.send_photo(
            chat_id=user_id,
            photo=photo,
            caption=f"💬 Фото от оператора:\n\n{caption}"
        )

        await update.message.reply_text("✅ Фото отправлено")

    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}")

async def user_media_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user

    caption = (
        f"📩 МЕДИА ОТ ПОЛЬЗОВАТЕЛЯ\n\n"
        f"👤 @{user.username or 'no_username'}\n"
        f"🆔 {user.id}"
    )

    # ФОТО
    if update.message.photo:

        photo = update.message.photo[-1].file_id

        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo,
            caption=caption
        )

    # ФАЙЛ
    elif update.message.document:

        document = update.message.document.file_id

        await context.bot.send_document(
            chat_id=ADMIN_ID,
            document=document,
            caption=caption
        )

    # ВИДЕО
    elif update.message.video:

        video = update.message.video.file_id

        await context.bot.send_video(
            chat_id=ADMIN_ID,
            video=video,
            caption=caption
        )

    # ГОЛОСОВОЕ
    elif update.message.voice:

        voice = update.message.voice.file_id

        await context.bot.send_voice(
            chat_id=ADMIN_ID,
            voice=voice,
            caption=caption
        )

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(CommandHandler("relay", relay))

    app.add_handler(CallbackQueryHandler(back, pattern="back_menu"))
    app.add_handler(CallbackQueryHandler(country_menu, pattern="country_menu"))
    app.add_handler(CallbackQueryHandler(set_country, pattern="set_"))

    app.add_handler(CallbackQueryHandler(shop, pattern="shop"))
    app.add_handler(CallbackQueryHandler(select_category, pattern="cat_"))
    app.add_handler(CallbackQueryHandler(select_sub, pattern="sub_"))
    app.add_handler(CallbackQueryHandler(select_item, pattern="item_"))

    app.add_handler(CallbackQueryHandler(select_city, pattern="city_"))
    app.add_handler(CallbackQueryHandler(select_district, pattern="dist_"))

    app.add_handler(CallbackQueryHandler(reviews, pattern="reviews"))
    app.add_handler(CallbackQueryHandler(job, pattern="job"))
    app.add_handler(CallbackQueryHandler(review_pages, pattern="review_"))
    app.add_handler(CallbackQueryHandler(support, pattern="support"))

    app.add_handler(
        MessageHandler(
            filters.PHOTO & filters.User(ADMIN_ID),
            relay_photo
        )
    )

    app.add_handler(
        MessageHandler(
            filters.PHOTO |
            filters.Document.ALL |
            filters.VIDEO |
            filters.VOICE,
            user_media_to_admin
        )
    )

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))

    print("Bot started")
    app.run_polling()


if __name__ == "__main__":
    main()