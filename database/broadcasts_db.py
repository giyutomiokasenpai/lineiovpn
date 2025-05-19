from database.connect_db import connect_db
from scheduler.broadcasts import broadcast_continue_broadcast
from datetime import datetime
import pytz

async def broadcast_continue():
    connect = connect_db()
    cursor = connect.cursor()

    interval_1day = f'1 day'
    interval_2days = f'2 days'
    interval_3days = f'3 days'
    cursor.execute(
        'select user_id, end_at from keys where end_at=current_date + interval %s or end_at=current_date + interval %s or end_at=current_date + interval %s',
        (interval_1day, interval_2days, interval_3days)
    )
    data = cursor.fetchall()

    datetime_now = datetime.now(pytz.timezone('Europe/Moscow')).date()
    for item in data:
        user_id = item[0]
        end_at = item[1]
        duration = (end_at - datetime_now).days

        await broadcast_continue_broadcast(user_id, duration)

    cursor.close()
    connect.close()