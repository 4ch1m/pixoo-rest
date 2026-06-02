from pydantic import BaseModel


class PassthroughModel(BaseModel):
    route_path: str
    payload_filename: str
    description: str
