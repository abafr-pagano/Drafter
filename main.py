from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from prompt_parser import PromptParser
from llm_wrapper import LLM_Wrapper
from request_parser import RequestParser
import time

import uvicorn

app = FastAPI()

# Configurazione CORS (fondamentale per Obsidian)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- INIZIALIZZAZIONE ---
# Creiamo le istanze all'avvio
# Imposta force_reload=True se vuoi che rilegga i file a ogni chiamata durante il dev
parser = PromptParser(force_reload=True)
llm = LLM_Wrapper()


@app.post("/ask")
async def chat(body: RequestParser):
    try:
        print(f"📨 Richiesta ricevuta: {body.prompt.strip()[:10]}...")
        prompt_data = body.prompt.strip()
        prompt = parser.get_prompt(prompt_data)
        print(f"🤖 Prompt generato. Inoltro a LLM")
        start = time.perf_counter()

        response_text = await llm.request(prompt)
        elapsed = time.perf_counter() - start
        print(f"🤖 tempo llm {elapsed:.2f} secondi.")

        return {"response": response_text}
    except Exception as e:
        print(f"💥 Errore critico nel server: {e}")
        return {"response": f"Errore server: {str(e)}"}


# Rotta extra per forzare il ricaricamento manuale (comoda!)
@app.get("/reload")
async def reload():
    parser.load_prompts()
    return {"status": "Cache ricaricata", "prompts": list(parser.prompts.keys())}


if __name__ == "__main__":
    # Caricamento iniziale dei prompt
    parser.load_prompts()
    print(f"🚀 Server 'Ollabot' attivo con {len(parser.prompts)} prompt pronti.")
    uvicorn.run(app, host="127.0.0.1", port=8000)
