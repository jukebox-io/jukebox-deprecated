from datetime import datetime

from pydantic import BaseModel, validator


class ResourceBase(BaseModel):
    # Any common logic to be shared by all models goes here
    class Config:
        orm_mode = True


class DateTimeModelMixin(ResourceBase):
    # Adds created-at and updated-at fields and validators to the given model
    created_at: datetime
    updated_at: datetime

    @validator('created_at', 'updated_at', pre=True)
    def default_datetime(cls, value: datetime) -> datetime:  # noqa
        return value or datetime.now()


class IDModelMixin(ResourceBase):
    # Adds ID field to the given model
    id: int
