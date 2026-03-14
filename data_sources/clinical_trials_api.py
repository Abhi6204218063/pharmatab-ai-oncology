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