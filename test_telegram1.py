import requests

TOKEN = "8546136873:AAFVTHt_HKorMqW3lksLwnvyKFEpOJAmmWI"
CHAT_ID = "-1002997050739"

r = requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    data={"chat_id": CHAT_ID, "text": "teste manual - pipeline telegram"}
)

print(r.status_code)
print(r.text)