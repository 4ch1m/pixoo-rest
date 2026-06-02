from pydantic import BaseModel, Field


class DialListModel(BaseModel):
    dial_type: str = Field(default='Game', description='The dial type.')
    page_number: int = Field(ge=1, default=1, description='The page number. (Note: Each page contains 30 items.)')
