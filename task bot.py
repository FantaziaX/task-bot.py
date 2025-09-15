import asyncio
import json
import os
import time
import random
from typing import Dict, Any, Optional
from random import choice
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

# ================== Настройки ==================
TOKEN = os.getenv('BOT_TOKEN', '8332411735:AAFzUvuzPnESLyQXxq1LTvO1HEin0LfSZQg')
ADMIN_ID = int(os.getenv('ADMIN_ID', '7944675607'))
ADMIN_PASSWORD = "gg666gg3_123"
DATA_FILE = "data.json"
ADMIN_USERNAME = "@FantaziaX"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ================== Магазин ==================
gear_items = [
    {"name": "🛡️ Броня 6 ур (Деф)", "price": 150, "category": "gear"},
    {"name": "🛡️ Броня 6 ур (СФ)", "price": 200, "category": "gear"},
    {"name": "🛡️ Броня 6 ур (КБ)", "price": 180, "category": "gear"},
    {"name": "⛑️ Шлем 6 ур (Деф)", "price": 150, "category": "gear"},
    {"name": "⛑️ Шлем 6 ур (СФ)", "price": 200, "category": "gear"},
    {"name": "⛑️ Шлем 6 ур (КБ)", "price": 180, "category": "gear"},
    {"name": "🎒 Рюкзак 6 ур", "price": 100, "category": "gear"},
]

weapon_items = [
    {"name": "🔫 МК14", "price": 70, "category": "weapon"},
    {"name": "🔫 АКМ", "price": 70, "category": "weapon"},
    {"name": "🔫 P90", "price": 70, "category": "weapon"},
    {"name": "🔫 AWM", "price": 90, "category": "weapon"},
    {"name": "🔫 AMR", "price": 90, "category": "weapon"},
    {"name": "🔫 M416", "price": 70, "category": "weapon"},
    {"name": "🔫 AUG", "price": 70, "category": "weapon"},
    {"name": "🔫 Гроза", "price": 70, "category": "weapon"},
    {"name": "🔫 M762", "price": 70, "category": "weapon"},
    {"name": "🔫 MG3", "price": 80, "category": "weapon"},
    {"name": "🔫 DBS", "price": 70, "category": "weapon"},
]

# ================== Квесты ==================
QUEST_REWARD = 5
available_quests = [
    {"id": f"q{i+1}", "text": text, "reward": QUEST_REWARD}
    for i, text in enumerate([
        "Сделай 3 кила с AWM",
        "Выиграй 2 катки подряд в TDM",
        "Открой кейс за 800к",
        "Собери полный комплект шмоток 6 уровня",
        "Используй рюкзак и шлем в одной катке",
        "Выстрели 50 раз из любого оружия",
        "Участвуй в 5 катках подряд",
        "Сделай 10 убийств в одной катке",
        "Выиграй матч без смертей",
        "Собери 3 разных пушки",
        "Повышай уровень оружия до 5 ур",
        "Используй гранату в катке",
        "Пройди миссию метро за 1 попытку",
        "Выиграй катку с командой полностью",
        "Сделай 2 убийства подряд без урона",
        "Собери 500 монет в катке",
        "Используй аптечку 3 раза",
        "Попади в 5 хедшотов подряд",
        "Выиграй матч с использованием только пистолетов",
        "Открой 3 кейса подряд",
        "Собери 3 одинаковых предмета экипировки",
        "Сделай 5 убийств с одной пушки",
        "Выиграй матч с AWM",
        "Используй аптечку и броню одновременно",
        "Сделай 3 убийства с гранатой",
        "Выстрели в голову 10 раз подряд",
        "Выиграй матч TDM без смертей",
        "Собери 5 разных пушек",
        "Сделай 7 убийств в одной катке",
        "Открой кейс за 500к",
        "Выиграй матч с командой 3 игрока",
        "Собери комплект шмоток 5 уровня",
        "Сделай 3 убийства с М416",
        "Используй аптечку и шлем в одной катке",
        "Выстрели 20 раз с P90",
        "Выиграй матч с использованием только AWM",
        "Сделай 2 убийства подряд без урона",
        "Собери 200 монет в одной катке",
        "Используй рюкзак и броню одновременно",
        "Сделай 10 выстрелов в голову",
        "Выиграй матч с командой полностью",
        "Сделай 3 убийства с DBS",
        "Открой 2 кейса подряд",
        "Собери 4 одинаковых предмета экипировки",
        "Сделай 5 убийств с M762",
    ])
]

