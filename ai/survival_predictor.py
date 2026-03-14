import pandas as pd
from sklearn.linear_model import LogisticRegression


class SurvivalPredictor:

    def train_model(self,df):

        if "OS_MONTHS" not in df.columns:
            return None

        X=df.select_dtypes(include="number").fillna(0)

        y=(df["OS_MONTHS"]>24).astype(int)

        model=LogisticRegression()

        model.fit(X,y)

        return model


    def predict(self,model,patient):

        pred=model.predict(patient)

        return pred