# ANT

<!-- ENUMINOUS-NETWORK:START -->
**eNuminous network:** [All repositories](https://enuminous.github.io/EFMW/repositories.html) · [EFMW](https://enuminous.github.io/EFMW/) · [102 equations](https://github.com/enuminous/Monolithic_102_EFMW) · [165 triplets](https://enuminous.github.io/FieldSpace/) · [Zoo](https://enuminous.github.io/Tortoise/) · [Lean](https://enuminous.github.io/Aristotle-102-Monolithic-Lean/) · [Engine](https://enuminous.github.io/Archimedes-Engine/) · [Papers](https://enuminous.github.io/medium/papers-essays-index.html) · [Audit](https://github.com/enuminous/EFMW_Post156_Zoo_Audit/blob/main/portfolio/INTERLOCK_AUDIT.md)

[Repository](https://github.com/enuminous/Ant) · This repository is linked through its source; GitHub Pages is not enabled.

<details>
<summary>Recent repositories (9)</summary>

- [Oroboros](https://github.com/enuminous/Oroboros) · [README](https://github.com/enuminous/Oroboros/blob/main/README.md) · [Page](https://enuminous.github.io/Oroboros/)
- [P-NP](https://github.com/enuminous/P-NP) · [README](https://github.com/enuminous/P-NP/blob/main/README.md) · [Page](https://enuminous.github.io/P-NP/)
- [Research-Program](https://github.com/enuminous/Research-Program) · [README](https://github.com/enuminous/Research-Program/blob/main/README.md) · [Page](https://enuminous.github.io/Research-Program/)
- [I-Have-Guts](https://github.com/enuminous/I-Have-Guts) · [README](https://github.com/enuminous/I-Have-Guts/blob/main/README.md) · [Page](https://enuminous.github.io/I-Have-Guts/)
- [Wrights-Law](https://github.com/enuminous/Wrights-Law) · [README](https://github.com/enuminous/Wrights-Law/blob/main/README.md) · [Page](https://enuminous.github.io/Wrights-Law/)
- [Aristotle-eNuminous](https://github.com/enuminous/Aristotle-eNuminous) · [README](https://github.com/enuminous/Aristotle-eNuminous/blob/main/README.md) · [Page](https://enuminous.github.io/Aristotle-eNuminous/)
- [Multiverse-Simulator](https://github.com/enuminous/Multiverse-Simulator) · [README](https://github.com/enuminous/Multiverse-Simulator/blob/main/README.md) · [Page](https://enuminous.github.io/Multiverse-Simulator/)
- [accelerando-8192](https://github.com/enuminous/accelerando-8192) · [README](https://github.com/enuminous/accelerando-8192/blob/main/README.md) · [Page source](https://github.com/enuminous/accelerando-8192/blob/main/docs/index.html)
- [Codex-888](https://github.com/enuminous/Codex-888) · [README](https://github.com/enuminous/Codex-888/blob/main/README.md) · [Page](https://enuminous.github.io/Codex-888/)

</details>
<!-- ENUMINOUS-NETWORK:END -->

**Adaptive Network Tracer**

ANT is an EFMW-derived framework for supply-chain and logistics propagation.

Its narrow question is:

> Given a disturbance somewhere in a dependency network, can ANT identify where stress is likely to propagate next, and which node is most likely to become operationally critical?

## Intended uses

- supply chains
- logistics networks
- warehouse networks
- manufacturing dependencies
- vendor networks
- fulfillment systems
- transport chains
- inventory networks
- service dependency systems

## Core signal path

```text
node state
→ dependency graph
→ inventory / delay stress
→ substitution capacity
→ edge propagation pressure
→ bottleneck concentration
→ multiscale persistence
→ next-node risk
```

## Flat-stack repository

```text
README.md
LICENSE
CITATION.cff
pyproject.toml
requirements.txt
ant.py
features.py
baselines.py
metrics.py
freeze.py
propagation_schema.json
example_config.yaml
example_nodes.csv
example_edges.csv
example_run.py
test_ant.py
MANIFEST.sha256
```

## Scientific hypothesis

> In dependency-rich logistics systems, failure risk may propagate through relational stress before downstream nodes independently cross conventional thresholds.

ANT does not assume this is true.

## Example signals

- inventory deficit
- lead-time inflation
- backlog growth
- supplier concentration
- substitution capacity
- dependency load
- upstream stress
- downstream exposure
- edge propagation pressure
- bottleneck concentration
- next-node risk

## Baselines

Included:

- node-only logistic model
- inventory-deficit baseline
- backlog baseline
- degree-weighted exposure model
- base-rate predictor

## Primary endpoint

> Does ANT improve out-of-sample prediction of next-node operational failure over a matched node-only model?

Primary metric:

- Brier score

Secondary metrics:

- log loss
- ROC-AUC
- average precision
- performance by dependency-load regime

## Installation

```bash
python -m pip install -r requirements.txt
```

## Run

```bash
python example_run.py
```

## Tests

```bash
pytest -q
```

## Minimal use

```python
import pandas as pd
from ant import ANTExperiment

nodes = pd.read_csv("example_nodes.csv")
edges = pd.read_csv("example_edges.csv")

exp = ANTExperiment(
    time_column="time",
    target_column="failure",
    node_prefixes=["A","B","C","D","E"],
    horizons=(3,7,23),
)

print(exp.run(nodes, edges))
```

## Freeze discipline

Freeze before prospective use:

- node list
- dependency graph
- edge direction
- lead-time definition
- inventory definition
- substitution-capacity rule
- propagation equations
- target
- horizons
- split
- baselines
- metrics
- exclusions
- seeds

Then run:

```bash
python freeze.py
```

## Negative results

If node-only inventory and backlog models match or beat ANT, then explicit propagation modeling has not demonstrated incremental value.

## Status

Research software. Experimental. Not validated for critical logistics decisions.
