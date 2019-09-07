import sys
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
    print(handler.handle(body, signature))
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        #print(handler.handle(body, signature))
        abort(400)

    return 'OK'


"""
@handler.add(FollowEvent, message=TextMessage)
def handle_message(event):
    global user_id
    global search_mode
    global search_word
    global session_list
    global to_geo
    global start_time
    user_id = event.source.user_id
    print(user_id)

    print(event)

    if "search_mode" not in globals():
        search_mode = "sex"
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text="初期設定を始めるので性別を教えて下さい" + chr(0x10008D)),
            ]
        )
    else:

        if event.type == "message":

            if search_mode == "sex":
                search_mode = "old"
                line_bot_api.reply_message(
                    event.reply_token,
                    [
                        TextSendMessage(text="次に年齢を教えて下さい" + chr(0x10008D)),
                    ]
                )
            if search_mode == "old":
                search_mode = "prefecture"
                line_bot_api.reply_message(
                    event.reply_token,
                    [
                        TextSendMessage(text="次に出身都道府県を教えて下さい" + chr(0x10008D)),
                    ]
                )
            if search_mode == "prefecture":
                del search_mode
                line_bot_api.reply_message(
                    event.reply_token,
                    [
                        TextSendMessage(text="初期設定は以上です" + chr(0x10008D)),
                    ]
                 )

"""

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global user_id
    global search_mode
    global complete_flug
    #print(event)
    #user_id = event.source.user_id
    #print(user_id)

    #print(event)

    if event.type == "message":

        if "search_mode" not in globals():
            search_mode = "sex"
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text="初期設定を始めるので性別を教えて下さい" + chr(0x10008D)),
                 ]
            )


        if search_mode == "sex":
            search_mode = "old"
            line_bot_api.reply_message(
                event.reply_token,
                    [
                        TextSendMessage(text="次に年齢を教えて下さい" + chr(0x10008D)),
                    ]
            )
        if search_mode == "old":
            search_mode = "prefecture"
            line_bot_api.reply_message(
                event.reply_token,
                    [
                        TextSendMessage(text="次に出身都道府県を教えて下さい" + chr(0x10008D)),
                    ]
            )
        if search_mode == "prefecture":
            del search_mode
            line_bot_api.reply_message(
                event.reply_token,
                    [
                        TextSendMessage(text="初期設定は以上です" + chr(0x10008D)),
                    ]
            )
            complete_flug = "true"


if __name__ == '__main__':
    app.run()
