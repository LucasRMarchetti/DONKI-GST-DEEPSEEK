#!/usr/bin/env python3
"""Exporta dados do Supabase para sample_gst.json."""
import os, json
from dotenv import load_dotenv
from supabase import create_client
import colorlog

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter('%(log_color)s%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
logger = colorlog.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel("INFO")

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def export_to_json():
    if not SUPABASE_URL or not SUPABASE_KEY:
        logger.error("Variáveis do Supabase não configuradas.")
        return
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    resp = supabase.table("eventos_solares").select("*").execute()
    if hasattr(resp, 'error') and resp.error:
        logger.error(f"Erro ao buscar dados: {resp.error}")
        return
    eventos = []
    for row in resp.data:
        eventos.append({
            "gstID": row["gst_id"],
            "startTime": row["start_time"],
            "kpIndex": row["kp_index"],
            "source": row["source"]
        })
    with open("data/sample_gst.json", "w", encoding="utf-8") as f:
        json.dump(eventos, f, indent=2, ensure_ascii=False)
    logger.info("Exportado sample_gst.json com sucesso.")

if __name__ == "__main__":
    export_to_json()
