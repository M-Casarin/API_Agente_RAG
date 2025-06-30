"""
Script para probar la recuperación semántica de chunks similares usando FAISS.
Pertenece a la Fase 3: Recuperación (Retriever).
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.rag.context_builder import build_context_prompt
from src.rag.retriever import search_similar_chunks
from src.rag.ask_llm import ask_llm
from colorama import Fore as Fr



def main():
    while True:
        pregunta = input(Fr.CYAN + "[Usuario] Ingresa tu pregunta (o escribe 'exit' para salir): " + Fr.RESET).strip()
        if pregunta.lower() in ("exit", "salir"):
            break

        # 1. Recuperar chunks relevantes
        chunks = search_similar_chunks(pregunta)
        print(Fr.GREEN + f"\n[✓] Se recuperaron {len(chunks)} chunks:\n" + Fr.RESET)
        for i, c in enumerate(chunks, start=1):
            print(f"({i}) Fuente: {c['source']} - Página/Párrafo/Línea: {c.get('page', '?')}")
            print(c["content_preview"])
            print("-" * 60)

        # 2. Construir prompt con contexto
        prompt = build_context_prompt(chunks, pregunta)

        # 3. Llamar al LLM (Azure o Google) para obtener respuesta
        respuesta = ask_llm(prompt)

        print(Fr.MAGENTA + "\n[Respuesta del LLM]\n" + "-" * 30)
        print(respuesta + Fr.RESET)
        print("\n\n")


if __name__ == "__main__":
    main()