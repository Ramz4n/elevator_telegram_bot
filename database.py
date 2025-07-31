import asyncmy
from config import DB_CONFIG

async def get_all_cities() -> list[tuple[int, str]]:
    async with asyncmy.connect(**DB_CONFIG) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT id, Город FROM goroda")
            result = await cursor.fetchall()
            return result

async def get_all_streets(city_id : int) -> list[tuple[int, str]]:
    async with asyncmy.connect(**DB_CONFIG) as conn:
        async with conn.cursor() as cursor:
            query = '''SELECT id, Улица 
                        FROM street 
                        WHERE id_города = %s'''
            await cursor.execute(query, (city_id,))
            result = await cursor.fetchall()
            return result

async def get_all_homes(street_id : int) -> list[tuple[int, str]]:
    async with asyncmy.connect(**DB_CONFIG) as conn:
        async with conn.cursor() as cursor:
            query = '''SELECT id, Номер 
                        FROM doma
                        WHERE id_улица = %s'''
            await cursor.execute(query, (street_id,))
            result = await cursor.fetchall()
            return result

async def get_all_sections(home_id : int) -> list[tuple[int, str]]:
    async with asyncmy.connect(**DB_CONFIG) as conn:
        async  with conn.cursor() as cursor:
            query = '''SELECT l.id_подъезд, p.номер
                        FROM lifts l
                        JOIN padik p ON l.id_падъезд = p.номер
                        WHERE id_дом = %s'''
            await cursor.execute(query, (home_id,))
            result = await cursor.fetchall()
            return result

async def get_all_lifts(home_id : int, section_id : int) -> list[tuple[int, str]]:
    async with asyncmy.connect(**DB_CONFIG) as conn:
        async  with conn.cursor() as cursor:
            query = '''SELECT тип_лифта 
                        FROM lifts l
                        WHERE id_дом = %s AND id_подъезд = %s'''
            await cursor.execute(query, (home_id, section_id,))
            result = await cursor.fetchall()
            return [row[0] for row in result]



