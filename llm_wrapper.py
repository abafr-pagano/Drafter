import httpx
from llm_prompt import LLMPrompt
import options


class LLM_Wrapper:
    async def request(self, prompt: LLMPrompt) -> str:
        try:
            payload = {
                "stream": prompt.stream,
                "model": prompt.model or options.LLM_LOCAL_DEFAULT_TEXT_MODEL,
                "messages": [
                    {"role": "system", "content": prompt.sys_prompt},
                    {"role": "user", "content": prompt.user_prompt},
                ],
                "options": {
                    "temperature": (
                        prompt.temperature or options.LLM_LOCAL_DEFAULT_TEMPERATURE
                    ),
                    "num_ctx": prompt.context_window
                    or options.LLM_DEFAULT_CONTEXT_WINDOW,
                },
            }

            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    options.LLM_LOCAL_URL,
                    json=payload,
                    timeout=options.LLM_REQUEST_TIMEOUT,
                )
                resp.raise_for_status()
                data = resp.json()

                # Estrazione contenuto messaggio
                return data.get("message", {}).get("content", "").strip()

        except Exception as e:
            error_msg = f"❌ Errore LLM: {str(e)}"
            print(error_msg)
            return error_msg
