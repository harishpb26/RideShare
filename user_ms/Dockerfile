FROM python:3

WORKDIR /app

ADD . /app

RUN pip3 install -r requirements.txt

EXPOSE 80

CMD [ "python3", "flaskapp.py" ]
