import pandas as pd
from simulation.kalpan_meier_survival import KaplanMeierFitter
import matplotlib.pyplot as plt

class KaplanMeierSurvival:

    def run_analysis(self, df):

        if "OS_MONTHS" not in df.columns or "OS_STATUS" not in df.columns:
            return None

        kmf = KaplanMeierFitter()

        T = df["OS_MONTHS"]
        E = df["OS_STATUS"].apply(lambda x: 1 if "DECEASED" in str(x) else 0)

        kmf.fit(T, event_observed=E)

        fig, ax = plt.subplots()
        kmf.plot(ax=ax)

        ax.set_title("Kaplan-Meier Survival Curve")

        return fig