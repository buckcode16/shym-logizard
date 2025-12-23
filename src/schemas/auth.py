from pydantic import BaseModel, ConfigDict


class LoginResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
