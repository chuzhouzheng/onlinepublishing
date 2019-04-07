FROM python:3.7

RUN mkdir /code
COPY requirements.txt /code
RUN pip install -r /code/requirements.txt -i https://pypi.douban.com/simple

WORKDIR /code
ADD . /code
EXPOSE 8000
CMD ["/bin/bash","run.sh"]
