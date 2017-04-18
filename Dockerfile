FROM python:3.5.2

RUN mkdir -p /provisioning
WORKDIR /provisioning

COPY ./urbanaccess.egg-info/requires.txt /provisioning/requires.txt

RUN pip install -r ./requires.txt

COPY . /provisioning
