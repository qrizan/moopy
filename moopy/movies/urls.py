from django.conf.urls import url
from . import views

app_name = "movies"

urlpatterns = [
    url(r'^$', views.movie_list, name='movie_list'),
    url(r'^detail/(?P<slug>[\w-]+)/$', views.movie_detail, name='movie_detail'),
    url(r'^create/$', views.movie_create, name='movie_create'),
    url(r'^(?P<movie_id>\d+)/edit/$', views.movie_update, name='movie_update'),
    url(r'^(?P<movie_id>\d+)/delete/$', views.movie_delete, name='movie_delete'),
    url(r'^(?P<genre_id>\d+)/genre/$', views.movie_list_genre, name='movie_list_genre'),
]