import aiohttp
import asyncio
from utils.text_constants import *
from datetime import datetime

async def send_request(method, account_number, url, proxy, token, retries=2, **kwargs):
    try:
        local_headers = headers.copy()
        local_headers["Authorization"] = token
        async with aiohttp.ClientSession() as session:
            for attempt in range(retries):
                try:
                    response = await session.request(method, url, proxy=proxy, headers=local_headers, **kwargs)
                    response_json = await response.json()
                    status = response.status
                    response.raise_for_status()
                    return status, response_json
                except Exception as e:
                    if "Unauthorized" in str(e):
                        print(f'Аккаунт {account_number} | Не удалось авторизоваться, возможно неверный токен: {token}')
                    elif proxy == str(e):
                        print(f'Аккаунт {account_number} | Не удалось подключиться к прокси: {proxy}')
                    else:
                        print(f'Аккаунт {account_number} | ошибка: {e}')
                await asyncio.sleep(3, 10)
    except:
        print(f'Unknown error, account number {account_number}')

    return -1, {}


async def check_in(account_number, proxy, token):


    response_status, response_json = await send_request(
        'POST',
        account_number,
        CHECK_IN_URL,
        proxy,
        token,
        data={}
    )

    try:
        if response_status == 200:
            if response_json['data']:
                print(f"Аккаунт {account_number} | успешно выполнел чек ин")
                return True
    except Exception as e:
        print(f"Аккаунт {account_number} | во время выполнения чек ина возникла ошибка: {e}")

    return False


async def check_daily_progress(account_number, proxy, token):

    response_status, response_json = await send_request(
        'GET',
        account_number,
        CHECK_DAILY_PROGRESS_URL,
        proxy,
        token
    )

    now = datetime.now()
    weekday = datetime.weekday(now)

    try:
        if response_status == 200:
            if response_json['data']['progress'][weekday]['checkedIn']:
                print(f"Аккаунт {account_number} | дата чек ина: {response_json['data']['progress'][weekday]['date']} | уже выполнен")
                return True
            else:
                print(f"Аккаунт {account_number} | дата чек ина: {response_json['data']['progress'][weekday]['date']} | чек ин не выполнен, начинаю выполнять..")
                return False
    except Exception as e:
        print(f"Не удалось проверить выполнение чек ина на аккаунте номер {account_number}, ошибка: {e}")

    return True