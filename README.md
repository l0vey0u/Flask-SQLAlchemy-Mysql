# CRUD using Flask + SQLAlchemy + Mysql 

> 설명

Create, Read, Update, Delete + 파일 업로드 기능을 해당 환경에서 구현하였습니다.

일일 코로나 확진자 수 데이터를 다루는 상황이며

models내에 db.Model 객체를 추가하고 ( 참고 : DailyConfirmed, UploadedFile )

routes.py 파일을 수정하면 됩니다. 

업로드 된 파일 저장은 간단한 보안조치로 [secure_filename](https://tedboy.github.io/flask/generated/werkzeug.secure_filename.html)을 사용하고 

2차적으로 uploaded_file 테이블에 file 이름을 저장하여 추후의 파일을 다운받는 기능을 만들 때 

해당 db에서 정보를 얻을 수 있게 구성하였습니다.

중복 데이터 등록 시도를 막기 위하여 checksum 비교를 통해 이미 업로드된 파일은 받지 않도록 하였습니다.

> 구성

flask <--> sqlalchemy ==== mysql