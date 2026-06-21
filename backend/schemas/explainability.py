from pydantic import BaseModel


class ExplainabilityRequest(BaseModel):
    city: str
