import copy
import options


class LLMPrompt:
    def __init__(self):
        self.name = ""
        self.sys_prompt = ""
        self.user_prompt = ""
        self.temperature = options.LLM_LOCAL_DEFAULT_TEMPERATURE
        self.context_window = options.LLM_DEFAULT_CONTEXT_WINDOW
        self.model = options.LLM_LOCAL_DEFAULT_TEXT_MODEL
        self.stream = False

    def copy(self):
        return copy.deepcopy(self)

    def get_messages(self) -> list:
        return [
            {
                "role": "system",
                "content": self.sys_prompt or "Rispondi in modo sintetico.",
            },
            {"role": "user", "content": self.user_prompt},
        ]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return (
            f"LLMPrompt("
            f"name='{self.name}', "
            f"model='{self.model}', "
            f"temperature={self.temperature}, "
            f"context_window={self.context_window}, "
            f"stream={self.stream}"
            f")"
        )
