import numpy as np
import pandas as pd
from typing import Dict, Any, List
from ..core.base import BaseDetector
from scipy import stats

class Mathematician(BaseDetector):
    @property
    def name(self) -> str:
        return "The Mathematician"

    @property
    def description(self) -> str:
        return "Statistical anomaly detection including Benford's Law, RSF, and Z-Score."

    def run(self, df: pd.DataFrame, amount_col: str = 'amount', entity_col: str = 'vendor_id') -> Dict[str, Any]:
        """
        Runs multiple statistical tests on transaction data.
        """
        results = {
            "detector_name": self.name,
            "benford_test": self.benford_law_test(df[amount_col]),
            "rsf_test": self.relative_size_factor(df, amount_col, entity_col),
            "statistical_outliers": self.detect_outliers(df, amount_col)
        }
        return results

    def benford_law_test(self, series: pd.Series) -> Dict[str, Any]:
        """
        Applies Benford's Law on the first digit of transaction amounts.
        """
        clean_series = series[series > 0]
        first_digits = clean_series.astype(str).str.lstrip('0. ').str[0].astype(int)
        
        counts = first_digits.value_counts().reindex(range(1, 10), fill_value=0)
        observed_freq = counts / len(first_digits)
        
        expected_freq = np.log10(1 + 1/np.arange(1, 10))
        mad = np.mean(np.abs(observed_freq - expected_freq))
        
        conformity = "High"
        if mad > 0.015: conformity = "Non-conformity"
        elif mad > 0.012: conformity = "Marginal"
        elif mad > 0.006: conformity = "Acceptable"

        return {
            "observed": observed_freq.to_dict(),
            "expected": dict(zip(range(1, 10), expected_freq)),
            "mad": float(mad),
            "conformity_status": conformity,
            "explanation": "Calculates the distribution of first digits. Significant deviation indicates potential data manipulation."
        }

    def relative_size_factor(self, df: pd.DataFrame, amount_col: str, entity_col: str) -> Dict[str, Any]:
        """
        RSF = (Largest Transaction) / (Average of Other Transactions)
        """
        grouped = df.groupby(entity_col)[amount_col].apply(list).to_dict()
        rsf_results = []

        for entity, amounts in grouped.items():
            if len(amounts) < 2:
                continue
            
            amounts = sorted(amounts)
            largest = amounts[-1]
            avg_others = np.mean(amounts[:-1])
            
            if avg_others == 0:
                rsf = 0
            else:
                rsf = largest / avg_others
            
            if rsf > 10:
                rsf_results.append({
                    "entity": entity,
                    "rsf_value": float(rsf),
                    "largest_transaction": float(largest),
                    "average_others": float(avg_others)
                })

        return {
            "high_risk_entities": sorted(rsf_results, key=lambda x: x['rsf_value'], reverse=True)[:10],
            "explanation": "RSF identifies entities whose largest transaction is significantly higher than their average."
        }

    def detect_outliers(self, df: pd.DataFrame, amount_col: str) -> Dict[str, Any]:
        """
        Outlier detection using standard Z-Score and IQR.
        """
        data = df[amount_col]
        z_scores = np.abs(stats.zscore(data))
        z_outliers = df[z_scores > 3]
        
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        iqr_outliers = df[(data < (Q1 - 1.5 * IQR)) | (data > (Q3 + 1.5 * IQR))]

        return {
            "z_score_outliers_count": len(z_outliers),
            "iqr_outliers_count": len(iqr_outliers),
            "top_outliers": z_outliers.nlargest(5, amount_col)[amount_col].to_list(),
            "explanation": "Z-Score (>3) and IQR identify statistical extremes in transaction values."
        }
