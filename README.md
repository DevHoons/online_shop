# 쇼핑몰 만들기

- #### Django 학습을 위해 유튜브 오지랖 파이썬 웹 프로그래밍 강의를 참고하였습니다.

---

# 프로젝트 생성법

#### 1. pip install pipenv : pip와 virtualenv를 동시에 사용하기 위한 패키지 설치

#### 2. pipenv --three : 파이썬3 프로젝트 생성

#### 3. pipenv shell : 가상환경 만들어주기

#### 4. pipenv install Django : 장고 설치

- (==x.x.x 처럼 버전을 명시 해주지 않으면 가장 최신 버전이 설치 됌)

#### 5. django-admin startproject config : 프로젝트 생성

- 효율적인 앱 구조화를 위하여 최상위 config 폴더 이름 변경
- 변경한 폴더 내의 manage.py와 config폴더를 밖으로 이동
- 변경한 폴더는 삭제
- 만약 manage.py를 열었을때 알람이 오지 않으면 extensions에서 python 을 설치해야 함!

#### 6. python manage.py migrate : 데이터베이스 업데이트

- 프로젝트 생성 후 Django에서 기본적으로 제공해주는 User Model을 업데이트 시켜주는 과정

#### 7. python manage.py runserver : 서버 가동

- https://127.0.0.1:8000/admin에 접속하여 로그인 페이지가 나오면 성공!
- Admin을 만들어주지 않았기 때문에 아래 명령어로 슈퍼유저 생성

#### 8. python manage.py createsuperuser : 슈퍼유저 생성

- 유저 생성 후 Admin 페이지에서 로그인 확인

#### 9. django-admin startapp app_name : 앱 생성
