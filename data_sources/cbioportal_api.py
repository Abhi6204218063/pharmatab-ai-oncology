import requests
import pandas as pd


class CBioPortalAPI:

    BASE_URL = "https://www.cbioportal.org/api"

    def get_mutations(self):

        study = "tcga_pan_can_atlas_2018"

        endpoint = f"{self.BASE_URL}/mutations"

        params = {
            "studyId": study,
            "projection": "SUMMARY",
            "pageSize": 100
        }

        headers = {
            "accept": "application/json"
        }

        response = requests.get(
            endpoint,
            params=params,
            headers=headers
        )

        if response.status_code != 200:
            return pd.DataFrame()

        data = response.json()

        df = pd.DataFrame(data)

        if "gene" in df.columns:
            df["Hugo_Symbol"] = df["gene"].apply(
                lambda x: x.get("hugoGeneSymbol")
                if isinstance(x, dict) else None
            )

        return df