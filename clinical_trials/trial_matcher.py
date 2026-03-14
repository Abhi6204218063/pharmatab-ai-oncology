import requests
import pandas as pd


class TrialMatcher:

    def search_trials(self,gene):

        url="https://clinicaltrials.gov/api/query/study_fields"

        params={
        "expr":gene,
        "fields":"NCTId,Condition,BriefTitle",
        "min_rnk":1,
        "max_rnk":10,
        "fmt":"json"
        }

        r=requests.get(url,params=params)

        data=r.json()

        studies=data["StudyFieldsResponse"]["StudyFields"]

        rows=[]

        for s in studies:

            rows.append({
            "Trial ID":s["NCTId"][0],
            "Condition":",".join(s["Condition"]),
            "Title":s["BriefTitle"][0]
            })

        return pd.DataFrame(rows)