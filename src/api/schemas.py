from decimal import Decimal
from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, Field


def cast_if_str(response_time: int | str | None):
    if isinstance(response_time, str):
        return int(response_time)
    
    return response_time

def to_camel_case(field: str) -> str:
    field_split = field.split("_")
    return field_split[0] + "".join(word.capitalize() for word in field_split[1:])



class Metric(BaseModel):
    service_name: str | None
    path: str | None
    response_time: int | None

    model_config = ConfigDict(alias_generator=to_camel_case, populate_by_name=True, from_attributes=True)


class MetricCreate(Metric):
    service_name: str
    path: str
    response_time: Annotated[int | str | None, AfterValidator(cast_if_str)]


class MetricResponse(BaseModel):
    path: str
    average: Decimal
    min_response: int = Field(alias="min")
    maximun_response: int = Field(alias="max")
    p99: bool | None = None
