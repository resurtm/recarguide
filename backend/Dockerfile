FROM python:3.6

#RUN apt-get update
#RUN apt-get install -y net-tools

ENV PYTHONUNBUFFERED 1
ENV WORKDIR /opt/recarguide/backend/

RUN mkdir -p $WORKDIR
WORKDIR $WORKDIR

COPY requirements.txt $WORKDIR
RUN pip install --requirement requirements.txt
ADD . $WORKDIR
