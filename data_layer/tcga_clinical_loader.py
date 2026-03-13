import pandas as pd

class TCGAClinicalLoader:

    def __init__(self, filepath):
        self.filepath = filepath

    def load(self):

        df = pd.read_csv(
            self.filepath,
            sep="\t",
            comment="#"
        )

        return df