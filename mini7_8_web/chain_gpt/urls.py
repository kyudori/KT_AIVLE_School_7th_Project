from django.urls import path
from .views import IndexView, chat

app_name = 'chain_chatgpt'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('chat/', chat, name='chat'),
]
