from database.connect_db import connect_db
from outline.delete_key import delete_outline_key
from scheduler.broadcasts import broadcast_deleted

async def delete_subscription():
    connect = connect_db()
    cursor = connect.cursor()

    cursor.execute(
        'select id, accessurl, location_city, user_id from keys where end_at=current_date'
    )
    data = cursor.fetchall()

    for key in data:
        key_id = key[0]
        accessurl = key[1]
        location_city = key[2]
        user_id = key[3]
        await broadcast_deleted(user_id)

        cursor.execute(
            'select api_url from servers where location_city=%s',
            (location_city,)
        )
        api_url = cursor.fetchone()[0]
        await delete_outline_key(api_url, accessurl)

        cursor.execute(
            'delete from keys where id=%s',
            (key_id,)
        )

        cursor.execute(
            'update users set service_subscribe=False where user_id=%s',
            (user_id,)
        )

    connect.commit()
    cursor.close()
    connect.close()