FROM python:3.7

RUN mkdir /onlinepublishing
COPY . /onlinepublishing
RUN pip install -r /onlinepublishing/requirements.txt -i https://pypi.douban.com/simple

WORKDIR /onlinepublishing
# EXPOSE 8002
#CMD ["/bin/bash","run.sh"]
