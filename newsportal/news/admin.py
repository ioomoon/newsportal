from django.contrib import admin
from .models import Post, Author, Comment, Category, PostCategory


#Настройка моделей в админке:
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'text', 'created_at')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'created_at')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(Category, CategoryAdmin)
admin.site.register(PostCategory)

