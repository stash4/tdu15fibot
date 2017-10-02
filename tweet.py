from requests_oauthlib import OAuth1Session


# tの内容をツイート
def tweet(twitter, t):
    params = {'status': t}
    req = twitter.post(
        'https://api.twitter.com/1.1/statuses/update.json',
        params=params)
    return req
