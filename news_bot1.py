import time
import os
import feedparser
import requests

BOT_TOKEN = "8546136873:AAFVTHt_HKorMqW3lksLwnvyKFEpOJAmmWI"
CHAT_ID = "-1002997050739"
TOPIC_ID = 9

DELAY = 1800  # 30 minutos
ARQUIVO_HISTORICO = "historico.txt"

FEEDS = [
    "https://br.cointelegraph.com/rss",
    "https://www.infomoney.com.br/feed/",
    "https://portaldobitcoin.uol.com.br/feed/"
]

def carregar_historico():
    if os.path.exists(ARQUIVO_HISTORICO):
        with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as f:
            return set(f.read().splitlines())
    return set()

def salvar_historico(historico):
    with open(ARQUIVO_HISTORICO, "w", encoding="utf-8") as f:
        for link in historico:
            f.write(link + "\n")

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "message_thread_id": TOPIC_ID,
        "text": mensagem,
        "disable_web_page_preview": True
    }
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print("Erro ao enviar mensagem:", e)

print("🚀 Bot de notícias CRIPTO/MACRO iniciado")

historico = carregar_historico()

while True:
    try:
        for feed_url in FEEDS:
            feed = feedparser.parse(feed_url)

            for entry in feed.entries[:2]:  # lê as 5 notícias mais recentes
                if not hasattr(entry, "link") or not hasattr(entry, "title"):
                    continue

                if entry.link in historico:
                    continue

                titulo = entry.title.strip()
                mensagem = f"📰 {titulo}\n{entry.link}"

                enviar_telegram(mensagem)
                historico.add(entry.link)
                salvar_historico(historico)

                time.sleep(10)  # pequeno delay entre mensagens

        print("⏸ Aguardando próximo ciclo")
    except Exception as e:
        print("Erro controlado:", e)

    time.sleep(DELAY)