import json
import pathlib
import re
from llm_prompt import LLMPrompt
import options


class PromptParser:
    def __init__(self, force_reload: bool = False):
        self.base_dir = pathlib.Path(__file__).parent
        self.prompts_dir = self.base_dir / options.PROMPTS_SUBDIR
        self.start_delim = options.REQUEST_KEY_TAGS["start"]
        self.end_delim = options.REQUEST_KEY_TAGS["end"]
        self.tag_pattern = re.compile(
            rf"{re.escape(self.start_delim)}(.*?){re.escape(self.end_delim)}"
        )

        self.reload_prompts = force_reload
        self.prompts = {}

    def load_prompts(self) -> None:
        """
        Forza la lettura del disco e popola la cache.
        """
        if not self.prompts_dir.exists():
            self.prompts_dir.mkdir(parents=True, exist_ok=True)

        # Svuotiamo la cache prima di ricaricare
        new_prompts = {}
        for json_file in self.prompts_dir.glob("*.json"):
            tag_key = json_file.stem.replace(".", "::")

            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    prompt = LLMPrompt()
                    prompt_data = json.load(f)

                    prompt.name = tag_key
                    prompt.temperature = prompt_data.get(
                        "temperature", options.LLM_LOCAL_DEFAULT_TEMPERATURE
                    )
                    prompt.model = prompt_data.get(
                        "model", options.LLM_LOCAL_DEFAULT_TEXT_MODEL
                    )
                    prompt.stream = prompt_data.get("stream", False)
                    prompt.sys_prompt = prompt_data.get("sys_prompt", "")
                    prompt.context_window = prompt_data.get(
                        "context_window", options.LLM_DEFAULT_CONTEXT_WINDOW
                    )
                    sys_prompt_file = json_file.with_suffix(".prompt.md")

                    if sys_prompt_file.exists():
                        prompt.sys_prompt = sys_prompt_file.read_text(
                            encoding="utf-8"
                        ).strip()

                    if not prompt.sys_prompt:
                        prompt.sys_prompt = options.LLM_DEFAULT_SYS_PROMPT

                    new_prompts[tag_key] = prompt
                    print(f"📦 [Parser] Cache aggiornata per: {tag_key}")

            except Exception as e:
                print(f"⚠️ [Parser] Errore caricamento {json_file.name}: {e}")

        self.prompts = new_prompts
        self._ensure_default_prompt()

    def _ensure_default_prompt(self) -> None:
        """
        Verifica la presenza del tag di default.
        Se manca, lo crea usando i valori di options.py.
        """
        default_key = options.LLM_DEFAULT_PROMPT_KEY

        if default_key not in self.prompts:
            print(
                f"🛡️ [Parser] Tag '{default_key}' non trovato. Creo fallback di emergenza."
            )

            default_prompt = LLMPrompt()
            default_prompt.name = "Default Emergency Prompt"
            default_prompt.sys_prompt = options.LLM_DEFAULT_SYS_PROMPT
            default_prompt.model = options.LLM_LOCAL_DEFAULT_TEXT_MODEL
            default_prompt.temperature = options.LLM_LOCAL_DEFAULT_TEMPERATURE
            default_prompt.stream = False

            self.prompts[default_key] = default_prompt

    def get_prompt(self, request_text) -> LLMPrompt:
        """
        Se la cache è vuota, carica i prompt. Poi estrae il tag e restituisce la config.
        """

        if not self.prompts or self.reload_prompts:
            print("🚀 [Parser] Cache vuota, avvio primo caricamento...")
            self.load_prompts()

        match = self.tag_pattern.search(request_text)

        if match:
            tag_found = match.group(1).strip()
            user_prompt_text = request_text.replace(match.group(0), "").strip()
        else:
            tag_found = "default::default"
            user_prompt_text = request_text.strip()

        selected_prompt = self.prompts.get(tag_found)
        assert selected_prompt is not None, f"⚠️ [Parser] Tag non trovato: {tag_found}"

        retVal = selected_prompt.copy()
        retVal.user_prompt = user_prompt_text
        return retVal
