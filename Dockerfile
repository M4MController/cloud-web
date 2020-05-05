FROM python:3.7
MAINTAINER Eduard Asriyan <ed-asriyan@protonmail.com>

WORKDIR /application

ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# for testing
ADD scripts/db_fill_random.py db_fill_random.py

ADD server ./server
ADD config/__init__.py ./config/__init__.py
ADD config/config.hjson ./config/config.hjson
ADD start.py .

CMD python start.py
