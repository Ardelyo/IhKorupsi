import networkx as nx
import pandas as pd
from typing import Dict, Any, List, Set
from ..core.base import BaseDetector

class Connector(BaseDetector):
    @property
    def name(self) -> str:
        return "The Connector"

    @property
    def description(self) -> str:
        return "Graph-based detection for circular trading and hidden communities."

    def run(self, df: pd.DataFrame, source_col: str = 'sender_id', target_col: str = 'receiver_id', amount_col: str = 'amount') -> Dict[str, Any]:
        """
        Builds a network and analyzes connections.
        """
        G = nx.from_pandas_edgelist(df, source_col, target_col, [amount_col], create_using=nx.DiGraph())
        
        results = {
            "detector_name": self.name,
            "circular_trading": self.detect_cycles(G),
            "centrality_analysis": self.analyze_centrality(G),
            "communities": self.detect_communities(G)
        }
        return results

    def detect_cycles(self, G: nx.DiGraph) -> Dict[str, Any]:
        """
        Detects circular transaction paths.
        """
        cycles = list(nx.simple_cycles(G))
        top_cycles = cycles[:10]
        
        return {
            "cycles_count": len(cycles),
            "sample_cycles": top_cycles,
            "explanation": "Simple cycles in the graph indicate potential circular trading or money laundering loops."
        }

    def analyze_centrality(self, G: nx.DiGraph) -> Dict[str, Any]:
        """
        Identifies key actors.
        """
        pagerank = nx.pagerank(G)
        betweenness = nx.betweenness_centrality(G)
        
        top_pagerank = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:5]
        top_betweenness = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "top_influencers_pagerank": top_pagerank,
            "top_bridges_betweenness": top_betweenness,
            "explanation": "PageRank finds important entities, while Betweenness finds 'bridge' actors who control flows between groups."
        }

    def detect_communities(self, G: nx.DiGraph) -> Dict[str, Any]:
        """
        Detects clusters.
        """
        undirected_G = G.to_undirected()
        components = list(nx.connected_components(undirected_G))
        large_clusters = [list(c) for c in components if len(c) > 3]
        
        return {
            "total_clusters": len(components),
            "large_clusters_count": len(large_clusters),
            "sample_large_clusters": large_clusters[:5],
            "explanation": "Identifies groups of actors who frequently interact with each other."
        }
