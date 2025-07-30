from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import CallbackQuery
from aiogram import F
from database import get_all_cities, get_all_streets, get_all_homes

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    cities = await get_all_cities()

    if not cities:
        await message.answer("Нет доступных городов.")
        return

    # Формируем кнопки
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=city, callback_data=f"city:{city}")]
            for city in cities])

    await message.answer( "Привет! Выбери город из списка:", reply_markup=keyboard )


@router.callback_query(F.data.startswith("city:"))
async def handle_city(callback: CallbackQuery):
    city = callback.data.split(":", 1)[1]  # достаём название города
    streets = await get_all_streets(city)

    if not streets:
        await callback.message.answer("Улицы не найдены.")
        return

    # Кнопки с улицами
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=street, callback_data=f"street:{city}:{street}")]
            for street in streets] )
    await callback.message.answer(f"Выбран город: {city}\nТеперь выбери улицу:", reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("street:"))
async def handle_street(callback: CallbackQuery):
    _, city, street = callback.data.split(":", 2)
    homes = await get_all_homes(city, street)

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
    entrance = get_all
