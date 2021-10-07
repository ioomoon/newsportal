""" Импортируем библиотеку для взаимодействия с операционной системой и саму библиотеку Celery """
import os
from celery import Celery

""" Библиотека для работы с переодическими задачами"""
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsportal.settings')
# связываем настройки Django с настройками Celery через переменную окружения

app = Celery('newsportal')
app.config_from_object('django.conf:settings', namespace='CELERY')
# создаем экземпляр приложения Celery и устанавливаем для него файл конфигурации

app.autodiscover_tasks()
# указываем Celery автоматически искать задания в файлах tasks.py каждого приложения проекта


app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'tasks.email_once_a_week',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        },
    }
