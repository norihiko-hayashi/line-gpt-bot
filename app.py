from flask import Flask, request, abort
import json
import datetime
import os

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
                timestamp = datetime.datetime.now().isoformat()

                # グループIDまたは個人識別
                source = event.get("source", {})
                if source.get("type") == "group":
                    group_id = source.get("groupId", "unknown_group")
                else:
                    group_id = "private_or_other"

                log = {
                    "timestamp": timestamp,
                    "user": user_id,
                    "group": group_id,
                    "message": text
                }

                # グループIDごとにファイル名を分けて保存
                log_path = f"daily_log_{group_id}.json"
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

# Heroku用：ポート番号を環境変数から取得してバインド
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
