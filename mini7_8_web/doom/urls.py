from django.urls import path
from . import views

app_name = 'doom'

urlpatterns = [
    path('', views.index, name='index'),
]
