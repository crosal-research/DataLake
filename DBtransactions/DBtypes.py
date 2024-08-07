########################################################
# Pydantic classes to exchange info with outside world,
# needed to provided the necessary data validataion
#######################################################

# import from system
from typing import Optional


# import from packages
from pydantic import BaseModel


class Series(BaseModel):
    series_id: str
    description: str
    survey_id: str
    frequency: Optional[str]
    last_update: Optional[str]


class Observation(BaseModel):
    dat: str
    valor: float
    series_id: str
