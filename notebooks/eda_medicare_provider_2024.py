#!/usr/bin/env python3
"""High-level EDA and data-quality audit for CMS 2024 Medicare provider file.

Usage:
  python eda_medicare_provider_2024.py --input cms_provider_2024.csv --output cms_eda_outputs

Requires pandas, numpy, matplotlib. Reads the full provider-level CSV. It does not
train a model and does not modify the source data.
"""
import argparse
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

TARGET = "Tot_Mdcr_Pymt_Amt"
ID = "Rndrng_NPI"
KEY_CATS = ["Rndrng_Prvdr_Type", "Rndrng_Prvdr_State_Abrvtn",
            "Rndrng_Prvdr_Mdcr_Prtcptg_Ind", "Rndrng_Prvdr_Ent_Cd",
            "Rndrng_Prvdr_Cntry", "Drug_Sprsn_Ind", "Med_Sprsn_Ind"]
KEY_NUMS = ["Tot_HCPCS_Cds", "Tot_Benes", "Tot_Srvcs", "Tot_Sbmtd_Chrg",
            "Tot_Mdcr_Alowd_Amt", TARGET, "Tot_Mdcr_Stdzd_Amt",
            "Bene_Avg_Age", "Bene_Avg_Risk_Scre"]
COUNT_GROUPS = {
    "age_count_fields": ["Bene_Age_LT_65_Cnt", "Bene_Age_65_74_Cnt", "Bene_Age_75_84_Cnt", "Bene_Age_GT_84_Cnt"],
    "sex_count_fields": ["Bene_Feml_Cnt", "Bene_Male_Cnt"],
    "dual_status_count_fields": ["Bene_Dual_Cnt", "Bene_Ndual_Cnt"],
    "race_count_fields": ["Bene_Race_Wht_Cnt", "Bene_Race_Black_Cnt", "Bene_Race_API_Cnt", "Bene_Race_Hspnc_Cnt", "Bene_Race_NatInd_Cnt", "Bene_Race_Othr_Cnt"],
}

