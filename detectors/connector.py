import networkx as nx
import pandas as pd
from typing import Dict, Any, List, Set
from core.base import BaseDetector

class Connector(BaseDetector):
    @property
    def name(self) -> str:
        return "Sang Penghubung"

    @property
    def description(self) -> str:
        return "Deteksi berbasis graf untuk perdagangan memutar dan komunitas tersembunyi."

    def run(self, df: pd.DataFrame, source_col: str = 'sender_id', target_col: str = 'receiver_id', amount_col: str = 'amount') -> Dict[str, Any]:
        """
        Membangun jaringan dan menganalisis koneksi.
        """
        G = nx.from_pandas_edgelist(df, source_col, target_col, [amount_col], create_using=nx.DiGraph())
        
        results = {
            "nama_detektor": self.name,
            "perdagangan_memutar": self.detect_cycles(G),
            "analisis_sentralitas": self.analyze_centrality(G),
            "komunitas": self.detect_communities(G)
        }
        return results

    def detect_cycles(self, G: nx.DiGraph) -> Dict[str, Any]:
        """
        Mendeteksi jalur transaksi memutar.
        """
        cycles = list(nx.simple_cycles(G))
        top_cycles = cycles[:10]
        
        return {
            "jumlah_siklus": len(cycles),
            "sampel_siklus": top_cycles,
            "penjelasan": "Siklus sederhana dalam graf mengindikasikan potensi perdagangan memutar atau pencucian uang."
        }

    def analyze_centrality(self, G: nx.DiGraph) -> Dict[str, Any]:
        """
        Mengidentifikasi aktor kunci.
        """
        pagerank = nx.pagerank(G)
        betweenness = nx.betweenness_centrality(G)
        
        top_pagerank = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:5]
        top_betweenness = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "pengaruh_tertinggi_pagerank": top_pagerank,
            "jembatan_teratas_betweenness": top_betweenness,
            "penjelasan": "PageRank menemukan entitas penting, sedangkan Betweenness menemukan aktor 'jembatan'."
        }

    def detect_communities(self, G: nx.DiGraph) -> Dict[str, Any]:
        """
        Mendeteksi kluster.
        """
        undirected_G = G.to_undirected()
        components = list(nx.connected_components(undirected_G))
        large_clusters = [list(c) for c in components if len(c) > 3]
        
        return {
            "total_kluster": len(components),
            "jumlah_kluster_besar": len(large_clusters),
            "sampel_kluster_besar": large_clusters[:5],
            "penjelasan": "Mengidentifikasi kelompok aktor yang sering berinteraksi satu sama lain."
        }
