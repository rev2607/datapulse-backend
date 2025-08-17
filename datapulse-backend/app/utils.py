import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

# ---- Outlier Detection (IQR) ----
def detect_outliers_iqr(df: pd.DataFrame):
    outlier_report = {}
    for col in df.select_dtypes(include=[np.number]).columns:
        # Drop NaN values for calculation
        col_clean = df[col].dropna()
        if len(col_clean) < 3:  # Need at least 3 values
            outlier_report[col] = 0
            continue
            
        Q1 = col_clean.quantile(0.25)
        Q3 = col_clean.quantile(0.75)
        IQR = Q3 - Q1
        lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
        outliers = col_clean[(col_clean < lower) | (col_clean > upper)].count()
        outlier_report[col] = int(outliers)
    return outlier_report

# ---- Outlier Detection (Isolation Forest) ----
def detect_outliers_iforest(df: pd.DataFrame):
    numeric = df.select_dtypes(include=[np.number])
    if numeric.shape[1] == 0:
        return {}
    
    # Drop rows with NaN values for Isolation Forest
    numeric_clean = numeric.dropna()
    if len(numeric_clean) < 10:  # Need sufficient data
        return {"outlier_count": 0, "note": "insufficient_clean_data"}
    
    clf = IsolationForest(contamination=0.05, random_state=42)
    preds = clf.fit_predict(numeric_clean)
    outlier_idx = np.where(preds == -1)[0]
    return {"outlier_count": int(len(outlier_idx))}

# ---- Population Stability Index (PSI) ----
def calculate_psi(expected, actual, buckets=10):
    def scale_series(s):
        return pd.qcut(s, buckets, duplicates="drop").value_counts(normalize=True).sort_index()
    
    expected_dist = scale_series(expected)
    actual_dist = scale_series(actual)
    psi = np.sum((expected_dist - actual_dist) * np.log((expected_dist + 1e-6) / (actual_dist + 1e-6)))
    return psi

def drift_check(old_df: pd.DataFrame, new_df: pd.DataFrame):
    drift_report = {}
    for col in new_df.select_dtypes(include=[np.number]).columns:
        if col in old_df.columns:
            # Ensure both series have enough data and no NaN values
            old_clean = old_df[col].dropna()
            new_clean = new_df[col].dropna()
            
            if len(old_clean) >= 5 and len(new_clean) >= 5:  # Need sufficient data
                psi = calculate_psi(old_clean, new_clean)
                drift_report[col] = round(psi, 3)
            else:
                drift_report[col] = "insufficient_data"
    return drift_report

# ---- Combined Analyzer ----
def analyze_csv(df: pd.DataFrame, prev_df: pd.DataFrame = None):
    schema = {col: str(dtype) for col, dtype in df.dtypes.items()}
    
    # Handle NaN values in summary stats
    summary_raw = df.describe(include="all").to_dict()
    summary = {}
    for col, stats in summary_raw.items():
        summary[col] = {}
        for stat_name, stat_value in stats.items():
            if pd.isna(stat_value):
                summary[col][stat_name] = None
            elif isinstance(stat_value, (np.integer, np.floating)):
                summary[col][stat_name] = float(stat_value)
            else:
                summary[col][stat_name] = stat_value
    
    missing = df.isnull().sum().to_dict()

    total_missing = df.isnull().sum().sum()
    total_cells = df.shape[0] * df.shape[1]
    score = round(100 * (1 - total_missing / total_cells), 2) if total_cells else 100

    return {
        "schema": schema,
        "summary": summary,
        "missing": missing,
        "health_score": score,
        "outliers_iqr": detect_outliers_iqr(df),
        "outliers_iforest": detect_outliers_iforest(df),
        "drift": drift_check(prev_df, df) if prev_df is not None else None
    }
