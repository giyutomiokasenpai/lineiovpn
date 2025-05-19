from database.connect_db import connect_db



async def get_user_key_names(user_id):
    connect = connect_db()
    cursor = connect.cursor()

    cursor.execute(
        'select id, name from keys where user_id=%s',
        (user_id,)
    )

    keys = cursor.fetchall()
    connect.close()
    cursor.close()
    return keys

async def get_vpn_keys(key_id):
    connect = connect_db()
    cursor = connect.cursor()

    cursor.execute(
        'select accessurl, name, duration, end_at, location_country, location_city from keys where id=%s',
        (key_id,)
    )

    key = cursor.fetchall()
    connect.close()
    cursor.close()
    return key

async def get_servers(current_location_city):
    connect = connect_db()
    cursor = connect.cursor()

    print(current_location_city)
    cursor.execute(
        'select location_city, location_country from servers where users_amount < 1000 and location_city not in (%s)',
        (current_location_city, )
    )
    servers = cursor.fetchall()

    cursor.close()
    connect.close()
    return servers