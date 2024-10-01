from pydantic import BaseModel

class IsAuthResponse(BaseModel):
    access: bool

    class Config:
        orm_mode = True