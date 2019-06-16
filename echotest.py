import requests 
from bs4 import BeautifulSoup
from urllib.request import urlretrieve

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from linebot.models import *

app = Flask(__name__)

# 填入你的 message api 資訊
line_bot_api = LineBotApi('Uv9eYbX9E4RxYHBmjwwoUr32eVymZNVkeqva7uvLhh8r8sLVSvUmZuIKx8rmANDE/29D5pGctD5nGeTTylHuHJ6o2DqQt210/+Esz+G/Cp18JCy/E9a5qfjF0DwgscCv5h0RZmzPujiIOBAGGVrQ4AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('745051379ec45343551c037a2ba74fc8')


# 設定你接收訊息的網址，如 https://YOURAPP.herokuapp.com/callback
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print("Request body: " + body, "Signature: " + signature)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'
def movie():
    target_url = 'https://movies.yahoo.com.tw/'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')   
    content = ""
    for index, data in enumerate(soup.select('div.movielist_info h1 a')):
        if index == 20:
            return content       
        title = data.text
        link =  data['href']
        content += '{}\n{}\n'.format(title, link)
    return content


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "最新電影":
        a=movie()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=a))


import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])


