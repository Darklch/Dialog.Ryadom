import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from aiogram.utils.formatting import Text, Bold, Italic, Code, Pre

from config import TOKEN
from states import TestStates
from keyboards import *
from text import *

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()


# ОТДЕЛЬНАЯ ФУНКЦИЯ ДЛЯ ОПРЕДЕЛЕНИЯ РЕЗУЛЬТАТА
def determine_result(answers: list) -> str:
    """
    answers = [ответ_на_вопрос1, ответ_на_вопрос2, ответ_на_вопрос3]
    Каждый ответ — это строка, начинающаяся с цифры
    """
    types_count = {"A": 0, "B": 0, "C": 0}
    
    # Тип А: ответы 1 или 2 в вопросах 1–2
    if answers[0] in ["1", "2"]:
        types_count["A"] += 1
    if answers[1] in ["1", "2"]:
        types_count["A"] += 1
    
    # Тип Б: ответы 3 или 4 в вопросе 1, ответ 4 в вопросе 3
    if answers[0] in ["3", "4"]:
        types_count["B"] += 1
    if answers[2] == "4":
        types_count["B"] += 1
    
    # Тип В: ответ 3 в вопросе 2, ответ 1 в вопросе 3
    if answers[1] == "3":
        types_count["C"] += 1
    if answers[2] == "1":
        types_count["C"] += 1
    
    # Определяем преобладающий тип
    max_type = max(types_count, key=types_count.get)
    
    # Если максимум 0 или все равны — универсальный
    if max(types_count.values()) == 0 or len(set(types_count.values())) == 1:
        return "4"
    
    return {"A": "1", "B": "2", "C": "3"}[max_type]


# ---- СТАРТ ----
@dp.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await state.clear()
    
    # Форматируем приветствие
    formatted_text = Text(
        "Привет. Меня зовут «Рядом» . Я простой бот. 😊\n\n",
        "Я здесь не для того, чтобы ставить диагнозы или говорить, что ты делаешь что-то не так. Честно говоря, я вообще не знаю, что у тебя происходит.\n\n",
        "Я просто хочу помочь тебе разобраться в своих ощущениях. Иногда, чтобы понять, что происходит в отношениях, нужно просто услышать правильный вопрос. Или увидеть ситуацию со стороны.🔍\n\n",
        "Давай я задам тебе 3 коротких вопроса. Ты выберешь варианты, которые тебе ближе всего. А в конце я предложу пару фраз, которые можно сказать партнеру при сложном разговоре.\n\n",
        Italic("Никакой магии. Просто подсказки. ✨")
    )
    
    await message.answer(
        formatted_text.as_html(),
        parse_mode="HTML",
        reply_markup=start_kb
    )


# ---- ОБРАБОТКА СТАРТОВОЙ КНОПКИ ----
@dp.callback_query(F.data == "start_test")
async def start_test(callback: CallbackQuery, state: FSMContext):
    await state.set_state(TestStates.question1)

    
    # Форматируем вопрос
    formatted_text = Text(
        Bold("Первый вопрос."), " Он про разговоры. 🗣️\n\n",
        "Как часто у вас получается говорить о том, что на душе, а не только о делах?\n\n"
        "1️⃣ Чаще всего только когда кто-то обижен или злится\n"
        "2️⃣Почти никогда. Обсуждаем только работу, детей или быт\n"
        "3️⃣ Раньше говорили чаще, сейчас всё реже. Я не знаю, как начать снова\n"
        "4️⃣ Сложно сказать. Я боюсь заводить такие темы первым(ой)\n"
    )
    
    await callback.message.answer(
        formatted_text.as_html(),
        parse_mode="HTML",
        reply_markup=get_question_keyboard(1)
    )
    await callback.answer()


