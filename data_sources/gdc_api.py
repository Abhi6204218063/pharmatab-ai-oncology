import requests
import pandas as pd


class GDCAPI:

    BASE_URL = "https://api.gdc.cancer.gov"

    def get_cases(self):

        url = f"{self.BASE_URL}/cases"

        params = {
            "size": 100,
            "format": "JSON"
        }

        response = requests.get(url, params=params)

        data = response.json()

        hits = data["data"]["hits"]

        df = pd.json_normalize(hits)

        return df