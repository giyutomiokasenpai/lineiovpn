import aiohttp

async def create_outline_key(api_url, location_city, location_country):
    name = {
        'name': f'{location_city}, {location_country}'
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(f'{api_url}/access-keys', ssl=False, json=name) as resp:
            print(f'Status: {resp.status}')
            if resp.status == 201:
                data = await resp.json()
                print('The key has been successful created')  
            else:
                print('Couldnt create a key')
                print(await resp.text())

    return data