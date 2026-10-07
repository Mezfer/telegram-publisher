import os
import requests

token = os.environ["TELEGRAM_BOT_TOKEN"]
chat = os.environ["TELEGRAM_CHAT_ID"]
text = "✅ اختبار: البوت يعمل ويستطيع النشر في القناة."

r = requests.post(
    f"https://api.telegram.org/bot{token}/sendMessage",
    data={"chat_id": chat, "text": text},
)
print(r.status_code, r.text)
