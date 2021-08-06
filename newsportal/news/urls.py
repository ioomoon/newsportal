from django.urls import path  # path — означает путь
from .views import PostList, PostDetail, PostSearch, PostAdd, PostUpdate, PostDelete, About, CategoryDetail, SubscribeCategory  # импортируем представления

urlpatterns = [
    path('', PostList.as_view()),  # т.к. сам по себе это класс, нам надо представить этот класс в виде view
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),  # pk — это первичный ключ товара,
    # который будет выводиться у нас в шаблон
    # name - имая, по которому можно обращаться в шаблоне
    path('search/', PostSearch.as_view()),
    path('add/', PostAdd.as_view(), name='post_add'),
    path('create/<int:pk>', PostUpdate.as_view(), name='post_update'),
    path('delete/<int:pk>', PostDelete.as_view(), name='post_delete'),
    path('about/', About.as_view(), name='about'),
    path('category/<int:pk>/', CategoryDetail.as_view(), name='category'),
    path('category/<int:pk>/subscribe', SubscribeCategory.as_view(), name='subscribe_category')
]