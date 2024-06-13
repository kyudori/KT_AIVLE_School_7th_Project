from django.urls import path
from .views import team_view

app_name = 'team'

urlpatterns = [
    path('', team_view, name='index'),
]
