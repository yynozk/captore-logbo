import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

WEBHOOK_URL = "https://discordapp.com/api/webhooks/{}".format(os.environ['DISCORD_ID_TOKEN'])

# メールアドレスとパスワードの指定
USER = os.environ['USER']
PASS = os.environ['PASS']

def lambda_handler(event, content):
    # セッションを開始
    session = requests.session()

    # トークン取得
    url_login = "https://capcom-netcatcher.com/login"
    soup = BeautifulSoup(session.get("https://capcom-netcatcher.com/login").text, "html.parser")
    token = soup.find('input', {'name': '_token'}).get('value')

    # ログイン
    login_info = {
        "user_id": USER,
        "user_pass": PASS,
        "_token": token,
    }

    res = session.post(url_login, data=login_info)
    res.raise_for_status()

    # 保有 Z 確認
    soup = BeautifulSoup(res.text, "html.parser")
    z = soup.find('td', {'data-label': '保有Z'}).text

    body = {"content": "{}: {}".format(USER, z)}
    requests.post(WEBHOOK_URL, body)
