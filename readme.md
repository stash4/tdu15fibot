# 15FI 研究室配属希望bot

## Description
Herokuで動かすbot．  
卒業研究配属希望登録サイト(https://www.mlab.im.dendai.ac.jp/bthesis2018/StudentDeploy.jsp)から各研究室の希望者数を取得し，ツイートする．

## Usage
1. Herokuでapp作成

2. Add-onsにHeroku Postgresを追加しテーブル作成

```
CREATE TABLE remain(
  prof TEXT PRIMARY KEY,
  curt INTEGER NOT NULL,
  cap INTEGER NOT NULL
  );
```
> 作成したら現在の状況をINSERTしておく．

3. 以下の変数をappのSettingsでConfig Varsに設定

- ACCESS_TOKEN
- ACCESS_TOKEN_SECRET
- CONSUMER_KEY
- CONSUMER_SECRET
- TDU_ID
- TDU_PASS

4. デプロイ
