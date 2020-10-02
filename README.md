# CRUD using Flask + SQLAlchemy + Mysql 

> 설명

Create, Read, Update, Delete + 파일 업로드/다운로드 기능을 해당 환경에서 구현하였습니다.

일일 코로나 확진자 수 데이터를 다루는 상황이며

models내에 db.Model 객체를 추가하고 ( 참고 : DailyConfirmed, UploadedFile )

routes.py 파일을 수정하면 됩니다. 

업로드 된 파일 저장은 간단한 보안조치로 [secure_filename](https://tedboy.github.io/flask/generated/werkzeug.secure_filename.html)을 사용하고 

2차적으로 uploaded_file 테이블에 file 이름을 저장하여 추후의 파일을 다운받는 기능을 만들 때 

해당 db에서 정보를 얻을 수 있게 구성하였습니다.

중복 데이터 등록 시도를 막기 위하여 checksum 비교를 통해 이미 업로드된 파일은 받지 않도록 하였습니다.



DailyConfirmed Table을 Pandas 모듈을 이용해 DataFrame 형태로 바꾸고 csv파일로 export 하는 기능을 

/export/에 구현해두었습니다.



> 구성

1. external request <-> backend_nginx ( 8099 to 5000 )
2. backend_nginx <-> uwsgi ( 8080 )
3. uwsgi <-> frontend_flask ( socket )

### NGINX

---

> Role

- Serve static page / file like css, image ...
  - Also do caching ( micro caching )
- Reverse Proxy 
- Load Balancing



### uWSGI

---

> Role

- Middleware
- Web Server(Nginx)와 Web Application(Flask)간의 연결을 중계
  - HTTP Request -> Python Request
  - Python Response -> HTTP Response
- Translate HTTP Protocol Request to Python Call

> Reference

- Nginx, Uwsgi, Flask
  - [Flask - uwsgi - Nginx 와 docker-compose를 사용해 서버를 만들자 - 개발자 울이 노트](https://woolbro.tistory.com/95)

> Usage

1. docker-compose up -d --build

   - docker-compose가 구버전일 경우 : [클릭](https://github.com/10up/wp-local-docker/issues/58#issuecomment-476786006)

     버전만 1.27.4로 바꿔준다.

   - docker가 없을 경우 ( ubuntu:20.04 기준 ): [설치 가이드](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04) 

> Customize

1. 포트포워딩 수정

   - docker-compose.yml 내 backend 서비스의 ports 설정 부분 수정

     ```- 8099:5000``` 를 ```wanna_port:5000```로 수정

