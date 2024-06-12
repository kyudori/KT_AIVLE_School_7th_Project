from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import HumanMessage, AIMessage
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

import openai
from .models import UsageLog, VectorData

# Set OpenAI API key from settings
openai.api_key = settings.OPENAI_API_KEY

# Chroma 데이터베이스 초기화 - 사전에 database가 완성 되어 있다는 가정하에 진행
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
database = Chroma(persist_directory="./db", embedding_function=embeddings)

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'chain_gpt/index.html'
    login_url = '/accounts/login/'

    def get(self, request, *args, **kwargs):
        # 세션 초기화
        request.session['chain_chat_history'] = []
        return super().get(request, *args, **kwargs)

@csrf_exempt
def chat(request):
    if request.method == 'POST':
        query = request.POST.get('question')

        # 세션에서 대화 히스토리 로드
        chat_history = request.session.get('chain_chat_history', [])

        # 대화 메모리 생성
        memory = ConversationBufferMemory(memory_key="chat_history", input_key="question", output_key="answer", return_messages=True)
        for message in chat_history:
            memory.chat_memory.add_message(HumanMessage(content=message['human']))
            memory.chat_memory.add_message(AIMessage(content=message['ai']))

        # chatgpt API 및 lang chain을 사용을 위한 선언
        chat = ChatOpenAI(model="gpt-3.5-turbo")
        k = 3
        retriever = database.as_retriever(search_kwargs={"k": k})
        qa = ConversationalRetrievalChain.from_llm(llm=chat, retriever=retriever, memory=memory, return_source_documents=True, output_key="answer")

        # 질의 수행
        result = qa({"question": query, "chat_history": memory.chat_memory.messages})

        # 대화 히스토리 업데이트
        chat_history.append({'human': query, 'ai': result["answer"]})
        request.session['chain_chat_history'] = chat_history

        # 사용 이력 저장
        if request.user.is_authenticated:
            UsageLog.objects.create(user=request.user, question=query, answer=result["answer"])

        # result.html에서 사용할 context 설정
        context = {
            'question': query,
            'result': result["answer"],
            'chat_history': chat_history,
        }

        # 응답을 보여주기 위한 HTML 선택 (위에서 처리한 context를 함께 전달)
        return render(request, 'chain_gpt/result.html', context)
    else:
        return redirect('chain_chatgpt:index')
