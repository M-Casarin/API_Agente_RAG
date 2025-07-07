"""
El modulo es parte de la Fase 2: **Embeddings e Indexación Semantica** 

Objetivo del modulo: 
    - Cargar los chunks de  chunks.json.
    - llamar al provedor del LLM para obtner los embeddings.
    - Guardar los vecotes en data/embeddings.npy. 
    - Guardar los metadatos paralelos en data/index_meta.json 

     
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json 
from pathlib import Path
from colorama import Fore as Fr
from dotenv import load_dotenv
import numpy as np 
# GOOGLE llm 
from vertexai.language_models import TextEmbeddingModel
import vertexai
# OpenAi 
import openai


# Directorio donde deben estar los chunks de la fase 1. 
CHUNKS_PATH = Path("data/chunks.json")


def load_chunks() -> list[dict]: 
    if not CHUNKS_PATH.exists(): 
        raise FileNotFoundError(f"[Error.load_chunks] {CHUNKS_PATH.resolve} no exist. Ejecute chunker.py primero.\nLeer Readme.md!!!")

    # Proceder a cargar cada chunk 
    with open(CHUNKS_PATH, "r", encoding="utf-8") as file: 
        chunks = json.load(file) # COrrecto formato de json 
    
    print(Fr.GREEN + f"[✓] Se cargaron {len(chunks)} chunks desde {CHUNKS_PATH}\n" + Fr.RESET)
    return chunks


# ==============================
# Funcion de embeddings que llama al provedor llm 
# ==============================

load_dotenv()
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "azure")

if LLM_PROVIDER == "google": 

    vertexai.init(
        project = os.environ["GOOGLE_PROJECT_ID"],
        location=os.environ["GOOGLE_LOCATION"]
    )

    # Hard codeando para forzar a usar el modelo del embedding 
    embedding_model = TextEmbeddingModel.from_pretrained("gemini-embedding-001")

    def get_embedding(text: str) -> list[float]: 

        text = text.strip()
        if not text: 
            return []
        return embedding_model.get_embeddings([text])[0].values
    

if LLM_PROVIDER == "azure": 

    openai.api_type = "azure"
    openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
    openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
    openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")

    def get_embedding(text:str) -> list[float]: 
        response = openai.embeddings.create(
            input=text, 
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT_EMBEDDING_NAME")
        )
        return response.data[0].embedding
    


# ==============================
# Hacer el embedding a cada uno de los chunks 
# ==============================

EMBEDDINGS_PATH = Path("data/embeddings.npy")
META_PATH = Path("data/faiss_index/index_meta.json")
META_PATH.parent.mkdir(parents=True, exist_ok=True)

def generate_embeddings():
    print(Fr.LIGHTWHITE_EX + "[...] Generando embeddings para los chunks..." + Fr.RESET)
    
    chunks = load_chunks()
    embeddings = []
    metadatos = []

    for i, chunk in enumerate(chunks, start=1):
        texto = chunk.get("content", "").strip()
        if not texto:
            continue

        vector = get_embedding(texto)
        if not vector:
            print(f"[!] Chunk vacío o sin vector: #{i}")
            continue

        embeddings.append(vector)

        # Guardamos los metadatos relevantes
        metadatos.append({
            "source": chunk.get("source"),
            "page": chunk.get("page", chunk.get("paragraph", chunk.get("line", None))),
            "content_preview": texto[:80] + "..." if len(texto) > 80 else texto
        })

        if i % 100 == 0:
            print(f"[✓] Procesados {i} chunks...")

    print(Fr.LIGHTBLACK_EX + f"├── Total de embeddings generados: {len(embeddings)}\n" + Fr.RESET)

    # Guardar .npy y metadatos
    np.save(EMBEDDINGS_PATH, np.array(embeddings))
    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(metadatos, f, ensure_ascii=False, indent=2)

    print(Fr.LIGHTBLACK_EX +f"[|] Embeddings Guardados en: {EMBEDDINGS_PATH.resolve()}")
    print(Fr.LIGHTBLACK_EX +f"[|] Index de Metadatos Guardados en: {META_PATH.resolve()}"+ Fr.RESET)



# Ejecutar para hacer los embeddings de cada chunk en chunks 
if __name__ == "__main__":
    generate_embeddings()

    

