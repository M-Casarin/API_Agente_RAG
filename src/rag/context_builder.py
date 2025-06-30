"""
Este módulo forma parte de la Fase 3: Generación de Respuestas (RAG)

Objetivo:
    - Construir el contexto plano que será enviado al LLM, 
      a partir de los chunks recuperados por el retriever.
"""

from typing import List
import os 
from dotenv import load_dotenv 
from colorama import Fore as Fr
from openai import AzureOpenAI
from pathlib import Path
import textwrap


LLM_PROMPT_INICIAL = Path("assets/prompt_llm_agente.txt")

def load_inicial_prompt(): 
    if not LLM_PROMPT_INICIAL.exists(): 
        raise FileNotFoundError(f"[Error.load_inicial_prompt] No existe el archivo: {LLM_PROMPT_INICIAL.resolve()}")
    with open(LLM_PROMPT_INICIAL, "r", encoding="utf-8") as file: 
        prompt_inicial = file.read()
    return prompt_inicial


def build_context_prompt(chunks: list[dict], pregunta: str) -> str:
    """
    Construye un prompt concatenando los chunks relevantes y añadiendo la pregunta del usuario.
    """

    # Concatenar los contenidos de los chunks
    contexto = ""
    for i, chunk in enumerate(chunks, start=1):
        fuente = chunk.get("source", "desconocido")
        ubicacion = chunk.get("page", chunk.get("paragraph", chunk.get("line", "?")))
        texto = chunk["content_preview"]
        contexto += f"\n[{i}] Fuente: {fuente} - Ubicación: {ubicacion}\n{texto}\n"

    # Prompt tipo Sage
    prompt =textwrap.dedent(f"""
        {load_inicial_prompt()}
        ### CONTEXTO
        {contexto}

        ### PREGUNTA
        {pregunta}

        ### RESPUESTA
    """).strip()

    return prompt.strip()
