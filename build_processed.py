import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / "data"
RAW = BASE / "raw"
LOOKUP = BASE / "lookup"
PROCESSED = BASE / "processed"
PROCESSED.mkdir(parents=True, exist_ok=True)

# Load
supply = pd.read_csv(RAW / "supply.csv", parse_dates=["Date"])
energy = pd.read_csv(RAW / "energy.csv", parse_dates=["Date"])
customers = pd.read_csv(RAW / "customers.csv", parse_dates=["Date"])
incidents = pd.read_csv(RAW / "incidents.csv", parse_dates=["StartDT", "EndDT"])
dma_lookup = pd.read_csv(LOOKUP / "dma_lookup.csv")
region_attr = pd.read_csv(LOOKUP / "region_attributes.csv")

# Example join: incidents → add Network_km by Region
inc_enriched = incidents.merge(dma_lookup[["DMA","Region"]], on=["DMA","Region"], how="left")
inc_enriched = inc_enriched.merge(region_attr, on="Region", how="left")
inc_enriched.to_csv(PROCESSED / "incidents_enriched.csv", index=False)

# Basic KPI aggregates by month/region
s = supply.groupby(["Date","Region"], as_index=False).agg({
    "SystemInput_m3":"sum",
    "BilledAuthCons_m3":"sum",
    "NonBilled_m3":"sum"
})
c = customers.groupby(["Date","Region"], as_index=False).agg({
    "Households":"sum",
    "Complaints":"sum",
    "Interruptions_Minutes_Total":"sum",
    "CustomersAffected":"sum"
})
e = energy.groupby(["Date","Region"], as_index=False).agg({
    "kWh":"sum","£_EnergyCost":"sum","Emissions_kgCO2e":"sum"
})
kpi = s.merge(c, on=["Date","Region"], how="left").merge(e, on=["Date","Region"], how="left")
kpi["NRW_pct"] = (kpi["SystemInput_m3"] - kpi["BilledAuthCons_m3"]) / kpi["SystemInput_m3"]
kpi.to_csv(PROCESSED / "kpi_monthly_region.csv", index=False)

print("Processed files written to", PROCESSED)
