import pandas as pd
import numpy as np
from typing import Dict, Any, List
from core.base import BaseDetector

class Chronologist(BaseDetector):
    @property
    def name(self) -> str:
        return "Sang Kronolog"

    @property
    def description(self) -> str:
        return "Deteksi anomali time-series: Cek kecepatan dan Fiscal Cliff dumping."

    def run(self, df: pd.DataFrame, date_col: str = 'date', amount_col: str = 'amount', entity_col: str = 'vendor_id') -> Dict[str, Any]:
        """
        Menganalisis pola waktu dari transaksi.
        """
        df[date_col] = pd.to_datetime(df[date_col])
        
        results = {
            "nama_detektor": self.name,
            "fiscal_cliff": self.detect_fiscal_cliff(df, date_col, amount_col),
            "anomali_kecepatan": self.velocity_check(df, date_col, entity_col)
        }
        return results

    def detect_fiscal_cliff(self, df: pd.DataFrame, date_col: str, amount_col: str) -> Dict[str, Any]:
        """
        Mendeteksi lonjakan pengeluaran Desember.
        """
        df['month'] = df[date_col].dt.month
        monthly_spending = df.groupby('month')[amount_col].sum()
        
        avg_spending = monthly_spending.mean()
        dec_spending = monthly_spending.get(12, 0)
        
        ratio = dec_spending / avg_spending if avg_spending > 0 else 0
        
        status = "Normal"
        if ratio > 2.5: status = "Dumping Ekstrem"
        elif ratio > 1.5: status = "Peningkatan Signifikan"

        return {
            "pengeluaran_bulanan": {str(k): float(v) for k, v in monthly_spending.to_dict().items()},
            "rasio_desember_vs_rata_rata": float(ratio),
            "status": status,
            "penjelasan": "Membandingkan pengeluaran Desember dengan rata-rata. Rasio tinggi menunjukkan 'budget dumping'."
        }

    def velocity_check(self, df: pd.DataFrame, date_col: str, entity_col: str) -> Dict[str, Any]:
        """
        Mendeteksi frekuensi transaksi tinggi.
        """
        df['date_only'] = df[date_col].dt.date
        freq = df.groupby([entity_col, 'date_only']).size().reset_index(name='jumlah')
        
        high_velocity = freq[freq['jumlah'] > 5].sort_values(by='jumlah', ascending=False)
        high_velocity['date_only'] = high_velocity['date_only'].astype(str)
        
        return {
            "kejadian_kecepatan_tinggi": high_velocity.head(10).to_dict(orient='records'),
            "penjelasan": "Mengidentifikasi entitas dengan volume transaksi sangat tinggi dalam satu hari."
        }
