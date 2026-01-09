import pandas as pd
import numpy as np
from typing import Dict, Any, List
from ..core.base import BaseDetector

class Chronologist(BaseDetector):
    @property
    def name(self) -> str:
        return "The Chronologist"

    @property
    def description(self) -> str:
        return "Time-series anomaly detection: Velocity checks and Fiscal Cliff dumping."

    def run(self, df: pd.DataFrame, date_col: str = 'date', amount_col: str = 'amount', entity_col: str = 'vendor_id') -> Dict[str, Any]:
        """
        Analyzes timing patterns of transactions.
        """
        df[date_col] = pd.to_datetime(df[date_col])
        
        results = {
            "detector_name": self.name,
            "fiscal_cliff": self.detect_fiscal_cliff(df, date_col, amount_col),
            "velocity_anomalies": self.velocity_check(df, date_col, entity_col)
        }
        return results

    def detect_fiscal_cliff(self, df: pd.DataFrame, date_col: str, amount_col: str) -> Dict[str, Any]:
        """
        Detects year-end spending spikes.
        """
        df['month'] = df[date_col].dt.month
        monthly_spending = df.groupby('month')[amount_col].sum()
        
        avg_spending = monthly_spending.mean()
        dec_spending = monthly_spending.get(12, 0)
        
        ratio = dec_spending / avg_spending if avg_spending > 0 else 0
        
        status = "Normal"
        if ratio > 2.5: status = "Extreme Dumping"
        elif ratio > 1.5: status = "Significant Increase"

        return {
            "monthly_spending": {str(k): float(v) for k, v in monthly_spending.to_dict().items()},
            "december_vs_avg_ratio": float(ratio),
            "status": status,
            "explanation": "Compares December spending to the yearly average. High ratios suggest 'budget dumping' to avoid losing funds."
        }

    def velocity_check(self, df: pd.DataFrame, date_col: str, entity_col: str) -> Dict[str, Any]:
        """
        Detects high transaction frequency.
        """
        df['date_only'] = df[date_col].dt.date
        freq = df.groupby([entity_col, 'date_only']).size().reset_index(name='count')
        
        high_velocity = freq[freq['count'] > 5].sort_values(by='count', ascending=False)
        high_velocity['date_only'] = high_velocity['date_only'].astype(str)
        
        return {
            "high_velocity_events": high_velocity.head(10).to_dict(orient='records'),
            "explanation": "Identifies entities with an unusually high volume of transactions on a single day."
        }
