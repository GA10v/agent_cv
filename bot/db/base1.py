import sqlite3 as sq
import json
from aiogram import types
import aiogram.utils.markdown as fmt # модуль для редактирования текста сообщения от бота
from utils.create_bot import bot


def sql_start1():
    '''
    функция подключается/создает к БД "base" при запуске бота
    '''

    global base, cur

    base = sq.connect('vacancies.db')
    cur = base.cursor()

    if base:
        print('[+] Data base connected OK!')
    base.execute(
        f'''CREATE TABLE IF NOT EXISTS base(
        id TEXT PRIMARY KEY,
        vacanci TEXT,
        link TEXT,
        name TEXT,
        salary TEXT,
        stack TEXT,
        timestamp TEXT,
        viewed INTEGER
            )'''
    )
    base.commit()


def sql_client(message):
    '''
    функция подключается/создает к БД "client" при запуске бота
    '''

    try:
        base.execute(
            f'''CREATE TABLE IF NOT EXISTS a{str(message.from_user.id)}(
            id TEXT PRIMARY KEY,
            vacanci TEXT,
            link TEXT,
            name TEXT,
            salary TEXT,
            stack TEXT,
            timestamp TEXT,
            viewed INTEGER
                )'''
        )
        base.commit()
    except Exception as e:
        print(f'при создании базы clent произошла ошибка: {e}')

    try:
        data = cur.execute('SELECT * FROM base').fetchall()
        for i in data:
            cur.execute(f'INSERT INTO a{str(message.from_user.id)} VALUES (?,?,?,?,?,?,?,?)', tuple(i))
            base.commit()
    except Exception as e:
        print(f'при клонировании базы произошла ошибка: {e}')


async def sql_update():
    '''
    функция обновляющая БД "base"
    '''

    with open('data.json', 'r', encoding='utf-8') as file:
        b_data = json.load(file)
    
    id_list = cur.execute('SELECT id FROM base').fetchall()
    print(id_list)

    for i in b_data:
        print((i['id'],))
        if (i['id'],) in id_list:
            continue
        else:
            stack = ', '.join(i['stack'])
            cur.execute('INSERT INTO base VALUES (?,?,?,?,?,?,?,?)', (i['id'],i['vacanci'],i['link'],i['name'],i['salary'],stack, i['timestamp'], 0))
            base.commit()


async def sql_read(message):
    '''
    функция читает данные из БД "client"
    '''

    for i in cur.execute(
        f'''SELECT * FROM a{str(message.from_user.id)} 
        WHERE viewed <> 1
        ORDER BY timestamp DESC LIMIT 1'''
    ).fetchall():
    
        mes = fmt.text(
            fmt.text(fmt.hlink(i[1],i[2])),
            fmt.text(fmt.hunderline('Компания: '), i[3]),
            fmt.text(fmt.hunderline('Зарплата: '), i[4]),
            fmt.text(fmt.hunderline('Требуемые знания: '), i[5]),
            sep='\n')

        await bot.send_message(message.from_user.id, mes, parse_mode=types.ParseMode.HTML)
        cur.execute(f'UPDATE a{str(message.from_user.id)} SET viewed == ? WHERE id == ? ', (1, i[0]))
        base.commit()


