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

import requests


app = Flask(__name__)

line_bot_api = LineBotApi('')
handler = WebhookHandler('')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

def exchange_rate():
    r=requests.get('https://tw.rter.info/capi.php')
    currency=r.json()
    usd_rate = currency['USDTWD']['Exrate']
    rmb_rate = currency['USDTWD']['Exrate']/currency['USDCNY']['Exrate']
    aud_rate = currency['USDTWD']['Exrate']/currency['USDAUD']['Exrate']
    content = '美金：{:.2f} 人民幣：{:.2f} 澳幣：{:.2f}'.format(usd_rate, rmb_rate, aud_rate)
    return content




@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    input_text = event.message.text

    if input_text == "匯率":
        content=exchange_rate()
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=content))


if __name__ == "__main__":
    app.run()


