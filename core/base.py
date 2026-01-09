from abc import ABC, abstractmethod
from typing import Dict, Any
import pandas as pd

class BaseDetector(ABC):
    """
    Kelas dasar untuk semua detektor forensik di IH-Korupsi.
    Setiap detektor harus memberikan penjelasan matematis deterministik untuk setiap flag yang dihasilkan.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Mengembalikan nama detektor."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Mengembalikan deskripsi singkat dari logika detektor."""
        pass

    @abstractmethod
    def run(self, df: pd.DataFrame, **kwargs) -> Dict[str, Any]:
        """
        Menjalankan logika deteksi pada DataFrame yang diberikan.
        Mengembalikan dictionary yang berisi temuan, statistik, dan record yang di-flag.
        """
        pass

    def explain(self, finding_id: str) -> str:
        """
        Memberikan penjelasan matematis untuk temuan spesifik.
        Bisa di-override untuk logika yang lebih kompleks.
        """
        return f"Temuan {finding_id} di-flag berdasarkan aturan algoritma {self.name}."
