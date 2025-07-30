import asyncmy
from config import DB_CONFIG

async def get_all_cities() -> list[tuple[int, str]]:
    async with asyncmy.connect(**DB_CONFIG) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT id, Город FROM goroda")
            result = await cursor.fetchall()
            return result

async def get_all_streets(town : int) -> list[tuple[int, str]]:
    async with asyncmy.connect(**DB_CONFIG) as conn:
        async with conn.cursor() as cursor:
            query = '''SELECT id, Улица 
                        FROM street 
                        WHERE id_города = %s'''
            await cursor.execute(query, (town,))
            result = await cursor.fetchall()
            return result

async def get_all_homes(street : int) -> list[tuple[int, str]]:
    async with asyncmy.connect(**DB_CONFIG) as conn:
        async with conn.cursor() as cursor:
            query = '''SELECT id, Номер 
                        FROM doma
                        WHERE id_улица = %s'''
            await cursor.execute(query, (street,))
            result = await cursor.fetchall()
            return result

async def get_all_sections(home : int) -> list[tuple[int, str]]:
    async with asyncmy.connect(**DB_CONFIG) as conn:
        async  with conn.cursor() as cursor:
            query = '''SELECT id_подъезд
                        FROM lifts
                        WHERE id_дом = %s'''
            await cursor.execute(query, (home,))
            result = await cursor.fetchall()
            return result

async def get_all_lifts(home : int, section : int) -> list[tuple[int, str]]:
    async with asyncmy.connect(**DB_CONFIG) as conn:
        async  with conn.cursor() as cursor:
            query = '''SELECT p.номер 
                        FROM padik p
                        JOIN doma d ON p.id_улица = d.id
                        JOIN street s ON d.id_улица = s.id
                        JOIN goroda g ON s.id_город = g.id
                        WHERE g.Город = %s AND s.Улица = %s'''
            await cursor.execute(query, (town, street, home,))
            result = await cursor.fetchall()
            return [row[0] for row in result]



