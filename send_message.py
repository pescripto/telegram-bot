import requests

TOKEN = "8546136873:AAGx7FqA0P_foLSyva1c0GGjQUgMHImmZJw"
CHAT_ID = -1002997050739

mensagem = "Bot online. Teste de envio bem-sucedido."

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

payload = {
    "chat_id": CHAT_ID,
    "text": mensagem
}

response = requests.post(url, data=payload)

print(response.text)
