"""
Script para probar la recuperación semántica de chunks similares usando FAISS.
Pertenece a la Fase 3: Recuperación (Retriever).
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.rag.retriever import search_similar_chunks
from colorama import Fore as Fr



if __name__ == "__main__": 
    print(Fr.CYAN + "\n Agente RAG - Recuperador Semántico" + Fr.RESET)

    try:
        while True:
            query = input(Fr.YELLOW + "\n[Usuario] Ingresa tu pregunta (o escribe 'exit' para salir): " + Fr.RESET)
            if query.strip().lower() == "exit":
                print(Fr.GREEN + "Hasta luego. Cerrando Retriever...\n" + Fr.RESET)
                break

            resultados = search_similar_chunks(query)

            print(Fr.MAGENTA + f"\n[✓] Se recuperaron {len(resultados)} chunks:\n" + Fr.RESET)
            for i, chunk in enumerate(resultados, start=1):
                print(f"{Fr.BLUE}({i}) Fuente: {chunk.get('source')} - Página/Párrafo/Línea: {chunk.get('page')}{Fr.RESET}")
                print(f"{chunk.get('content_preview')}\n{'-'*60}")


    except KeyboardInterrupt:
        print(Fr.GREEN + "\n\n[✓] Finalizado por el usuario.\n" + Fr.RESET)
