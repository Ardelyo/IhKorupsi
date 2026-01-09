import pandas as pd
from typing import Dict, Any, List, Tuple
from core.base import BaseDetector

class StringDetective(BaseDetector):
    @property
    def name(self) -> str:
        return "Detektif String"

    @property
    def description(self) -> str:
        return "Mendeteksi nama entitas yang hampir sama (Vendor Hantu)."

    def run(self, df: pd.DataFrame, name_col: str = 'vendor_name') -> Dict[str, Any]:
        """
        Mengidentifikasi nama yang mirip.
        """
        unique_names = df[name_col].unique().tolist()
        potential_duplicates = []
        
        for i in range(len(unique_names)):
            for j in range(i + 1, len(unique_names)):
                name1 = str(unique_names[i])
                name2 = str(unique_names[j])
                score = self.levenshtein_ratio(name1.lower(), name2.lower())
                
                if 0.85 <= score < 1.0:
                    potential_duplicates.append({
                        "nama_1": name1,
                        "nama_2": name2,
                        "skor_kemiripan": float(score)
                    })

        return {
            "nama_detektor": self.name,
            "potensi_vendor_hantu": sorted(potential_duplicates, key=lambda x: x['skor_kemiripan'], reverse=True)[:20],
            "penjelasan": "Menemukan nama dengan kesamaan tinggi. Ini sering mengungkap 'Vendor Hantu'."
        }

    def levenshtein_ratio(self, s1: str, s2: str) -> float:
        """
        Rasio jarak Levenshtein.
        """
        rows = len(s1) + 1
        cols = len(s2) + 1
        distance = [[0 for _ in range(cols)] for _ in range(rows)]

        for i in range(1, rows):
            distance[i][0] = i
        for i in range(1, cols):
            distance[0][i] = i

        for col in range(1, cols):
            for row in range(1, rows):
                if s1[row-1] == s2[col-1]:
                    cost = 0
                else:
                    cost = 1
                distance[row][col] = min(distance[row-1][col] + 1,
                                     distance[row][col-1] + 1,
                                     distance[row-1][col-1] + cost)

        ratio = ((len(s1) + len(s2)) - distance[row][col]) / (len(s1) + len(s2))
        return ratio
