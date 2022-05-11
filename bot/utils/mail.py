import smtplib
from utils import EMAIL
from utils import PASSWORD


def send_email(email_to, msg):
    
    

    letter = f'''
    From: {EMAIL}
    To: {email_to}
    Subject: Вакансии

    {msg}
    '''.encode('utf-8')

    server = smtplib.SMTP_SSL('smtp.yandex.com:465')
    server.login(EMAIL, PASSWORD)
    # server.set_debuglevel(1)
    server.sendmail(EMAIL, email_to, letter)
    server.quit()

 

