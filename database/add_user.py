import psycopg2

from database.connect_db import connect_db
from database.referral_program import generate_referral_code

async def add_user(user_id, username):
    connect = connect_db()
    cursor = connect.cursor()

    try:
        cursor.execute(
            'select user_id from users where user_id=%s',
            (user_id,)
        )
        user = cursor.fetchone()

        if user is None:
            referral_code = generate_referral_code()

            cursor.execute(
                'insert into users(user_id, username, referral_code) values (%s, %s, %s)',
                (user_id, username, referral_code)
            )

            connect.commit()

    except Exception as e:
        print(f'Error: {e}')
    
    cursor.close()
    connect.close()