# Portfolio optimiser (binary knapsack with options) — requires PuLP (pip install pulp) or OR-Tools
import pandas as pd
import numpy as np
from pathlib import Path

try:
    import pulp as pl
except Exception as e:
    raise SystemExit("This script requires PuLP. Install with: pip install pulp")

BASE = Path(__file__).resolve().parents[1]
RAW = BASE / "data" / "raw"
OUT = BASE / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)

projects = pd.read_csv(RAW / "projects.csv")
benefits = pd.read_csv(RAW / "project_benefits.csv")

# Aggregate a simple risk-adjusted NPV proxy using Base benefits and risk penalty
# In practice you'd build year-by-year cash flows and discount them.
disc_rate = 0.06
life = projects["Life_Years"].fillna(10)
# Approximate NPV = (Annual_Benefit_Base * annuity_factor) - Capex
annuity_factor = (1 - (1 + disc_rate) ** (-life)) / disc_rate
benefit_sum = benefits.groupby("ProjectID")["Annual_Benefit_£_Base"].sum().reindex(projects["ProjectID"]).fillna(0.0).values
npv = benefit_sum * annuity_factor.values - projects["£_Capex"].values
risk_penalty = projects["Risk_Prob"].values * projects["Risk_Impact_£"].values
risk_adj_npv = npv - risk_penalty

# Optional KPI score = count of KPIs with positive improvement
kpi_score = benefits.groupby("ProjectID")["KPI"].nunique().reindex(projects["ProjectID"]).fillna(0).values

capex = projects["£_Capex"].values
budget = np.quantile(capex, 0.5) * (len(projects) * 0.35)  # illustrative budget ~= select ~1/3 of total

model = pl.LpProblem("CapexPortfolio", pl.LpMaximize)
x = {pid: pl.LpVariable(f"x_{pid}", lowBound=0, upBound=1, cat="Binary") for pid in projects["ProjectID"]}

lam = 0.0  # weight for KPI score (set >0 to include)
obj = pl.lpSum(x[pid] * (float(risk_adj_npv[i]) + lam*float(kpi_score[i])) for i, pid in enumerate(projects["ProjectID"]))
model += obj

# Budget constraint
model += pl.lpSum(x[pid] * float(capex[i]) for i, pid in enumerate(projects["ProjectID"])) <= float(budget)

# Example constraint: at least one Quality project
is_quality = (projects["Category"] == "Quality").astype(int).values
model += pl.lpSum(x[pid] * int(is_quality[i]) for i, pid in enumerate(projects["ProjectID"])) >= 1

# Solve
model.solve(pl.PULP_CBC_CMD(msg=False))

# Export selection
projects["Selected"] = [int(pl.value(x[pid])) for pid in projects["ProjectID"]]
projects["RiskAdjNPV_£"] = risk_adj_npv
sel = projects[projects["Selected"] == 1].copy()
sel.to_csv(OUT / "selected_portfolio.csv", index=False)
print("Wrote", OUT / "selected_portfolio.csv")
