from pydantic import BaseModel, EmailStr

class UserData(BaseModel):
    id: int
    email: EmailStr
    role: str