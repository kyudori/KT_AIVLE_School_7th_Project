from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
import openai

# Set OpenAI API key from settings
openai.api_key = settings.OPENAI_API_KEY

# Chroma 데이터베이스 초기화 - 사전에 database가 완성 되어 있다는 가정하에 진행
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
database = Chroma(persist_directory="./db", embedding_function=embeddings)

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'rag_gpt/index.html'
    login_url = '/accounts/login/'
    
    def get(self, request, *args, **kwargs):
        # 세션 초기화
        request.session['rag_gpt_chat_history'] = []
        return super().get(request, *args, **kwargs)

@csrf_exempt
def chat(request):
    if request.method == 'POST':
        query = request.POST.get('question')
        
        # 세션에서 RAG GPT의 대화 히스토리 가져오기
        chat_history = request.session.get('rag_gpt_chat_history', [])
        
        # chatgpt API 및 lang chain을 사용을 위한 선언
        chat = ChatOpenAI(model="gpt-3.5-turbo")
        k = 3
        retriever = database.as_retriever(search_kwargs={"k": k})
        qa = RetrievalQA.from_llm(llm=chat, retriever=retriever, return_source_documents=True)

        result = qa(query)

        # 대화 히스토리 업데이트
        chat_history.append({"question": query, "answer": result["result"]})
        request.session['rag_gpt_chat_history'] = chat_history

        # result.html에서 사용할 context
        context = {
            'question': query,
            'result': result["result"],
            'rag_gpt_chat_history': chat_history,
        }

        # 응답을 보여주기 위한 html 선택 (위에서 처리한 context를 함께 전달)
        return render(request, 'rag_gpt/result.html', context)
    else:
        return redirect('rag_chatgpt:index')