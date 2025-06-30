"""
Pertenece a la Fase 3: Recuperación Semántica (Subfase: Llamada al LLM)

Módulo encargado de interactuar con el LLM (Azure OpenAI o Vertex AI) y obtener una respuesta a partir de un prompt.
"""

import os 
from dotenv import load_dotenv 
from colorama import Fore as Fr
from openai import AzureOpenAI
from pathlib import Path



# Cargar las variables del entorno 
load_dotenv()
LLM_PROVIDER = os.getenv('LLM_PROVIDER', "azure")


if LLM_PROVIDER == "azure": 
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )

    # DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME") # gpt-4o-mini-2

    DEPLOYMENT_NAME = "gpt-4o-mini-2" 
    
    def ask_llm(prompt: str) -> str:
        print(Fr.LIGHTBLACK_EX + "[✓] Llamando al modelo de Azure OpenAI..." + Fr.RESET)

        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=512,
        )

        return response.choices[0].message.content.strip()

elif LLM_PROVIDER == "google":
    from vertexai.language_models import ChatModel, InputOutputTextPair
    import vertexai

    vertexai.init(
        project=os.environ["GOOGLE_PROJECT_ID"],
        location=os.environ["GOOGLE_LOCATION"]
    )

    chat_model = ChatModel.from_pretrained("chat-bison")

    def ask_llm(prompt: str) -> str:
        print(Fr.YELLOW + "[✓] Llamando al modelo de Vertex AI (Gemini/PaLM)..." + Fr.RESET)

        chat = chat_model.start_chat(
            context="Eres un experto en seguros. Responde de forma clara, profesional y concisa."
        )

        response = chat.send_message(prompt, temperature=0.3, max_output_tokens=600)
        return response.text.strip()

else:
    raise ValueError(f"[Error.llm_answerer] Proveedor de LLM no soportado: {LLM_PROVIDER}")    
