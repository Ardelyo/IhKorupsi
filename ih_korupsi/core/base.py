from abc import ABC, abstractmethod
from typing import Dict, Any
import pandas as pd

class BaseDetector(ABC):
    """
    Base class for all forensic detectors in IH-Korupsi.
    Each detector must provide a deterministic mathematical explanation for its findings.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Returns the name of the detector."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Returns a brief description of the detector's logic."""
        pass

    @abstractmethod
    def run(self, df: pd.DataFrame, **kwargs) -> Dict[str, Any]:
        """
        Executes the detection logic on the provided DataFrame.
        Returns a dictionary containing findings, statistics, and flagged records.
        """
        pass

    def explain(self, finding_id: str) -> str:
        """
        Provides a mathematical explanation for a specific finding.
        Can be overridden for complex logic.
        """
        return f"Finding {finding_id} was flagged based on the {self.name} algorithm rules."
