from datetime import datetime

import pydantic


class BaseModel(pydantic.BaseModel):
    # Any common logic to be shared by all models goes here
    pass


class DateTimeModelMixin(BaseModel):
    created_at: datetime
    updated_at: datetime

    @pydantic.validator('created_at', 'updated_at', pre=True)
    def default_datetime(cls, value: datetime) -> datetime:  # noqa
        return value or datetime.now()


class IDModelMixin(BaseModel):
    id: int
