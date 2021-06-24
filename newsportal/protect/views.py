from django.shortcuts import render
from django.contrib.auth.models import User
from .models import BaseRegisterForm
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import redirect  # Пакет django.shortcuts собирает вспомогательные функции и классы,
# которые «охватывают» несколько уровней MVC (render, redirect)
from django.contrib.auth.decorators import login_required


class ProtectView(LoginRequiredMixin, TemplateView):  # информация об авторизированном пользователе
    template_name = 'index.html'

    # Переопределяем метод получения контекста. Сначала мы получили весь контекст из класса-родителя, а после чего
    # добавили новую контекстную переменную.
    def get_context_data(self, **kwargs):  #
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()  # добавляем новую
        # контекстную переменную is_not_author
        # Заходим в переменную запроса self.request, из нее можем вытащить текущего юзера, в поле groups хранятся
        # все группы, в которых он состоит. Далее мы применяем фильтр к этим группам.
        return context


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/news/'


@login_required
def upgrade_me(request):  # функция-представление для апгрейда аккаунта до Author
    # Получаем объект текущего пользователя из переменной запроса
    user = request.user
    author_group = Group.objects.get(name='authors')
    # Проверяем, находится ли пользователь в группе
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect('/')  # перенаправляем пользователя
