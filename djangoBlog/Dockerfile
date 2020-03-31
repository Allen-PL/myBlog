FROM python:3.6.6
RUN mkdir -p /usr/src/djangoBlog
WORKDIR /usr/src/djangoBlog
COPY pip.conf /root/.pip/pip.conf
COPY requirements.txt /usr/src/djangoBlog/
RUN pip install -r /usr/src/djangoBlog/requirements.txt
RUN rm -rf /usr/src/djangoBlog
COPY . /usr/src/djangoBlog
CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000"]