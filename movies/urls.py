from django.conf.urls import url
from . import views

app_name = "movies"

urlpatterns = [
    url(r'^$', views.movie_list, name='movie_list'),
    url(r'^detail/(?P<slug>[\w-]+)/$', views.movie_detail, name='movie_detail'),
    url(r'^create/$', views.movie_create, name='movie_create'),
    url(r'^edit/$', views.movie_update, name='movie_update'),
    url(r'^delete/$', views.movie_delete, name='movie_delete'),

    url(r'^genres/$', views.genre_list, name='genre_list'),
    url(r'^genres/detail/(?P<slug>[\w-]+)/$', views.genre_detail, name='genre_detail'),
    url(r'^genres/create/$', views.genre_create, name='genre_create'),
    url(r'^genres/(?P<genre_id>\d+)/edit/$', views.genre_update, name='genre_update'),
    url(r'^genres/(?P<genre_id>\d+)/delete/$', views.genre_delete, name='genre_delete'),
]
