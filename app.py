from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage
import os
import csv
from datetime import datetime
import re

app = Flask(__name__)
line_bot_api = LineBotApi(os.environ["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

def extract_name(text):
    match = re.search(r'([一-龥]{2,})(さん|様)?', text)
    if match:
        return match.group(1)
    return None

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.source.type != "group":
        return
    user_text = event.message.text
    name = extract_name(user_text)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if name:
        filepath = "daily_log.csv"
        with open(filepath, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, name, user_text])
