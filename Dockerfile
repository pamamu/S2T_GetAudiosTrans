FROM python:3.6-alpine

WORKDIR /srv/S2T/S2T_GetAudiosTrans

ADD . .

RUN apk add --update build-base openssl-dev libffi-dev python-dev libxml2-dev libxml2 libxslt-dev
RUN pip install -r requirements.txt

#CMD ["cat", "src/app.py"]


