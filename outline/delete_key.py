import aiohttp

from database.connect_db import connect_db

async def find_key_id(api_url, accessurl):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{api_url}/access-keys', ssl=False) as resp:
            data = await resp.json()
            for key in data.get('accessKeys', []):
                if key['accessUrl'] == accessurl:
                    return key['id']

async def get_api_url(accessUrl, location_city):
    connect = connect_db()
    cursor = connect.cursor()

    cursor.execute(
        'select api_url from servers where location_city=%s',
            (location_city,)    
        )
    data = cursor.fetchall()
    return data

async def delete_outline_key(api_url, accessurl):
    async with aiohttp.ClientSession() as session:
        access_key_id = await find_key_id(api_url, accessurl)
        async with session.delete(f'{api_url}/access-keys/{access_key_id}', ssl=False) as resp:
            print(f'Status: {resp.status}')
            if resp.status == 204:
                print('The key has been successful deleted')
            else:
                print('Couldnt delete the key')
                print(await resp.text())