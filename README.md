# Utility-Dashboard
This repo contains **synthetic** data and a starter structure for the Water Utility KPI & Capex Prioritisation Dashboard.

## Contents
- `data/raw/` — input CSVs (incidents, supply, energy, customers, costs, projects, project_benefits)
- `data/lookup/` — `dma_lookup.csv`, `region_attributes.csv`, `targets_penalties.csv`
- `data/processed/` — left empty for Power Query / Python output
- `powerbi/` — `MEASURES.txt` (copy DAX measures into your model), `README.md` instructions
- `excel/` — `Capex_Optimiser.xlsx` (skeleton)
- `python/` — `build_processed.py`, `optimise_portfolio.py`
- `deck/` — (empty placeholder)
- `assets/` — (screenshots placeholder)

All values are invented for portfolio/demo use.

## Quick Start (Power BI)
1. **Get Data → Folder** point to `/data/raw` and `/data/lookup` (or import each CSV).
2. Create relationships using keys (`Region`, `DMA`, `Date`). Bring in `region_attributes` for `Network_km`.
3. Paste DAX from `powerbi/MEASURES.txt` for KPI and financial measures.
4. Use `targets_penalties.csv` to set targets and penalty weights for KPI cards.
5. (Optional) Import `excel/Capex_Optimiser.xlsx` outputs (`selected_portfolio.csv`) once you run Solver or the Python optimiser.

## Notes
- Date coverage: 2024-04 → 2025-09 across 6 regions and 120 DMAs.
- `incidents.csv` has ~3000 rows with 60% bursts.
- Emissions use an illustrative factor of 0.233 kgCO₂e/kWh.
