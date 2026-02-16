import requests

TOKEN = "8546136873:AAGx7FqA0P_foLSyva1c0GGjQUgMHImmZJw"

url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

response = requests.get(url)
data = response.json()

if "result" in data and len(data["result"]) > 0:
    for update in data["result"]:
        if "message" in update:
            chat = update["message"]["chat"]
            chat_id = chat["id"]
            topic_id = update["message"].get("message_thread_id", "Nenhum tópico")
            text = update["message"].get("text", "")
            print(f"Chat: {chat_id} | Topic: {topic_id} | Texto: {text}")
else:
    print("Nenhuma mensagem encontrada. Envie uma mensagem de teste no tópico NOTICIAS AO VIVO.")