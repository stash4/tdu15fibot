import os
import psycopg2
import time
from tweet import tweet
from db import connect_db

# Twitter OAuth
twitter = OAuth1Session(
    os.environ['CONSUMER_KEY'],
    os.environ['CONSUMER_SECRET'],
    os.environ['ACCESS_TOKEN'],
    os.environ['ACCESS_TOKEN_SECRET'])

conn = connect_db()
cur = conn.cursor()

table = ['矢島', '齊藤', '小坂', '中島', '高橋', '鉄谷', '川澄', '増田',
         '猪俣', '岩井', '大野', '竜田', '山田', '池田', '森谷', '井ノ上']

tw = '研究室配属 第一次募集の希望登録数は，以下の結果になりました．\n'

for i in range(16):
    # prof研の人数をdbから取得
    prof = table[i]
    cur.execute('SELECT curt FROM remain WHERE prof=%s;', (prof,))
    curt = cur.fetchone()[0]

    cur.execute('SELECT cap FROM remain WHERE prof=%s;', (prof,))
    cap = cur.fetchone()[0]

    tw += prof + '研: ' + curt + ' / ' + cap + '名\n'
    print(tw)

    conn.commit()

    # tweet140文字制限対策
    if i == 7 or i == 15:
        if i == 7:
            tw += '(続く)'

        tweet(twitter, tw)
        time.sleep(15)
