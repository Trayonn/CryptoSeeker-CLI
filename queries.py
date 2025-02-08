import requests
import yaml
import os
from datetime import datetime, timedelta, time

config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')

cache = {"data": None, "last_update": None}

def config():
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config




def listar_moeda():
    global cache
    agora = datetime.now()

    if cache["last_update"] and (agora - cache["last_update"]) < timedelta(minutes=5):
        return cache["data"]

    API_ENDPOINT = r'/coins/markets?vs_currency=usd'
    url = f"{config()['url_api']}" + API_ENDPOINT

    try:
        response = requests.get(url)

        if response.status_code == 429:
            print("⚠️ Muitas requisições! Esperando 60 segundos...")
            time.sleep(60)
            return listar_moeda()

        response.raise_for_status()
        data = response.json()

        if isinstance(data, list):
            cache["data"] = [{"id": i["id"], "symbol": i["symbol"], "name": i["name"]} for i in data]
            cache["last_update"] = datetime.now()
            return cache["data"]
        else:
            print(f"Erro inesperado: resposta da API não é uma lista. Resposta: {data}")
            return []
    
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return []


def moeda_preco(moeda, moeda_corrente):
    API_ENDPOINT = r'simple/price?'
    filters = f'ids={moeda}&vs_currencies={moeda_corrente}' 

    url = f"{config()['url_api']}" + API_ENDPOINT + filters

    response = requests.get(url)

    return response.json()


def informacao_moeda(moeda, moeda_corrente):
    API_ENDPOINT = r'simple/price?'
    filters = f'ids={moeda}&vs_currencies={moeda_corrente}&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true'  #Se quiser buscar pelo ID botar ids no lugar de symbols

    url = f"{config()['url_api']}" + API_ENDPOINT + filters

    response = requests.get(url)

    return response.json()


