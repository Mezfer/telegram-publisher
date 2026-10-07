import os
import datetime
import requests

token = os.environ["TELEGRAM_BOT_TOKEN"]
chat = os.environ["TELEGRAM_CHAT_ID"]

with open("posts.txt", encoding="utf-8") as f:
    posts = [p.strip() for p in f.read().split("---") if p.strip()]

day = datetime.date.today().toordinal()
post = posts[day % len(posts)]
text = post + "\n\nتابعنا للمزيد 👇"

r = requests.post(
    f"https://api.telegram.org/bot{token}/sendMessage",
    data={"chat_id": chat, "text": text},
)
print(r.status_code, r.text)
r.raise_for_status()
