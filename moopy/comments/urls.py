from django.conf.urls import url
from . import views

app_name = "comments"

urlpatterns = [
    url(r'^detail/(?P<id>\d+)/$', views.comment_thread, name='comment_thread'),
    url(r'^(?P<id>\d+)/delete/$', views.comment_delete, name='comment_delete'),
]