from flask import Flask, request, abort
import json
import datetime
import os

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    return "LINE GPT Bot is running!", 200

@app.route("/callback", methods=['POST'])
def callback():
    try:
        payload = request.get_json()

        if not payload:
            return "No JSON payload", 400

        # LINEのイベント取得
        events = payload.get("events", [])
        for event in events:
            if event.get("type") == "message":
                text = event["message"].get("text", "")
                user_id = event["source"].get("userId", "unknown")
                timestamp = datetime.datetime.now().isoformat()

                # 保存データ作成
                log = {
                    "timestamp": timestamp,
                    "user": user_id,
                    "message": text
                }

                # JSONファイルに追加保存
                log_path = "daily_log.json"
                if os.path.exists(log_path):
                    with open(log_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                else:
                    data = []

                data.append(log)
                with open(log_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)

        return "OK", 200

    except Exception as e:
        return f"Error: {e}", 500
