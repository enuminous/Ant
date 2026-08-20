import json
import pandas as pd
from ant import ANTExperiment

nodes=pd.read_csv("example_nodes.csv")
edges=pd.read_csv("example_edges.csv")

exp=ANTExperiment(
    time_column="time",
    target_column="failure",
    node_prefixes=["A","B","C","D","E"],
    horizons=(3,7,23),
    random_state=23,
)

result=exp.run(nodes,edges)
print(json.dumps(result,indent=2))
