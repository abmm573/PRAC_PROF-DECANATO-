from pydantic import BaseModel, Field


class PasswordResetRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=255)


class PasswordResetConfirm(BaseModel):
    token: str = Field(..., min_length=10, max_length=400)
    nueva_password: str = Field(..., min_length=6, max_length=200)

