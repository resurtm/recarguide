FROM python:3.6

ENV PYTHONUNBUFFERED 1
ENV WORKDIR=/opt/recarguide/backend/

RUN mkdir -p $WORKDIR
WORKDIR $WORKDIR

COPY requirements.txt $WORKDIR
RUN pip install --requirement requirements.txt
ADD . $WORKDIR
