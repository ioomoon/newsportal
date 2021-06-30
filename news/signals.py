'''Импортируем модули, позволяющие отрабатывать сигналы или "события", такие как отправка post запроса'''
from django.db.models.signals import post_save  # сигнал после post запроса
from django.dispatch import receiver  # декоратор, объявляющий функцию приемника сигнала
from .models import Post, Category
from django.template.loader import render_to_string  # # импортируем функцию, которая срендерит наш html в текст
from django.core.mail import EmailMultiAlternatives, send_mail
from django.shortcuts import redirect


# В декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправителе - модель
# Создаем функцию обработчик с параметрами под регистрацию сигнала
# Арг: sender - модель, instance - фактически сохраняемый экз, created - бул, истинно, если была создана новая запись
@receiver(post_save, sender=Post)
def notify_new_post(sender, instance, created, **kwargs):

    if created:  # если создан новый пост
        # Наблюдаем категорию, которая была изменена
        new_post_categories = instance.category.all()
        list_of_subscribers = []
        html_context = {'new_post': instance, 'new_post_id': instance.id, }

        for category in new_post_categories:
            html_context['new_post_category'] = category
            subs = category.subscribers.all()
            for sub in subs:
                list_of_subscribers.append(sub.email)

            html_content = render_to_string('new_post_in_category.html', html_context)

            msg = EmailMultiAlternatives(
                subject=f'Новый пост в Вашей любимой категории {html_context["new_post_category"]}',
                from_email='merrimorlavrushina@yandex.ru',
                to=list_of_subscribers,
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        return redirect('/')
