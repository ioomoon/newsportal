from django.core.management.base import BaseCommand, CommandError
from news.models import Category, PostCategory


# Имя файла = название команды
class Command(BaseCommand):
    help = 'Удалить все новости из выбранной категории'
    missing_args_message = 'Введите id категории'
    requires_migrations_checks = True  # напоминать ли о миграциях. Если тру — то будет напоминание о том, что не сделаны все миграции (если такие есть)

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('argument', type=int, help=u'Id категории')

    def handle(self, *args, **kwargs):
        # код, который выполняется при вызове команды
        category_id = kwargs['argument']
        self.stdout.readable()
        self.stdout.write(str(kwargs['argument']))
        self.stdout.write(
            'Вы точно хотите очистить категорию? да/нет')  # спрашиваем пользователя действительно ли он хочет удалить все новости из категории
        answer = input()  # считываем подтверждение

        if answer == 'да':
            Category.objects.filter(id=category_id).delete()
            self.stdout.write(self.style.SUCCESS('Новости удалены'))
            return

        self.stdout.write(
            self.style.ERROR('Access denied'))  # в случае неправильного подтверждения, говорим что в доступе отказано
