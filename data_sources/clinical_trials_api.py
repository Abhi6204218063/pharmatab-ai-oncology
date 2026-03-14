import requests
import pandas as pd


class ClinicalTrialsAPI:

    BASE_URL = "https://clinicaltrials.gov/api/query/study_fields"

    def search_trials(self, condition="lung cancer"):

        params = {
            "expr": condition,
            "fields": "NCTId,Condition,InterventionName,Phase",
            "min_rnk": 1,
            "max_rnk": 50,
            "fmt": "json"
        }

        response = requests.get(self.BASE_URL, params=params)

        data = response.json()

        studies = data["StudyFieldsResponse"]["StudyFields"]

        df = pd.json_normalize(studies)

        return df
    
        st.markdown("""
        Clinical trials allow patients to access experimental therapies that may not yet be widely available.

        This tool searches the ClinicalTrials.gov database to identify trials related
        to the specified cancer type.

        Researchers can explore potential treatment strategies and emerging therapies.
        """)