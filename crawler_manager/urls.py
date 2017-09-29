from django.conf.urls import url

from . import views

app_name = 'crawler_manager'
urlpatterns = [
    url(r'^', views.home, name='home'),
    # url(r'^index_show', views.index_show, name='index_show'),
]