from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ============ СТАРТ ============
start_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="👉 Хорошо, давай", callback_data="start_test")]
    ]
)

# ============ ВОПРОСЫ ============
def get_question_keyboard(question_num: int):
    if question_num == 1:
        buttons = [
            [InlineKeyboardButton(text="1️⃣ Когда кто-то обижен или злится", callback_data="q1_1")],
            [InlineKeyboardButton(text="2️⃣ Почти никогда", callback_data="q1_2")],
            [InlineKeyboardButton(text="3️⃣ Раньше говорили чаще", callback_data="q1_3")],
            [InlineKeyboardButton(text="4️⃣ Сложно сказать", callback_data="q1_4")]
        ]
    elif question_num == 2:
        buttons = [
            [InlineKeyboardButton(text="1️⃣ Утыкаемся в телефоны", callback_data="q2_1")],
            [InlineKeyboardButton(text="2️⃣ Смотрим кино или сериал", callback_data="q2_2")],
            [InlineKeyboardButton(text="3️⃣ Обсуждаем что-то важное", callback_data="q2_3")],
            [InlineKeyboardButton(text="4️⃣ Гуляем или занимаемся вместе", callback_data="q2_4")]
        ]
    else:  # question 3
        buttons = [
            [InlineKeyboardButton(text="1️⃣ Больше разговаривать", callback_data="q3_1")],
            [InlineKeyboardButton(text="2️⃣ Больше времени вместе", callback_data="q3_2")],
            [InlineKeyboardButton(text="3️⃣ Вернуть былую страсть", callback_data="q3_3")],
            [InlineKeyboardButton(text="4️⃣ Просто хочу понять, что происходит", callback_data="q3_4")]
        ]
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# ============ РЕЗУЛЬТАТЫ ============
def result_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Пройти тест заново", callback_data="restart")],
            [InlineKeyboardButton(text="📚 Полезные материалы", callback_data="materials")]
        ]
    )

# ============ МАТЕРИАЛЫ ============
materials_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📖 Гайд", callback_data="guide")],
        [InlineKeyboardButton(text="❓ Методика 5 ПОЧЕМУ", callback_data="five_whys")],
        [InlineKeyboardButton(text="✅ Чек-лист", callback_data="checklist")],
        [InlineKeyboardButton(text="🔄 Пройти тест заново", callback_data="restart_from_materials")]
    ]
)

def material_buttons(material_type: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад к материалам", callback_data="materials")]
        ]
    )
