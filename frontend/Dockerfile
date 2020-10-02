FROM python:3.8
WORKDIR /app

COPY requirements.txt /app
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install -y locales
RUN locale-gen ko_KR.UTF-8
ENV LC_ALL ko_KR.UTF-8

COPY ./src /app

CMD ["uwsgi","uwsgi.ini"]