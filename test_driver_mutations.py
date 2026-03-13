import pandas as pd
from ai.driver_mutation_engine import DriverMutationEngine

data = pd.read_csv(
    "data/data_mutations.txt",
    sep="\t",
    comment="#",
    low_memory=False
)

engine = DriverMutationEngine()

drivers = engine.detect(data)

print("\n===== Top Driver Mutations =====")

print(drivers)