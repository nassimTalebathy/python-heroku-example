from pydantic import BaseModel, validator, Field
import numpy as np
from typing import List

try:
    import src.config as config
except:
    import config


class DataInput(BaseModel):
    array: List[List[float]]
    verbose: bool = False

    class Config:
        arbitrary_types_allowed = True

    @validator("array", pre=True, allow_reuse=True)
    def validate_array(array: List[float] | List[List[float]]):
        assert len(array) > 0, "Array must have at least one element"
        if isinstance(array[0], float):
            array = [array]
        for el in array:
            assert len(el) == config.NUM_COLS, f"Must have {config.NUM_COLS} columns"
        return array

    def to_np_array(self) -> np.ndarray:
        return np.vstack(self.array, dtype=np.float64)


class DataOutput(BaseModel):
    predictions: List[float] = Field(..., min_items=1)
    start_time: float
    time_taken: float = Field(..., gt=0)
