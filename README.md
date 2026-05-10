# Counterfactual Inflation Analysis: Ukraine and the Euro Area

This repository contains my take-home exam project for **Quantitative Methods in Finance**.

The research question is:

> What would Ukraine's inflation trajectory have looked like if Ukraine had been part of the Euro Area?

The project combines a documented monetary-regime chronology with counterfactual econometric methods. It first analyses Ukraine's exchange-rate and monetary-policy regime from 2000 to 2025, then estimates counterfactual Ukrainian inflation under the hypothetical scenario of Euro Area membership.

---

## 1. Project Overview

Ukraine was never a member of the Euro Area. It maintained its own currency, the hryvnia, and its own central bank, the National Bank of Ukraine. However, Ukraine did not have the same degree of effective monetary sovereignty throughout the full sample.

Between 2000 and 2025, Ukraine alternated between:

- de facto dollar pegs;
- crisis devaluations;
- capital controls and foreign-exchange restrictions;
- inflation targeting after 2015–2016;
- a wartime fixed exchange-rate regime after the 2022 full-scale invasion;
- managed exchange-rate flexibility after October 2023.

This matters for the counterfactual. Euro Area membership should not be interpreted as a constant treatment over time. During de facto peg periods, Ukraine was already constrained by an exchange-rate anchor. During devaluation episodes and the post-2016 inflation-targeting period, Euro Area membership would have represented a larger loss of monetary and exchange-rate autonomy.

The analysis is divided into two parts:

- **Part A:** Ukraine's exchange-rate and monetary-policy regime chronology.
- **Part B:** Counterfactual Ukrainian inflation under hypothetical Euro Area membership.

---

## 2. Repository Contents

