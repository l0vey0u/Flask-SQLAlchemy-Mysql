## Flask Web APP running on Docker container

> Simple CRUD Implementation using Flask, SQLAlchemy running on uwsgi + nginx

### Flask app

Simple board showing the number of confirmed cases using user input data

Endpoints
- /
  - redirect read except having no data ( redirect insert at having no data )
- /read/
  - show data list from database
  - if data list has no data, redirect to insert
- /insert/
  - insert data to database
  - can batch input to upload csv file
- `/edit/<date>?count=value`
  - no page layout but can use request url that like below format
  - ```localhost/edit/2020-10-01?count=64```
- /remove_all_data/
  - **CAUTION**
  - Delete all rows at DailyConfirmed and UploadedFile Table with delete uploaded csv file
  - after delete redirect insert
  - I recommend that disable end point at non debug  
- /upload/
  - handle upload file
  - insert real file name to database with file checksum ( Cuz Duplicate File ) and use row idx to save name   
- /export/
  - no page layout but can use request url that like below format
  - ```localhost/export```

### Docker Container Orchestration

1. external request <-> nginx ( proxy ) ( 8099 to 5000 )
  - Nginx Recieve Request
  - Return Response if request was about cached data or static file
  - if Not send request to uwsgi
2. nginx <-> uwsgi ( 8080 )
  - cuz nginx don't know python, uwsgi interpret request as middleware and send to flask app 
3. uwsgi <-> frontend_flask ( socket )
  - flask app will process the request and send response

### Reference

- [Flask - uwsgi - Nginx 와 docker-compose를 사용해 서버를 만들자 - 개발자 울이 노트](https://woolbro.tistory.com/95)

### Usage
> Clean Ubuntu
- Install Docker follow [this guide](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04)
> Clean Ubuntu with docker ( like github codespace )
- execute ```./install_docker-compose.sh```
> Docker compose
- docker-compose up -d --build
- After docker container orchestration, Can access Flask web app to **localhost:8099**  
> Check logs
- docker logs container_name
> Customize Portforward
- change ports value at backend service in docker-compose.yml
  - ```- 8099:5000``` to ```wanna_port:5000```

