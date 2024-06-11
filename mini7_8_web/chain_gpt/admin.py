from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from django.http import HttpResponseRedirect
from .models import UsageLog, VectorData
from .forms import CSVUploadForm
import csv
from langchain.embeddings import OpenAIEmbeddings

class UsageLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'answer', 'timestamp')
    list_filter = ('timestamp', 'user')
    search_fields = ('question', 'answer', 'user__username')

class VectorDataAdmin(admin.ModelAdmin):
    list_display = ('data',)
    search_fields = ('data',)
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
                reader = csv.reader(csv_file.read().decode('utf-8').splitlines())
                embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
                for row in reader:
                    data = row[0]
                    vector = embeddings.embed_documents([data])[0]
                    VectorData.objects.create(data=data, vector=vector)
                self.message_user(request, "CSV file has been uploaded successfully.")
                return HttpResponseRedirect("../")
        form = CSVUploadForm()
        payload = {"form": form}
        return render(request, "admin/csv_form.html", payload)

admin.site.register(UsageLog, UsageLogAdmin)
admin.site.register(VectorData, VectorDataAdmin)
