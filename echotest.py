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

line_bot_api = LineBotApi('/l3lrV/6VKSQOz0HN5iB/9QQwOJltRAjC+kR3h4g9wdiwGWwt3+i7i069DThcx6r/29D5pGctD5nGeTTylHuHJ6o2DqQt210/+Esz+G/Cp0npnEVH8wqyfWGdD0cOlagY6WIdJy1L+JOcj54WwaXwAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('745051379ec45343551c037a2ba74fc8')


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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()


