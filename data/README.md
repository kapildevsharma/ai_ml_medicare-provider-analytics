# Data Source and Handling

## Dataset

CMS Medicare Physician & Other Practitioners — by Provider (2024 reporting year), provider-level aggregate data.

Official landing page:
https://data.cms.gov/provider-summary-by-type-of-service/medicare-physician-other-practitioners/medicare-physician-other-practitioners-by-provider

API documentation:
https://data.cms.gov/provider-summary-by-type-of-service/medicare-physician-other-practitioners/medicare-physician-other-practitioners-by-provider/api-docs

Data dictionary:
https://data.cms.gov/resources/medicare-physician-other-practitioners-by-provider-data-dictionary

## Download and placement

1. Download the intended reporting-year file from the official CMS page.
2. Record the exact source version, download date, and filename in your analysis notes.
3. Place the CSV locally as `data/raw/cms_provider_2024.csv` (create the folder if needed).
4. Do not commit the raw CSV unless the course requirements and dataset license/terms have been reviewed and publishing the file is appropriate. Prefer documenting the official source and reproducible download steps.

## Unit of analysis and scope

The unit of analysis is the provider/NPI row in the CMS aggregate file, not an individual patient or claim. Interpret results within the dataset's Original Medicare Part B fee-for-service reporting scope. Do not generalize directly to Medicare Advantage, Medicaid, commercial coverage, or all U.S. healthcare spending.

## Data-quality cautions

- Missing, suppressed, and top-coded values are not equivalent to zero.
- Inspect the CMS data dictionary before recoding any field.
- Investigate outliers; do not automatically classify high payments as errors or improper billing.
- Avoid target leakage when predicting `Tot_Mdcr_Pymt_Amt`; payment-related variables should be excluded from the primary feature set unless there is a clearly justified, prospective use case.
- Provider-level associations do not establish causality, fraud, waste, or provider quality.