def savefig(path):
    plt.tight_layout()
    plt.savefig(path, dpi=160, bbox_inches="tight")
    plt.close()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', default='cms_provider_2024.csv')
    ap.add_argument('--output', default='cms_eda_outputs')
    args = ap.parse_args()
    src = Path(args.input).expanduser().resolve()
    out = Path(args.output).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    if not src.exists():
        raise FileNotFoundError(f"Input CSV not found: {src}")

    df = pd.read_csv(src, low_memory=False)
    n, p = df.shape
    lines = []
    def note(s=''):
        lines.append(str(s))
        print(s)

    note('CMS 2024 Medicare Physician & Other Practitioners — by Provider')
    note(f'Input: {src}')
    note(f'Rows: {n:,} | Columns: {p:,} | File size: {src.stat().st_size / 1e6:.1f} MB')
    note(f'Unit of analysis: provider/NPI; unique non-null NPIs: {df[ID].nunique(dropna=True):,}')
    note(f'Exact duplicate rows: {int(df.duplicated().sum()):,}')
    note(f'Duplicate NPIs: {int(df[ID].duplicated(keep=False).sum()):,} rows involved')

    # Column-level profile and missingness
    profile = pd.DataFrame({
        'column': df.columns,
        'dtype': [str(df[c].dtype) for c in df.columns],
        'non_null_n': [int(df[c].notna().sum()) for c in df.columns],
        'missing_n': [int(df[c].isna().sum()) for c in df.columns],
        'missing_pct': [float(df[c].isna().mean()*100) for c in df.columns],
        'unique_non_null': [int(df[c].nunique(dropna=True)) for c in df.columns],
    })
    numcols = df.select_dtypes(include=np.number).columns
    profile['zero_n'] = [int((df[c] == 0).sum()) if c in numcols else np.nan for c in df.columns]
    profile['negative_n'] = [int((df[c] < 0).sum()) if c in numcols else np.nan for c in df.columns]
    profile.to_csv(out/'column_profile.csv', index=False)
    missing = profile[['column','missing_n','missing_pct']].sort_values('missing_pct', ascending=False)
    missing.to_csv(out/'missingness.csv', index=False)
    note('\nTop 15 fields by missingness:')
    note(missing.head(15).to_string(index=False, formatters={'missing_pct':'{:,.2f}%'.format}))

    # Duplicate, key and category checks
    quality = [
        ('row_count', n), ('column_count', p), ('exact_duplicate_rows', int(df.duplicated().sum())),
        ('NPI_missing', int(df[ID].isna().sum())), ('unique_NPI', int(df[ID].nunique(dropna=True))),
        ('duplicate_NPI_rows', int(df[ID].duplicated(keep=False).sum())),
        ('target_missing', int(df[TARGET].isna().sum())),
        ('target_zero', int((df[TARGET] == 0).sum())),
        ('target_negative', int((df[TARGET] < 0).sum())),
    ]
    pd.DataFrame(quality, columns=['check','value']).to_csv(out/'quality_checks.csv', index=False)

    for c in KEY_CATS:
        if c in df:
            df[c].value_counts(dropna=False).rename_axis(c).reset_index(name='count').to_csv(out/f'category_{c}.csv', index=False)
    note('\nKey categorical distributions:')
    for c in ['Rndrng_Prvdr_Type','Rndrng_Prvdr_State_Abrvtn','Rndrng_Prvdr_Mdcr_Prtcptg_Ind','Rndrng_Prvdr_Ent_Cd','Drug_Sprsn_Ind','Med_Sprsn_Ind']:
        if c in df:
            note(f'\n{c} (top 10):\n{df[c].value_counts(dropna=False).head(10).to_string()}')

    # Numeric summaries
    numeric = df.select_dtypes(include=np.number)
    numeric.describe(percentiles=[.01,.05,.10,.25,.50,.75,.90,.95,.99,.999]).T.to_csv(out/'numeric_summary.csv')
    selected = [c for c in KEY_NUMS if c in df]
    note('\nKey numeric summary:')
    note(df[selected].describe(percentiles=[.01,.05,.10,.25,.50,.75,.90,.95,.99,.999]).T.round(3).to_string())

    # Range checks: CMS chronic-condition percentages are privacy top-coded at 75 and low-count values may be suppressed.
    pctcols = [c for c in df.columns if c.endswith('_Pct')]
    pct_rows = []
    for c in pctcols:
        s = df[c]
        pct_rows.append({'column':c,'missing_n':int(s.isna().sum()),'missing_pct':float(s.isna().mean()*100),
                         'min':s.min(),'max':s.max(),'zero_n':int((s==0).sum()),
                         'below_0_n':int((s<0).sum()),'above_100_n':int((s>100).sum()),'exactly_75_n':int((s==75).sum())})
    pd.DataFrame(pct_rows).to_csv(out/'chronic_condition_percent_checks.csv', index=False)

    # Cross-field count consistency checks only where every component is observed.
    consistency=[]
    for label, cols in COUNT_GROUPS.items():
        available=[c for c in cols if c in df]
        if len(available)!=len(cols): continue
        complete=df[available].notna().all(axis=1)
        total=df[available].sum(axis=1, min_count=len(available))
        diff=(total-df['Tot_Benes']).abs()
        consistency.append({'check':label,'complete_rows':int(complete.sum()),
                            'exact_sum_matches_Tot_Benes':int(((diff==0)&complete).sum()),
                            'mismatches':int(((diff>0)&complete).sum()),
                            'missing_component_rows':int((~complete).sum()),
                            'median_abs_difference_complete':float(diff[complete].median()) if complete.any() else np.nan})
    pd.DataFrame(consistency).to_csv(out/'beneficiary_count_consistency.csv', index=False)
    note('\nBeneficiary count consistency:')
    note(pd.DataFrame(consistency).to_string(index=False))

    # Target distribution, upper-tail definitions and correlations
    target=df[TARGET]
    qlevels=[0,.01,.05,.10,.25,.50,.75,.90,.95,.99,.999,1]
    quant=target.quantile(qlevels)
    quant.rename_axis('quantile').rename('payment_amount').to_csv(out/'target_quantiles.csv')
    thresholds=[]
    for q in [.90,.95,.99]:
        th=float(target.quantile(q))
        thresholds.append({'quantile':q,'threshold':th,'n_at_or_above':int((target>=th).sum()),'pct_at_or_above':float((target>=th).mean()*100)})
    pd.DataFrame(thresholds).to_csv(out/'high_cost_threshold_candidates.csv',index=False)
    note('\nTarget payment quantiles ($):')
    note(quant.round(2).to_string())
    note('\nHigh-cost candidate thresholds:')
    note(pd.DataFrame(thresholds).round(3).to_string(index=False))

    corrcols=[c for c in ['Tot_HCPCS_Cds','Tot_Benes','Tot_Srvcs','Tot_Sbmtd_Chrg','Tot_Mdcr_Alowd_Amt','Tot_Mdcr_Stdzd_Amt','Bene_Avg_Age','Bene_Avg_Risk_Scre',TARGET] if c in df]
    df[corrcols].corr(method='spearman').to_csv(out/'spearman_correlations.csv')
    df[corrcols].corr(method='pearson').to_csv(out/'pearson_correlations.csv')
    note('\nSpearman correlation with target:')
    note(df[corrcols].corr(method='spearman')[TARGET].sort_values(ascending=False).round(4).to_string())

    # Specialty summaries
    if 'Rndrng_Prvdr_Type' in df:
        spec=df.groupby('Rndrng_Prvdr_Type', dropna=False).agg(
            provider_rows=(ID,'size'), median_payment=(TARGET,'median'), mean_payment=(TARGET,'mean'),
            p90_payment=(TARGET,lambda x:x.quantile(.9)), median_beneficiaries=('Tot_Benes','median'))
        spec.sort_values('provider_rows',ascending=False).to_csv(out/'specialty_summary.csv')
        spec.sort_values('provider_rows',ascending=False).head(15).to_csv(out/'top15_specialties.csv')

    # Visuals
    plt.figure(figsize=(9,5)); plt.hist(target.clip(upper=target.quantile(.99)), bins=60)
    plt.xlabel('Total Medicare payment ($), values capped at 99th percentile for display'); plt.ylabel('Provider count')
    plt.title('Distribution of Total Medicare Payments (display-capped at P99)')
    savefig(out/'payment_distribution_capped_p99.png')

    plt.figure(figsize=(9,5)); plt.hist(np.log1p(target), bins=60)
    plt.xlabel('log(1 + Total Medicare payment in $)'); plt.ylabel('Provider count')
    plt.title('Log-Transformed Total Medicare Payment Distribution')
    savefig(out/'payment_distribution_log1p.png')

    plt.figure(figsize=(10,7))
    m=missing.head(25).sort_values('missing_pct')
    plt.barh(m['column'],m['missing_pct'])
    plt.xlabel('Missing values (%)'); plt.title('Top 25 Fields by Missingness')
    savefig(out/'missingness_top25.png')

    top_spec=df['Rndrng_Prvdr_Type'].value_counts().head(12).index
    sp=df[df['Rndrng_Prvdr_Type'].isin(top_spec)].groupby('Rndrng_Prvdr_Type')[TARGET].median().sort_values()
    plt.figure(figsize=(10,6)); plt.barh(sp.index,sp.values)
    plt.xlabel('Median total Medicare payment ($)'); plt.title('Median Payment by Provider Type (12 most common types)')
    savefig(out/'median_payment_top_provider_types.png')

    # A concise machine-readable summary for downstream notebook/report use
    summary={
      'source_file':str(src),'rows':int(n),'columns':int(p),'file_size_mb':round(src.stat().st_size/1e6,2),
      'npi_unique':int(df[ID].nunique(dropna=True)),'duplicate_npi_rows':int(df[ID].duplicated(keep=False).sum()),
      'exact_duplicate_rows':int(df.duplicated().sum()),'target_missing':int(target.isna().sum()),
      'target_zero':int((target==0).sum()),'target_median':float(target.median()),'target_mean':float(target.mean()),
      'target_p90':float(target.quantile(.90)),'target_p95':float(target.quantile(.95)),
      'target_p99':float(target.quantile(.99)),'target_max':float(target.max()),
      'high_cost_threshold_primary_candidate':'90th percentile; finalize after reviewing research design',
      'high_cost_threshold_p90_count':int((target>=target.quantile(.90)).sum()),
      'top_missing_fields':missing.head(10).to_dict(orient='records'),
      'notes':['Provider-level public aggregate data, not individual claims/patients.',
               'Chronic-condition percentages are privacy top-coded at 75; missingness may reflect suppression/availability.',
               'Avoid using allowed/standardized payment amounts as predictors of total payment in the primary model due to target leakage.',
               'This script is EDA only; it does not fit or validate predictive models.']
    }
    (out/'eda_summary.json').write_text(json.dumps(summary,indent=2,default=str))
    (out/'eda_summary.txt').write_text('\n'.join(lines),encoding='utf-8')
    print(f'\nOutputs written to: {out}')

if __name__ == '__main__':
    main()
