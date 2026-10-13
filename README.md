# ai_ml_medicare-provider-analytics
# Predicting Medicare Payment Costs and Identifying High-Cost Provider Patterns Using Machine Learning

**Course:** QM640 — Data Analytics Capstone  
**Institution:** Walsh College  
**Mentor:** Sharath Srivatsa  
**Term:** Fall 2026  
**Student:** Kapil Dev Sharma

## Project Overview

This project examines provider-level Medicare payment patterns using the 2024 CMS Medicare Physician & Other Practitioners — by Provider dataset. It applies exploratory data analysis, statistical techniques, regression, classification, and risk-ranking methods to investigate payment variation and identify providers with comparatively high total Medicare payments.

## Research Questions

1. Which provider, utilization, and beneficiary characteristics are associated with differences in Medicare payments?
2. Which eligible features predict total Medicare payment amounts?
3. Which machine-learning model best identifies high-cost providers?
4. Can a provider-level risk score help prioritize records for human review?

## Data Source

Centers for Medicare & Medicaid Services (CMS):  
https://data.cms.gov/provider-summary-by-type-of-service/medicare-physician-other-practitioners/medicare-physician-other-practitioners-by-provider

API documentation:  
https://data.cms.gov/provider-summary-by-type-of-service/medicare-physician-other-practitioners/medicare-physician-other-practitioners-by-provider/api-docs

Data dictionary:  
https://data.cms.gov/resources/medicare-physician-other-practitioners-by-provider-data-dictionary

## Analytical Workflow

1. Data loading and schema verification.
2. Data-quality assessment and exploratory data analysis.
3. Missingness, suppression, outlier, and consistency analysis.
4. Target definition and prevention of target leakage.
5. Statistical analysis and regression.
6. High-cost classification and model comparison.
7. Risk-score evaluation and reproducibility documentation.

## Reproducibility

Use Python and the dependencies listed in `requirements.txt`. Follow the instructions in `data/README.md` to obtain the appropriate CMS dataset version. Run the notebooks in numerical order.

## Scope and Limitations

The analysis is performed at the provider level, not the individual patient or claim level. The dataset represents the specified CMS Original Medicare Part B fee-for-service reporting scope. Missing and suppressed values, top-coded fields, one-year coverage, and potential target leakage are explicitly assessed. High payments are not evidence of fraud, inappropriate billing, or poor quality.

## Responsible Use

Risk scores are exploratory prioritization aids for human review, not automated determinations of fraud, reimbursement eligibility, or provider quality.
