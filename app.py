from flask import Flask, request, abort
from preprocess import Preprocess
from process import Process
import json

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

line_bot_api = LineBotApi('HS0qGAoYpsNgCXPDABPZQ8UYzDYMUCUz2UVIzIVYNsQxZuDhuIfgxpEsSNOi3NR4o7N4t9jlOJ/R1bCJMqL++ntSYOlmYqL8Ro1i5gH4yeSzyffOFmyLM6NEqG6f/vsAcrEC2mO7eWiKC/BZCQBx0gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('b84fbd8f41f604f63f3d62e6fbfbd747')


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
    print(event)
    
    msgtext = event.message.text
    res = ""
    
    if( msgtext.lower().startswith("halo")):
        res = "Halo juga"
    elif( msgtext.lower() == "hai"):
        res = "hai juga"
    elif( msgtext.lower() == "assalamualaikum"):
        res = "Wa'alaikumussalam"
    elif( msgtext.lower().startswith("selamat pagi")):
        res = "Selamat pagi juga"
    elif( msgtext.lower().startswith("selamat siang")):
        res = "Selamat siang juga"
    elif( msgtext.lower().startswith("selamat sore")):
        res = "Selamat sore juga"
    elif( msgtext.lower().startswith("selamat malam")):
        res = "Selamat malam juga"

    if(res != ""):
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=res))
    else:
        keywords =  Preprocess(msgtext)
        proc = Process(keywords.result)

        if(proc.result["val"] >= 15):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Jawaban tidak ditemukan"))
        else:        
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=proc.result["jawaban"]))
          


if __name__ == "__main__":
    app.run()