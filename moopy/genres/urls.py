from django.conf.urls import url
from . import views

app_name = "genres"

urlpatterns = [
    url(r'^$', views.genre_list, name='genre_list'),
    url(r'^(?P<slug>[\w-]+)/$', views.genre_detail, name='genre_detail'),
    url(r'^create/$', views.genre_create, name='genre_create'),
    url(r'^(?P<genre_id>\d+)/edit/$', views.genre_update, name='genre_update'),
    url(r'^(?P<genre_id>\d+)/delete/$', views.genre_delete, name='genre_delete'),
]