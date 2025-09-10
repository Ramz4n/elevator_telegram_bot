import asyncmy
from config import DB_CONFIG

async def get_all_cities() -> list[tuple[int, str]]:
    async with asyncmy.connect(**DB_CONFIG) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute('''SELECT DISTINCT g.id, g.Город 
                        FROM goroda g
                        JOIN street s ON g.id = s.id_город
                        JOIN doma d ON s.id = d.id_улица
                        WHERE d.is_active = 1''')
            result = await cursor.fetchall()
            return result

async def get_city_name(city_id: int) -> str:
    async with asyncmy.connect(**DB_CONFIG) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute('''SELECT DISTINCT g.Город 
                        FROM goroda g
                        JOIN street s ON g.id = s.id_город
                        JOIN doma d ON s.id = d.id_улица
                        WHERE g.id = %s AND d.is_active = 1''', (city_id,))
            row = await cursor.fetchone()
            return row[0] if row else "Неизвестный город"


async def get_all_streets(city_id : int) -> list[tuple[int, str]]:
    async with asyncmy.connect(**DB_CONFIG) as conn:
        async with conn.cursor() as cursor:
            query = '''SELECT DISTINCT s.id, s.Улица 
                        FROM street s
                        JOIN doma d ON s.id = d.id_улица
                        WHERE s.id_город = %s AND d.is_active = 1'''
            await cursor.execute(query, (city_id,))
            result = await cursor.fetchall()
            return result

async def get_street_name(street_id: int) -> str:
    async with asyncmy.connect(**DB_CONFIG) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute('''SELECT DISTINCT s.Улица 
                        FROM street s
                        JOIN doma d ON s.id = d.id_улица
                        WHERE s.id = %s AND d.is_active = 1''', (street_id,))
            row = await cursor.fetchone()
            return row[0] if row else "Неизвестная улица"

async def get_all_homes(street_id : int) -> list[tuple[int, str]]:
    async with asyncmy.connect(**DB_CONFIG) as conn:
        async with conn.cursor() as cursor:
            query = '''SELECT id, Номер 
                        FROM doma
                        WHERE id_улица = %s AND is_active = 1'''
            await cursor.execute(query, (street_id,))
            result = await cursor.fetchall()
            return result

async def get_home_name(home_id: int) -> str:
    async with asyncmy.connect(**DB_CONFIG) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute('''SELECT Номер FROM doma WHERE id = %s AND is_active = 1''', (home_id,))
            row = await cursor.fetchone()
            return row[0] if row else "Неизвестный номер дома"

async def get_all_sections(home_id : int) -> list[tuple[int, str]]:
    async with asyncmy.connect(**DB_CONFIG) as conn:
        async  with conn.cursor() as cursor:
            query = '''SELECT l.id_подъезд,
                        p.Номер
                        FROM lifts l
                        JOIN padik p ON l.id_подъезд = p.id
                        JOIN doma d ON l.id_дом = d.id
                        WHERE l.id_дом = %s AND d.is_active = 1
                        GROUP BY id_подъезд'''
            await cursor.execute(query, (home_id,))
            result = await cursor.fetchall()
            return result

async def get_section_name(section_id: int) -> str:
    async with asyncmy.connect(**DB_CONFIG) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute('''SELECT p.Номер 
                        FROM padik p
                        JOIN lifts l ON p.id = l.id_подъезд
                        JOIN doma d ON l.id_дом = d.id
                        WHERE p.id = %s AND d.is_active = 1''', (section_id,))
            row = await cursor.fetchone()
            return row[0] if row else "Неизвестный номер подъезда"

async def get_all_lifts(home_id : int, section_id : int) -> list[tuple[int, str]]:
    async with asyncmy.connect(**DB_CONFIG) as conn:
        async  with conn.cursor() as cursor:
            query = '''SELECT lifts.id, тип_лифта 
                        FROM lifts
                        JOIN doma d ON lifts.id_дом = d.id
                        WHERE lifts.id_дом = %s AND lifts.id_подъезд = %s AND d.is_active = 1'''
            await cursor.execute(query, (home_id, section_id,))
            result = await cursor.fetchall()
            return result

async def get_lift_name(home_id: int, section_id: int) -> str:
    async with asyncmy.connect(**DB_CONFIG) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute('''SELECT Тип_лифта 
            FROM lifts 
            JOIN doma d ON lifts.id_дом = d.id
            WHERE lifts.id_дом = %s AND lifts.id_подъезд = %s AND d.is_active = 1''', (home_id, section_id, ))
            row = await cursor.fetchone()
            return row[0] if row else "Неизвестный лифт"

async def get_history(lift_id: int) -> list[tuple[int, str]]:
    async with asyncmy.connect(**DB_CONFIG) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute('''SELECT FROM_UNIXTIME(Дата_заявки, '%%d.%%m.%%Y, %%H:%%i') as formatted_date,
                        Комментарий
                        FROM zayavki 
                        WHERE id_лифт = %s
                        ORDER BY Дата_заявки DESC
                        ''', (lift_id, ))
            result = await cursor.fetchall()
            return result

async def get_full_address_lift(lift_id: int) -> list[tuple[str, str, str, str, str]]:
    async with asyncmy.connect(**DB_CONFIG) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute('''SELECT 
                                    g.Город AS Город,
                                    s.Улица AS Улица,
                                    d.Номер AS Дом,
                                    p.Номер AS Падик,
                                    l.Тип_лифта AS Лифт
                                    FROM lifts l
                                    JOIN padik p ON l.`id_подъезд` = p.id
                                    JOIN doma d ON l.`id_дом` = d.id
                                    JOIN street s ON d.`id_улица` = s.id
                                    JOIN goroda g ON s.`id_город` = g.id
                                    WHERE l.id = %s AND d.is_active = 1''', (lift_id, ))
            result = await cursor.fetchall()
            return result