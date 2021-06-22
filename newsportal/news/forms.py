from django.forms import ModelForm
from .models import Post


# Создаём модельную форму
class PostForm(ModelForm):
    # в класс мета описываем модель, по которой будет строится форма
    class Meta:
        model = Post
        fields = ['author', 'kind', 'category', 'title', 'text']