# ---- ОБРАБОТКА ОТВЕТОВ НА ВОПРОСЫ ----
@dp.callback_query(F.data.startswith("q"))
async def handle_answer(callback: CallbackQuery, state: FSMContext):
    # Разбираем callback data
    data = callback.data
    question_num = int(data[1])  # q1_1 -> 1, q2_2 -> 2, etc.
    answer = data[3]  # q1_1 -> 1, q2_2 -> 2, etc.
    
    # Сохраняем ответ
    await state.update_data({f"q{question_num}": answer})
    
    # Определяем следующий вопрос
    next_question = question_num + 1
    
    if next_question <= 3:
        # Переход к следующему вопросу
        await state.set_state(getattr(TestStates, f"question{next_question}"))
        
        # Форматируем следующий вопрос
        if next_question == 2:
            formatted_text = Text(
                Bold("Второй вопрос."), " Представь обычный вечер. 🌙\n\n",
                "Как вы обычно проводите время, когда остаетесь вдвоем?\n\n"
                "1️⃣ Каждый утыкается в свой телефон или ноутбук. Иногда перекидываемся парой слов\n"
                "2️⃣ Смотрим кино или сериал. Обсуждаем только то, что происходит на экране\n"
                "3️⃣ Обсуждаем что-то важное\n"
                "4️⃣ Гуляем или занимаемся вместе\n"
            )
        else:  # question 3
            formatted_text = Text(
                Italic("И последний, третий вопрос."), "\n\n",
                "Если бы можно было что-то изменить прямо сейчас, что бы ты выбрал(а)? ✏\n\n"
                "1️⃣ Больше разговаривать\n"
                "2️⃣ Больше времени вместе\n"
                "3️⃣ Вернуть былую страсть\n"
                "4️⃣ Просто хочу понять, что происходит\n"
            )
        
        await callback.message.answer(
            formatted_text.as_html(),
            parse_mode="HTML",
            reply_markup=get_question_keyboard(next_question)
        )
    else:
        # Все вопросы отвечены - показываем результат
        data = await state.get_data()
        q1 = data.get("q1")
        q2 = data.get("q2")
        q3 = data.get("q3")
        
        # Определяем результат
        result_num = determine_result([q1, q2, q3])
        
        # Выбираем текст результата с форматированием
        result_texts = {
            "1": Text(
        Bold("Спасибо, что ответил(а)."), " 🙏 \n\n",
        "Знаешь, судя по твоим ответам, вы с партнером, кажется, превратились в удобных соседей. Быт, графики, экраны — они съедают всё пространство. И это не про то, что вы разлюбили друг друга. Это просто про привычку молчать. Она появляется незаметно. 📱\n\n",
        "Мне кажется, тебе могло бы помочь одно маленькое действие.\n\n",
        "Не надо говорить о чувствах. Просто предложи партнеру поиграть в игру:\n",
        Italic('«Слушай, давай сегодня вечером на час уберем все телефоны в ящик? Просто посидим, посмотрим друг на друга, вспомним, как это — быть вдвоем без экранов?»'), " 🎲 \n\n",
        Bold("Важно:"), " не жди, что этот час будет наполнен разговорами. Просто побудьте рядом. А если захочешь что-то спросить, можешь сказать:\n",
        Italic('«Если бы у нас был свободный день без дел, куда бы ты хотел(а) поехать?»')
    ),
            "2": Text(
        Bold("Спасибо, что ответил(а). 🙏"), "\n\n",
        "Похоже, ты боишься, что если заговоришь о своей грусти или одиночестве, то партнер воспримет это как обвинение. Или что после этого разговора всё пойдет под откос. Знакомо?\n\n",
        "Этот страх очень мешает. Но правда в том, что молчание разрушает отношения медленнее, но вернее, чем любой разговор. ⏳ \n\n",
        "Может быть, попробуешь не говорить сразу обо всем? Просто начни с одной фразы. Она про тебя, а не про него/неё:\n", Italic("""«Я чувствую себя немного одиноко, даже когда мы рядом. Я понимаю, что звучит странно. Просто хочется иногда говорить не только о делах. Ты не против, если я иногда буду задавать "глупые" вопросы?»"""), " 😌 \n\n"
        "Не вываливай всё сразу. Просто один вопрос. Посмотри на реакцию."
    ),
            "3": Text(
        Bold("Спасибо, что ответил(а)."), "🙏 \n\n",
        "Я чувствую по твоим ответам: ты помнишь, как раньше было тепло и легко. Сейчас этого тепла меньше, и ты не знаешь, как его вернуть. Кажется, что темы для разговоров просто закончились. 🌸 \n\n",
        "Честно говоря, темы не закончились. Просто вы перестали задавать друг другу открытые вопросы, на которые нельзя ответить «да» или «нет». \n\n",
        "Попробуй сегодня за ужином (или в любой спокойной обстановке) спросить просто:\n",
        Italic('«Если бы у нас выдался один свободный день, и мы могли делать всё, что захотим — где бы мы оказались и почему?» '), "🌍\n\n"
        "Или, если хочешь немного глубже, попробуй методику «Пять почему». Она помогает докопаться до сути. Например:", Italic('«Мне грустно, когда мы молчим». — Почему? — «Потому что я чувствую себя ненужным(ой)». — Почему? — «Потому что мне кажется, я тебя больше не интересую».'), "И так дальше.\n\n"
        "Ты не обязана(ен) докапываться до конца. Просто попробуй задать одно «почему» к своему первому чувству. Это поможет понять, что именно ты хочешь сказать."
    ),
            "4": Text(
        Bold("Спасибо, что ответил(а) 🙏"), "\n\n",
        "Знаешь, я не могу сказать, что у тебя какой-то один «тип» ситуации. Похоже, в ваших отношениях смешалось всё понемногу: и быт, и усталость, и страх, и желание что-то изменить. И это, на самом деле, нормально. Так бывает у большинства пар. 👥\n\n",
        "Мне кажется, самое сложное в такой ситуации — просто начать. Не с глобального разговора, а с маленького шага. \n\n"
        "Попробуй сегодня сделать самую простую вещь. Когда будете рядом, просто скажи:\n",
        Italic("«Слушай, я тут задумался(лась)… А как у тебя сегодня настроение по шкале от 1 до 10? Просто интересно»."), "🧩\n\n"
        "Это не обязывает к большому разговору. Но это открывает дверь. А дальше — посмотришь по реакции."
    )                                                                            
}
        
        result_text = result_texts.get(result_num, result_texts["4"])
        
        await callback.message.answer(
            result_text.as_html(),
            parse_mode="HTML",
            reply_markup=result_keyboard()
        )
        
    await callback.answer()