# ================== Работа с data.json ==================
def ensure_datafile():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({"users": {}}, f, ensure_ascii=False, indent=2)

def load_data() -> Dict[str, Any]:
    ensure_datafile()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data: Dict[str, Any]):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_user_record(uid: int) -> Dict[str, Any]:
    data = load_data()
    users = data.setdefault("users", {})
    s = str(uid)
    if s not in users:
        users[s] = {
            "profile": {
                "username": None, 
                "first_seen": int(time.time()), 
                "last_seen": int(time.time()), 
                "time_spent": 0,
                "completed_quests": 0
            },
            "economy": {"coins": 100, "earned": 0, "spent": 0},
            "inventory": [],
            "quests": {"active": None, "history": []},
            "admin_state": {
                "awaiting_admin_pass": False, 
                "awaiting_user_id": False, 
                "awaiting_coins": False, 
                "awaiting_item": False,
                "is_admin": False
            },
            "game_state": {
                "awaiting_guess": False,
                "target_number": 0
            },
            "feedback": [],
            "contact_state": {
                "awaiting_quest_submit": False,
                "awaiting_bug_report": False,
                "awaiting_bot_request": False
            }
        }
        save_data(data)
    return users[s]

def update_user_record(uid: int, record: Dict[str, Any]):
    data = load_data()
    data["users"][str(uid)] = record
    save_data(data)

# ================== Клавиатуры ==================
def start_menu_markup() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📋 Главное меню", callback_data="menu:main")
    builder.button(text="📞 Связь с админом", callback_data="menu:contact_options")
    return builder.as_markup()

def contact_admin_markup() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Сдать задание", callback_data="contact:submit_quest")
    builder.button(text="🐞 Сообщить об ошибке/баге", callback_data="contact:report_bug")
    builder.button(text="🤖 Запрос на нового бота", callback_data="contact:request_bot")
    builder.button(text="◀️ Назад", callback_data="menu:start")
    return builder.as_markup()

def main_menu_markup(uid: Optional[int] = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🎯 Задания", callback_data="menu:quests")
    builder.button(text="🎮 Игры", callback_data="menu:games")
    builder.button(text="🛒 Магазин", callback_data="menu:shop")
    builder.row(
        InlineKeyboardButton(text="🎒 Инвентарь", callback_data="menu:inv"),
        InlineKeyboardButton(text="📜 Профиль", callback_data="menu:profile")
    )
    builder.row(
        InlineKeyboardButton(text="📤 Фидбек", callback_data="menu:feedback")
    )
    if uid == ADMIN_ID or (uid and get_user_record(uid)["admin_state"]["is_admin"]):
        builder.button(text="⚙️ Админ-меню", callback_data="menu:admin")
    builder.button(text="💰 Баланс", callback_data="menu:balance")
    builder.button(text="◀️ Назад", callback_data="menu:start")
    return builder.as_markup()

def quests_markup() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Взять новый квест", callback_data="quest:new")
    builder.button(text="История квестов", callback_data="quest:history")
    builder.button(text="◀️ Назад", callback_data="menu:main")
    return builder.as_markup()

def games_markup() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🎲 Кости", callback_data="game:dice")
    builder.button(text="❌⭕ Крестики-нолики", callback_data="game:tictactoe")
    builder.button(text="🔢 Угадай число", callback_data="game:guess")
    builder.button(text="◀️ Назад", callback_data="menu:main")
    return builder.as_markup()

def shop_categories_markup() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🎽 Шмотки", callback_data="shop:gear")
    builder.button(text="🔫 Пушки", callback_data="shop:weapons")
    builder.button(text="◀️ Назад", callback_data="menu:main")
    return builder.as_markup()

def shop_items_markup(category: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    if category == "gear":
        items = gear_items
    else:
        items = weapon_items
        
    for item in items:
        builder.button(text=f"{item['name']} - {item['price']}💰", callback_data=f"buy:{item['name']}")
    
    builder.button(text="◀️ Назад", callback_data="menu:shop")
    builder.adjust(1)
    return builder.as_markup()

def tictactoe_markup(board: list = None) -> InlineKeyboardMarkup:
    if board is None:
        board = [" "] * 9
        
    builder = InlineKeyboardBuilder()
    for i in range(9):
        builder.button(text=board[i], callback_data=f"ttt:{i}")
    builder.button(text="◀️ Назад", callback_data="menu:games")
    builder.adjust(3, 3, 1)
    return builder.as_markup()

def admin_menu_markup() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="💰 Выдать монеты", callback_data="admin:give_coins")
    builder.button(text="🎁 Выдать предмет", callback_data="admin:give_item")
    builder.button(text="📊 Статистика", callback_data="admin:stats")
    builder.button(text="◀️ Назад", callback_data="menu:main")
    return builder.as_markup()

# ================== Вспомогательные функции ==================
def format_time(seconds: int) -> str:
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{hours}ч {minutes}м"

# ================== Обработчики ==================
@dp.message(Command("start"))
async def cmd_start(message: Message):
    rec = get_user_record(message.from_user.id)
    rec["profile"]["username"] = message.from_user.username
    rec["profile"]["last_seen"] = int(time.time())
    update_user_record(message.from_user.id, rec)
    await message.answer("Привет! Выберите опцию:", reply_markup=start_menu_markup())

@dp.callback_query(lambda c: c.data == "menu:start")
async def back_to_start(callback: CallbackQuery):
    uid = callback.from_user.id
    rec = get_user_record(uid)
    rec["profile"]["last_seen"] = int(time.time())
    update_user_record(uid, rec)
    
    try:
        await callback.message.delete()
    except:
        pass
    
    msg = await callback.message.answer("Выберите опцию:", reply_markup=start_menu_markup())
    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("menu:"))
