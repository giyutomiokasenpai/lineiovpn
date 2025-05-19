import psycopg2

from database.connect_db import connect_db
from outline.create_key import create_outline_key

async def insert_new_key(username, duration, user_id):
    connect = connect_db()
    cursor = connect.cursor()

    cursor.execute(
        'select api_url, location_city, location_country from servers where users_amount < 1000 order by users_amount asc limit 1'
    )
    data = cursor.fetchall()[0]
    api_url = data[0]
    location_city = data[1]
    location_country = data[2]
    print(api_url, location_city, location_country)

    key = await create_outline_key(api_url, location_city, location_country)
    accessurl = key['accessUrl']
    location: str = key['name']
    #location_city = location.split(', ')[0]
    #location_country = location.split(', ')[1]
    end_at = f'{duration} month'

    cursor.execute(
        'select id from keys where user_id=%s',
        (user_id,)
    )
    subscriptions_amount = len(cursor.fetchall()) + 1
    name = f'VPN subscription №{subscriptions_amount}'

    cursor.execute(
        'insert into keys(location_country, location_city, accessurl, username, end_at, duration, user_id, name) values (%s, %s, %s, %s, current_date + interval %s, %s, %s, %s)',
        (location_country, location_city, accessurl, username, end_at, duration, user_id, name)
    )

    cursor.execute(
        'update users set service_subscribe=True where user_id=%s',
        (user_id,)
    )

    cursor.execute(
        'select users_amount from servers where location_city=%s',
        (location_city, )
    )
    users_amount = cursor.fetchone()[0] + 1
    cursor.execute(
        'update servers set users_amount=%s where location_city=%s',
        (users_amount, location_city)
    )

    connect.commit()
    cursor.close()
    connect.close()