"""
El modulo es parte de la Fase 2: **Embeddings e Indexación Semantica** 

Genera los indeces de los embeddings usando el método FAISS. Toma la distancia euclideana de cada vector 

"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import numpy as np 
import faiss 
from pathlib import Path
from colorama import Fore as Fr


# ------------------------------
# Rutas de archivos requeridos
# ------------------------------

EMBEDDINGS_PATH = Path("data/embeddings.npy")
INDEX_PATH = Path("data/faiss_index/index.faiss")
INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)


# -----------------------------
# Cargar los embeddings
# ------------------------------

def load_embeddings() -> np.ndarray: 
    if not EMBEDDINGS_PATH.exists(): 
        raise FileNotFoundError(f"[Error] No se encontró embeddings.npy en {EMBEDDINGS_PATH.resolve()}")

    embeddings = np.load(EMBEDDINGS_PATH)
    print(Fr.GREEN + f"[✓] {len(embeddings)} vectores cargados desde {EMBEDDINGS_PATH}" + Fr.RESET)
    return embeddings.astype("float32") # Faiss requiere el float32

# -----------------------------
# Crear el indice FAISS
# -----------------------------

def create_faiss_index(embeddings: np.ndarray) -> faiss.IndexFlatL2: 

    # IndexFlat2 es el algoritmo con el que se construiran los indices, 
    # Este tomará la distancia euclideana de los vectores

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim) # Dist Euclideana 
    index.add(embeddings)
    print(Fr.BLUE + f"[✓] Índice FAISS construido con {index.ntotal} vectores." + Fr.RESET)
    return index

# -----------------------------
# Guardar el indice 
# -----------------------------

def save_index(index: faiss.Index, path: Path): 
    faiss.write_index(index, str(path))
    print(Fr.YELLOW + f"[↓] Índice guardado en {path.resolve()}" + Fr.RESET)


# -----------------------------
# Indexacion Semántica
# -----------------------------

if __name__ == '__main__': 
    print(Fr.CYAN + "[...] Iniciando construcción del índice FAISS..." + Fr.RESET)
    # Cargar los embeddings 
    embeddings = load_embeddings()
    # Generar los indices FAISS con el algoritmo FlatL2 de cada embeddings 
    index = create_faiss_index(embeddings)
    # Guardar los indices FAISS de los embeddings 
    save_index(index, INDEX_PATH)