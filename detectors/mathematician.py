import numpy as np
import pandas as pd
from typing import Dict, Any, List
from core.base import BaseDetector
from scipy import stats

class Mathematician(BaseDetector):
    @property
    def name(self) -> str:
        return "Sang Matematikawan"

    @property
    def description(self) -> str:
        return "Deteksi anomali statistik termasuk Hukum Benford, RSF, dan Z-Score."

    def run(self, df: pd.DataFrame, amount_col: str = 'amount', entity_col: str = 'vendor_id') -> Dict[str, Any]:
        """
        Menjalankan beberapa tes statistik pada data transaksi.
        """
        results = {
            "nama_detektor": self.name,
            "uji_benford": self.benford_law_test(df[amount_col]),
            "uji_rsf": self.relative_size_factor(df, amount_col, entity_col),
            "pencilan_statistik": self.detect_outliers(df, amount_col)
        }
        return results

    def benford_law_test(self, series: pd.Series) -> Dict[str, Any]:
        """
        Menerapkan Hukum Benford pada digit pertama dari nilai transaksi.
        """
        clean_series = series[series > 0]
        first_digits = clean_series.astype(str).str.lstrip('0. ').str[0].astype(int)
        
        counts = first_digits.value_counts().reindex(range(1, 10), fill_value=0)
        observed_freq = counts / len(first_digits)
        
        expected_freq = np.log10(1 + 1/np.arange(1, 10))
        mad = np.mean(np.abs(observed_freq - expected_freq))
        
        kesesuaian = "Tinggi"
        if mad > 0.015: kesesuaian = "Tidak Sesuai"
        elif mad > 0.012: kesesuaian = "Marginal"
        elif mad > 0.006: kesesuaian = "Dapat Diterima"

        return {
            "observasi": observed_freq.to_dict(),
            "ekspektasi": dict(zip(range(1, 10), expected_freq)),
            "mad": float(mad),
            "status_kesesuaian": kesesuaian,
            "penjelasan": "Menghitung distribusi digit pertama. Penyimpangan signifikan mengindikasikan potensi manipulasi data."
        }

    def relative_size_factor(self, df: pd.DataFrame, amount_col: str, entity_col: str) -> Dict[str, Any]:
        """
        RSF = (Transaksi Terbesar) / (Rata-rata Transaksi Lainnya)
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
                    "entitas": entity,
                    "nilai_rsf": float(rsf),
                    "transaksi_terbesar": float(largest),
                    "rata_rata_lainnya": float(avg_others)
                })

        return {
            "entitas_risiko_tinggi": sorted(rsf_results, key=lambda x: x['nilai_rsf'], reverse=True)[:10],
            "penjelasan": "RSF mengidentifikasi entitas yang transaksi terbesarnya jauh lebih tinggi dari rata-ratanya."
        }

    def detect_outliers(self, df: pd.DataFrame, amount_col: str) -> Dict[str, Any]:
        """
        Deteksi outlier menggunakan Z-Score dan IQR.
        """
        data = df[amount_col]
        z_scores = np.abs(stats.zscore(data))
        z_outliers = df[z_scores > 3]
        
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        iqr_outliers = df[(data < (Q1 - 1.5 * IQR)) | (data > (Q3 + 1.5 * IQR))]

        return {
            "jumlah_pencilan_z_score": len(z_outliers),
            "jumlah_pencilan_iqr": len(iqr_outliers),
            "pencilan_teratas": z_outliers.nlargest(5, amount_col)[amount_col].to_list(),
            "penjelasan": "Z-Score (>3) dan IQR mengidentifikasi nilai ekstrem dalam transaksi."
        }
