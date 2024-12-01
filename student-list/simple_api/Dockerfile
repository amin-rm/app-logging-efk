FROM python:3.8-buster

WORKDIR /

COPY . /

RUN apt update -y && \
    apt install python-dev python3-dev libsasl2-dev libldap2-dev libssl-dev -y && \
    pip install --no-cache-dir -r requirements.txt

RUN mkdir /data

COPY student_age.json /data/student_age.json

EXPOSE 5000

CMD [ "python", "./student_age.py" ]

