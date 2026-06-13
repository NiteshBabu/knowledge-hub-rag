from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}
