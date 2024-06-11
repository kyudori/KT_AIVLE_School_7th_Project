from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from django.http import HttpResponseRedirect
from .models import UsageLog, VectorData
from .forms import CSVUploadForm
import csv
from langchain.embeddings import OpenAIEmbeddings
import pickle  # 추가

class UsageLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'answer', 'timestamp')
    list_filter = ('timestamp', 'user')
    search_fields = ('question', 'answer', 'user__user_id')

class VectorDataAdmin(admin.ModelAdmin):
    list_display = ('category', 'question', 'answer')
    search_fields = ('category', 'question', 'answer')
    change_list_template = "admin/vector_data_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-csv/', self.upload_csv, name='upload_csv'),
        ]
        return custom_urls + urls

    def upload_csv(self, request):
        if request.method == "POST":
            form = CSVUploadForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = request.FILES['csv_file']
                # 인코딩을 명시적으로 지정
                reader = csv.DictReader(csv_file.read().decode('euc-kr', errors='ignore').splitlines())
                embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
                for row in reader:
                    try:
                        category = row['구분']
                        qa = row['QA'].split('\n', 1)
                        question = qa[0]
                        answer = qa[1] if len(qa) > 1 else ''
                        embedding = embeddings.embed_documents([question])[0]
                        embedding_bytes = pickle.dumps(embedding)  # 리스트를 바이너리로 변환
                        VectorData.objects.create(category=category, question=question, answer=answer, embedding=embedding_bytes)
                    except KeyError as e:
                        self.message_user(request, f"CSV 파일에 '{e.args[0]}' 열이 없습니다.")
                        return HttpResponseRedirect("../")
                self.message_user(request, "CSV file has been uploaded successfully.")
                return HttpResponseRedirect("../")
        form = CSVUploadForm()
        payload = {"form": form}
        return render(request, "admin/csv_form.html", payload)

admin.site.register(UsageLog, UsageLogAdmin)
admin.site.register(VectorData, VectorDataAdmin)
