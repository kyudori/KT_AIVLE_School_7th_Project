# 미니프로젝트 7차
조원 : 문동규, 김성규, 한규현, 박성훈, 박종범, 김아영, 하세호, 정주영

## 주제
에이블스쿨 지원자들을 위한 QA Chatbot 서비스 구축


결과물 및 내용은 ppt 참고

## Server Option
Public IP : [3.14.131.41](http://3.14.131.41/)   
현재 운영 종료

서버 실행 명령어   
sudo su - root   
cd /home/ubuntu/7P_AWS/mini7_8_web/   
/home/ubuntu/anaconda3/envs/7p-aws/bin/python manage.py runserver 0:80

백그라운드 실행
nohup /home/ubuntu/anaconda3/envs/7p-aws/bin/python manage.py runserver 0:80&   
백그라운드 실행 종료
sudo fuser -k -n tcp 80
