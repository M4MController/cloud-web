FROM python:3
MAINTAINER Eduard Asriyan <ed-asriyan@protonmail.com>

WORKDIR /application

# notice: crete for docker-compose in controller deploy. build context is on one level up: ..

ADD requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install smbus gpiozero termcolor obd

ADD server ./server
ADD m4m_client ./m4m_client
ADD config/__init__.py ./config/__init__.py
ADD config/config.hjson ./config/config.hjson
ADD sensors_polling/main.py ./main.py
ADD sensors_polling/m4m_gsm.py ./m4m_gsm.py
ADD sensors_polling/m4m_imu.py ./m4m_imu.py
ADD sensors_polling/m4m_obd.py ./m4m_obd.py
ADD sensors_polling/m4m_utils.py ./m4m_utils.py

CMD python3 ./main.py
