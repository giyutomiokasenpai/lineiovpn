from database.connect_db import connect_db

async def insert_server(api_url, ip, password, location_country, location_city):
    connect = connect_db()
    cursor = connect.cursor()

    cursor.execute(
        'insert into servers(api_url, ip, password, location_country, location_city) values (%s, %s, %s, %s, %s)',
        (api_url, ip, password, location_country, location_city)
    )

    connect.commit()
    cursor.close()
    connect.close()