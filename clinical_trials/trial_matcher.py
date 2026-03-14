import requests
import pandas as pd


class TrialMatcher:

    def __init__(self):
        self.base_url = "https://clinicaltrials.gov/api/v2/studies"


    def search_trials(self, condition):

        params = {
            "query.term": condition,
            "pageSize": 20
        }

        try:

            response = requests.get(self.base_url, params=params)

            if response.status_code != 200:
                return pd.DataFrame()

            try:
                data = response.json()
            except:
                return pd.DataFrame()

            studies = data.get("studies", [])

            trials = []

            for study in studies:

                try:

                    protocol = study.get("protocolSection", {})

                    identification = protocol.get("identificationModule", {})
                    status = protocol.get("statusModule", {})
                    conditions = protocol.get("conditionsModule", {})
                    design = protocol.get("designModule", {})

                    title = identification.get("briefTitle", "NA")

                    nct = identification.get("nctId", "NA")

                    trial_status = status.get("overallStatus", "NA")

                    cond = conditions.get("conditions", ["NA"])

                    phase = design.get("phases", ["NA"])

                    trials.append({
                        "NCT_ID": nct,
                        "Title": title,
                        "Condition": ", ".join(cond),
                        "Phase": ", ".join(phase),
                        "Status": trial_status,
                        "Link": f"https://clinicaltrials.gov/study/{nct}"
                    })

                except:
                    continue

            df = pd.DataFrame(trials)

            return df

        except Exception as e:

            print("Clinical trial API error:", e)

            return pd.DataFrame()