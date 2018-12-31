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



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()


