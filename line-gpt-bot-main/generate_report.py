import csv
from datetime import datetime

def generate_report():
    filepath = "daily_log.csv"
    try:
        with open(filepath, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
    except FileNotFoundError:
        print("ログファイルが見つかりません")
        return

    today = datetime.now().strftime("%Y-%m-%d")
    summary = f"📄 {today} の日報：\n"

    for row in rows:
        if len(row) < 3:
            continue
        timestamp, name, message = row
        if timestamp.startswith(today):
            summary += f"[{timestamp}] {name}：{message}\n"

    print(summary)

if __name__ == "__main__":
    generate_report()
