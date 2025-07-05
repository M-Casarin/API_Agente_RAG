from fastapi import FastAPI, HTTPException
from src.models.RequestRAG import QueryRequest, QueryResponse
from src.rag.retriever import search_similar_chunks
from src.rag.context_builder import build_context_prompt
from src.rag.ask_llm import ask_llm


app = FastAPI(
    title="Agente RAG", 
)

@app.get("/")
def info(): 
    return {'message': "API AGENTE RAG"}

@app.post("/consulta", response_model=QueryResponse)
def consulta_rag(data: QueryRequest): 
    try: 
        chunks = search_similar_chunks(data.question)
        if not chunks: 
            raise HTTPException(status_code=404, detail="No se encontraron coincidencias relevantes a tu consuta")
        
        prompt = build_context_prompt(chunks, data.question)
        respuesta = ask_llm(prompt=prompt)

        # context_list = [
        #     f"[{i+1}] {chunk['content_preview']} ({chunk['source']})"
        #     for i, chunk in enumerate(chunks)
        # ]

        return QueryResponse(
            question=data.question, 
            answer=respuesta, 
            # context=context_list
        )
    

    except Exception as e: 
        raise HTTPException(status_code=500, detail=str(e))
