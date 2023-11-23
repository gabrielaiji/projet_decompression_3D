from typing import List
import numpy as np
from math import log2

def getEntropyValue(values: List[int]) -> float:
    symbols = set(values)
    nb_values = len(values)
    values = np.array(values)
    H = 0

    for symbol in symbols:
        count_s = np.count_nonzero(values == symbol)
        freq_s = count_s/nb_values
        H -= freq_s * log2(freq_s)

    return H
