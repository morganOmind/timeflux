"""timeflux.core.io: lightweight i/o wrapper"""

import datetime
import numpy as np
import pandas as pd
from timeflux.core.registry import Registry

class Port:

    def __init__(self, persistant=False):
        self.persistant = persistant
        self.clear()

    def clear(self):
        if not self.persistant:
            self.data = None
            self.meta = {}

    def ready(self):
        return self.data is not None and not self.data.empty

    def set(self, rows, timestamps=None, names=None):
        if timestamps is None:
            rate = 1 if Registry.rate == 0 else Registry.rate
            stop = int(Registry.cycle_start * 1e6)
            start = stop - int(1e6 / rate)
            timestamps = np.linspace(start, stop, len(rows), False, dtype='datetime64[us]')
        self.data = pd.DataFrame(rows, index=timestamps, columns=names)
