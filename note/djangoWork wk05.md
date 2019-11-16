# 개발 환경 준비
###1. 파이썬 설치
  튜토리얼(https://tutorial.djangogirls.org/ko/) 참조

###2. 작업 폴더 생성
```
C:\>mkdir work    # (C:\ 폴더 하위에) work 폴더 생성
C:\>cd work       # work 폴더 내부로 진입
C:\work>          # work 폴더 내부로 진입한 상태
```
###3. 가상 환경
- 가상 환경 설치
  ```
  C:\work>python -m venv myvenv  # C:\work 폴더 하위에 myvenv 가상 환경 생성
  ```

- 가상 환경 활성화/비활성화
  ```
  C:\work>myvenv\Scripts\activate            # 활성화
  (myvenv) C:\work>                          # 활성화 된 상태
  (myvenv) C:\work>deactivate           # 비활성화
  C:\work>                              # 비활성화 된 상태
  ```

###4. 장고 및 기타 모듈 설치
- pip 최신화
  ```
  (myvenv) C:\work>python -m pip install --upgrade pip      # pip 최신화
  ```
- 장고 설치  
  ```
  (myvenv) C:\work>pip install django~=2.0.0                # 장고 설치
  ```
- 장고 외 모든 모듈을 일괄 설치하는 방법
  ```
  (myvenv) C:\work>pip freeze > requirements.txt  # 설치된 모듈 목록 저장
  (myvenv) C:\work>pip install -r lstModule.txt # 모듈 목록 일괄/개별 설치
  ```
- 설치가 필요한 모듈 목록 (lstModule.txt)
  ```
  asn1crypto==0.23.0
  cffi==1.11.2
  cryptography==2.1.3
  Django~=1.11.7
  django-disqus==0.5
  django-tagging==0.4.6
  enum34==1.1.6
  funcsigs==1.0.2
  idna==2.6
  ipaddress==1.0.16
  mock==2.0.0
  ndg-httpsclient==0.4.0
  olefile==0.44
  pbr==3.1.1
  Pillow==4.1.1
  pyasn1==0.3.7
  pycparser==2.18
  pyOpenSSL==17.3.0
  pytz==2017.3
  six==1.11.0
  ```

# 장고 개발
###1. startproject 작업
```
(myvenv) C:\work>django-admin.exe startproject mysite .  # 마지막 '.' 주의
```
```
work
├───manage.py
└───mysite
        settings.py
        urls.py
        wsgi.py
        __init__.py
```
- django-admin.exe는 C:\work>\myvenv\Scripts\ 폴더에 존재하지만,
  가상 환경이 활성화된 상태에서는 (자동적으로 path가 연결되므로) 실행됨
- startproject 작업에서 현재 폴더라는 의미로 '.'을 명시하는 방법
- 현재 폴더에 manage.py 파일과 mysite 폴더가 생성됨

###2. mysite/settings.py 수정
```python {.line-numbers}
# mysite/settings.py
# ...
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.pythonanywhere.com']
# ...
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
# ...
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
```

###3. DB 및 수퍼유저 생성
- DB 생성
  ```
  (myvenv) C:\work>python manage.py migrate
  ```
- 수퍼유저 작업
  ```
  (myvenv) C:\work>python manage.py createsuperuser

  (myvenv) C:\work>python manage.py changepassword yeshin
  ```

###4. 웹 서버 기동 및 접속
```
(myvenv) C:\work>python manage.py runserver
# UnicodeDecodeError 오류 발생한다면, ...
(myvenv) C:\work>python manage.py runserver 0:8000
```
브라우저에서 http:localhost:8000 접속

###5. 앱 작성

#####5.1 startapp 작업
```
(myvenv) C:\work>python manage.py startapp blog
```
- manage.py 파일이 존재하는 작업 폴더에서 startapp 작업을 수행하면, 해당 폴더에 blog 앱 폴더가 생성됨
  ```
  work
  ├───manage.py
  └───mysite          # 프로젝트 폴더
          settings.py
          urls.py
          wsgi.py
          __init__.py
  └───blog            # 앱 폴더
          migrations    # DB 현행화 작업용 폴더
          __init__.py   # blog 폴더를 파이썬 모듈로 취급하기 위한 초기화 코드 파일
          admin.py      # 관리자 페이지를 설정하는 코드 파일
          apps.py       # 앱 설정 코드 파일
          models.py     # (DB) 모델 코드 파일
          works.py      # 테스트 코드 파일
          views.py      # 뷰 코드 파일
  ```
#####5.2 앱 등록
```python {.line-numbers}
# mysite/settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    # ...
    'blog',       # !!!
]
```
#####5.3 모델 작성
- 모델 코드 작성
```python {.line-numbers}
# blog/models.py
from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
```
- 모델 DB 작업
  ```
  (myvenv) C:\work>python manage.py makemigrations blog   # DB 현행화 준비
  (myvenv) C:\work>python manage.py sqlmigrate blog       # DB 현행화 검토/확인
  (myvenv) C:\work>python manage.py migrate blog          # DB 현행화 실행
  ```
  - makemigrations 및 migrate 작업은 늘 쌍으로 수행되어야 함
  - 단, 최초 DB 생성 작업은 migrate 작업만 수행

#####5.4 관리자 화면 작업
- 생성된 모델을 (관리자 화면에) 등록
```python {.line-numbers}
# blog/admin.py
from django.contrib import admin
from .models import Post

admin.site.register(Post)
```  
- 관리자 화면 접속
  - 수퍼유저 생성
  - 웹 서버 기동
  - http://127.0.0.1:8000/admin/ 접속
  - 새로운 게시글 작성

###6. 배포
- Git 설치
  - http://git-scm.com에서 내려받기
  - 딱 한 단계만 빼고, 기본 설정대로 다음을 계속 눌러주기
  - 다섯 번째 PATH 환경 설정(Adjusting your PATH environment) 화면
    - 윈도우 커맨드라인에서 Git과 유닉스 도구를 사용(Use Git and optional Unix tools from the Windows Command Prompt)을 선택
    - 윈도우 스타일로 체크아웃, 유닉스 스타일로 라인엔딩 커밋하기(Checkout Windows-style, commit Unix-style line endings)를 체크
    - 나머지는 모두 기본 설정대로 선택

- Git 저장소 초기화
  ```
  (myvenv) C:\work>git init
  (myvenv) C:\work>git config --global user.name "Your Name"
  (myvenv) C:\work>git config --global user.email you@example.com
  ```
  - .gitignore 파일 작성
  ```
  *.pyc
  *~
  __pycache__
  myvenv
  db.sqlite3
  /static
  .DS_Store
  ```
- Git 저장소 상태 확인 및 등록
  ```
  (myvenv) C:\work>git status
  (myvenv) C:\work>git add --all .
  (myvenv) C:\work>git commit -m "first commit"
  ```

- GitHub.com 준비
  - 계정 생성
  - new repository "my-first-blog" 생성
    ![](https://tutorial.djangogirls.org/ko/deploy/images/new_github_repo.png)
    ![](https://tutorial.djangogirls.org/ko/deploy/images/github_get_repo_url_screenshot.png)

- Git add 및 push
  ```
  (myvenv) C:\work>git remote add origin https://github.com/<your-github-username>/my-first-blog.git
  (myvenv) C:\work>git push -u origin master
  ```

- www.pythonanywhere.com  
  - "초보자(Beginner)" 회원가입
  - git clone 작업
    ```
    $ git clone https://github.com/<your-github-username>/my-first-blog.git
    $ cd my-first-blog
    $ virtualenv --python=python3.6 myvenv
    $ source myvenv/bin/activate
    (myvenv) $ pip install django~=1.11.0
    (myvenv) $ python manage.py migrate
    (myvenv) $ python manage.py createsuperuser
    ```
  - 웹 앱으로 블로그 배포
    - 대시보드에서 Web 클릭하고, Add a new web app 선택
    - 수동설정(manual configuration) ("Django"옵션이 아님!) 클릭
    - Python 3.7 선택하고 다음 클릭
  - 가상환경 설정
    ![](https://tutorial.djangogirls.org/ko/deploy/images/pythonanywhere_web_tab_virtualenv.png)
  - WSGI 파일 설정
    - 가상환경 설정 바로 윗 섹션에서, WSGI configuration file 링크 클릭하고 아래 내용으로 대체
      ```python {.line-numbers}
      import os
      import sys

      path = '/home/<your-PythonAnywhere-username>/my-first-blog'  # PythonAnywhere 계정으로 바꾸세요.
      if path not in sys.path:
          sys.path.append(path)

      os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

      from django.core.wsgi import get_wsgi_application
      from django.contrib.staticfiles.handlers import StaticFilesHandler
      application = StaticFilesHandler(get_wsgi_application())
      ```
    - 저장(Save) 후, Web 탭에서 큰 녹색 다시 불러오기(Reload) 버튼 클릭 후, 페이지 최상단 링크로 브라우징

- 간단 홈페이지 제작 및 로컬에서 runserver
  ```python {.line-numbers}
  # mysite/urls.py
  from django.contrib import admin
  from django.urls import path
  from . import views                           # !!!

  urlpatterns = [
      path('', views.homepage, name='home'),    # !!!
      path('admin/', admin.site.urls),
  ]
  ```
  ```python {.line-numbers}
  # mysite/views.py
  from django.shortcuts import render
  from django.http import HttpResponse

  def homepage(request):
      return HttpResponse('여기는 홈 페이지')
  ```
- 2차 이후 배포 (push)   
  ```
  (myvenv) C:\work>git status
  (myvenv) C:\work>git add --all .
  (myvenv) C:\work>git status
  (myvenv) C:\work>git commit -m "Changed the HTML for the site."
  (myvenv) C:\work>git push
  ```

- 2차 이후 서버 작업 (pull)
  ```
  $ cd my-first-blog
  $ git pull
  ```
  - Web tab에서 Reload
