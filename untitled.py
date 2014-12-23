# coding=utf-8
import requests
from flask import Flask, request

app = Flask(__name__)


class Bittly:
    api = "https://api-ssl.bitly.com"
    oauth_link = api + "/oauth/access_token"
    user_info = api + "/v3/user/info?access_token="
    client_id = "bb47d3d5a21316c6d6da210da7c312fe8c1e0030"
    client_secret = "b46c948b926b083057f1823c7d3c335ac090d5ae"
    token = ""
    code = ""


class Site:
    home_page = "http://127.0.0.1:5000/"
    page1 = home_page + "page1"
    page2 = home_page + "page2"
    page3 = home_page + "page3"


def oauth_request():
    return \
        "https://bitly.com/oauth/authorize?client_id={0}" \
        "&redirect_uri={1}".format(Bittly.client_id, Site.page1)


def get_token(code):
    payload = (dict(client_id=Bittly.client_id.encode('UTF-8'),
                    client_secret=Bittly.client_secret.encode('UTF-8'),
                    code=code.encode('UTF-8'),
                    redirect_uri=Site.page1.encode('UTF-8')))

    hdr = {'content-type': 'application/x-www-form-urlencoded'}

    print "payload=", payload
    response = requests.post(url=Bittly.oauth_link, headers=hdr, data=payload)
    print (response.text)
    Bittly.token = response.text.split("&", 1)[0].split("=")[1]
    return Bittly.token


@app.route('/')
def home():
    print "started"
    url = \
        '<h2 align = "Center">Лабораторная работа 1</h2>' \
        '<a href="{0}">Войти с помощью OAuth 2.0</a><br>' \
        '<a href="{1}">Пользовательские данные</a><br>' \
        '<a href="{2}">Выход</a><br>'.format(oauth_request(), Site.page2, Site.page3)
    return url


@app.route("/page1")
def page1():
    print "Current token={0}.".format(Bittly.token)
    url = '<h2 align = "Center">Страница входа</h2>'
    if Bittly.token:
        url += "<h6>Вы уже вошли</h6>"
    else:
        code = request.args.get('code')
        print "code:{0}".format(code)
        Bittly.token = get_token(code)
        url += '<h6>Вход: Успешно!</h6>'
        print "token = " + Bittly.token
    return url + '<a href="/">Домашняя страница</a><br>'


@app.route("/page2")
def page2():
    url = ""
    if Bittly.token:
        udata = requests.get(url=(Bittly.user_info + Bittly.token))
        print udata.text
        url = \
            '<h2 align = "Center">Пользовательские данные</h2><br>' \
            '<h6>{0}</h6>'\
            '<a href="/">Домашняя страница</a><br>'.format(udata.text)
    else:
        url = \
            '<h2 align = "Center">Пользовательские данные</h2><br>' \
            '<h6>Ошибка: Требуется войти!</h6>'\
            '<a href="/">Домашняя страница</a><br>'
    return url


@app.route("/page3")
def page3():
    url = '<h2 align = "Center">Выход</h2>'

    if Bittly.token:
        url += '<p>Выход: Успешно</p>'
        Bittly.token = ""
        Bittly.code = ""
    else:
        url += '<p>Ошибка! Вы не вошли</p>'

    url += '<a href="/">Домашняя страница</a><br>'
    return url


if __name__ == '__main__':
    app.run()
