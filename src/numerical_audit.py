import pandas as pd
from pandas.api.types import is_numeric_dtype

def numerical_audit(df):
    if not isinstance(df, pd.DataFrame):
        raise TypeError('input must be a pandas dataframe')
    
    results = []
    
    for col in df.columns:
        if not is_numeric_dtype(df[col]):
            continue
        
        s = df[col]
        n = len(s)
        s_non_null = s.dropna()
        n_non_null = len(s_non_null)
        
        dtype = s.dtype
        missing_count = s.isna().sum()
        missing_rate = round(missing_count / n, 2) * 100
        mean = s.mean()
        median = s.median()
        min_val = s.min()
        max_val = s.max()
        skew = s.skew()
        q1 = s.quantile(0.25)
        q3 = s.quantile(0.75) 
        iqr = q3 - q1 
        lower = q1 - 1.5 * iqr   
        upper = q3 + 1.5 * iqr
        outlier_count = s_non_null[(s_non_null < lower) | (s_non_null > upper)].count() 
        outlier_rate = round((outlier_count / n_non_null) * 100, 2) if n_non_null else None
        
        
        stats = {
            'column_name': col,
            'data_type': dtype,
            'missing_count': missing_count,
            'missing_rate': missing_rate,
            'mean': mean,
            'median': median,
            'min_val': min_val,
            'max_val': max_val,
            'skew': skew,
            'outlier_count': outlier_count,
            'outlier_rate': outlier_rate
        }
        
        results.append(stats)
        
    return pd.DataFrame(results)