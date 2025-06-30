import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import json
from pathlib import Path
from dotenv import load_dotenv
import numpy as np
import faiss
from colorama import Fore as Fr
from openai import AzureOpenAI




# -----------------------------
# Cargar la indexacion FAISS de los embeddings 
# -----------------------------

INDEX_PATH = Path("data/faiss_index/index.faiss")
META_PATH = Path("data/faiss_index/index_meta.json")
EMBEDDINGS_PATH = Path("data/embeddings.npy")

def load_faiss_index():
    if not INDEX_PATH.exists():
        raise FileNotFoundError(f"indice FAISS no encontrado en: {INDEX_PATH.resolve()}")
    
    if not META_PATH.exists():
        raise FileNotFoundError(f"Metadatos no encontrados en: {META_PATH.resolve()}")

    if not EMBEDDINGS_PATH.exists():
        raise FileNotFoundError(f"Embeddings no encontrados en: {EMBEDDINGS_PATH.resolve()}")

    # Cargar índice FAISS
    index = faiss.read_index(str(INDEX_PATH))

    # Cargar metadatos
    with open(META_PATH, "r", encoding="utf-8") as f:
        metadatos = json.load(f)

    # Cargar embeddings (por si se necesitan para validación u otros fines)
    embeddings = np.load(EMBEDDINGS_PATH)

    return index, metadatos, embeddings
