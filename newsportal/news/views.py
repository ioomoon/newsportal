from django.shortcuts import render
from django.views import View  # класс простого представления
from django.views.generic import ListView  # класс, который позволяет в представлении выводить список объектов из БД
from django.views.generic import DetailView  # класс, который позволяет вывести детали объекта на отдельной странице
from django.views.generic import UpdateView, CreateView, DeleteView  # классы, повзволяющие добавлять,
                                                                     # удалять и обновлять объекты
from .models import Post
from .filters import PostFilter  # импортируем фильтр
from .forms import PostForm


class PostList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'posts.html'  # указываем имя шаблона, показывающий как именно выводить страницу (HTML)
    context_object_name = 'posts'  # имя списка с объектами (нужен, чтобы обратиться к нему в HTML)
    queryset = Post.objects.order_by('-created_at')  # то в каком порядке мы выводим элементы (сначала новые)
    # Далее настраиваем URL, чтобы к представлению можно было "обратиться". Создаем urls.py

    paginate_by = 2  # постраничный вывод в х элементов


class PostDetail(DetailView):  # редставление, в котором будут детали конкретного отдельного товара
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostSearch(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'search.html'  # указываем имя шаблона, показывающий как именно выводить страницу (HTML)
    context_object_name = 'posts'  # имя списка с объектами (нужен, чтобы обратиться к нему в HTML)
    queryset = Post.objects.order_by('-created_at')  # то в каком порядке мы выводим элементы (сначала новые)
    # Далее настраиваем URL, чтобы к представлению можно было "обратиться". Создаем urls.py

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты
        # переопределяя метод get_context_data у наследуемого класса
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,
                                       queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class PostAdd(CreateView):  # Джейнерик для создания объекта
    template_name = 'add.html'
    form_class = PostForm


class PostUpdate(UpdateView):  # Джейнерик для редактирования объекта, используем тот же шаблон add
    template_name = 'add.html'
    form_class = PostForm

    # get_object используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDelete(DeleteView):  # Джейнерик для удаления объекта
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'