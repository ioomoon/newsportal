#  Этот файл хранит все модели проекта.
from django.db import models
from django.contrib.auth.models import User  #  Модель User
"""Импортируем кэш"""
from django.core.cache import cache


class Author(models.Model):  # Модель, содержащая объекты всех авторов
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')
    def update_rating(self):  # Обновление рейтинга суммарный рейтинг каждой статьи автора умножается на 3; суммарный рейтинг всех комментариев автора; суммарный рейтинг всех комментариев к статьям автора.
        total_post_rating = 0
        for post in Post.objects.filter(author=self):
            total_comment_post_rating = 0
            for comment in Comment.objects.filter(post=post):
                total_comment_post_rating += comment.rating
            total_post_rating += post.rating * 3 + total_comment_post_rating

        total_self_comment_user_rating = 0
        for comments in Comment.objects.filter(user=self.user):
            total_self_comment_user_rating += comments.comment_rating

        self.rating = total_post_rating + total_self_comment_user_rating
        self.save()

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Category(models.Model):  # Модель, содержащая объекты категорий
    name = models.CharField(max_length=30, unique=True, verbose_name='Название категории')
    subscribers = models.ManyToManyField(User, blank=True, verbose_name='Подписчики')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Post(models.Model):  # Модель, содержащая объекты всех постов
    news = 'NW'
    article = 'AT'

    CHOICE = [
        (news, 'Новость'),
        (article, 'Статья')
    ]

    author = models.ForeignKey(Author, on_delete=models.PROTECT, verbose_name='Автор')
    kind = models.CharField(max_length=2, choices=CHOICE, default=news, verbose_name='Тип поста')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    category = models.ManyToManyField(Category, through='PostCategory', verbose_name='Категория')
    title = models.CharField(max_length=50, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def like(self): # Рейтинг поста
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        preview = self.text[:124]
        return str(preview) + '...'

    def __str__(self):
        return f'{self.title}:\n{self.text}'

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на главную страницу
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # удаляем его из кэша, чтобы сбросить его


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self):
        return f'{self.category}'

    class Meta:
        verbose_name = 'Категория новости'
        verbose_name_plural = 'Категории новостей'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.PROTECT, verbose_name='Пост')
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Пользователь')
    text = models.CharField(max_length=250, verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def like(self): # Рейтинг коммента
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.text}'