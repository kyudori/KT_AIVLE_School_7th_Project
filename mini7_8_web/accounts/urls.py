from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # 메인 페이지 URL 패턴 추가
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
]