#!/usr/bin/env python3
"""Script para buscar dados da API DONKI (GST) da NASA."""
import os, sys, json, logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import requests
from dotenv import load_dotenv
from supabase import create_client
import colorlog

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter('%(log_color)s%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
logger = colorlog.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

load_dotenv()
NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
DATA_DIR = "data"
SAMPLE_FILE = os.path.join(DATA_DIR, "sample_gst.json")
OUTPUT_FILE = os.path.join(DATA_DIR, "gst_latest.json")

def get_date_range(days: int = 30):
    end = datetime.utcnow()
    start = end - timedelta(days=days)
    return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")

def fetch_from_api(start_date: str, end_date: str) -> Optional[List[Dict]]:
    url = "https://api.nasa.gov/DONKI/GST"
    params = {"startDate": start_date, "endDate": end_date, "api_key": NASA_API_KEY}
    try:
        logger.info(f"Buscando dados de {start_date} a {end_date}...")
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Recebidos {len(data)} eventos.")
        return data
    except requests.exceptions.Timeout:
        logger.error("Timeout ao conectar com a API.")
        return None
    except requests.exceptions.HTTPError as e:
        logger.error(f"Erro HTTP: {e}")
        return None
    except Exception as e:
        logger.error(f"Erro na requisição: {e}")
        return None

def deduplicar(eventos: List[Dict]) -> List[Dict]:
    vistos = set()
    unicos = []
    for ev in eventos:
        gst_id = ev.get("gstID")
        if gst_id and gst_id not in vistos:
            vistos.add(gst_id)
            unicos.append(ev)
    logger.info(f"Deduplicação: {len(eventos)} -> {len(unicos)} eventos únicos.")
    return unicos

def save_json(data: List[Dict], filepath: str) -> bool:
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Dados salvos em {filepath}")
        return True
    except Exception as e:
        logger.error(f"Erro ao salvar JSON: {e}")
        return False

def load_sample() -> Optional[List[Dict]]:
    try:
        with open(SAMPLE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning("Arquivo de exemplo não encontrado.")
        return None
    except json.JSONDecodeError:
        logger.error("Erro ao decodificar JSON de exemplo.")
        return None

def send_to_supabase(eventos: List[Dict]) -> bool:
    if not SUPABASE_URL or not SUPABASE_KEY:
        logger.warning("Supabase não configurado. Pulando envio.")
        return False
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        for ev in eventos:
            row = {
                "gst_id": ev.get("gstID"),
                "start_time": ev.get("startTime"),
                "kp_index": ev.get("kpIndex"),
                "source": ev.get("source"),
                "created_at": datetime.utcnow().isoformat()
            }
            if row["gst_id"] is None:
                continue
            resp = supabase.table("eventos_solares").upsert(row, on_conflict="gst_id").execute()
            if hasattr(resp, 'error') and resp.error:
                logger.error(f"Erro ao inserir evento {row['gst_id']}: {resp.error}")
        logger.info("Dados enviados ao Supabase com sucesso.")
        return True
    except Exception as e:
        logger.error(f"Falha ao enviar ao Supabase: {e}")
        return False

def main():
    logger.info("Iniciando busca de tempestades geomagnéticas (GST)")
    os.makedirs(DATA_DIR, exist_ok=True)
    start_date, end_date = get_date_range(30)
    dados = fetch_from_api(start_date, end_date)
    if dados is None:
        logger.warning("Falha na API. Tentando usar dados de exemplo.")
        dados = load_sample()
        if dados is None:
            logger.critical("Não foi possível obter dados nem da API nem do sample.")
            sys.exit(1)
    dados_unicos = deduplicar(dados)
    if not save_json(dados_unicos, OUTPUT_FILE):
        logger.critical("Falha ao salvar JSON.")
        sys.exit(1)
    if not send_to_supabase(dados_unicos):
        logger.warning("Falha no envio para Supabase (continuando).")
    logger.info("Script finalizado com sucesso.")
    sys.exit(0)

if __name__ == "__main__":
    main()
