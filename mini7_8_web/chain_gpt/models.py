from django.db import models
from django.conf import settings

class UsageLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.timestamp}'

class VectorData(models.Model):
    data = models.TextField()
    vector = models.BinaryField()  # 실제 벡터 데이터는 바이너리로 저장

    def __str__(self):
        return self.data[:50]  # 데이터의 첫 50자를 표시
