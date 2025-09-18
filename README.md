# Utility-Dashboard
This repo contains **synthetic** data and a starter structure for the Water Utility KPI & Capex Prioritisation Dashboard.

## Problem Statement
A UK water operator is under budget pressure. Which interventions—leak repairs, DMA metering, pump upgrades—maximise service performance and economic value under Ofwat-style constraints? I built a Power BI KPI stack, linked each CapEx to KPI deltas and £-impact, then used an Excel/Python optimiser to pick the best portfolio across Base/Drought/High-energy scenarios.

## Target outcomes

- Transparent KPI library aligned to water ops.

- Traceability from raw data → KPI → £ impact → portfolio choice.

- Executable ‘what‑if’ levers (energy price, leakage uplift, penalty weights).

- Board‑ready deck summarising ROI, risks, and next steps.

## Contents
- `data/raw/` — input CSVs (incidents, supply, energy, customers, costs, projects, project_benefits)
- `data/lookup/` — `dma_lookup.csv`, `region_attributes.csv`, `targets_penalties.csv`
- `data/processed/` — Power Query / Python output
- `powerbi/` — `MEASURES.txt` (DAX measures for the model), `README.md` instructions
- `excel/` — `Capex_Optimiser.xlsx` (optimisation model)
- `python/` — `build_processed.py`, `optimise_portfolio.py`
- `deck/` 
- `assets/` — (screenshots)

All values are invented for portfolio/demo use.

## Notes
- Date coverage: 2024-04 → 2025-09 across 6 regions and 120 DMAs.
- `incidents.csv` has ~3000 rows with 60% bursts.
- Emissions use an illustrative factor of 0.233 kgCO₂e/kWh.
