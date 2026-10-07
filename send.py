import os
import datetime
import requests

token = os.environ["TELEGRAM_BOT_TOKEN"]
chat = os.environ["TELEGRAM_CHAT_ID"]
gemini_key = os.environ.get("GEMINI_API_KEY", "")

with open("posts.txt", encoding="utf-8") as f:
    posts = [p.strip() for p in f.read().split("---") if p.strip()]

day = datetime.date.today().toordinal()

topics = [
    "أداة ذكاء اصطناعي مفيدة وكيف تستخدمها",
    "فكرة عمل حر يمكن البدء بها من الهاتف",
    "نصيحة لتعلم مهارة رقمية مطلوبة",
    "طريقة لاستخدام الذكاء الاصطناعي في الكتابة أو التصميم",
    "فكرة منتج رقمي يمكن بيعه",
    "نصيحة لتجنب النصب والوعود الوهمية في الربح من الإنترنت",
    "أداة مجانية لتصميم أو مونتاج الفيديو",
    "فكرة لمحتوى قصير على يوتيوب أو تيك توك",
    "نصيحة لتنظيم الوقت أثناء تعلم مهارة جديدة",
    "فكرة خدمة صغيرة يمكن تقديمها لأصحاب المحلات",
    "طريقة للأتمتة وتوفير الوقت بأدوات مجانية",
    "كيف تكتب أمرًا جيدًا للذكاء الاصطناعي",
]


def ai_post():
    if not gemini_key:
        return None
    topic = topics[day % len(topics)]
    prompt = (
        "اكتب منشورًا قصيرًا لقناة تيليجرام عربية عن: " + topic + ". "
        "الشروط: لغة عربية فصحى مبسطة، من 2 إلى 4 جمل قصيرة، "
        "ابدأ بإيموجي واحد مناسب، لا تضع روابط ولا هاشتاغات، "
        "لا تستخدم النجوم ولا التنسيق، لا تعد بأرباح مضمونة أو أرقام مبالغ فيها، "
        "ولا تكتب جملة ختامية عن المتابعة. أعد نص المنشور فقط."
        "مهم: اجعل المنشور جملتين أو ثلاثًا فقط (حوالي 40 كلمة) مع خطوة عملية واحدة يطبقها القارئ اليوم، دون شرح عام عن الأداة، ولا تكرر الأدوات المشهورة جدًا."
    )
    for model in ["gemini-3.6-flash", "gemini-2.5-flash"]:
        try:
            r = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                headers={"x-goog-api-key": gemini_key},
                json={"contents": [{"parts": [{"text": prompt}]}]},
                timeout=60,
            )
            if r.status_code != 200:
                print("Gemini HTTP", model, r.status_code, r.text[:300])
                continue
            parts = r.json()["candidates"][0]["content"]["parts"]
            text = "".join(p.get("text", "") for p in parts).strip()
            text = text.replace("*", "").replace("#", "")
            if 40 < len(text) < 900:
                print("Gemini OK:", model)
                return text
            print("Gemini text rejected:", model, len(text))
        except Exception as e:
            print("Gemini failed:", model, type(e).__name__)
    return None


body = ai_post() or posts[day % len(posts)]
text = body + "\n\nتابعنا للمزيد 👇"

r = requests.post(
    f"https://api.telegram.org/bot{token}/sendMessage",
    data={"chat_id": chat, "text": text},
)
print(r.status_code, r.text)
r.raise_for_status()
