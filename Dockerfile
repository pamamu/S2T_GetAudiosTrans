FROM pamamu/s2t_main-controller

ARG SHARED_FOLDER
ENV SHARED_FOLDER = $SHARED_FOLDER
ARG GET_AUDIO_TRANS_NAME
ENV GET_AUDIO_TRANS_NAME = $GET_AUDIO_TRANS_NAME

WORKDIR /srv/S2T/S2T_GetAudiosTrans

ADD . .

RUN apk add --update openssl-dev libffi-dev python-dev libxml2-dev libxml2 libxslt-dev
RUN pip install -r requirements.txt

CMD python src/app.py $GET_AUDIO_TRANS_NAME $SHARED_FOLDER


