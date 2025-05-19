import psycopg2

from database.connect_db import connect_db, create_connection, close_connection
from outline.create_key import create_outline_key
from outline.delete_key import delete_outline_key

async def change_name(key_id, name):
    connect = connect_db()
    cursor = connect.cursor()

    cursor.execute(
        'update keys set name=%s where id=%s',
        (name, key_id)
    )
    connect.commit()
    cursor.close()
    connect.close()
    return name

async def subscription_continue_db(key_id, duration):
    connect = connect_db()
    cursor = connect.cursor()

    cursor.execute(
        'select end_at from keys where id=%s',
        (key_id,)
    )
    end_at = cursor.fetchone()

    duration = f'{duration} month'
    cursor.execute(
        'update keys set end_at=%s + %s where id=%s',
        (duration, end_at, key_id)
    )

    connect.commit()
    cursor.close()
    connect.close()

async def select_servers(location_city: str) -> tuple:
    connect = connect_db()
    cursor = connect.cursor()

    cursor.execute(
        'select api_url, location_country from servers where location_city=%s',
        (location_city,)
    )
    data = cursor.fetchone()
    cursor.close()
    connect.close()
    return data

async def select_keys(key_id: str) -> tuple:
    connect = connect_db()
    cursor = connect.cursor()

    cursor.execute(
        'select accessurl, location_city, location_country from keys where id=%s',
        (key_id,)
    )
    data = cursor.fetchone()
    return data

async def change_location_db(key_id, location_city):
    connect = connect_db()
    cursor = connect.cursor()

    data = await select_servers(location_city)
    api_url = data[0]
    location_country = data[1]

    data = await select_keys(key_id)
    accessurl = data[0]
    print(accessurl)
    await delete_outline_key(api_url, accessurl)

    key = await create_outline_key(api_url, location_city, location_country)
    accessurl = key['accessUrl']

    cursor.execute(
        'update keys set accessurl=%s, location_country=%s, location_city=%s where id=%s',
        (accessurl, location_country, location_city, key_id)
    )
    connect.commit()
    cursor.close()
    connect.close()
    return location_country

async def recreate_key_db(key_id):
    connect, cursor = await create_connection()

    data = await select_keys(key_id)
    accessurl = data[0]
    location_city = data[1]
    location_country = data[2]
    data = await select_servers(location_city)
    api_url = data[0]
    await delete_outline_key(api_url, accessurl)

    key = await create_outline_key(api_url, location_city, location_country)
    accessurl = key['accessUrl']
    cursor.execute(
        'update keys set accessurl=%s where id=%s',
        (accessurl, key_id)
    )
    connect.commit()
    await close_connection(connect, cursor)