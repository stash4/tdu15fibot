import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from requests_oauthlib import OAuth1Session
import datetime
import os
import psycopg2
import urllib

session = requests.session()

login_info = {
    'id': os.environ['TDU_ID'],
    'code': os.environ['TDU_PASS'],
    'func': 'authByRadius'
}

url_login = 'https://www.mlab.im.dendai.ac.jp/bthesis2018/StudentDeploy.jsp'
res = session.post(url_login, data=login_info, timeout=30)
res.raise_for_status()

soup = BeautifulSoup(res.text, 'html.parser')
table = soup.find('table', {'class': 'remain_table'}).findAll('td')

urllib.parse.uses_netloc.append('postgres')
url = urllib.parse.urlparse(os.environ['DATABASE_URL'])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port)

cur = conn.cursor()

for i in range(0, len(table), 3):
    prof = table[i].text
    cap = table[i + 1].text
    curt = table[i + 2].text
    cur.execute('SELECT curt FROM remain WHERE prof=%s;', (prof,))
    c = cur.fetchone()[0]
    if curt > c:
        cur.execute('UPDATE remain SET curt=%s WHERE prof=%s;', (curt, prof,))
        tw = prof + '研の希望者が増えました．\n' + '現在 ' + curt + '名 / ' + cap + '名'
        tweet(tw)
    elif curt < c:
        cur.execute('UPDATE remain SET curt=%s WHERE prof=%s;', (curt, prof,))
        tweet = prof + '研の希望者が減りました．\n' + '現在 ' + curt + '名 / ' + cap + '名'
        tweet(tw)


def tweet(t):
    twitter = OAuth1Session(
        os.environ['CONSUMER_KEY'],
        os.environ['CONSUMER_SECRET'],
        os.environ['ACCESS_TOKEN'],
        os.environ['ACCESS_TOKEN_SECRET'])

    params = {'status': t}
    req = twitter.post(
        'https://api.twitter.com/1.1/statuses/update.json',
        params=params)
    return req
