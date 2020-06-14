FROM python:3.8-alpine
MAINTAINER Rafa Muñoz rafa93m@gmail.com (@rafa93m)


RUN set -eux \
  && pip install --no-cache-dir nslookup \
  && pip install --no-cache-dir urllib3 \
  && pip install --no-cache-dir pytelegrambotapi

RUN mkdir /opt/src
COPY ./src /opt/src
RUN chmod -R +x /opt/src


WORKDIR /opt/src


CMD ["python3","/opt/src/getippublic.py"]
