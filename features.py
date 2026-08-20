import numpy as np
import pandas as pd

EPS = 1e-8

def _get(df, node, metric):
    name = f"{node}_{metric}"
    if name in df.columns:
        return df[name].astype(float)
    return pd.Series(0.0, index=df.index)

def build_ant_features(df, edges, node_prefixes, horizons=(3,7,23)):
    out = pd.DataFrame(index=df.index)

    # Node-local logistics stress.
    node_risks = {}
    for node in node_prefixes:
        inventory = _get(df, node, "inventory")
        demand = _get(df, node, "demand")
        backlog = _get(df, node, "backlog")
        lead = _get(df, node, "lead_time")
        substitute = _get(df, node, "substitution")

        inventory_deficit = (demand - inventory).clip(lower=0)
        lead_rank = lead.rank(pct=True)
        backlog_rank = backlog.rank(pct=True)
        substitution_deficit = 1.0 - substitute.clip(0,1)

        risk = (
            inventory_deficit.rank(pct=True)
            + lead_rank
            + backlog_rank
            + substitution_deficit
        ) / 4.0

        out[f"{node}__inventory_deficit"] = inventory_deficit
        out[f"{node}__local_risk"] = risk
        node_risks[node] = risk

    # Graph propagation pressure.
    edge_cols = []
    for _, row in edges.iterrows():
        src = row["source"]
        dst = row["target"]
        weight = float(row.get("weight",1.0))
        lag = int(row.get("lag",1))
        if src not in node_risks or dst not in node_risks:
            continue

        upstream = node_risks[src].shift(lag).fillna(0.0)
        downstream = node_risks[dst]
        exposure = upstream * weight
        mismatch = (exposure - downstream).abs()

        cname = f"edge__{src}__{dst}__pressure"
        out[cname] = exposure + mismatch
        edge_cols.append(cname)

    if edge_cols:
        edge_df = out[edge_cols]
        out["propagation_pressure_mean"] = edge_df.mean(axis=1)
        out["propagation_pressure_max"] = edge_df.max(axis=1)
        out["propagation_dispersion"] = edge_df.std(axis=1).fillna(0.0)
        total = edge_df.sum(axis=1).replace(0,np.nan)
        shares = edge_df.div(total, axis=0).fillna(0.0)
        out["bottleneck_concentration"] = (shares**2).sum(axis=1)
    else:
        out["propagation_pressure_mean"] = 0.0
        out["propagation_pressure_max"] = 0.0
        out["propagation_dispersion"] = 0.0
        out["bottleneck_concentration"] = 0.0

    # Aggregate local risk.
    local_cols = [f"{n}__local_risk" for n in node_prefixes]
    out["network_local_risk"] = out[local_cols].mean(axis=1)
    out["network_risk_divergence"] = (
        out["propagation_pressure_mean"].rank(pct=True)
        - out["network_local_risk"].rank(pct=True)
    ).abs()

    out["propagation_velocity"] = out["propagation_pressure_mean"].diff().fillna(0.0)

    for h in horizons:
        out[f"pressure_mean_{h}"] = out["propagation_pressure_mean"].rolling(h, min_periods=1).mean()
        out[f"bottleneck_mean_{h}"] = out["bottleneck_concentration"].rolling(h, min_periods=1).mean()
        out[f"local_risk_mean_{h}"] = out["network_local_risk"].rolling(h, min_periods=1).mean()
        out[f"velocity_mean_{h}"] = out["propagation_velocity"].rolling(h, min_periods=1).mean()

    components = [
        out["propagation_pressure_mean"],
        out["propagation_pressure_max"],
        out["propagation_dispersion"],
        out["bottleneck_concentration"],
        out["network_local_risk"],
        out["network_risk_divergence"],
        out["propagation_velocity"].clip(lower=0),
    ]
    for h in horizons:
        components.extend([
            out[f"pressure_mean_{h}"],
            out[f"bottleneck_mean_{h}"],
            out[f"local_risk_mean_{h}"],
            out[f"velocity_mean_{h}"].clip(lower=0),
        ])

    ranked = pd.concat(components, axis=1).rank(pct=True)
    out["ant_network_risk"] = ranked.mean(axis=1).fillna(0.0)

    return out.replace([np.inf,-np.inf], np.nan).fillna(0.0)
