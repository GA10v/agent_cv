from bs4 import BeautifulSoup
import fake_useragent
from datetime import datetime
import json
import asyncio
import aiohttp
from uuid import NAMESPACE_URL, uuid5


UA = fake_useragent.UserAgent()
big_data = []


async def get_links(session, page):
    '''
    функция для парсинга сайта hh.ru
    '''

    text = 'python'
    headers={'user-agent': UA.random}
    url=f'https://hh.ru/search/vacancy?clusters=true&area=1&ored_clusters=true&enable_snippets=true&search_period=1&salary=&text={text}&page={page}'
    # url=f'https://hh.ru/search/vacancy?area=1&fromSearchLine=true&text={text}&page={page}'

    async with session.get(url=url, headers=headers) as response:

        if response.status != 200:
            return print('get_links() != 200')
        soup = BeautifulSoup(await response.text(), 'lxml')
        data = soup.find_all('a', attrs={'class':'bloko-link'})

        for i in data:
            url = f'{i.attrs["href"].split("?")[0]}'
            vacanci = i.text
            if 'https://nn.hh.ru/vacancy/' in url:
                async with session.get(url=url, headers=headers) as response:
                    if response.status != 200:
                        continue
                    soup = BeautifulSoup(await response.text(), 'lxml')

                    try:
                        company_name = soup.find(attrs={'class':'bloko-header-section-2 bloko-header-section-2_lite'}).text.replace('\xa0',' ')
                    except:
                        company_name = 'не указана'

                    try:
                        salary = soup.find('div', attrs={'data-qa':'vacancy-salary'}).find('span', attrs={'data-qa':'vacancy-salary-compensation-type-net'}).text.replace('\xa0','')
                    except:
                        salary = 'не указана'
                    
                    try:
                        stack = [tag.text.replace('\xa0',' ') for tag in soup.find(attrs={'class':'bloko-tag-list'}).find_all(attrs={'class':'bloko-tag__section_text'})]
                    except:
                        stack = ['не указан']

                    id = str(uuid5(NAMESPACE_URL, url))
                    timestamp = datetime.now().strftime('%d/ %m/ %y, %H:%M:%S')
                    
                    vacancies = {
                        'id' : id,
                        'vacanci' : vacanci,
                        'link' : url,
                        'name' : company_name,
                        'salary' : salary,
                        'stack' : stack,
                        'timestamp' : timestamp
                        }

                    big_data.append(vacancies)


async def gather_data():
    '''
    функции формируют список задач
    '''

    headers={'user-agent': UA.random}
    
    text = 'python'

    url=f'https://hh.ru/search/vacancy?clusters=true&area=1&ored_clusters=true&enable_snippets=true&search_period=1&salary=&text={text}&page=2'
    # url=f'https://hh.ru/search/vacancy?area=1&fromSearchLine=true&text={text}'

    async with aiohttp.ClientSession() as session: # клиент сессию позволяющий повторно использовать открытое соединение
        response = await session.get(url=url, headers=headers)
        if response.status != 200:
            return print('get_data() != 200')
        soup = BeautifulSoup(await response.text(), 'lxml')
        pages_count = int(soup.find('div', attrs={'class':'pager'}).find_all('span', recursive=False)[-1].find('a').find('span').text)
        
        tasks = []

        for page in range(1, pages_count):
            task = asyncio.create_task(get_links(session, page)) # создание не задачи
            tasks.append(task)
            print('[+] Started task', task)

        await asyncio.gather(*tasks)


async def start_parsing():
    '''
    функция бота, запускающая парсинг 
    '''
    
    print('[+] Parsing in progress...')
    await gather_data()

    with open('data.json','w', encoding='utf-8') as file:
        json.dump(big_data,file,indent=4,ensure_ascii=False)


if __name__ == '__main__':

    asyncio.run(gather_data())

    with open('data.json','w', encoding='utf-8') as file:
        json.dump(big_data,file,indent=4,ensure_ascii=False)