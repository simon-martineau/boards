FROM python:3.8
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /code
WORKDIR /code

COPY requirements/base.txt requirements/test.txt requirements/dev.txt /code/requirements/
RUN pip install -r requirements/base.txt && \
		pip install -r requirements/test.txt && \
		pip install -r requirements/dev.txt

COPY scripts/dev/start_dev.sh /
COPY . /code/