# ANT

<!-- ENUMINOUS-UNIFIED-NAV:START -->
## Repository navigation

**eNuminous network:** [All public repositories](https://github.com/enuminous/EFMW/blob/main/REPOSITORY_NAVIGATION.md) · [EFMW](https://github.com/enuminous/EFMW) · [102 equations](https://github.com/enuminous/Monolithic_102_EFMW) · [Frozen Lean](https://github.com/enuminous/Monolithic-102-Zoo-Lean4) · [Zoo](https://github.com/enuminous/Tortoise) · [Papers](https://github.com/enuminous/papers) · [Quantum geometry](https://github.com/enuminous/Base888-Quantum-Geometry)

**This project:** [Repository home](https://github.com/enuminous/Ant) · [Subject index](https://github.com/enuminous/EFMW/blob/main/REPOSITORY_NAVIGATION.md#zoo-index-and-agents)

<details open>
<summary><strong>On this page</strong></summary>

- [Intended uses](#intended-uses)
- [Core signal path](#core-signal-path)
- [Flat-stack repository](#flat-stack-repository)
- [Scientific hypothesis](#scientific-hypothesis)
- [Example signals](#example-signals)
- [Baselines](#baselines)
- [Primary endpoint](#primary-endpoint)
- [Installation](#installation)
- [Run](#run)
- [Tests](#tests)
- [Minimal use](#minimal-use)
- [Freeze discipline](#freeze-discipline)
- [Negative results](#negative-results)
- [Status](#status)


</details>

**Related repositories:** [Tortoise](https://github.com/enuminous/Tortoise) · [Monolithic-Zoo-Lean4](https://github.com/enuminous/Monolithic-Zoo-Lean4) · [Monolithic-102-Zoo-Lean4](https://github.com/enuminous/Monolithic-102-Zoo-Lean4) · [Moth](https://github.com/enuminous/Moth) · [Dolphin](https://github.com/enuminous/Dolphin) · [Shark](https://github.com/enuminous/Shark) · [Raven](https://github.com/enuminous/Raven)

> **Evidence boundary:** A link between projects is navigation, not an assertion of proven equivalence, experimental validation, or shared authorship. See each repository’s own status and review notes.
<!-- ENUMINOUS-UNIFIED-NAV:END -->


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
