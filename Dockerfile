FROM python:3.11

ADD ./conda_flask /app

WORKDIR /app


RUN pip3 install -i   --upgrade pip

RUN pip3 install flask -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com



CMD ["python","/app/flask/app.py"]