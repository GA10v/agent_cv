# agent_cv

A telegram bot witch can search for job vacancies. 
Bot uses appropriate API of HH.ru resource and sends links of favorite jobs via email.

## Requirements

- Python 3.7+
- pip
- smtplib 
- aiogram
- asyncio
- aiohttp
- fake-useragent
- peewee

## Configuration

Add the following values into utils/config.py.

Configuration Values:
- TOKEN = Get it from @BotFather
- NAME = Vacancy name
- EMAIL = Vacancies will be sent from this email
- PASSWORD = email password

## Installing Requirements

Install the required Python Modules in your machine.

'''pip3 install -r requirements.txt'''

