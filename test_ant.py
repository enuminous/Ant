import pandas as pd
from features import build_ant_features
from ant import ANTExperiment

NODES=["A","B","C","D","E"]

def test_features():
    nodes=pd.read_csv("example_nodes.csv")
    edges=pd.read_csv("example_edges.csv")
    af=build_ant_features(nodes,edges,NODES)
    assert len(af)==len(nodes)
    assert "ant_network_risk" in af.columns
    assert af["ant_network_risk"].between(0,1).all()

def test_experiment_runs():
    nodes=pd.read_csv("example_nodes.csv")
    edges=pd.read_csv("example_edges.csv")
    exp=ANTExperiment(
        time_column="time",
        target_column="failure",
        node_prefixes=NODES,
    )
    out=exp.run(nodes,edges)
    assert "results" in out
    assert "ant" in out["results"]
    assert "node_only" in out["results"]
