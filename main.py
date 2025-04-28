import asyncio
from random import randint
from utils.requests_utils import check_in, check_daily_progress
from utils.file_utils import read_proxies, read_tokens
import configs.config as config

PROXIES = read_proxies()
TOKENS = read_tokens()

async def start_check_in(account_number, proxy, token):
    await asyncio.sleep(config.DELAY_BEFORE_START[0], config.DELAY_BEFORE_START[1])
    while True:
        if not (await check_daily_progress(account_number, proxy, token)):
                if await check_in(account_number, proxy, token):
                    await asyncio.sleep(randint(12*60*60, 17*60*60))
                else:
                    time_to_sleep = randint(40, 80)
                    print(f"Аккаунт {account_number} | ожидаю {time_to_sleep} минут перед следующей попыткой")
                    await asyncio.sleep(time_to_sleep*60)
        else:
            await asyncio.sleep(randint(3*60*60, 7*60*60))

async def main():
    for account_number, data in enumerate(zip(PROXIES, TOKENS)):
        proxy, token = data[0], data[1]
        asyncio.create_task(start_check_in(account_number+1, proxy, token))
        await asyncio.sleep(config.DELAY_BETWEEN_ACCOUNTS)

    await asyncio.sleep(float('inf'))

asyncio.run(main())
