import json
from typing import List, Dict, Any
import pandas as pd
from .base import BaseDetector
from ..detectors.mathematician import Mathematician
from ..detectors.connector import Connector
from ..detectors.chronologist import Chronologist
from ..detectors.string_detective import StringDetective

class FraudEngine:
    """
    Orchestration layer for IH-Korupsi.
    """
    def __init__(self):
        self.detectors: List[BaseDetector] = [
            Mathematician(),
            Connector(),
            Chronologist(),
            StringDetective()
        ]

    def process(self, df: pd.DataFrame) -> Dict[str, Any]:
        full_report = {
            "metadata": {
                "total_rows": len(df),
                "total_amount": float(df['amount'].sum()),
                "currency": "IDR"
            },
            "findings": {}
        }

        for detector in self.detectors:
            print(f"Running {detector.name}...")
            try:
                full_report["findings"][detector.name] = detector.run(df)
            except Exception as e:
                full_report["findings"][detector.name] = {"error": str(e)}

        return full_report

    def save_report(self, report: Dict[str, Any], output_path: str):
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=4)
        print(f"Report saved to {output_path}")
