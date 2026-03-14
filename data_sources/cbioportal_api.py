import requests
import pandas as pd


class CBioPortalAPI:

    def __init__(self):

        self.url="https://www.cbioportal.org/api/mutations"

    def get_mutations(self):

        params={
            "molecularProfileId":"brca_tcga_mutations",
            "sampleListId":"brca_tcga_all",
            "projection":"DETAILED"
        }

        headers={
            "Accept":"application/json"
        }

        try:

            r=requests.get(self.url,params=params,headers=headers)

            if r.status_code!=200:
                return pd.DataFrame()

            data=r.json()

            df=pd.DataFrame(data)

            return df

        except:

            return pd.DataFrame()