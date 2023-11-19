import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

from accounts.models import CustomUser


def send_ya_mail(res_email,  msg_text):
    login =  "...@yandex.ru"
    password = "x4B7u5fvKhjvz@."
    # msg = MIMEText(f'{msg_text}', 'plan', 'utf-8')
    msg = MIMEText(f'{msg_text}', 'plain', 'utf-8')
    msg['Subject'] = Header('test message????', 'utf-8')
    msg['From'] = res_email
    msg["To"] = 'rama050102@gmail.com'
    
    s = smtplib.SMTP('smtp.yandex.kz', 587, timeout=10)
    
    try:
        s.starttls()
        s.login(login, password)
        s.send_message(msg)
    except Exception as e:
        print(e)
    finally:
        s.quit()


def get_user_from_token(request) -> CustomUser | None:
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Token '):
        return None
    token = auth_header.split(' ')[1]
    try:
        user = Token.objects.get(key=token).user
        return user
    except Token.DoesNotExist:
        return None