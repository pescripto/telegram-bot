import requests
import time
import math
import logging

TOKEN = "8546136873:AAFVTHt_HKorMqW3lksLwnvyKFEpOJAmmWI"
CHAT_ID = -1002997050739
TOPIC_ID = 0

DELAY = 30
BTC_STEP = 1000
ETH_STEP = 100
HISTORICO_ARQUIVO = "niveis_alertados.txt"

logging.basicConfig(
    filename="crypto_bot.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def carregar_historico():
    try:
        with open(HISTORICO_ARQUIVO, "r", encoding="utf-8") as f:
            return set(f.read().splitlines())
    except:
        return set()

def salvar_historico(h):
    with open(HISTORICO_ARQUIVO, "w", encoding="utf-8") as f:
        for i in h:
            f.write(i + "\n")

def enviar(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "message_thread_id": TOPIC_ID,
        "text": msg,
        "disable_web_page_preview": True
    }
    try:
        r = requests.post(url, data=data, timeout=10)
        if r.ok:
            logging.info(f"Mensagem enviada: {msg}")
            print(f"Mensagem enviada: {msg}")
        else:
            logging.error(f"Erro Telegram {r.status_code} | {r.text}")
            print(f"Erro Telegram {r.status_code} | {r.text}")
    except Exception as e:
        logging.exception(f"Exceção ao enviar mensagem: {e}")
        print(f"Exceção ao enviar mensagem: {e}")

def pegar_precos():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "bitcoin,ethereum", "vs_currencies": "usd"}
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        btc = float(data["bitcoin"]["usd"])
        eth = float(data["ethereum"]["usd"])
        return btc, eth
    except Exception as e:
        logging.warning(f"Falha ao pegar preços: {e}")
        print(f"Falha ao pegar preços: {e}")
        return None, None

historico = carregar_historico()
ultimo_btc_nivel = None
ultimo_eth_nivel = None

enviar("🟢 Crypto Alert Bot iniciado")
logging.info("Crypto Alert Bot iniciado")

while True:
    try:
        btc, eth = pegar_precos()
        if btc is None or eth is None:
            time.sleep(DELAY)
            continue

        btc_nivel = math.floor(btc / BTC_STEP) * BTC_STEP
        eth_nivel = math.floor(eth / ETH_STEP) * ETH_STEP

        if ultimo_btc_nivel is None:
            ultimo_btc_nivel = btc_nivel
        if btc_nivel != ultimo_btc_nivel:
            chave = f"BTC_{btc_nivel}"
            if chave not in historico:
                emoji = "📈" if btc_nivel > ultimo_btc_nivel else "📉"
                enviar(f"{emoji} BTC rompeu ${btc_nivel:,}")
                historico.add(chave)
                salvar_historico(historico)
            ultimo_btc_nivel = btc_nivel

        if ultimo_eth_nivel is None:
            ultimo_eth_nivel = eth_nivel
        if eth_nivel != ultimo_eth_nivel:
            chave = f"ETH_{eth_nivel}"
            if chave not in historico:
                emoji = "📈" if eth_nivel > ultimo_eth_nivel else "📉"
                enviar(f"{emoji} ETH rompeu ${eth_nivel:,}")
                historico.add(chave)
                salvar_historico(historico)
            ultimo_eth_nivel = eth_nivel

    except Exception as e:
        logging.exception(f"Erro controlado: {e}")
        print(f"Erro controlado: {e}")

    time.sleep(DELAY)
