import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import RobustScaler

class LogisticModel:
    def __init__(self, random_state=23):
        self.scaler = RobustScaler()
        self.model = LogisticRegression(max_iter=4000, random_state=random_state)
        self.constant_ = None

    def fit(self, X, y):
        y = np.asarray(y, dtype=int)
        if len(np.unique(y)) < 2:
            self.constant_ = float(y.mean()) if len(y) else 0.0
            return self
        self.scaler.fit(X)
        self.model.fit(self.scaler.transform(X), y)
        return self

    def predict_proba(self, X):
        if self.constant_ is not None:
            return np.full(len(X), self.constant_)
        return self.model.predict_proba(self.scaler.transform(X))[:,1]

class BaseRateModel:
    def fit(self, X, y):
        self.p_ = float(np.mean(y))
        return self
    def predict_proba(self, X):
        return np.full(len(X), self.p_, dtype=float)

def inventory_feature(df, node_prefixes):
    vals = []
    for n in node_prefixes:
        inv = df[f"{n}_inventory"].astype(float)
        dem = df[f"{n}_demand"].astype(float)
        vals.append((dem-inv).clip(lower=0))
    return pd.DataFrame({"inventory_deficit": pd.concat(vals,axis=1).mean(axis=1)})

def backlog_feature(df, node_prefixes):
    vals = [df[f"{n}_backlog"].astype(float) for n in node_prefixes]
    return pd.DataFrame({"backlog": pd.concat(vals,axis=1).mean(axis=1)})

def degree_weighted_exposure(df, edges, node_prefixes):
    degree = {n:0.0 for n in node_prefixes}
    for _,r in edges.iterrows():
        if r["source"] in degree:
            degree[r["source"]] += float(r.get("weight",1.0))
        if r["target"] in degree:
            degree[r["target"]] += float(r.get("weight",1.0))
    total = sum(degree.values()) or 1.0
    score = pd.Series(0.0,index=df.index)
    for n in node_prefixes:
        local = (
            df[f"{n}_backlog"].astype(float).rank(pct=True)
            + df[f"{n}_lead_time"].astype(float).rank(pct=True)
        )/2.0
        score += local*(degree[n]/total)
    return pd.DataFrame({"degree_weighted_exposure":score})
