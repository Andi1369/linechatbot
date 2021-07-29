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

line_bot_api = LineBotApi('XQqaoSC/Aamnj5d+aLJB0j6mTlhA1ebLcB3xwR9HZYmbdmyh8/6/wCkP4trmKUewD4AcNYThLpigZSo3AG3geCr+WA8hQkeLz+4n/LXjvNQvu75o3g+dsLw2aOhPKFOJ8XsKzTYNI7Ywb7sTQZAlSgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('4cde8dbb8a27fd0a1e4b182290a4c572')


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
        res = "Halo juga ^.^"
    elif( msgtext.lower() == "hi"):
        res = "Hi ju.ga ^.^"
    elif( msgtext.lower().startswith("selamat malam")):
        res = "Selamat malam juga"
    

    if(res != ""):
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=res))
    else:
        keywords =  Preprocess(msgtext)
        proc = Process(keywords.result)

        if(proc.result["val"] >= 10):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Jawaban tidak ditemukan"))
        else:        
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=proc.result["jawaban"]))
          


if __name__ == "__main__":
    app.run()