async def menu_handler(callback: CallbackQuery):
    uid = callback.from_user.id
    rec = get_user_record(uid)
    rec["profile"]["last_seen"] = int(time.time())
    update_user_record(uid, rec)
    
    try:
        await callback.message.delete()
    except:
        pass
    
    if callback.data == "menu:quests":
        msg = await callback.message.answer("Выберите действие с квестами:", reply_markup=quests_markup())
    elif callback.data == "menu:games":
        msg = await callback.message.answer("🎮 Выберите игру:", reply_markup=games_markup())
    elif callback.data == "menu:shop":
        msg = await callback.message.answer("🛒 Выберите категорию магазина:", reply_markup=shop_categories_markup())
    elif callback.data == "menu:inv":
        if rec["inventory"]:
            inventory_text = "\n".join(f"• {item}" for item in rec["inventory"])
            msg = await callback.message.answer(f"🎒 Ваш инвентарь:\n{inventory_text}")
        else:
            msg = await callback.message.answer("🎒 Ваш инвентарь пуст.")
    elif callback.data == "menu:profile":
        time_spent = int(time.time()) - rec["profile"]["first_seen"]
        profile_text = f"""
📜 Профиль @{rec['profile']['username'] or 'Неизвестно'}:
⏰ В боте: {format_time(time_spent)}
✅ Выполнено квестов: {rec['profile']['completed_quests']}
💰 Монет: {rec['economy']['coins']}
💵 Заработано: {rec['economy']['earned']}
💸 Потрачено: {rec['economy']['spent']}
        """
        msg = await callback.message.answer(profile_text)
    elif callback.data == "menu:feedback":
        msg = await callback.message.answer("📤 Отправьте ваш фидбек или доказательство выполнения квеста:")
    elif callback.data == "menu:contact_options":
        msg = await callback.message.answer("📞 Выберите тип обращения к администратору:", reply_markup=contact_admin_markup())
    elif callback.data == "menu:admin":
        # Проверяем, является ли пользователь админом
        if uid == ADMIN_ID or rec["admin_state"]["is_admin"]:
            msg = await callback.message.answer("⚙️ Админ-меню:", reply_markup=admin_menu_markup())
        else:
            rec["admin_state"]["awaiting_admin_pass"] = True
            update_user_record(uid, rec)
            msg = await callback.message.answer("Введите пароль администратора:")
    elif callback.data == "menu:balance":
        msg = await callback.message.answer(f"💰 Ваш баланс: {rec['economy']['coins']} монет")
    elif callback.data == "menu:main":
        msg = await callback.message.answer("Главное меню:", reply_markup=main_menu_markup(uid))
    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("contact:"))
