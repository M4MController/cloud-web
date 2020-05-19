FROM python:3.7
MAINTAINER Eduard Asriyan <ed-asriyan@protonmail.com>

WORKDIR /application

RUN apt update && apt -y install cron

ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN echo "* 0 * * * root sh -c 'cd /application; /usr/local/bin/python /application/sync_db_with_yadisk.py >> /var/log/cron.log 2>&1'" > /etc/cron.d/hello-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/hello-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

ADD server ./server
ADD config/__init__.py ./config/__init__.py
ADD config/config.hjson ./config/config.hjson
ADD sync/sync_db.py .

CMD cron && tail -f /var/log/cron.log
