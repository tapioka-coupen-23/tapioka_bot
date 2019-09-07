import sys
import time
import csv
import os
import jaconv
import prefecture_list
from flask import Flask, request, abort, send_file, session, render_template

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, LocationMessage, MessageImagemapAction, ImagemapArea, ImagemapSendMessage, BaseSize, LocationSendMessage, TemplateSendMessage, CarouselTemplate, FollowEvent, UnfollowEvent
)

app = Flask(__name__)

app.config['SECRET_KEY'] = 'The secret key which ciphers the cookie'

channel_secret = os.environ["YOUR_CHANNEL_SECRET"]
channel_access_token = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

if "complete_flug" in globals():
    del search_mode
    del complete_flug
    #f.close()


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route("/callback", methods=['POST'])
def callback():

    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    #print(signature)

    # get request body as text
    body = request.get_data(as_text=True)
    #print(body)
    app.logger.info("Request body: " + body)
    #print(app.logger.info)

    # handle webhook body
    #print(handler.handle(body, signature))
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        #print(handler.handle(body, signature))
        abort(400)

    return 'OK'






@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global user_id
    global search_mode
    global complete_flug
    global user_list
    user_id = event.source.user_id
    if "user_list" not in globals():
        user_list = []
    #search_mode = ""
    #print(event)
    #user_id = event.source.user_id
    #print(user_id)

    #print(event)



    if event.type == "message":

        if "search_mode" not in globals():

            user_list.append(user_id)
            search_mode = "sex"
            #time.sleep(1)
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text="初期設定を始めるので性別を教えて下さい" + chr(0x10008D)),
                 ]
            )
            #time.sleep(1)
        else:
            #print(search_mode)
            #print(event)
            if search_mode == "sex":
                if event.message.text == "男":
                    event.message.text = "男性"
                elif event.message.text == "女":
                    event.message.text = "女性"
                if event.message.text == "男性" or event.message.text == "女性":
                    search_mode = "old"
                #time.sleep(1)
                    user_list.append(event.message.text)
                    line_bot_api.reply_message(
                        event.reply_token,
                        [
                            TextSendMessage(text="次に年齢を教えて下さい" + chr(0x10008D)),
                        ]
                    )
                else:
                    line_bot_api.reply_message(
                        event.reply_token,
                        [
                            TextSendMessage(text="性別を入力して下さい" + chr(0x10008D)),
                        ]
                    )
            elif search_mode == "old":
                age = jaconv.z2h(event.message.text, digit=True, kana=False, ascii=False)
                if age.find("歳") != -1 or age.find("才") != -1:
                    age = age[:-1]
                    print(age)
                if age.isdecimal() == True:
                    search_mode = "prefecture"
                    user_list.append(age)
                    #time.sleep(1)
                    line_bot_api.reply_message(
                        event.reply_token,
                        [
                            TextSendMessage(text="次に出身都道府県を教えて下さい" + chr(0x10008D)),
                        ]
                    )
                else:
                    line_bot_api.reply_message(
                        event.reply_token,
                        [
                            TextSendMessage(text="年齢を入力して下さい" + chr(0x10008D)),
                        ]
                    )
            elif search_mode == "prefecture":
                if event.message.text == "東京都" or event.message.text == "大阪府" or event.message.text == "京都府":
                    prefecture = event.message.text
                elif event.message.text == "東京":
                    prefecture = "東京都"
                elif event.message.text == "大阪" or event.message.text == "京都":
                    prefecture = f"{event.message.text}府"
                elif event.message.text.find("県") == -1 and (event.message.text != "東京都" or event.message.text != "大阪府" or event.message.text != "京都府"):
                    #print(event.message.text)
                    prefecture = f"{event.message.text}県"
                else:
                    prefecture = event.message.text

                print(prefecture)
                prefecture_info = prefecture_list.prefecture_list
                #print(prefecture_info)

                if (prefecture in prefecture_info) == True:

                    del search_mode
                    user_list.append(prefecture)
                    user_info = ",".join(user_list)
                    #print(user_info)
                    csv_wtite(user_list)
                    del user_list
                    #f.write(user_info)
                    #f.write("\n")
                    #print(f)
                    #time.sleep(1)
                    line_bot_api.reply_message(
                        event.reply_token,
                        [
                            TextSendMessage(text="初期設定は以上です" + chr(0x10008D)),
                        ]
                    )
                    complete_flug = "true"
                else:
                    #print(prefecture in prefecture_info)
                    line_bot_api.reply_message(
                        event.reply_token,
                        [
                            TextSendMessage(text="都道府県を入力して下さい" + chr(0x10008D)),
                        ]
                    )


def csv_wtite(user_list):
    file = "user.csv"
    f = open(file, "a")
    user_info = ",".join(user_list)
    f.write(user_info)
    f.write("\n")
    f.close()

if __name__ == '__main__':
    app.run()
