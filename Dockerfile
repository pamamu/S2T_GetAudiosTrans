FROM pablomacias/s2t_main-controller

WORKDIR /srv/S2T/S2T_GetAudiosTrans

ADD . .

RUN apk add --update openssl-dev libffi-dev python-dev libxml2-dev libxml2 libxslt-dev
RUN pip install -r requirements.txt

#CMD ["cat", "src/app.py"]