async def contact_handler(callback: CallbackQuery):
    uid = callback.from_user.id
    rec = get_user_record(uid)
    
    try:
        await callback.message.delete()
    except:
        pass
    
    # Отправляем сообщение админу сразу при нажатии на кнопку
    if callback.data == "contact:submit_quest":
        contact_text = f"✅ Пользователь @{callback.from_user.username} (ID: {uid}) хочет сдать задание"
        await bot.send_message(ADMIN_ID, contact_text)
        msg = await callback.message.answer("✅ Ваш запрос отправлен администратору. Ожидайте ответа.")
        
    elif callback.data == "contact:report_bug":
        contact_text = f"🐞 Пользователь @{callback.from_user.username} (ID: {uid}) сообщает об ошибке/баге"
        await bot.send_message(ADMIN_ID, contact_text)
        msg = await callback.message.answer("✅ Ваш запрос отправлен администратору. Ожидайте ответа.")
        
    elif callback.data == "contact:request_bot":
        contact_text = f"🤖 Пользователь @{callback.from_user.username} (ID: {uid}) просит добавить/сделать нового бота"
        await bot.send_message(ADMIN_ID, contact_text)
        msg = await callback.message.answer("✅ Ваш запрос отправлен администратору. Ожидайте ответа.")
    
    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("shop:"))
async def shop_category_handler(callback: CallbackQuery):
    uid = callback.from_user.id
    rec = get_user_record(uid)
    
    try:
        await callback.message.delete()
    except:
        pass
    
    if callback.data == "shop:gear":
        msg = await callback.message.answer("🎽 Выберите шмотку для покупки:", reply_markup=shop_items_markup("gear"))
    elif callback.data == "shop:weapons":
        msg = await callback.message.answer("🔫 Выберите оружие для покупки:", reply_markup=shop_items_markup("weapons"))
    
    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("buy:"))
async def buy_item_handler(callback: CallbackQuery):
    uid = callback.from_user.id
    rec = get_user_record(uid)
    
    try:
        await callback.message.delete()
    except:
        pass
    
    item_name = callback.data.split(":", 1)[1]
    
    # Ищем предмет в магазине
    item = None
    for shop_item in gear_items + weapon_items:
        if shop_item["name"] == item_name:
            item = shop_item
            break
    
    if not item:
        msg = await callback.message.answer("❌ Такого предмета нет в магазине.")
        await callback.answer()
        return
    
    # Проверяем, хватает ли монет
    if rec["economy"]["coins"] >= item["price"]:
        # Списание монет
        rec["economy"]["coins"] -= item["price"]
        rec["economy"]["spent"] += item["price"]
        
        # Добавление предмета в инвентарь
        rec["inventory"].append(item["name"])
        
        update_user_record(uid, rec)
        
        msg = await callback.message.answer(f"✅ Покупка совершена успешно! Вы приобрели: {item['name']}")
    else:
        msg = await callback.message.answer("❌ Покупка не удалась. Не хватает монет.")
    
    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("quest:"))
async def quest_handler(callback: CallbackQuery):
    uid = callback.from_user.id
    rec = get_user_record(uid)
    rec["profile"]["last_seen"] = int(time.time())
    update_user_record(uid, rec)
    
    try:
        await callback.message.delete()
    except:
        pass
    
    if callback.data == "quest:new":
        quest = choice(available_quests)
        rec["quests"]["active"] = quest
        update_user_record(uid, rec)
        msg = await callback.message.answer(f"🎯 Новый квест:\n{quest['text']} — награда {quest['reward']} 💰")
    elif callback.data == "quest:history":
        history = rec["quests"]["history"]
        if history:
            history_text = "\n".join([f"{i+1}. {q['text']} - {q['reward']} 💰" for i, q in enumerate(history)])
            msg = await callback.message.answer(f"📜 История квестов:\n{history_text}")
        else:
            msg = await callback.message.answer("📜 История квестов пуста.")
    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("game:"))
