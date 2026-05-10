# Counterfactual Inflation Analysis: Ukraine and the Euro Area

This repository contains my take-home exam project for **Quantitative Methods in Finance**.

The research question is:

> What would Ukraine's inflation trajectory have looked like if Ukraine had been part of the Euro Area?

The project combines a monetary-regime chronology with counterfactual econometric methods. It first documents Ukraine's exchange-rate and monetary-policy regime from 2000 to 2025, then estimates counterfactual Ukrainian inflation under the hypothetical scenario of Euro Area membership.

---

## 1. Repository Contents

The repository contains the following main files:

```text
.
├── README.md
├── main.tex
├── final_report.pdf
│
├── part_a_ukraine_regime_change.py
├── part_b_counterfactual_inflation.py
├── data_nbu_key_rates_parsing.py
│
├── data_ecb_hicp_panel.csv
├── data_ukraine_cpi_raw.csv
├── Official hrivnya exchange rates.csv
├── data_nbu_key_policy_rate.csv
├── ua_industry_yoy.csv
│
├── figures/
│   ├── figure_1_uah_usd_regime_breaks.png
│   ├── figure_2_uah_usd_policy_rate.png
│   ├── figure_3_monthly_depreciation_spikes.png
│   ├── main_lp_actual_vs_counterfactual.png
│   ├── bq_svar_actual_vs_counterfactual.png
│   ├── synthetic_control_actual_vs_counterfactual.png
│   └── method_comparison_counterfactuals.png
│
└── outputs/
    ├── cleaned data
    ├── summary tables
    └── intermediate results
