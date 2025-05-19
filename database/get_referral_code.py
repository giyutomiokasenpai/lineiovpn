from database.connect_db import connect_db

async def get_referral_code(user_id):
    connect = connect_db()
    cursor = connect.cursor()

    cursor.execute(
        'select referral_code from users where user_id = %s',
        (user_id,)
    )

    referral_code = cursor.fetchone()
    connect.close()
    cursor.close()
    return referral_code[0]