async def game_handler(callback: CallbackQuery):
    uid = callback.from_user.id
    rec = get_user_record(uid)
    rec["profile"]["last_seen"] = int(time.time())
    update_user_record(uid, rec)
    
    try:
        await callback.message.delete()
    except:
        pass
    
    if callback.data == "game:dice":
        player_dice = random.randint(1, 6)
        bot_dice = random.randint(1, 6)
        
        result = "🎲 Вы выиграли!" if player_dice > bot_dice else "🎲 Бот выиграл!" if bot_dice > player_dice else "🎲 Ничья!"
        
        msg = await callback.message.answer(
            f"🎲 Игра в кости:\n\n"
            f"Ваш бросок: {player_dice}\n"
            f"Бросок бота: {bot_dice}\n\n"
            f"{result}"
        )
    elif callback.data == "game:tictactoe":
        msg = await callback.message.answer("❌⭕ Выберите клетку для хода:", reply_markup=tictactoe_markup())
    elif callback.data == "game:guess":
        rec["game_state"]["awaiting_guess"] = True
        rec["game_state"]["target_number"] = random.randint(1, 10)
        update_user_record(uid, rec)
        msg = await callback.message.answer("🔢 Я загадал число от 1 до 10. Попробуйте угадать!")
    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("ttt:"))
async def tictactoe_move_handler(callback: CallbackQuery):
    uid = callback.from_user.id
    rec = get_user_record(uid)
    
    try:
        await callback.message.delete()
    except:
        pass
    
    # Здесь должна быть логика игры в крестики-нолики
    # Для простоты просто покажем сообщение
    msg = await callback.message.answer("❌⭕ Игра в разработке. Скоро будет доступна!")
    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("admin:"))
async def admin_handler(callback: CallbackQuery):
    uid = callback.from_user.id
    if uid != ADMIN_ID and not get_user_record(uid)["admin_state"]["is_admin"]:
        await callback.answer("Доступ запрещен")
        return
    
    rec = get_user_record(uid)
    rec["profile"]["last_seen"] = int(time.time())
    update_user_record(uid, rec)
    
    try:
        await callback.message.delete()
    except:
        pass
    
    if callback.data == "admin:give_coins":
        rec["admin_state"]["awaiting_user_id"] = True
        rec["admin_state"]["awaiting_coins"] = True
        update_user_record(uid, rec)
        msg = await callback.message.answer("Введите ID пользователя и количество монет через пробел (например: 123456789 100):")
    elif callback.data == "admin:give_item":
        rec["admin_state"]["awaiting_user_id"] = True
        rec["admin_state"]["awaiting_item"] = True
        update_user_record(uid, rec)
        items_list = "\n".join([f"{i+1}. {item['name']}" for i, item in enumerate(gear_items + weapon_items)])
        msg = await callback.message.answer(f"Введите ID пользователя и название предмета через пробел:\n\nДоступные предметы:\n{items_list}")
    elif callback.data == "admin:stats":
        data = load_data()
        total_users = len(data["users"])
        active_today = sum(1 for user in data["users"].values() if time.time() - user["profile"]["last_seen"] < 86400)
        total_coins = sum(user["economy"]["coins"] for user in data["users"].values())
        
        stats_text = f"""
📊 Статистика бота:
👥 Всего пользователей: {total_users}
🔥 Активных за сегодня: {active_today}
💰 Всего монет в системе: {total_coins}
        """
        msg = await callback.message.answer(stats_text, reply_markup=admin_menu_markup())
    await callback.answer()

