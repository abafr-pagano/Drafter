LLM_LOCAL_URL = "http://localhost:11434/api/chat"
LLM_LOCAL_DEFAULT_TEMPERATURE = 0.3
LLM_LOCAL_DEFAULT_TEXT_MODEL = "llama3.1:8b"
LLM_LOCAL_DEFAULT_CODE_MODEL = "qwen2.5-coder:16b"
LLM_DEFAULT_SYS_PROMPT = "Sei un assistente utile e professionale."
LLM_DEFAULT_PROMPT_KEY = "default::default"
LLM_DEFAULT_CONTEXT_WINDOW = 2048
LLM_REQUEST_TIMEOUT = 60  # seconds

REQUEST_KEY_TAGS = {"start": "{{", "end": "}}"}
PROMPTS_SUBDIR = "prompts"
