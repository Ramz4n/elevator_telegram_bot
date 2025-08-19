import asyncmy
from config import DB_CONFIG

async def get_all_cities() -> list[tuple[int, str]]:
    async with asyncmy.connect(**DB_CONFIG) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute('''SELECT id, Город FROM goroda''')
            result = await cursor.fetchall()
            return result

async def get_city_name(city_id: int) -> str:
    async with asyncmy.connect(**DB_CONFIG) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute('''SELECT Город FROM goroda WHERE id = %s''', (city_id,))
            row = await cursor.fetchone()
            return row[0] if row else "Неизвестный город"


async def get_all_streets(city_id : int) -> list[tuple[int, str]]:
    async with asyncmy.connect(**DB_CONFIG) as conn:
        async with conn.cursor() as cursor:
            query = '''SELECT id, Улица 
                        FROM street 
                        WHERE id_город = %s'''
            await cursor.execute(query, (city_id,))
            result = await cursor.fetchall()
            return result

async def get_street_name(street_id: int) -> str:
    async with asyncmy.connect(**DB_CONFIG) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute('''SELECT Улица FROM street WHERE id = %s''', (street_id,))
            row = await cursor.fetchone()
            return row[0] if row else "Неизвестная улица"

async def get_all_homes(street_id : int) -> list[tuple[int, str]]:
    async with asyncmy.connect(**DB_CONFIG) as conn:
        async with conn.cursor() as cursor:
            query = '''SELECT id, Номер 
                        FROM doma
                        WHERE id_улица = %s'''
            await cursor.execute(query, (street_id,))
            result = await cursor.fetchall()
            return result

async def get_home_name(home_id: int) -> str:
    async with asyncmy.connect(**DB_CONFIG) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute('''SELECT Номер FROM doma WHERE id = %s''', (home_id,))
            row = await cursor.fetchone()
            return row[0] if row else "Неизвестный номер дома"

async def get_all_sections(home_id : int) -> list[tuple[int, str]]:
    async with asyncmy.connect(**DB_CONFIG) as conn:
        async  with conn.cursor() as cursor:
            query = '''SELECT l.id_подъезд,
                        p.Номер
                        FROM lifts l
                        JOIN padik p ON l.id_подъезд = p.id
                        WHERE l.id_дом = %s
                        GROUP BY id_подъезд'''
            await cursor.execute(query, (home_id,))
            result = await cursor.fetchall()
            return result

async def get_section_name(section_id: int) -> str:
    async with asyncmy.connect(**DB_CONFIG) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute('''SELECT Номер FROM padik WHERE id = %s''', (section_id,))
            row = await cursor.fetchone()
            return row[0] if row else "Неизвестный номер подъезда"

async def get_all_lifts(home_id : int, section_id : int) -> list[tuple[int, str]]:
    async with asyncmy.connect(**DB_CONFIG) as conn:
        async  with conn.cursor() as cursor:
            query = '''SELECT id, тип_лифта 
                        FROM lifts
                        WHERE id_дом = %s AND id_подъезд = %s'''
            await cursor.execute(query, (home_id, section_id,))
            result = await cursor.fetchall()
            return result

async def get_lift_name(home_id: int, section_id: int) -> str:
    async with asyncmy.connect(**DB_CONFIG) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute('''SELECT Тип_лифта 
            FROM lifts 
            WHERE id_дом = %s and id_подъезд = %s''', (home_id, section_id, ))
            row = await cursor.fetchone()
            return row[0] if row else "Неизвестный лифт"

async def get_history(lift_id: int) -> list[tuple[int, str]]:
    async with asyncmy.connect(**DB_CONFIG) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute('''SELECT FROM_UNIXTIME(Дата_заявки, '%d.%m.%Y, %H:%i') as Дата_заявки,
             Комментарий
             FROM zayavki 
             WHERE id_лифт = %s''', (lift_id, ))
            result = await cursor.fetchone()
            return result