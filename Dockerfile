# pull official base image
FROM python:3.8.2
# set work directory
WORKDIR /usr/src/gelios_services
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install dependencies
RUN python -m pip install --upgrade pip
RUN pip install numpy
RUN pip install psycopg2
COPY ./requirements.txt .
RUN pip install -r requirements.txt
# copy project
COPY . .