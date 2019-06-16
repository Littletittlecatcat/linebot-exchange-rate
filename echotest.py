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



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    print(msg)
    msg = msg.encode('utf-8')
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))
    
if __name__ == "__main__":
    app.run()