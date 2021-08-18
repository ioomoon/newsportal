"""Импортируем декоратор для тасков"""
from celery import shared_task
from django.template.loader import render_to_string
from .models import *
from datetime import datetime, timedelta
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone


# @shared_task
# def hello():
#     time.sleep(1)
#     print("Hello, world!")

@shared_task
def email_once_a_week():
    '''Еженедельная рассылка новых новостей'''
    date_end = datetime.now(tz=timezone.utc)
    date_start = date_end - timedelta(days=7)
    last_posts = Post.objects.filter(created_at__range=(date_start,date_end))
    print(last_posts)

    for user in User.objects.all():
        html_content = render_to_string(
            'weekly_news.html',
            {
                'news': last_posts,
            }
        )
        msg = EmailMultiAlternatives(
            subject='Не пропусти новость!',
            body=' ',  # это то же, что и message
            from_email='merrimorlavrushina@yandex.ru',
            # recipient_list=[user.email],
            to=['lavrushina.maria@mail.ru'],  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html

        msg.send()  # отсылаем