The repository contains the following main files and folders:

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
```

Depending on the final upload, some figures and output files may be stored directly in the root folder instead of inside `figures/` or `outputs/`.

---

## 3. Description of the Data

The project uses monthly macroeconomic data. The main variables are Ukrainian inflation, Euro Area inflation, exchange rates, policy rates, and industrial-production growth.

---

### 3.1 Ukraine CPI Data

**File:** `data_ukraine_cpi_raw.csv`

This file contains Ukraine monthly CPI data.

The original Ukrainian CPI observations are expressed as monthly index changes, with the previous month equal to 100. For example:

- `100.0` means no monthly price change;
- `101.5` means prices increased by 1.5% relative to the previous month;
- `99.5` means prices decreased by 0.5% relative to the previous month.

The code converts the monthly CPI index into year-on-year inflation using the rolling twelve-month cumulative product:

```text
Ukraine year-on-year inflation =
cumulative product of the last 12 monthly CPI factors - 1
```

This transformation is necessary because the Euro Area HICP panel is expressed in year-on-year percentage changes.

The resulting Ukrainian inflation variable is used as the actual inflation series in Part B.

---

### 3.2 Euro Area HICP Inflation Panel

**File:** `data_ecb_hicp_panel.csv`

This file contains monthly HICP year-on-year inflation rates for eleven Euro Area countries:

- Germany;
- France;
- Italy;
- Spain;
- Netherlands;
- Belgium;
- Austria;
- Portugal;
- Ireland;
- Finland;
- Greece.

The Euro Area panel is used to construct a common Euro Area inflation factor. Instead of using a simple cross-sectional average of country inflation rates, the project extracts the first principal component of the Euro Area HICP panel.

This factor is interpreted as the common Euro Area nominal inflation component that Ukraine would have imported under Euro Area membership.

The first principal component explains approximately 80% of the cross-country variance in the Euro Area inflation panel.

---

### 3.3 Official Hryvnia Exchange Rates

**File:** `Official hrivnya exchange rates.csv`

This file contains official National Bank of Ukraine exchange-rate data.

It is used for two purposes.

First, in **Part A**, it is used to construct the monthly UAH/USD exchange-rate series and document Ukraine's exchange-rate regime chronology.

Second, in **Part B**, it is used to construct the exchange-rate depreciation channel, especially the year-on-year depreciation of the hryvnia against the euro.

For Part A, the monthly UAH/USD series helps identify:

- the de facto peg around 5 UAH/USD before the 2008–2009 Global Financial Crisis;
- the de facto peg around 8 UAH/USD from 2010 to early 2014;
- the 2014–2015 hryvnia collapse;
- the wartime peg after the 2022 full-scale invasion;
- the post-2023 managed flexibility period.

For Part B, the code computes year-on-year log depreciation:

```text
Depreciation = 100 × [log(exchange rate at time t) - log(exchange rate at time t-12)]
```

A positive value means that the hryvnia depreciated.

This variable is important because exchange-rate depreciation is one of the main channels through which Ukraine's monetary sovereignty affected domestic inflation.

---

### 3.4 NBU Key Policy Rate

**File:** `data_nbu_key_policy_rate.csv`

This file contains the National Bank of Ukraine key policy-rate data.

It is mainly used in Part A to document Ukraine's monetary-policy regime.

The policy-rate series helps distinguish between:

- periods when the exchange-rate objective dominated monetary policy;
- the transition to inflation targeting in 2015–2016;
- the post-2016 period when the NBU policy rate became a more meaningful monetary-policy instrument;
- the wartime monetary tightening after the 2022 full-scale invasion.

The policy rate is not the dependent variable in the counterfactual inflation model, but it is important for understanding the timing and intensity of Ukraine's monetary sovereignty.

---

### 3.5 Ukraine Industrial Production

**File:** `ua_industry_yoy.csv`

This file contains Ukraine industrial-production year-on-year growth.

It is used as the Ukrainian activity variable in the Blanchard–Quah SVAR robustness exercise.

The BQ-SVAR requires two variables:

```text
activity growth
inflation
```

For Ukraine, the activity variable is Ukraine industrial-production growth.

This variable allows the model to separate supply shocks and demand shocks. In the counterfactual, Ukraine-specific supply shocks are preserved, while Ukraine's domestic demand shocks are partly replaced by Euro Area demand shocks.

---

### 3.6 Euro Area Industrial Production

The Euro Area industrial-production series is used as the Euro Area activity variable in the BQ-SVAR robustness exercise.

Depending on the final version of the code, this series may be loaded from an included file or constructed inside the script from the available data.

It is used together with Euro Area inflation to estimate Euro Area supply and demand shocks.

This variable is required for the structural identification strategy. It is not used only for description.

---

## 4. Python Scripts

---

### 4.1 `part_a_ukraine_regime_change.py`

This script produces the Part A monetary-regime analysis.

It performs the following steps:

1. Loads and cleans the official NBU exchange-rate data.
2. Keeps the relevant UAH/USD exchange-rate series.
3. Converts daily exchange rates into monthly averages.
4. Loads the NBU key policy-rate data.
5. Aligns the policy rate with the monthly exchange-rate series.
6. Computes monthly depreciation diagnostics.
7. Identifies the largest hryvnia depreciation episodes.
8. Builds a regime chronology table.
9. Generates Part A figures and output tables.

Main Part A outputs include:

```text
figure_1_uah_usd_regime_breaks.png
figure_2_uah_usd_policy_rate.png
figure_3_monthly_depreciation_spikes.png
```

These figures are used in the final report.

---

### 4.2 `part_b_counterfactual_inflation.py`

This script produces the Part B counterfactual inflation analysis.

It performs the following steps:

1. Loads Ukraine monthly CPI data.
2. Converts Ukraine CPI into year-on-year inflation.
3. Loads the Euro Area HICP inflation panel.
4. Extracts the Euro Area common inflation factor using PCA.
5. Loads the exchange-rate data.
6. Computes year-on-year hryvnia depreciation against the euro.
7. Builds the treatment-intensity schedule from Part A.
8. Estimates the baseline ARDL/local-projection model.
9. Simulates the dynamic counterfactual inflation path.
10. Estimates the Blanchard–Quah SVAR robustness exercise.
11. Estimates the synthetic-control robustness benchmark.
12. Exports result tables and figures.

Main Part B outputs include:

```text
main_lp_actual_vs_counterfactual.png
bq_svar_actual_vs_counterfactual.png
synthetic_control_actual_vs_counterfactual.png
method_comparison_counterfactuals.png
```

---

### 4.3 `data_nbu_key_rates_parsing.py`

This helper script prepares the National Bank of Ukraine key policy-rate data.

It is used to generate or clean:

```text
data_nbu_key_policy_rate.csv
```

This script is auxiliary and supports the Part A monetary-policy analysis.

---

## 5. Report Files

---

### 5.1 `main.tex`

This is the LaTeX source of the final report.

It contains:

- the title page;
- abstract;
- Part A;
- Part B;
- tables;
- figure inclusions;
- bibliography.

---

### 5.2 `final_report.pdf`

This is the final compiled report submitted for the project.

It contains:

- the full written analysis;
- tables;
- figures;
- methodology;
- results;
- interpretation;
- limitations.

If the final PDF has a different name in the repository, use that file as the report output.

---

## 6. Figures and Outputs

The repository may contain a `figures/` folder and/or an `outputs/` folder.

The expected figures are:

```text
figure_1_uah_usd_regime_breaks.png
figure_2_uah_usd_policy_rate.png
figure_3_monthly_depreciation_spikes.png
main_lp_actual_vs_counterfactual.png
bq_svar_actual_vs_counterfactual.png
synthetic_control_actual_vs_counterfactual.png
method_comparison_counterfactuals.png
```

The expected outputs include:

- cleaned data;
- summary tables;
- devaluation episode diagnostics;
- intermediate results;
- figures used in the report.

---

## 7. Part A: Ukraine's Monetary Regime

Part A constructs a documented chronology of Ukraine's exchange-rate and monetary-policy regime from 2000 to 2025.

It identifies five main features.

---

### 7.1 De Facto Dollar Pegs

Ukraine had long periods of de facto exchange-rate stabilization against the US dollar.

The most important peg periods are:

- around 5 UAH/USD before the 2008–2009 Global Financial Crisis;
- around 8 UAH/USD from 2010 to early 2014.

During these periods, Ukraine formally had its own currency and central bank, but monetary policy was effectively constrained by the exchange-rate objective.

---

### 7.2 Major Devaluation Episodes

The analysis identifies three major hryvnia depreciation episodes:

1. **2008–2009 Global Financial Crisis**  
   The hryvnia moved from the quasi-peg around 5 UAH/USD to around 8 UAH/USD.

2. **2014–2015 Crimea/Donbas crisis**  
   The NBU abandoned the peg, and the exchange rate moved from around 8 UAH/USD to above 20 UAH/USD.

3. **2022 full-scale invasion**  
   The NBU first fixed the exchange rate around 29.25 UAH/USD, then devalued it by 25% to 36.5686 UAH/USD in July 2022.

---

### 7.3 Capital Controls and FX Restrictions

Capital controls and FX restrictions were not equally important throughout the full sample.

They were:

- crisis-management tools in 2008–2009;
- central stabilization instruments in 2014–2015;
- constitutive features of the wartime monetary regime after 2022.

This is important because monetary sovereignty was often exercised under severe constraints rather than in normal conditions.

---

### 7.4 Inflation Targeting

Ukraine moved toward inflation targeting in 2015–2016.

Before 2015, the NBU key policy rate had a limited operational role because the exchange-rate objective dominated monetary policy.

After the 2015–2016 reform, the policy rate became a more meaningful monetary-policy instrument. This period therefore represents a higher degree of effective monetary sovereignty than the earlier peg periods.

---

### 7.5 Wartime Monetary Regime

After the full-scale invasion in February 2022, the NBU introduced a wartime fixed exchange-rate regime and strict foreign-exchange restrictions.

In July 2022, the official exchange rate was devalued and fixed at a new level.

From October 2023, Ukraine moved toward managed exchange-rate flexibility. However, this was not a full return to normal inflation targeting because wartime restrictions and interventions remained relevant.

---

## 8. Part B: Counterfactual Inflation Analysis

Part B estimates what Ukrainian inflation might have looked like under hypothetical Euro Area membership.

The counterfactual is not a simple average of Euro Area inflation. It uses explicit econometric identification strategies and remains consistent with the Part A regime chronology.

Three approaches are used:

1. baseline ARDL/local-projection model;
2. Blanchard–Quah SVAR robustness check;
3. synthetic-control robustness benchmark.

---

## 9. Treatment Intensity

The counterfactual treatment is time-varying.

The idea is that Euro Area membership would have mattered little during periods when Ukraine was already constrained by a peg, but would have mattered strongly during periods when Ukraine was actively using its own monetary sovereignty.

The treatment intensity is low during:

- conventional peg periods;
- stabilized exchange-rate arrangements;
- wartime fixed exchange-rate periods.

The treatment intensity is high during:

- forced devaluations;
- the 2014–2015 hryvnia collapse;
- the post-2016 inflation-targeting period.

The treatment schedule is directly based on the regime chronology from Part A.

---

## 10. Baseline ARDL / Local-Projection Model

The baseline model explains Ukraine's year-on-year inflation using:

- Ukrainian inflation persistence;
- the Euro Area common inflation factor;
- year-on-year depreciation of the hryvnia against the euro.

The model is estimated at monthly frequency.

The counterfactual simulation removes the domestic depreciation channel proportionally to the treatment intensity.

The dynamic recursion uses lagged simulated counterfactual inflation rather than actual lagged inflation. This allows the counterfactual path to evolve endogenously over time.

---

## 11. Blanchard–Quah SVAR Robustness

The structural robustness check uses a bivariate Blanchard–Quah SVAR.

The model uses:

```text
activity growth
inflation
```

for both Ukraine and the Euro Area.

The identifying restriction is that demand shocks have no long-run effect on activity, while supply shocks may have permanent effects.

In the counterfactual:

- Ukraine-specific supply shocks are kept unchanged;
- Ukraine's domestic demand shocks are partly replaced by Euro Area demand shocks;
- the replacement is weighted by the treatment intensity.

This method is useful because Euro Area membership would not have eliminated Ukraine-specific real shocks, such as war damage or production disruption, but it would have changed nominal and demand-side monetary conditions.

---

## 12. Synthetic-Control Robustness

The synthetic-control robustness exercise constructs a weighted combination of European inflation series to approximate Ukraine's inflation dynamics.

It is used as an additional benchmark rather than the main identification strategy.

This is because Ukraine never joined the Euro Area, so there is no clean treatment date in the standard synthetic-control sense. The synthetic-control results are therefore interpreted as robustness evidence rather than the central estimate.

---

## 13. Main Results

The results suggest that Euro Area membership would have reduced Ukrainian inflation volatility mainly during episodes of large hryvnia depreciation.

The strongest effect appears during the 2014–2015 Crimea/Donbas crisis, when the collapse of the hryvnia generated strong exchange-rate pass-through into consumer prices.

The 2008–2009 crisis also shows a disinflationary counterfactual effect, although smaller than in 2014–2015.

The 2022–2023 results are more nuanced. The baseline ARDL/local-projection counterfactual gap is smaller because Ukraine had already reintroduced a wartime fixed exchange-rate regime, meaning that domestic monetary sovereignty was already constrained.

The BQ-SVAR robustness check can generate higher counterfactual inflation in 2022–2023 because Euro Area shocks were themselves inflationary during the European energy crisis.

Overall, the results imply that monetary sovereignty was costly in nominal terms during devaluation episodes, but it also provided an exchange-rate adjustment mechanism that Euro Area membership would have removed.

---

## 14. How to Reproduce the Results

Install the required Python packages:

```bash
pip install pandas numpy matplotlib statsmodels scikit-learn scipy
```

Run the Part A script:

```bash
python part_a_ukraine_regime_change.py
```

Run the Part B script:

```bash
python part_b_counterfactual_inflation.py
```

The scripts generate the figures, tables, and intermediate files used in the report.

If the scripts are run from a clean clone, make sure that all CSV files are located in the expected paths. If needed, adjust the input paths at the top of each Python script.

---

## 15. Expected Outputs

The expected main outputs are:

```text
figure_1_uah_usd_regime_breaks.png
figure_2_uah_usd_policy_rate.png
figure_3_monthly_depreciation_spikes.png
main_lp_actual_vs_counterfactual.png
bq_svar_actual_vs_counterfactual.png
synthetic_control_actual_vs_counterfactual.png
method_comparison_counterfactuals.png
```

The report uses these figures to compare actual Ukrainian inflation with the counterfactual paths.

---

## 16. Reproducibility Notes

The project is designed to be reproducible from the files included in this repository.

The code performs the following transformations:

- converts Ukraine monthly CPI indices into year-on-year inflation;
- computes monthly exchange-rate series from NBU exchange-rate data;
- constructs year-on-year exchange-rate depreciation;
- extracts the Euro Area common inflation factor using PCA;
- estimates the baseline ARDL/local-projection counterfactual;
- estimates the BQ-SVAR robustness counterfactual;
- estimates the synthetic-control robustness benchmark;
- exports figures and tables used in the report.

All external datasets are either included as CSV files or described directly in the code and report.

---

## 17. Methodological References

The project uses concepts and methods from:

- Mundell (1961), McKinnon (1963), and Kenen (1969) on optimum currency areas.
- Calvo and Reinhart (2002) on fear of floating.
- Blanchard and Quah (1989) on structural shock decomposition.
- Bayoumi and Eichengreen (1993) on monetary integration and asymmetric shocks.
- Ciccarelli and Mojon (2010) on common inflation factors.
- Abadie, Diamond, and Hainmueller (2010) on synthetic control.
- De Grauwe (2012) on sovereign fragility inside monetary unions.
- National Bank of Ukraine publications for exchange-rate and policy-rate data.
- IMF Ukraine country reports for exchange-rate regime classifications and wartime macroeconomic policy.

---

## 18. Author

Akram S. Benaissa
Master 2 Finance Technology Data  
Université Paris 1 Panthéon-Sorbonne  
Academic Year 2025–2026
