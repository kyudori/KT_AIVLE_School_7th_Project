from django.shortcuts import render

def home(request):
    # 메인 페이지 로직 구현
    return render(request, 'admin_page/index.html')