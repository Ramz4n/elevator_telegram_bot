import asyncmy
from config import DB_CONFIG

async def get_all_cities() -> list[str]:
    async with asyncmy.connect(**DB_CONFIG) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT Город FROM goroda")
            result = await cursor.fetchall()
            return [row[0] for row in result]

async def get_all_streets(town : str) -> list[str]:
    async with asyncmy.connect(**DB_CONFIG) as conn:
        async with conn.cursor() as cursor:
            query = '''SELECT s.Улица 
                        FROM street s
                        JOIN goroda g ON s.id_город = g.id
                        WHERE g.Город = %s'''
            await cursor.execute(query, (town,))
            result = await cursor.fetchall()
            return [row[0] for row in result]

async def get_all_homes(town : str, street : str) -> list[str]:
    async with asyncmy.connect(**DB_CONFIG) as conn:
        async with conn.cursor() as cursor:
            query = '''SELECT d.номер 
                        FROM doma d
                        JOIN street s ON d.id_улица = s.id
                        JOIN goroda g ON s.id_город = g.id
                        WHERE g.Город = %s AND s.Улица = %s'''
            await cursor.execute(query, (town, street,))
            result = await cursor.fetchall()
            return [row[0] for row in result]

async def get_all_entrance(town : str, street : str, home : str) -> list[str]:
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


