import asyncio
import aiohttp
import json
import fake_useragent
from utils.config import NAME
from progress.bar import Bar
from datetime import datetime, timedelta


UA = fake_useragent.UserAgent()


async def get_gather(text, today):
    
    url = f'https://api.hh.ru/vacancies'
    headers = {'User-agent' : UA.random}
    date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    if today:
        params = {
            'text' : f'NAME:{text}',
            'per_page': 20,
            'date_from' : f'{date}'
            }
    else:
        params = {
            'text' : f'NAME:{NAME}',
            'per_page' : 90
            }

    async with aiohttp.ClientSession() as session:

        response = await session.get(url=url, headers=headers, params=params)

        if response.status != 200:
            print('[-] Response status: {response.status}')

        try:
            tasks = []
            pages = int(json.loads(await response.text())['pages'])
            items = int(json.loads(await response.text())['found'])

            for page in range(pages):
                task = asyncio.create_task(get_vacancies(session, page, text, today))
                tasks.append(task)
            
            print(f'[+] Found {items} vacansies in {pages+1} pages')
            await asyncio.gather(*tasks)
        except Exception as e:
            print(f'[-] Exception {e}')


async def get_vacancies(session, page, text, today):

    url = f'https://api.hh.ru/vacancies'
    headers = {'User-agent' : UA.random}
    date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    if today:
        params = {
            'text' : f'NAME:{text}',
            'page' : page,
            'per_page': 20,
            'date_from' : f'{date}'
            }
    else:
        params = {
            'text' : f'NAME:{text}',
            'page' : page,
            'per_page': 90
            }
    
    async with session.get(url=url, headers=headers,params=params) as response:

        if response.status != 200:
            print(f'[-] Response status: {response.status}')

        try:
            id = []
            soup = json.loads(await response.text())['items'] # все вакансии со страницы
        
            for i in range(len(soup)):
                id.append(soup[i]['id'])

            bar = Bar(f'[+] Processing in page: ', suffix = '%(percent)d%%')

            for i in id:
                url = f'https://api.hh.ru/vacancies/{i}'
                headers = {'User-agent' : UA.random}

                async with session.get(url=url, headers=headers) as response:

                    if response.status != 200:
                        print(f'[-] Response status: {response.status}')

    
                    data = json.loads(await response.text())

                    skills = ', '.join([i['name']  for i in data['key_skills']])
                    skills = skills if skills else 'не указаны'

                    vacanсy = {
                        'name' : data['name'],
                        'link' : data['alternate_url'],
                        'company' : data['employer']['name'],
                        'area' : data['area']['name'],
                        'experience' : data['experience']['name'] if data['experience'] else 'не указан',
                        'salary' : str(data['salary']['from']) if data['salary'] else 'не указана',
                        'skills' : skills,
                        'time' : data['published_at']                            
                        }
                
                vacancies.append(vacanсy)

                bar.next()
            bar.finish()
         
        except Exception as e:
            print(f'[-] Exception {e}')


async def get_all(text):

    print('[+] Start searching!')
    global vacancies 
    vacancies = []
        
    try:
        asyncio.run(get_gather(text, today=False))
    except Exception as e:
        print (f'[-] Exceptinon {e}')
    finally:
        with open('vacancies.json', 'w', encoding='utf-8') as file:
            json.dump(vacancies, file, ensure_ascii=False, indent=4)


async def get_today(text):

    print('[+] Start searching!')
    global vacancies 
    vacancies = []
    date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    params = {
        'text' : f'NAME:{text}',
        'per_page': 20,
        'date_from' : f'{date}'
        }

    try:
        await get_gather(text, today=True) #для старта бота

    except Exception as e:
        print (f'[-] Exceptinon {e}')
    finally:
        with open('vacancies_today.json', 'w', encoding='utf-8') as file:
            json.dump(vacancies, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':

    print('[+] Start searching!')
    vacancies = []
    date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    params = {
        'text' : f'NAME:{NAME}',
        'per_page': 20,
        'date_from' : f'{date}'
        }
        
    try:
        if input('today = True?  "y" or "n" ') == 'y':
            today = True
        else:
            today = False
        asyncio.run(get_gather(text=NAME,today=today))
    except Exception as e:
        print (f'[-] Exceptinon {e}')
    finally:
        with open('vacancies_today.json', 'w', encoding='utf-8') as file:
            json.dump(vacancies, file, ensure_ascii=False, indent=4)

# 1330 items at 0:00:43.541049 