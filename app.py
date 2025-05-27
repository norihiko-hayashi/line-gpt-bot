from flask import Flask, request, abort
import json
import datetime
import os

# 🔽 追記：utils.py の関数を読み込む
from utils import save_message_to_json, append_to_google_sheet

app = Flask(__name__)  # ← 最初に必要！

@app.route("/", methods=['GET'])
def index():
    return "LINE GPT Bot is running!", 200

@app.route("/callback", methods=['POST'])
def callback():
    try:
        payload = request.get_json()

        if not payload:
            return "No JSON payload", 400

        events = payload.get("events", [])
        for event in events:
            if event.get("type") == "message":
                text = event["message"].get("text", "")
                user_id = event["source"].get("userId", "unknown")
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # グループIDまたは個人識別
                source = event.get("source", {})
                if source.get("type") == "group":
                    group_id = source.get("groupId", "unknown_group")
                else:
                    group_id = "private_or_other"

                # JSON保存（旧処理）
                log = {
                    "timestamp": timestamp,
                    "user": user_id,
                    "group": group_id,
                    "message": text
                }

                log_path = f"daily_log_{group_id