# ---- ОБРАБОТКА КНОПОК РЕЗУЛЬТАТОВ ----
@dp.callback_query(F.data == "restart")
async def restart(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    
    formatted_text = Text(
        "Привет. Меня зовут ", Bold("«Рядом»"), ". Я простой бот.\n\n",
        Bold("Давай я задам тебе 3 коротких вопроса."), " Ты выберешь варианты, которые тебе ближе всего. А в конце я предложу пару фраз, которые можно сказать партнеру при сложном разговоре.\n\n",
        Italic("Никакой магии. Просто подсказки.")
    )
    
    await callback.message.answer(
        formatted_text.as_html(),
        parse_mode="HTML",
        reply_markup=start_kb
    )
    await callback.answer()


@dp.callback_query(F.data == "materials")
async def show_materials(callback: CallbackQuery):
    formatted_text = Text(
        Bold("Отлично!"), " Я не психолог, но могу поделиться несколькими вещами, которые помогут:\n\n",
        "• Почитать про отношения\n",
        "• Методику «5 почему»\n",
        "• Чек-лист для разговора\n\n",
        Italic("Выбери, что тебе интересно:")
    )
    
    await callback.message.answer(
        formatted_text.as_html(),
        parse_mode="HTML",
        reply_markup=materials_kb
    )
    await callback.answer()

# ---- МАТЕРИАЛЫ: ГАЙД ----
@dp.callback_query(F.data == "guide")
async def guide(callback: CallbackQuery):
    formatted_text = Text(
        Bold("Гайд для разговора"), "\n\n",
        "Это простая памятка на 1 страницу, которая поможет начать сложный разговор.\n\n",
        Italic("Гайд здесь: https://dialog-ryadom.tilda.ws/materials")
    )
    
    await callback.message.answer(
        formatted_text.as_html(),
        parse_mode="HTML",
        reply_markup=material_buttons("guide")
    )
    await callback.answer()


# ---- МАТЕРИАЛЫ: МЕТОДИКА 5 ПОЧЕМУ ----
@dp.callback_query(F.data == "five_whys")
async def five_whys(callback: CallbackQuery):
    formatted_text = Text(
        Bold("Методика «5 почему»"), "\n\n",
        "Это инструмент, который помогает добраться до настоящей причины проблемы.\n\n",
        Italic("Методика здесь: https://dialog-ryadom.tilda.ws/materials")
    )
    
    await callback.message.answer(
        formatted_text.as_html(),
        parse_mode="HTML",
        reply_markup=material_buttons("five_whys")
    )
    await callback.answer()


# ---- МАТЕРИАЛЫ: ЧЕК-ЛИСТ ----
@dp.callback_query(F.data == "checklist")
async def checklist(callback: CallbackQuery):
    formatted_text = Text(
        Bold("Чек-лист для разговора"), "\n\n",
        "Это список из 5 вопросов, которые можно задать партнеру, чтобы лучше понять его состояние.\n\n",
        Italic("Чек-лист здесь: https://dialog-ryadom.tilda.ws/materials")
    )
    
    await callback.message.answer(
        formatted_text.as_html(),
        parse_mode="HTML",
        reply_markup=material_buttons("checklist")
    )
    await callback.answer()

# ---- ПЕРЕЗАПУСК ИЗ МАТЕРИАЛОВ ----
@dp.callback_query(F.data == "restart_from_materials")
async def restart_from_materials(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    
    await callback.message.answer(
        "Давай начнем сначала! 👋",
        reply_markup=start_kb
    )
    await callback.answer()

# ---- ЗАПУСК ----
async def main():
    # Удаляем вебхук перед запуском
    await bot.delete_webhook(drop_pending_updates=True)
    print("✅ Webhook удален!")
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
