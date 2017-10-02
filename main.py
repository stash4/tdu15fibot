from bs4 import BeautifulSoup
from requests_oauthlib import OAuth1Session
import os
import psycopg2
import requests
import time
import urllib
from tweet import tweet
from scraping import get_table

table = get_table()

# db接続
urllib.parse.uses_netloc.append('postgres')
url = urllib.parse.urlparse(os.environ['DATABASE_URL'])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port)

cur = conn.cursor()


# Twitter OAuth
twitter = OAuth1Session(
    os.environ['CONSUMER_KEY'],
    os.environ['CONSUMER_SECRET'],
    os.environ['ACCESS_TOKEN'],
    os.environ['ACCESS_TOKEN_SECRET'])


# 各研究室ごとに処理
for i in range(0, len(table), 3):
    # 教授，定員，現在の希望者数
    prof = table[i].text
    cap = table[i + 1].text
    curt = table[i + 2].text
    print(prof, curt)

    # prof研の前回の人数をdbから取得
    cur.execute('SELECT curt FROM remain WHERE prof=%s;', (prof,))
    c = cur.fetchone()[0]

    if int(curt) > c:
        # 増えていた場合
        cur.execute(
            'UPDATE remain SET curt=%s WHERE prof=%s;',
            (int(curt), prof,))
        d = int(curt) - c
        tw = prof + '研の希望者が増えました．\n現在 ' + curt + ' / ' + cap + '名 (+' + str(d) + '名)'
        print(tw)
        tweet(twitter, tw)
    elif int(curt) < c:
        # 減っていた場合
        cur.execute(
            'UPDATE remain SET curt=%s WHERE prof=%s;',
            (int(curt), prof,))
        d = c - int(curt)
        tw = prof + '研の希望者が減りました．\n現在 ' + curt + ' / ' + cap + '名 (-' + str(d) + '名)'
        print(tw)
        tweet(twitter, tw)

    conn.commit()

    # インターバルを設ける
    time.sleep(15)
