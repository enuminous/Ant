from dataclasses import dataclass
import pandas as pd

from features import build_ant_features
from baselines import LogisticModel, BaseRateModel, inventory_feature, backlog_feature, degree_weighted_exposure
from metrics import binary_metrics, stratify

@dataclass
class ANTExperiment:
    time_column: str
    target_column: str
    node_prefixes: list
    horizons: tuple = (3,7,23)
    train_fraction: float = 0.65
    random_state: int = 23

    def run(self, df, edges):
        df = df.sort_values(self.time_column).reset_index(drop=True).copy()
        cut=max(20,int(len(df)*self.train_fraction))
        y=df[self.target_column].astype(int).to_numpy()

        af=build_ant_features(df,edges,self.node_prefixes,self.horizons)

        raw_cols=[]
        for n in self.node_prefixes:
            raw_cols += [
                f"{n}_inventory",
                f"{n}_demand",
                f"{n}_backlog",
                f"{n}_lead_time",
                f"{n}_substitution",
            ]
        raw=df[raw_cols].astype(float).ffill().fillna(0.0)
        full=pd.concat([raw,af],axis=1).fillna(0.0)

        inventory=inventory_feature(df,self.node_prefixes)
        backlog=backlog_feature(df,self.node_prefixes)
        degree=degree_weighted_exposure(df,edges,self.node_prefixes)

        models={
            "ant":(LogisticModel(self.random_state),full),
            "node_only":(LogisticModel(self.random_state),raw),
            "inventory_only":(LogisticModel(self.random_state),inventory),
            "backlog_only":(LogisticModel(self.random_state),backlog),
            "degree_weighted":(LogisticModel(self.random_state),degree),
            "base_rate":(BaseRateModel(),raw),
        }

        results={}
        for name,(model,X) in models.items():
            model.fit(X.iloc[:cut],y[:cut])
            p=model.predict_proba(X.iloc[cut:])
            results[name]={
                "overall":binary_metrics(y[cut:],p),
                "by_dependency_stress":stratify(
                    y[cut:],p,af["propagation_pressure_mean"].to_numpy()[cut:]
                )
            }

        return {
            "n_total":len(df),
            "train_n":cut,
            "test_n":len(df)-cut,
            "results":results,
            "primary_delta_brier_node_minus_ant":(
                results["node_only"]["overall"]["brier"]
                - results["ant"]["overall"]["brier"]
            ),
            "interpretation":(
                "Positive delta favors ANT over the matched node-only model. "
                "Inspect whether any gain concentrates in high dependency-stress periods."
            )
        }
