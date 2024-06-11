# 미니프로젝트 7차
조원 : 문동규, 김성규, 한규현, 박성훈, 박종범, 김아영, 하세호, 정주영

#### Discord URL
https://discord.gg/upXzegsCUk

#### 공유 드라이브 URL
https://drive.google.com/drive/folders/1vVdcFe6iJi2gSgmN6JasCLwZz0Jqe66T?usp=drive_link

## Server Option
Public IP : 3.128.204.87
user ID : ubuntu

pem, ppk : https://drive.google.com/drive/folders/1cJr9PSZdcq3D5PNxwLrbwu783PGjg2L-?usp=drive_link

서버 실행 명령어
sudo su - root
cd /home/ubuntu/7P_AWS/mini7_8_web/
/home/ubuntu/anaconda3/envs/7p-aws/bin/python manage.py runserver 0:80

백그라운드 실행
nohup /home/ubuntu/anaconda3/envs/7p-aws/bin/python manage.py runserver 0:80&
백그라운드 실행 종료
sudo fuser -k -n tcp 80
