from django.conf.urls import url

from . import views

app_name = 'crawler_manager'
urlpatterns = [
    url(r'^', views.home, name='home'),
    url(r'^second-scrap', views.second_scrap, name='second_scrap'),
]