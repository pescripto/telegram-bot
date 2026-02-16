import time
import os
from asyncio import print_call_graph

import feedparser
import requests
from bs4 import BeautifulSoup

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
def extrair_imagem(entry)
    if hasattr(entry, "media_content"):
        try:
            return entry.media_content[0]["url"]
        except:
            pass
        try:
            r = requests.get(entry.link, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            og = soup.find("meta", property="og:image")
            if og and og.get("content")
                return og["content"]
        except:
            pass
        return None

def carregar_historico():
    if os.path.exists(ARQUIVO_HISTORICO):
        with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as f:
            return set(f.read().splitlines())
    return set()

def salvar_historico(historico):
    with open(ARQUIVO_HISTORICO, "w", encoding="utf-8") as f:
        for link in historico:
            f.write(link + "\n")

def enviar_texto(mensagem):
    url = f"https://api.telegram.org/bot{8546136873:AAFVTHt_HKorMqW3lksLwnvyKFEpOJAmmWI}/sendMessage"
    payload = {
        "chat_id": -1002997050739,
        "message_thread_id": 9,
        "text": mensagem,
        "disable_web_page_preview": True
    }
    requests.post(url, data=payload, timeout=10)


def enviar_com_imagem(titulo, link, image_url):
    url = f"https://api.telegram.org/bot{AAFVTHt_HKorMqW3lksLwnvyKFEpOJAmmWI}/sendPhoto"
    payload = {
        "chat_id": -1002997050739,
        "message_thread_id": 9,
        "photo": image_url,
        "caption": f"📰 {titulo}\n{link}"
    }
    requests.post(url, data=payload, timeout=10)

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
                imagem = extrair_imagem(entry)

                if imagem:
                    enviar_com_imagem(titulo, entry.link, imagem)
                else:
                    enviar_texto(f"📰 {titulo}\n{entry.link}")
                historico.add(entry.link)
                salvar_historico(historico)

                time.sleep(10)  # pequeno delay entre mensagens

        print("⏸ Aguardando próximo ciclo")
    except Exception as e:
        print("Erro controlado:", e)

    time.sleep(DELAY)