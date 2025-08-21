from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import CallbackQuery
from aiogram import F
from database import get_all_cities, get_all_streets, get_all_homes, get_all_sections, get_all_lifts, get_city_name, \
    get_street_name, get_home_name, get_section_name, get_history
from math import ceil
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()  # очищаем старое состояние

    cities = await get_all_cities()
    if not cities:
        msg = await message.answer("Нет доступных городов.")
        await state.update_data(messages=[msg.message_id])
        return

    # Формируем кнопки
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=city_name, callback_data=f"city:{city_id}")]
        for city_id, city_name in cities
    ])

    msg = await message.answer("Выбери город из списка:", reply_markup=keyboard)
    await save_message(state, msg)

@router.callback_query(F.data.startswith("city:"))
async def handle_city(callback: CallbackQuery, state: FSMContext):
    _, city_id_str = callback.data.split(":", 1)  # достаём id города
    city_id = int(city_id_str)

    streets = await get_all_streets(city_id)

    if not streets:
        await callback.message.answer("Улицы не найдены.")
        return

    city_name = await get_city_name(city_id)

    # Кнопки с улицами
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=street_name, callback_data=f"street:{city_id}:{street_id}")]
            for street_id, street_name in streets] )
    msg = await callback.message.answer(f"Выбран город: {city_name}\nТеперь выбери улицу:", reply_markup=keyboard)
    await save_message(state, msg)
    await callback.answer()


@router.callback_query(F.data.startswith("street:"))
async def handle_street(callback: CallbackQuery, state: FSMContext):
    _, city_id_str, street_id_str = callback.data.split(":", 2)
    city_id = int(city_id_str)
    street_id = int(street_id_str)

    homes = await get_all_homes(street_id)

    if not homes:
        await callback.message.answer("Дома не найдены.")
        return

    city_name = await get_city_name(city_id)
    street_name = await get_street_name(street_id)

    # Кнопки с домами
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=home_name, callback_data=f"home:{city_id}:{street_id}:{home_id}")]
            for home_id, home_name in homes] )
    msg = await callback.message.answer(f"Выбран город: {city_name}\n"
                                        f"Выбрана улица: {street_name}\n"
                                        f"Теперь выбери дом:", reply_markup=keyboard)
    await save_message(state, msg)
    await callback.answer()


@router.callback_query(F.data.startswith("home:"))
async def handler_home(callback: CallbackQuery, state: FSMContext):
    _, city_id_str, street_id_str, home_id_str = callback.data.split(":", 3)
    city_id = int(city_id_str)
    street_id = int(street_id_str)
    home_id = int(home_id_str)

    sections = await get_all_sections(home_id)

    if not sections:
        await callback.message.answer("Подъезды не найдены.")
        return

    city_name = await get_city_name(city_id)
    street_name = await get_street_name(street_id)
    home_name = await get_home_name(home_id)

    # Кнопки с падиками
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=section_name, callback_data=f"section:{city_id}:{street_id}:{home_id}:{section_id}")]
            for section_id, section_name in sections])
    msg = await callback.message.answer(f"Выбран город: {city_name}\n"
                                  f"Выбрана улица: {street_name}\n"
                                  f"Выбран дом: {home_name}\n"
                                  f"Теперь выбери подъезд:",
                                  reply_markup=keyboard)
    await save_message(state, msg)
    await callback.answer()


# --- Хендлер для подъезда ---
@router.callback_query(F.data.startswith("section:"))
async def handler_section(callback: CallbackQuery, state: FSMContext):
    _, city_id_str, street_id_str, home_id_str, section_id_str = callback.data.split(":", 4)
    city_id = int(city_id_str)
    street_id = int(street_id_str)
    home_id = int(home_id_str)
    section_id = int(section_id_str)

    lifts = await get_all_lifts(home_id, section_id)

    if not lifts:
        await callback.message.answer("Лифты не найдены.")
        return

    city_name = await get_city_name(city_id)
    street_name = await get_street_name(street_id)
    home_name = await get_home_name(home_id)
    section_name = await get_section_name(section_id)

    # Кнопки с падиками
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=lift_name,
                                  callback_data=f"lift:{lift_id}")]
            for lift_id, lift_name in lifts])
    msg = await callback.message.answer(
        f"Выбран город: {city_name}\n"
        f"Выбрана улица: {street_name}\n"
        f"Выбран дом: {home_name}\n"
        f"Выбран подъезд: {section_name}\n"
        f"Теперь выбери лифт:",
        reply_markup=keyboard)
    await save_message(state, msg)
    await callback.answer()

@router.callback_query(F.data.startswith("lift:"))
async def handler_lift_history(callback: CallbackQuery, state: FSMContext):
    parts = callback.data.split(":")

    lift_id = int(parts[1])
    page = int(parts[2]) if len(parts) > 2 else 0  # если страница не передана → 0

    await show_lift_history(callback, lift_id, page)

async def show_lift_history(callback: CallbackQuery, lift_id: int, page: int = 0, per_page: int = 5):
    history = await get_history(lift_id)  # [(date, event), ...]

    total_records = len(history)
    total_pages = ceil(total_records / per_page)  # считаем кол-во страниц

    if total_records == 0:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🏠 Выбрать другой адрес", callback_data="restart")]
            ]
        )
        await callback.message.edit_text("История пуста.", reply_markup=keyboard)
        return

    # диапазон записей для текущей страницы
    start = page * per_page
    end = start + per_page
    chunk = history[start:end]

    text = "📜 История лифта:\n\n" + "\n".join(
        [f"{date:<20} | {event}" for date, event in chunk]
    )
    text += f"\n\nСтраница {page+1} из {total_pages}"  # ⚡ добавляем счётчик страниц

    # кнопки пагинации
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(
            text="⬅️ Назад", callback_data=f"lift:{lift_id}:{page - 1}"
        ))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton(
            text="Вперёд ➡️", callback_data=f"lift:{lift_id}:{page + 1}"
        ))

    # кнопка "новый адрес"
    extra_buttons = [
        InlineKeyboardButton(text="🏠 Выбрать новый адрес", callback_data="restart")
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[nav_buttons] + [extra_buttons] if nav_buttons else [extra_buttons]
    )

    await callback.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(F.data == "restart")
async def restart(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    for msg_id in data.get("messages", []):
        try:
            await callback.bot.delete_message(callback.message.chat.id, msg_id)
        except Exception:
            pass

    await state.clear()  # очищаем всё
    await cmd_start(callback.message, state)  # запускаем заново
    await callback.answer()

async def save_message(state: FSMContext, msg: types.Message):
    data = await state.get_data()
    messages = data.get("messages", [])
    messages.append(msg.message_id)
    await state.update_data(messages=messages)

def build_keyboard(buttons, n_cols=3):
    """
    Разбивает список кнопок на строки по n_cols
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    )
