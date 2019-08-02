__author__ = 'Administrator'

import requests
from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth

auth = ('root', '123456')
user = {
    "username": 'root',
    "password": '123456',
}

def session_login():
    session = requests.Session()
    # s.auth = auth
    session.post(url='http://127.0.0.1:8000/publish/login', data=user)
    # print(session.cookies)
    response = session.get(url='http://127.0.0.1:8000/publish/test')
    print(session.cookies.items)
    print(response.text)

def auth_login():
    response = requests.get(url='http://127.0.0.1:8000/publish/test',auth=HTTPDigestAuth('root', '123456'))
    print(response.text)


if __name__ == '__main__':
    session_login()
    # auth_login()

