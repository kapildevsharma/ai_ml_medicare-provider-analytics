from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from pathlib import Path
import json, os
base=Path('/mnt/data')
out=base/'QM640_Capstone_Interim_Report_Rubric_Expanded.pdf'
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='TTitle',parent=styles['Title'],fontName='Times-Bold',fontSize=17,leading=23,alignment=TA_CENTER,spaceAfter=18))
styles.add(ParagraphStyle(name='Center12',parent=styles['Normal'],fontName='Times-Roman',fontSize=12,leading=24,alignment=TA_CENTER))
styles.add(ParagraphStyle(name='H1A',parent=styles['Heading1'],fontName='Times-Bold',fontSize=14,leading=20,spaceBefore=10,spaceAfter=8,keepWithNext=True))
styles.add(ParagraphStyle(name='H2A',parent=styles['Heading2'],fontName='Times-Bold',fontSize=12,leading=18,spaceBefore=8,spaceAfter=5,keepWithNext=True))
styles.add(ParagraphStyle(name='BA',parent=styles['BodyText'],fontName='Times-Roman',fontSize=11.5,leading=21,spaceAfter=8))
styles.add(ParagraphStyle(name='CA',parent=styles['BodyText'],fontName='Times-Italic',fontSize=9,leading=12,spaceAfter=7))
styles.add(ParagraphStyle(name='TH',parent=styles['BodyText'],fontName='Times-Bold',fontSize=8,leading=10))
styles.add(ParagraphStyle(name='TC',parent=styles['BodyText'],fontName='Times-Roman',fontSize=8,leading=10))
def P(t,s='BA'): return Paragraph(t,styles[s])
def T(headers,rows,widths):
 d=[[P(str(x),'TH') for x in headers]]+[[P(str(x),'TC') for x in r] for r in rows]
 t=Table(d,colWidths=widths,repeatRows=1,hAlign='LEFT')
 t.setStyle(TableStyle([('GRID',(0,0),(-1,-1),.4,colors.grey),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E9EDF2')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
 return t
story=[]
story += [Spacer(1,1.05*inch),P('Predicting Medicare Payment Costs and Identifying High-Cost Provider Patterns Using Machine Learning','TTitle'),P('Ungraded Capstone Interim Report — Expanded Draft Submission','Center12'),Spacer(1,.35*inch),P('Kapil Dev Sharma','Center12'),P('Walsh College','Center12'),P('QM640: Data Analytics Capstone','Center12'),P('Mentor: Sharath Srivatsa','Center12'),P('Fall 2026 Term','Center12'),P('October 20, 2026','Center12'),Spacer(1,.35*inch),P('Prepared for mentor feedback. This is an interim draft, not a final model-results report. Preliminary EDA statistics are based on the current project EDA outputs; model performance is intentionally marked pending until validated experiments are completed.','CA'),PageBreak()]
story += [P('Repository and Report Guide','H1A'),P('GitHub repository: <link href="https://github.com/kapildevsharma/ai_ml_medicare-provider-analytics" color="blue">https://github.com/kapildevsharma/ai_ml_medicare-provider-analytics</link>. Before submission, confirm public access and verify that code, instructions, output files, and the data dictionary mapping are present. If the raw file is too large or should not be redistributed, include a CMS download URL and reproducible download instructions instead.','BA'),P('This standalone interim report documents the project problem, literature, source data, data-quality checks, EDA, sample-size rationale, planned modeling and validation, limitations, and next steps. Appendix A lists reproducible execution commands. The EDA pipeline and prior output files are not equivalent to validated predictive model results.','BA'),P('Table of Contents','H1A')]
for x in ['1. Introduction and Project Status','2. Problem, Purpose, Scope, and Objectives','3. Research Questions and Hypotheses','4. Literature Review and Method Synthesis','5. Data Source and Dataset Description','6. Data Dictionary and Variable Roles','7. Data Cleaning and Preprocessing','8. Exploratory Data Analysis and Interpretation','9. Sample Size, Power, and Confidence Intervals','10. Modeling Strategy and Feature Engineering','11. Evaluation Metrics and Validation','12. Preliminary Findings by Research Question','13. Limitations, Ethics, and Validity','14. Next Steps','References','Appendix A. Reproducible EDA Execution','Appendix B. Rubric Coverage Checklist']:
 story.append(P(x))
story.append(PageBreak())

sections=[
('1. Introduction and Project Status',[
'Medicare payment analysis matters because public provider-level data can help describe the relationship between provider practice characteristics, service utilization, beneficiary mix, and payment totals. However, payment amount is not a direct measure of quality, waste, or fraud. Higher payments may reflect legitimate differences in specialty, service volume, patient complexity, geographic practice conditions, or procedure mix. This project treats high payments as a pattern for statistical investigation and possible human review, not as proof of wrongdoing.',
'The Centers for Medicare & Medicaid Services (CMS) publishes the Medicare Physician & Other Practitioners—by Provider public-use file. The file describes Original Medicare fee-for-service Part B utilization, payments, submitted charges, and selected aggregated beneficiary characteristics by rendering provider NPI. CMS states that data elements representing fewer than 11 beneficiaries are suppressed to protect privacy; therefore, some missingness is structural rather than ordinary data loss (CMS, 2026a, 2026b).',
'Problem statement. The provider file contains many records and variables, but the target payment distribution is strongly right-skewed, multiple beneficiary fields have substantial missingness or suppression, and related payment variables may be almost mathematical substitutes for the target. If these issues are not handled, analyses may be misleading and predictive models may appear successful because of target leakage. The project develops a reproducible quality-first workflow and evaluates whether non-leaky provider and utilization features can predict payment variation and identify high-cost records.',
'Purpose. The study will describe payment distribution, test associations between payment and provider/utilization/beneficiary characteristics, compare baseline and machine-learning prediction methods, and evaluate whether a ranked list could prioritize limited review capacity. The output is a research prototype, not a deployed compliance system.',
'Interim status: completed in the existing project outputs—schema profile, exact-duplicate check, provider identifier checks, target missingness and zero checks, missingness summaries, descriptive target statistics, categorical frequency summaries, target correlation screening, and selected consistency diagnostics. In progress—re-running the EDA against the exact file, validating field definitions, finalizing the non-leaky feature list, and preparing modeling pipelines. Pending—model training, tuning, held-out evaluation, ranking evaluation, uncertainty estimates, final recommendations, and mentor feedback integration.'
]),
('2. Problem, Purpose, Scope, and Objectives',[
'Scope. The unit of analysis is one provider-level aggregate record in the selected 2024 CMS file. The project does not join beneficiary-level records, infer individual patient outcomes, estimate causal effects, or determine fraudulent billing. Findings apply first to the published file and year; generalization to future years requires temporal validation.',
'Objectives: (1) profile payment amounts, utilization, missingness, and anomalies; (2) compare payment distributions across selected provider categories and geography; (3) identify non-leaky features associated with payment; (4) compare baseline, linear, and tree-based regression; (5) compare a dummy classifier, logistic regression, and tree ensemble for a training-defined high-cost label; (6) measure top-k capture for review prioritization; and (7) document reproducible code and limitations.',
'Feasibility. The source is publicly accessible, the reported file has about 1.3 million rows and 76 columns, and the existing Python environment includes pandas, NumPy, matplotlib, SciPy, statsmodels, and scikit-learn. The file is large but manageable with staged loading, selected columns, efficient dtypes, and a first EDA run before model fitting. The main constraints are runtime, missingness, definition consistency, and target leakage.',
'Stakeholders include the student researcher and mentor, academic reviewers, analysts interested in Medicare payment patterns, and potential reviewers who may use aggregate risk scores only as a triage aid. Any downstream use would require governance, validation, human review, and careful communication of uncertainty.'
]),
('3. Research Questions and Hypotheses',[
'RQ1: What provider characteristics, healthcare utilization measures, and beneficiary health characteristics are associated with differences in Medicare payment costs? Planned evidence: stratified distributions, effect sizes, confidence intervals, and group-comparison tests chosen after checking assumptions.',
'RQ2: Which provider, utilization, and beneficiary health characteristics predict Medicare payment amounts? Planned evidence: regression coefficients, out-of-sample error, tree-based importance, and sensitivity analysis after excluding payment-adjacent predictors.',
'RQ3: Which model most accurately identifies high-cost Medicare providers? Planned label: total payment at or above the 90th percentile calculated on training data only. Planned comparison: dummy baseline, logistic regression, random forest or gradient boosting; metrics include recall, precision, F1, ROC-AUC, and average precision.',
'RQ4: Can provider-level risk scoring prioritize providers for payment/utilization review? Planned evidence: precision@5%, @10%, @20%, recall@k, and lift compared with random selection or an unranked review baseline.',
'Hypotheses (provisional): H1—payment distributions differ across provider groups and utilization levels; H2—available non-leaky provider and utilization features provide predictive signal beyond a median/mean baseline; H3—at least one validated model improves high-cost identification over a dummy baseline on held-out data; H4—ranking by predicted risk captures a greater share of high-cost providers within fixed review capacity than random selection. These are hypotheses to test, not conclusions.'
]),
('4. Literature Review and Method Synthesis',[
'Source selection. This interim review prioritizes official CMS documentation, foundational peer-reviewed machine-learning methods, predictive-modeling texts, and primary software documentation. Search themes include Medicare provider payments, administrative healthcare data, regression, random forests, gradient boosting, model validation, classification metrics, and interpretability. For the final report, expand the empirical healthcare-cost literature through the college library and record the databases, search dates, search terms, and inclusion criteria.',
'CMS documentation establishes the scope and meaning of the source. The dataset covers Original Medicare fee-for-service Part B and selected aggregated beneficiary attributes, rather than all healthcare spending or every payer (CMS, 2026a). The dictionary is essential for distinguishing actual missing values from suppression, interpreting payment fields, and validating cross-field arithmetic (CMS, 2026b).',
'Ordinary least squares regression is a useful interpretable baseline, but a skewed target and nonlinear relationships can violate its assumptions. A log1p target transformation may stabilize scale, but results must be back-transformed and assessed in dollars. Random forests aggregate decision trees and can represent nonlinear relationships and interactions (Breiman, 2001). Gradient boosting builds an additive model by iteratively reducing prediction errors (Friedman, 2001). Neither method is automatically superior; both can overfit and require held-out comparison.',
'Predictive modeling guidance emphasizes separating training and evaluation data, fitting preprocessing only within training folds, and selecting metrics aligned to the task (James et al., 2021; Kuhn & Johnson, 2013). Scikit-learn provides standard, reproducible implementations of preprocessing, cross-validation, and evaluation metrics (Pedregosa et al., 2011; scikit-learn developers, 2026). SHAP is a framework for explaining model outputs, but feature attributions are not causal effects (Lundberg & Lee, 2017).',
'Synthesis and gap. A high observed payment, a predictable payment, and an improper payment are different concepts. CMS public-use data does not supply a definitive ground-truth fraud label. Therefore, this study focuses on payment prediction and review prioritization, not fraud classification. Its methodological contribution is a leakage-aware workflow that combines data-quality checks, transparent baselines, multiple metrics, explicit uncertainty, and cautious interpretation.'
]),
('5. Data Source and Dataset Description',[
'Official dataset: CMS, Medicare Physician & Other Practitioners—by Provider, 2024. Dataset page: https://data.cms.gov/provider-summary-by-type-of-service/medicare-physician-other-practitioners/medicare-physician-other-practitioners-by-provider. Data dictionary: https://data.cms.gov/resources/medicare-physician-other-practitioners-by-provider-data-dictionary. API documentation: https://data.cms.gov/provider-summary-by-type-of-service/medicare-physician-other-practitioners/medicare-physician-other-practitioners-by-provider/api-docs (CMS, 2026a, 2026b).',
'The local CSV profiled for the project contains 1,296,739 rows and 76 columns. This is the exact file-specific profile reported in the current EDA summary. CMS webpages can show a different current row/column count as data releases are updated, so the final report must identify the downloaded file, download date, and checksum and must not silently mix versions.',
'Unit of analysis: provider-level aggregate row, keyed by rendering provider NPI. Target: Tot_Mdcr_Pymt_Amt, total Medicare payment amount. NPI is an identifier used for data quality checks, never a numeric feature. The dataset is a public-use administrative summary; aggregate values should not be interpreted as beneficiary-level observations.',
'Coverage limitation: it represents Original Medicare fee-for-service Part B as described by CMS, not Medicare Advantage claims, all private insurance, all healthcare spending, or clinical quality. Small beneficiary counts can be suppressed. Provider payment totals may be affected by legitimate differences in practice size, service mix, and beneficiary characteristics.'
]),
('6. Data Dictionary and Variable Roles',[
'Table 1 summarizes the principal variable groups. The complete field-level dictionary must be mapped against the exact downloaded file and official CMS dictionary before final modeling.',
]),
('7. Data Cleaning and Preprocessing',[
'Duplicates and keys. The current EDA summary reports zero exact duplicate rows, zero missing provider identifiers, and zero duplicate non-null provider identifiers. These checks must be rerun from the exact file. If duplicates appear, inspect the data grain before removal; do not remove rows solely because they look unusual.',
'Missingness. The reported target has no missing values. Med_Sprsn_Ind and Drug_Sprsn_Ind each have 1,145,043 missing values (88.30%). Several beneficiary race and health-condition fields have roughly 65%–82% missingness. Because CMS suppression is related to small beneficiary counts, missingness may not be random. Never replace suppression with zero. Verify definitions and use complete-enough feature sets or train-fold imputers with missing indicators where justified.',
'Outliers. The reported target maximum is $306,357,782.68 and the 99th percentile is $1,141,640.46. The mean ($92,584.47) is far above the median ($26,513.00), showing a long right tail. Extreme records must be investigated but not automatically dropped or winsorized. Use log-scale plots, robust summaries, MAE and RMSE, and segment-level errors.',
'Leakage. Spearman screening reported correlations above 0.99 between the target and payment-adjacent fields. Allowed, standardized, average payment, and charge totals may encode nearly the same underlying amount. Exclude them from primary predictors when predicting total payment; otherwise the model may reconstruct the target rather than generalize. Document all exclusions.',
'Reproducible preprocessing. Preserve raw data, write outputs to separate folders, log package versions and random seeds, parse numeric columns explicitly, encode categories in a pipeline, and fit imputers/encoders/scalers only on training folds. Generate a column profile, missingness table, numeric summaries, target quantiles, cross-field diagnostics, and labeled figures. The accompanying code is an EDA pipeline, not a completed model-training pipeline.'
]),
('8. Exploratory Data Analysis and Interpretation',[
'Table 2. Reported target distribution. Mean $92,584.47; median $26,513.00; 75th percentile $66,672.41; 90th percentile $151,995.92; 95th percentile $261,353.12; 99th percentile $1,141,640.46; maximum $306,357,782.68. The mean is approximately 3.5 times the median and the 99th percentile is over 43 times the median. This is strong evidence of right skew and motivates quantile summaries, log-scale visualizations, robust error metrics, and sensitivity analysis.',
'The 90th percentile is a candidate threshold for high-cost classification, but the final threshold must be computed from the training split only. The reported $151,995.92 value is descriptive for the current complete file and should not be reused blindly after screening or train/test splitting.',
'Missingness results indicate that suppression indicators and several beneficiary characteristics are incomplete for most records. This constrains RQ1 and RQ2: analyses using those fields may describe only a subset and may be biased toward records with larger beneficiary counts. Report the denominator for every group comparison and compare included versus excluded records where feasible.',
'Categorical summaries displayed Nurse Practitioner as the most common provider type and California as the most common displayed state. These are frequency facts only; they do not show that these groups have the highest payment. Compare distributions and per-provider payment metrics, not raw counts alone.',
'The completed-case consistency checks in the current EDA output found no mismatches: age-band counts matched Tot_Benes in 532,533 rows where all age components were available; sex counts matched in 1,120,401 rows; dual-status counts matched in 832,257 rows; and six race-count fields matched in 78,681 rows. These are conditional checks on complete cases, not evidence that suppressed or missing components sum correctly. The small complete-case denominator for race fields limits race-specific inference.',
'RQ implications: RQ1 requires stratified distribution and effect-size analysis; RQ2 requires a verified non-leaky feature set; RQ3 requires class-imbalance-aware classification metrics; RQ4 requires top-k ranking measures. These observations are preliminary EDA findings, not validated causal explanations.'
]),
('9. Sample Size, Power, and Confidence Intervals',[
'The file is a large released administrative extract, so the primary analysis should use all eligible records after documented quality screening. Sample-size planning is still required by the rubric to show inferential assumptions and to support any smaller audit or validation sample. Distinguish inference about the released 2024 file from generalization to future years.',
'RQ1 group comparisons: a worked planning calculation uses one-way ANOVA, k=10 provider groups as a provisional planning assumption, Cohen f=.10, alpha=.05, and power=.80. Statsmodels FTestAnovaPower gives total N≈1,574 (rounded up from 1,573.46), assuming balanced independent groups and ANOVA assumptions. Replace k=10 with the actual groups used in the final test. If assumptions fail, use Kruskal–Wallis or robust methods. Given the large sample, report effect sizes and confidence intervals rather than treating tiny p-values as important by themselves.',
'RQ2 regression: a worked planning calculation assumes 20 tested predictors, Cohen f²=.02, alpha=.05, and power=.80 using the overall multiple-regression F test. A noncentral-F calculation gives N≈1,064 (df1=20, df2=N−21). This is a planning approximation and must be recalculated if the final predictor count or test changes. The complete dataset is much larger than this minimum, so use all eligible data where feasible and use bootstrap intervals or cross-validation for predictive uncertainty.',
'RQ3 classification: define high cost as at or above the training-set 90th percentile. For estimating a proportion with 95% confidence and ±3 percentage-point margin under conservative p=.50, n=z²p(1-p)/e² = 1.96²×.25/.03² = 1,067.1, rounded up to 1,068 independent observations. This is a proportion-estimation planning value, not a full classifier power analysis. At approximately 10% prevalence, a 20% holdout from 1,296,739 records would contain roughly 25,935 positives before any filtering, but the actual count must be measured after splitting. The test set must include enough positive cases for stable recall and precision estimates.',
'RQ4 ranking: for a simple proportion estimate with 95% confidence and ±3 percentage-point margin under p=.50, n=1,068. This does not directly power a difference in top-k capture; a paired bootstrap or simulation-based power analysis should be used once the minimum meaningful improvement in recall@k is specified. Ranking utility depends on review capacity and positive prevalence. Report precision@5%, @10%, @20%, recall@k, lift@k, and bootstrap confidence intervals. For every RQ, state alpha, power or confidence level, effect-size/margin assumptions, and exact software result in the final report.'
]),
('10. Modeling Strategy and Feature Engineering',[
'Model 1, baseline regression: predict the training-set median payment for every test record. This provides a robust reference and is particularly useful for MAE. A mean baseline may also be included for comparison. Model 2, linear/log-linear regression: use a transparent linear baseline; assess residuals and compare original-dollar errors. Model 3, random forest or gradient boosting: model nonlinearities and interactions. These candidates should be compared on the same split and feature set.',
'Classification baseline: use DummyClassifier with a documented strategy. Compare logistic regression with a random forest or gradient-boosted classifier. If the positive class is the top 10% by payment, report the prevalence and use class weights or threshold tuning only within training folds. Do not optimize the final test threshold.',
'Candidate features: provider type, state/geography, practice-setting fields, service counts, beneficiary counts, and selected beneficiary mix/health measures after dictionary verification. Exclude NPI, names, direct target-derived fields, allowed/standardized/average payment totals, and fields unavailable at the time of intended prediction. Correlated variables should be reviewed; VIF or correlation diagnostics can support regression stability checks.',
'Preprocessing: preserve category codes as strings; one-hot encode nominal categories; impute numeric predictors with training-fold medians and categories with a training-fold most-frequent value or explicit missing category; optionally use missingness indicators; consider log1p for skewed count features. All transformations must be inside Pipeline/ColumnTransformer objects and fit only within training folds.',
'Feature importance: report coefficients for the linear model and permutation importance for tree models on held-out data. SHAP may be used as a supplementary explanation if feasible, but attributions are conditional on the fitted model and correlated predictors can split importance. Neither coefficient significance nor feature importance establishes causality.'
]),
('11. Evaluation Metrics and Validation',[
'Validation plan: reserve a fixed 20% holdout with a documented random seed. For classification, stratify by the training-defined high-cost label. Conduct five-fold cross-validation within the remaining training set for tuning. The holdout is used once for final model comparison and not for feature selection or hyperparameter tuning. Since the file is one year, a future-year test is recommended if a comparable subsequent release becomes available.',
'Regression metrics: MAE=(1/n)Σ|yᵢ−ŷᵢ|; RMSE=sqrt[(1/n)Σ(yᵢ−ŷᵢ)²]; R²=1−SSE/SST. MAE reports average absolute dollar error and is less sensitive to extreme errors than RMSE. RMSE penalizes very large misses. R² measures improvement over the test mean baseline and can be negative on test data. Report original-dollar metrics even if the target is log-transformed.',
'Classification metrics: precision=TP/(TP+FP); recall=TP/(TP+FN); F1=2PR/(P+R); specificity=TN/(TN+FP); ROC-AUC summarizes ranking across thresholds; average precision summarizes the precision-recall curve. Accuracy alone is insufficient for an imbalanced top-decile label. Include a confusion matrix at a documented threshold and probability calibration if scores are interpreted as probabilities.',
'Ranking metrics: precision@k is the share of the top-k selected records that are truly high cost; recall@k is the share of all high-cost records captured within the top k; lift@k is precision@k divided by overall prevalence. These directly measure whether a fixed review capacity is used more efficiently.',
'No validated model metrics are currently available in this draft. The model comparison table should remain “pending” until the code has run and the split, features, threshold, predictions, metric calculations, and software versions are saved. Do not invent scores or describe planned results as completed findings.'
]),
('12. Preliminary Findings by Research Question',[
'RQ1: Preliminary evidence shows a strongly right-skewed target, wide differences between median and upper quantiles, high missingness in selected beneficiary fields, and variation in category frequencies. These observations motivate stratified comparisons but do not yet quantify adjusted group differences. Next, report median and quantile payment by provider type/state, effect sizes, confidence intervals, and suitable tests.',
'RQ2: The correlation screen found near-perfect associations between target and payment-adjacent fields. This is a leakage warning, not evidence that those fields are independent drivers. Next, exclude them from the primary feature set, fit baseline and tree models, and report out-of-sample errors and importance stability.',
'RQ3: The reported full-file p90 is $151,995.92, a provisional reference point only. No classifier has been validated. Next, derive p90 from training data and compare dummy, logistic, and tree-based classifiers with recall, precision, F1, ROC-AUC, and average precision.',
'RQ4: Risk ranking has not yet been evaluated. Next, compute precision@5/10/20%, recall@5/10/20%, and lift on held-out data, compare with random selection, and estimate uncertainty. The score is only a triage aid and must not be described as a fraud score.'
]),
('13. Limitations, Ethics, and Validity',[
'Data limitations include annual provider-level aggregation, coverage limited to Original Medicare fee-for-service Part B, suppression-related missingness, possible version changes, and lack of ground-truth labels for inappropriate payment. The public-use file cannot establish clinical appropriateness or causality.',
'Model limitations include possible temporal drift, high-cardinality categories, skewed targets, unstable feature importance under correlation, and class imbalance. A random holdout from one year estimates within-year generalization, not future-year performance. Outlier handling choices may materially affect results.',
'Validity depends on correct field definitions, no target leakage, proper train/test separation, and metrics aligned to the research question. Reliability improves with raw-file checksums, saved environment versions, deterministic seeds, documented feature exclusions, and reproducible outputs. Report confidence intervals and sensitivity checks where feasible.',
'Ethical use: do not publish accusatory lists or label providers as fraudulent. High payment may be legitimate. Avoid exposing unnecessary identifiers in figures, state uncertainty, and require qualified human review and corroborating evidence for any operational action. This project is an academic analysis and not a clinical or enforcement tool.'
]),
('14. Next Steps',[
'1. Record the exact CSV download date, filename, checksum, and CMS dictionary version. 2. Run the supplied EDA script in a clean environment and replace preliminary summary values with freshly generated outputs. 3. Preserve and report complete-case beneficiary consistency checks and clarify suppression semantics using the CMS dictionary. 4. Freeze the non-leaky feature list and record excluded variables. 5. Execute and save exact power calculations after defining group counts, predictor count, effect size, alpha, and power. 6. Build reproducible preprocessing pipelines. 7. Train regression baselines and tree candidates; tune only within training folds. 8. Train high-cost classifiers with a training-derived threshold. 9. Report held-out metrics, confusion matrices, residual plots, calibration, and feature importance. 10. Evaluate top-k review utility and uncertainty. 11. Expand the verified empirical literature review, incorporate mentor feedback, verify APA 7 details, and check GitHub public access before final submission.'
])]
for title,paras in sections:
 story.append(P(title,'H1A'))
 for para in paras: story.append(P(para))
 # section-specific tables
 if title.startswith('6.'):
  story.append(T(['Variable/group','Definition and type','Role','Cautions'],[
   ['Rndrng_NPI','Provider identifier; string/code','Deduplication only','Never a numeric predictor'],
   ['Tot_Mdcr_Pymt_Amt','Total Medicare payment; numeric currency','Continuous target','Check zeros, extreme values, missingness'],
   ['Provider type','CMS specialty category; categorical','RQ1 strata/predictor','One-hot encoding; inspect rare groups'],
   ['State/geography','Provider location code; categorical','RQ1 strata/predictor','Check unknown/missing codes'],
   ['Tot_Benes, Tot_Srvcs','Beneficiary/service counts; numeric counts','Utilization predictors','Collinearity and target timing must be assessed'],
   ['Bene_Avg_Age and age-band counts','Aggregated beneficiary profile; numeric','Exploratory predictor','Validate sum consistency and suppression'],
   ['Race/health condition fields','Aggregated counts or percentages; type per dictionary','Sensitivity predictors','Substantial missingness/suppression'],
   ['Allowed/standardized/payment totals','Numeric payment/charge measures','Descriptive only in primary analysis','Leakage risk when predicting total payment']
  ],[1.25*inch,1.65*inch,1.45*inch,1.65*inch]))
 if title.startswith('8.'):
  story.append(T(['Statistic','Reported result','Interpretation'],[
   ['Mean','$92,584.47','Mean exceeds median; upper tail influences average'],
   ['Median','$26,513.00','Half of provider records at or below this amount'],
   ['P75','$66,672.41','Upper quartile begins at this amount'],
   ['P90','$151,995.92','Candidate high-cost threshold; recompute on training set'],
   ['P95','$261,353.12','Sensitivity threshold for more extreme cases'],
   ['P99','$1,141,640.46','Very heavy upper tail'],
   ['Maximum','$306,357,782.68','Investigate, do not automatically delete']
  ],[1.1*inch,1.5*inch,3.4*inch]))
  for img_path, cap in [(base/'target_payment_distributions.png','Figure 1. Payment target distribution from existing EDA output. The distribution is highly right-skewed; inspect axes and captions in the original figure.'),(base/'missingness_top25.png','Figure 2. Twenty-five fields with highest missingness from existing EDA output. Suppression and beneficiary fields require dictionary review.'),(base/'payment_by_provider_type.png','Figure 3. Payment by provider type from existing EDA output. Compare medians and spread; raw category counts alone do not indicate payment risk.'),(base/'target_spearman_correlations.png','Figure 4. Spearman associations with payment target from existing EDA output. Near-perfect correlations for payment-adjacent fields are leakage warnings, not independent explanatory findings.')]:
   if img_path.exists():
    story.append(P(cap.split('. ')[0]+'. '+cap.split('. ',1)[1],'H2A'))
    story.append(Image(str(img_path),width=6.0*inch,height=3.1*inch,kind='proportional'))
    story.append(P('Interpretation: this figure is included from the current project outputs and should be regenerated from the exact data file before final submission. Use it to motivate the next analysis, not as a standalone causal conclusion.','CA'))
 if title.startswith('11.'):
  story.append(T(['Metric','Formula','Interpretation'],[
   ['MAE','(1/n)Σ|y−ŷ|','Average absolute error in dollars'],
   ['RMSE','sqrt[(1/n)Σ(y−ŷ)²]','Penalizes large misses more strongly'],
   ['R²','1−SSE/SST','Relative fit; may be negative on test data'],
   ['Precision','TP/(TP+FP)','Share of flagged providers that are high cost'],
   ['Recall','TP/(TP+FN)','Share of all high-cost providers detected'],
   ['F1','2PR/(P+R)','Harmonic balance of precision and recall'],
   ['ROC-AUC / AP','ROC area / precision-recall summary','Ranking metrics; AP useful for imbalanced class'],
   ['Precision@k / Recall@k','Top-k capture formulas','Directly answers review-capacity question']
  ],[1.0*inch,2.0*inch,3.0*inch]))
 story.append(PageBreak())

story += [P('References','H1A'),
P('Breiman, L. (2001). Random forests. <i>Machine Learning, 45</i>, 5–32. https://doi.org/10.1023/A:1010933404324'),
P('Centers for Medicare & Medicaid Services. (2026a). <i>Medicare Physician &amp; Other Practitioners—by Provider</i>. https://data.cms.gov/provider-summary-by-type-of-service/medicare-physician-other-practitioners/medicare-physician-other-practitioners-by-provider'),
P('Centers for Medicare & Medicaid Services. (2026b). <i>Medicare Physician &amp; Other Practitioners—by Provider data dictionary</i>. https://data.cms.gov/resources/medicare-physician-other-practitioners-by-provider-data-dictionary'),
P('Friedman, J. H. (2001). Greedy function approximation: A gradient boosting machine. <i>The Annals of Statistics, 29</i>(5), 1189–1232. https://doi.org/10.1214/aos/1013203451'),
P('James, G., Witten, D., Hastie, T., &amp; Tibshirani, R. (2021). <i>An introduction to statistical learning: With applications in R</i> (2nd ed.). Springer. https://www.statlearning.com/'),
P('Kuhn, M., &amp; Johnson, K. (2013). <i>Applied predictive modeling</i>. Springer. https://doi.org/10.1007/978-1-4614-6849-3'),
P('Lundberg, S. M., &amp; Lee, S.-I. (2017). A unified approach to interpreting model predictions. In <i>Advances in Neural Information Processing Systems 30</i>. https://proceedings.neurips.cc/paper/2017/hash/8a20a8621978632d76c43dfd28b67767-Abstract.html'),
P('Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., &amp; Duchesnay, É. (2011). Scikit-learn: Machine learning in Python. <i>Journal of Machine Learning Research, 12</i>, 2825–2830. https://jmlr.org/papers/v12/pedregosa11a.html'),
P('scikit-learn developers. (2026). <i>Model evaluation: Quantifying the quality of predictions</i>. https://scikit-learn.org/stable/modules/model_evaluation.html'),
P('U.S. Department of Health and Human Services. (2018). <i>Data source and methodology: CMS Program Statistics, section: Medicare providers</i>. Centers for Medicare &amp; Medicaid Services. https://www.cms.gov/research-statistics-data-and-systems/statistics-trends-and-reports/cmsprogramstatistics/downloads/med_providers_methods.pdf'),
P('APA note: verify source dates and metadata at final submission and expand the empirical literature review with directly reviewed studies on healthcare expenditure prediction and Medicare payment variation. The references above support the current methods and dataset description; they do not substitute for the final domain-specific literature review.','CA'),PageBreak(),
P('Appendix A. Reproducible EDA Execution','H1A'),
P('A companion EDA package is available as QM640_CMS_EDA_Code_and_Preliminary_Outputs.zip. The current project folder also contains cms_provider_2024.csv and earlier EDA scripts/output tables. Keep the raw CSV unchanged and write all new outputs to a separate folder.','BA'),
P('Install dependencies: <font name="Courier">python -m pip install -r requirements.txt</font>','BA'),
P('Run the existing script: <font name="Courier">python eda_medicare_provider_2024.py --help</font> (inspect its argument options first), or use the project notebook <font name="Courier">01_data_quality_eda_results_updated.ipynb</font> in Jupyter. If using a script without CLI arguments, open it and update only the input/output paths.','BA'),
P('Required outputs to preserve: data quality summary JSON, column profile, missingness table, numeric summary, category summaries, target quantiles, correlation/leakage screening, consistency checks, and labeled plots. Compare every variable with the official CMS data dictionary. Do not interpret inferred data types as authoritative.','BA'),
P('Before final submission, confirm that each figure/table in the report is generated from the same exact CSV and that the output values match. The current report deliberately labels model results as pending because the EDA pipeline alone does not train and validate models. Completed EDA consistency outputs show no mismatches among complete age, sex, dual-status, and race component rows; missing components remain a limitation.','BA'),PageBreak(),
P('Appendix B. Rubric Coverage Checklist','H1A'),
T(['Rubric criterion','Report section','Interim status'],[
['Title page, student/course/mentor/date, APA hierarchy, page numbers, tables/figures','Title page; all sections','Included; inspect final pagination and template specifics'],
['Problem, motivation, objectives, scope, variables, feasibility','Sections 1–2','Addressed'],
['10+ sources, methods comparison, gap, synthesis','Section 4 and References','Methods synthesis included; add more empirical healthcare studies'],
['Data source URL, dataset, variables/types, completeness/limits','Sections 5–6','Addressed; verify exact file dictionary'],
['Missing values, outliers, duplicates, preprocessing, reproducibility','Section 7 and Appendix A','Addressed; rerun exact pipeline'],
['Statistical summaries, visualizations, anomalies','Section 8','Reported preliminary values; replace with fresh outputs where possible'],
['Power/CI/sample size for each RQ','Section 9','Planning assumptions given; exact test-specific power values remain to calculate'],
['Labeled/readable charts','Section 8','Use generated figures from EDA output in final report'],
['Insights tied to RQs','Sections 8 and 12','Addressed provisionally'],
['Models and baseline','Section 10','Specified; not yet trained'],
['Features, transformations, importance, leakage','Sections 7 and 10','Addressed'],
['Model rationale, assumptions, alternatives','Sections 4 and 10','Addressed'],
['Metrics and validation method','Section 11','Formulas and plan included'],
['Results tables/plots and correctly reported metrics','Section 11','Model metrics pending; no scores invented'],
['Compare and interpret model performance','Sections 11–12','Pending execution'],
['Explicit RQ answers','Section 12','Status and next steps per RQ included'],
['Limitations and validity','Section 13','Addressed'],
['APA citations and references','In-text citations and References','Verify dates/APA metadata; expand empirical literature']
],[2.3*inch,1.55*inch,2.15*inch]),
P('Submission note: this is an ungraded interim draft for mentor review. Before submission, rerun the EDA against the exact dataset, replace preliminary figures/tables with reproducible outputs, finish exact test-specific power calculations, and verify APA 7 details. Submit the PDF only, as requested by the academic team.','BA')]

def footer(canvas,doc):
 canvas.saveState(); canvas.setFont('Times-Roman',9); canvas.drawRightString(letter[0]-0.7*inch,0.42*inch,str(doc.page)); canvas.restoreState()
doc=SimpleDocTemplate(str(out),pagesize=letter,leftMargin=1*inch,rightMargin=1*inch,topMargin=.8*inch,bottomMargin=.72*inch,title='QM640 Expanded Interim Report',author='Kapil Dev Sharma')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(out, out.stat().st_size)
