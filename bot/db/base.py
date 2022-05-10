from django import views
from db.models import Base, User, View, Like, db
from peewee import *
import json
from progress.bar import Bar
import aiogram.utils.markdown as fmt
from aiogram import types
from utils import bot


def db_start():
    try:
        db.connect()
        base = Base()
        users = User()
        views = View()
        likes = Like()
        db.create_tables([base,users,views,likes])

        if base.select().count() > 1:
            with open('vacancies_today.json', 'r', encoding='utf-8') as file:
                vacancies = json.load(file)
        else:
            try:
                with open('vacancies.json', 'r', encoding='utf-8') as file:
                    vacancies = json.load(file)
            except Exception as e:
                with open('vacancies_today.json', 'r', encoding='utf-8') as file:
                    vacancies = json.load(file)

        bar = Bar(f'[+] Processing: ', max=len(vacancies))
        for vacancy in vacancies:
            # db_set_vacavcies(base, vacancy)
            flag = True
            old_vacancies = base.select()
            links = []

            for vc in old_vacancies:
                links.append(vc.link)

            if vacancy['link'] in links:
                flag = False

            if flag:
                with db:
                    base.insert(vacancy).execute()
                    bar.next()
                bar.finish()

        print('[+] Base update')
    except Exception as e:
        print(f'[-] {e}')


'''___________________________________________________________________________________'''
def db_set_vacavcies(table, vacancy):

    flag = True
    old_vc = table.select()
    links = []

    for vc in old_vc:
        links.append(vc.link)

    if vacancy['link'] in links:
        flag = False

    if flag:
        with db:
            table.insert(vacancy).execute()
'''___________________________________________________________________________________'''


'''___________________________________________________________________________________'''
async def db_admin_today():

    with open('vacancies_today.json', 'r', encoding='utf-8') as file:
        vacancies = json.load(file)

    base = Base()

    bar = Bar(f'[+] Processing: ', max=len(vacancies))
    for vacancy in vacancies:
        db_set_vacavcies(base, vacancy)
        bar.next()
    bar.finish()
'''___________________________________________________________________________________'''


def db_join_user(message):

    try:
        user = User.create(user_id = message.from_user.id).save()
    except IntegrityError as er:
        user = User.select().where(User.user_id == message.from_user.id).get()

    return user


async def db_get_vacancy(message):

    user = db_join_user(message)
    views_list = []
    view = View.select().where(user.id == View.user_id)

    for i in view:
        views_list.append(i.link_id)
    
    vacancy = Base.select().where(Base.link.not_in(views_list)).order_by(Base.time.desc()).get()

    View.create(user_id = user.id, link_id=vacancy.link)
        
    mes = fmt.text(
        fmt.text(fmt.hlink(vacancy.name, vacancy.link)),
        fmt.text(fmt.hunderline('Компания: '), vacancy.company),
        fmt.text(fmt.hunderline('Расположение: '), vacancy.area),
        fmt.text(fmt.hunderline('Зарплата: '), vacancy.salary),
        fmt.text(fmt.hunderline('Требуемые знания: '), vacancy.skills),
        fmt.text(fmt.hunderline('Опыт работы: '), vacancy.experience),
        sep='\n')


    await bot.send_message(message.from_user.id, mes, parse_mode=types.ParseMode.HTML)
    

async def db_set_like(message):

    try:
        user = db_join_user(message)
        vacancy = View.select().where(user.id == View.user_id).order_by(View.id.desc()).get()       
        Like.create(user_id = user.id, link_id=vacancy.link_id)
    except IntegrityError as er:
        print('[-] ... ')

