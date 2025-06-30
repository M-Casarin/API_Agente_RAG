"""
Modulo encargado de recuperar los chunks más relevantes usando FAISS dado un query del usuario.

Pertenece a la Fase 3: Recuperación Semántica (Retriever)
"""

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
from src.indexer.embed import get_embedding  # ya manejamos proveedor (Azure/GCP)
from src.rag.load_faiss_index import load_faiss_index 


# -----------------------------
# Buscar chunks similares 
# -----------------------------


def search_similar_chunks(query: str, k: int = 8) -> list[dict]: 

    if not query.strip(): 
        raise ValueError("[Error.search_similar_chunks] la consulta esta vacia")

    # Obtener embedding del query del usuario 
    query_vector = np.array(get_embedding(query), dtype=np.float32).reshape(1, -1)
    # Cargar el indice semantico y los metadatos 
    index, metadatos, embed = load_faiss_index()
    # Buscar los k mas similares 
    distancias, indices = index.search(query_vector, k)
    resultados = []
    for idx in indices[0]:
        if idx < len(metadatos):
            resultados.append(metadatos[idx])
        else: 
            print(f"[!] indice fuera de rango: {idx}")  
    
    print(Fr.GREEN + f"[✓] Recuperados {len(resultados)} chunks relevantes para el query" + Fr.RESET)
    return resultados