@dp.message()
async def handle_messages(message: Message):
    uid = message.from_user.id
    rec = get_user_record(uid)
    rec["profile"]["last_seen"] = int(time.time())
    
    # Обработка ввода пароля администратора
    if rec["admin_state"]["awaiting_admin_pass"]:
        if message.text == ADMIN_PASSWORD:
            rec["admin_state"]["awaiting_admin_pass"] = False
            rec["admin_state"]["is_admin"] = True
            update_user_record(uid, rec)
            try:
                await message.delete()
            except:
                pass
            await message.answer("Доступ разрешен. Админ-меню:", reply_markup=admin_menu_markup())
        else:
            await message.answer("Неверный пароль.")
            rec["admin_state"]["awaiting_admin_pass"] = False
            update_user_record(uid, rec)
    
    # Обработка выдачи монет
    elif rec["admin_state"]["awaiting_coins"] and (uid == ADMIN_ID or rec["admin_state"]["is_admin"]):
        try:
            user_id, coins = message.text.split()
            user_id = int(user_id)
            coins = int(coins)
            
            target_rec = get_user_record(user_id)
            target_rec["economy"]["coins"] += coins
            target_rec["economy"]["earned"] += coins
            update_user_record(user_id, target_rec)
            
            rec["admin_state"]["awaiting_coins"] = False
            rec["admin_state"]["awaiting_user_id"] = False
            update_user_record(uid, rec)
            
            try:
                await message.delete()
            except:
                pass
            
            await message.answer(f"✅ Пользователю {user_id} выдано {coins} монет")
            await bot.send_message(user_id, f"⚡ Администратор выдал вам {coins} монет!")
            
        except (ValueError, IndexError):
            await message.answer("Неверный формат. Введите ID пользователя и количество монет через пробел (например: 123456789 100)")
    
    # Обработка выдачи предмета
    elif rec["admin_state"]["awaiting_item"] and (uid == ADMIN_ID or rec["admin_state"]["is_admin"]):
        try:
            parts = message.text.split()
            user_id = int(parts[0])
            item_name = " ".join(parts[1:])
            
            # Проверяем, существует ли предмет
            item_exists = any(item["name"] == item_name for item in gear_items + weapon_items)
            
            if not item_exists:
                await message.answer("Такого предмета не существует в магазине.")
                return
            
            target_rec = get_user_record(user_id)
            target_rec["inventory"].append(item_name)
            update_user_record(user_id, target_rec)
            
            rec["admin_state"]["awaiting_item"] = False
            rec["admin_state"]["awaiting_user_id"] = False
            update_user_record(uid, rec)
            
            try:
                await message.delete()
            except:
                pass
            
            await message.answer(f"✅ Пользователю {user_id} выдан предмет: {item_name}")
            await bot.send_message(user_id, f"⚡ Администратор выдал вам предмет: {item_name}!")
            
        except (ValueError, IndexError):
            await message.answer("Неверный формат. Введите ID пользователя и название предмета через пробел")
    
    # Обработка угадывания числа
    elif rec["game_state"]["awaiting_guess"]:
        try:
            guess = int(message.text)
            target = rec["game_state"]["target_number"]
            
            if guess == target:
                reward = random.randint(5, 15)
                rec["economy"]["coins"] += reward
                rec["economy"]["earned"] += reward
                rec["game_state"]["awaiting_guess"] = False
                update_user_record(uid, rec)
                await message.answer(f"🎉 Правильно! Вы угадали число {target} и получаете {reward} монет!")
            else:
                hint = "больше" if guess < target else "меньше"
                await message.answer(f"❌ Неправильно. Загаданное число {hint} чем {guess}. Попробуйте еще раз.")
                
        except ValueError:
            await message.answer("Пожалуйста, введите число от 1 до 10.")
    
    # Обработка фидбека
    elif message.reply_to_message and message.reply_to_message.text == "📤 Отправьте ваш фидбек или доказательство выполнения квеста:":
        # Отправляем фидбек администратору
        feedback_text = f"📤 Фидбек от @{message.from_user.username} (ID: {uid}):\n{message.text}"
        await bot.send_message(ADMIN_ID, feedback_text)
        await message.answer("✅ Ваше сообщение отправлено администратору.")
        
        # Сохраняем фидбек в историю
        rec["feedback"].append({"text": message.text, "time": int(time.time())})
        update_user_record(uid, rec)
    
    # Обработка обычных сообщений (не reply)
    elif not message.reply_to_message:
        # Если это не ответ на сообщение, проверяем, не является ли оно фидбеком
        if "фидбек" in message.text.lower() or "отзыв" in message.text.lower():
            feedback_text = f"📤 Фидбек от @{message.from_user.username} (ID: {uid}):\n{message.text}"
            await bot.send_message(ADMIN_ID, feedback_text)
            await message.answer("✅ Ваше сообщение отправлено администратору.")
            
            # Сохраняем фидбек в историю
            rec["feedback"].append({"text": message.text, "time": int(time.time())})
            update_user_record(uid, rec)
    
    update_user_record(uid, rec)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
