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

app = Flask(__name__)


line_bot_api = LineBotApi('AeSmr7gCsdw2nqvlM6JD+efhuDhifLeNrL5UwEkChCmmzrx4PLe/C0EgAkSxQQy36rM1jcqZfgBQDZRJQDTJJClF4vxJUSFm4Dq85q4uPFcUbgaB0W/KpVyAMlqXwF/IK//qwpp5TS31VNHA1yBMsgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('32d295f4d12e043a195444580e6786c5')


@app.route("/", methods=['POST'])
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




@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #print("Handle: reply_token: " + event.reply_token + ", message: " + event.message.text)
    content = "{}: {}".format(event.source.user_id, event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=content))


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


import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])


