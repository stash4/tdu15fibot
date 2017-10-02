import os
import requests
from bs4 import BeautifulSoup


# 希望登録数を取得
def get_table():
    # 配属希望登録サイトへのログイン情報
    login_info = {
        'id': os.environ['TDU_ID'],
        'code': os.environ['TDU_PASS'],
        'func': 'authByRadius'
    }
    url = 'https://www.mlab.im.dendai.ac.jp/bthesis2018/StudentDeploy.jsp'
    # ログインしてresponse取得
    session = requests.session()
    res = session.post(url, data=login_info, timeout=30)
    res.raise_for_status()
    # soupで現在の希望登録数のtableを取得
    soup = BeautifulSoup(res.text, 'html.parser')
    table = soup.find('table', {'class': 'remain_table'}).findAll('td')
    return table
