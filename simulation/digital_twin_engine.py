import numpy as np
import pandas as pd

class DigitalTwinEngine:

    def simulate_tumor_growth(self, mutations, therapy):

        time = np.arange(0, 24, 1)

        base_growth = 1.05

        therapy_effect = 0.85

        tumor_size = []

        size = 1

        for t in time:

            if therapy:

                size = size * base_growth * therapy_effect
            else:
                size = size * base_growth

            tumor_size.append(size)

        df = pd.DataFrame({
            "month": time,
            "tumor_size": tumor_size
        })

        return df