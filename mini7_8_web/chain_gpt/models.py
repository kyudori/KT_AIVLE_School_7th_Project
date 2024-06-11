from django.db import models
from django.conf import settings

class UsageLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.user_id} - {self.timestamp}'

class VectorData(models.Model):
    category = models.CharField(max_length=255, default='default_category')
    question = models.TextField(default='default_question')
    answer = models.TextField(default='default_answer')
    embedding = models.BinaryField(default=b'')  # 기본값으로 빈 바이트 설정

    def __str__(self):
        return self.question[:50]  # 데이터의 첫 50자를 표시
