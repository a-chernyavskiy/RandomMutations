from typing import NamedTuple, Any

import numpy as np


class Status(NamedTuple):
    iteration: int
    time: int
    last_best_f: float
    stall: int
    n_stall: int
    fevals: int
    i: int = None
    n: int = None
    callback_result: Any = None

