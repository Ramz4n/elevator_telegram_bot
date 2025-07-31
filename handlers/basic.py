from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import CallbackQuery
from aiogram import F
from database import get_all_cities, get_all_streets, get_all_homes, get_all_sections

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    cities = await get_all_cities()

    if not cities:
        await message.answer("Нет доступных городов.")
        return

    # Формируем кнопки
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=city_name, callback_data=f"city:{city_id}")]
            for city_id, city_name in cities])

    await message.answer( "Привет! Выбери город из списка:", reply_markup=keyboard )


@router.callback_query(F.data.startswith("city:"))
async def handle_city(callback: CallbackQuery):
    city_id = int(callback.data.split(":", 1)[1])  # достаём id города
    streets = await get_all_streets(city_id)
    cities = await get_all_cities()[1]
    city_name = cities[1][1]

    if not streets:
        await callback.message.answer("Улицы не найдены.")
        return

    # Кнопки с улицами
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=street_name, callback_data=f"street:{city_id}:{street_id}")]
            for street_id, street_name in streets] )
    await callback.message.answer(f"Выбран город: {city_name}\nТеперь выбери улицу:", reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("street:"))
async def handle_street(callback: CallbackQuery):
    _, city_id, street_id = callback.data.split(":", 2)
    homes = await get_all_homes(int(street_id))

    if not homes:
        await callback.message.answer("Дома не найдены.")
        return

    # Кнопки с домами
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=home, callback_data=f"home:{city}:{street}:{home}")]
            for home in homes] )
    await callback.message.answer(f"Выбран город: {city}\nВыбрана улица: {street}\nТеперь выбери дом:", reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("home:"))
async def handler_home(callback: CallbackQuery):
    _, city, street, home = callback.data.split(":", 3)
    sections = await get_all_sections(home)

    if not sections:
        await callback.message.answer("Подъезды не найдены.")
        return

    # Кнопки с падиками
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=section, callback_data=f"section:{city}:{street}:{home}:{section}")]
            for section in sections])
    await callback.message.answer(f"Выбран город: {city}\nВыбрана улица: {street}\nВыбран дом: {home}\nТеперь выбери подъезд:",
                                  reply_markup=keyboard)
    await callback.answer()