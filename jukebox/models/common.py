from pydantic import BaseModel, BaseConfig


class JBModel(BaseModel):
    class Config(BaseConfig):
        pass
