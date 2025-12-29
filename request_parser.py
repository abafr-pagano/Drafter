from pydantic import BaseModel


class RequestParser(BaseModel):
    prompt: str
