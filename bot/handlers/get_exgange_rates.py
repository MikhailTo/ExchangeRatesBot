import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from config import settings

import asyncio
import aiohttp
async def get_exgange_rates(date, apiVersion, endpoint, convert_to):
   
    url=settings.exchange_rates_url_template.format(
        date=date, 
        apiVersion=apiVersion, 
        endpoint=endpoint
        )

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            response = await resp.read()
        response_data = json.loads(response.decode('utf-8'))
    return response_data[endpoint][convert_to]

date="latest"
apiVersion = "v1"
endpoint = "usd"
convert_to = "eur"
response_data = asyncio.run(get_exgange_rates(date, apiVersion, endpoint, convert_to))

print(f"{response_data:.2f}")