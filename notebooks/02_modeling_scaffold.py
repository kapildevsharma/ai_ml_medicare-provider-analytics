#!/usr/bin/env python
"""Leakage-aware modeling scaffold for QM640 Medicare provider cost analysis.

Run after reviewing the EDA and official CMS data dictionary:
 python 02_modeling_scaffold.py --input /path/to/cms_provider_2024.csv --output outputs/modeling --sample-frac 0.05

Use a small fraction for development/runtime testing only. Final report metrics must
be generated from a documented, adequately sized run and interpreted with caution.
"""
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.dummy import DummyRegressor, DummyClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import (mean_absolute_error, mean_squared_error, r2_score,
    precision_score, recall_score, f1_score, roc_auc_score, average_precision_score,
    confusion_matrix)

TARGET = "Tot_Mdcr_Pymt_Amt"
ID_COLS = {"Rndrng_NPI", "NPI"}
LEAKAGE_TERMS = ("pymt", "payment", "alowd", "allowed", "chrg", "charge",
                 "stdzd", "standardized", "avg_mdcr", "avg_mcr")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True)
    ap.add_argument('--output', default='outputs/modeling')
    ap.add_argument('--sample-frac', type=float, default=0.05,
                    help='Development sample fraction; use 1.0 for final if resources allow')
    args = ap.parse_args()
    if not (0 < args.sample_frac <= 1):
        raise ValueError('--sample-frac must be in (0, 1].')
    source, out = Path(args.input), Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(source, low_memory=False)
    df.columns = [str(c).strip() for c in df.columns]
    if TARGET not in df.columns:
        raise KeyError(f"Target {TARGET!r} not found; inspect the exact CMS schema.")
    df[TARGET] = pd.to_numeric(df[TARGET], errors='coerce')
    df = df.dropna(subset=[TARGET])
    df = df.loc[df[TARGET] >= 0].copy()
    if args.sample_frac < 1:
        df = df.sample(frac=args.sample_frac, random_state=42)

    # Conservative name-based screen only. Manually review this list against the CMS dictionary.
    excluded = {c for c in df.columns if c in ID_COLS or c == TARGET or
                any(term in c.lower() for term in LEAKAGE_TERMS)}
    X = df.drop(columns=list(excluded), errors='ignore')
    y = df[TARGET]
    X = X.loc[:, X.notna().any(axis=0)]
    X = X.loc[:, X.nunique(dropna=True) > 1]
    cat_cols = X.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()
    num_cols = [c for c in X.columns if c not in cat_cols]
    preprocessor = ColumnTransformer([
        ('numeric', Pipeline([('impute', SimpleImputer(strategy='median')),
                              ('scale', StandardScaler())]), num_cols),
        ('categorical', Pipeline([('impute', SimpleImputer(strategy='most_frequent')),
                                  ('onehot', OneHotEncoder(handle_unknown='ignore',
                                                          min_frequency=20))]), cat_cols)
    ], remainder='drop')
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=.20, random_state=42)
    threshold = float(y_train.quantile(.90))
    y_train_cls = (y_train >= threshold).astype(int)
    y_test_cls = (y_test >= threshold).astype(int)

    regression_models = {
        'Median baseline': DummyRegressor(strategy='median'),
        'Linear regression': LinearRegression(),
        'Random forest': RandomForestRegressor(n_estimators=80, min_samples_leaf=10,
                                                random_state=42, n_jobs=-1)
    }
    reg_rows = []
    for name, estimator in regression_models.items():
        pipe = Pipeline([('preprocess', preprocessor), ('model', estimator)])
        pipe.fit(X_train, y_train)
        pred = pipe.predict(X_test)
        reg_rows.append({'model': name, 'MAE': mean_absolute_error(y_test, pred),
                         'RMSE': float(np.sqrt(mean_squared_error(y_test, pred))),
                         'R2': r2_score(y_test, pred)})
    pd.DataFrame(reg_rows).to_csv(out/'regression_metrics.csv', index=False)

    classification_models = {
        'Prior baseline': DummyClassifier(strategy='prior'),
        'Logistic regression': LogisticRegression(max_iter=1000, class_weight='balanced'),
        'Random forest': RandomForestClassifier(n_estimators=80, min_samples_leaf=10,
            class_weight='balanced_subsample', random_state=42, n_jobs=-1)
    }
    cls_rows = []
    for name, estimator in classification_models.items():
        pipe = Pipeline([('preprocess', preprocessor), ('model', estimator)])
        pipe.fit(X_train, y_train_cls)
        pred = pipe.predict(X_test)
        score = pipe.predict_proba(X_test)[:, 1] if hasattr(pipe, 'predict_proba') else pred
        cls_rows.append({'model': name,
            'precision': precision_score(y_test_cls, pred, zero_division=0),
            'recall': recall_score(y_test_cls, pred, zero_division=0),
            'F1': f1_score(y_test_cls, pred, zero_division=0),
            'ROC_AUC': roc_auc_score(y_test_cls, score),
            'average_precision': average_precision_score(y_test_cls, score),
            'confusion_matrix_tn_fp_fn_tp': confusion_matrix(y_test_cls, pred).ravel().tolist()})
    (out/'classification_metrics.json').write_text(json.dumps(cls_rows, indent=2), encoding='utf-8')
    (out/'run_manifest.json').write_text(json.dumps({
        'input_file': str(source.resolve()), 'records_after_target_filter': int(len(df)),
        'sample_fraction': args.sample_frac, 'target': TARGET,
        'threshold_quantile': .90, 'threshold_from_training_data': threshold,
        'test_size': .20, 'random_state': 42, 'excluded_columns': sorted(excluded),
        'feature_columns': X.columns.tolist(),
        'warning': 'Name-based leakage screening is incomplete; manually audit every feature.'
    }, indent=2), encoding='utf-8')
    print(f'Modeling complete. Outputs written to {out.resolve()}')

if __name__ == '__main__':
    main()
