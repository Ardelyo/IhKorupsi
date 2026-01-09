import pandas as pd
import json
import sqlite3
from typing import Union, Optional

class DataLoader:
    """
    Menangani ingestion dari berbagai format.
    """
    @staticmethod
    def load(source: str, type: str = 'csv') -> pd.DataFrame:
        if type == 'csv':
            return pd.read_csv(source)
        elif type == 'json':
            return pd.read_json(source)
        elif type == 'sql':
            # Asumsi source adalah path ke sqlite db
            conn = sqlite3.connect(source)
            # Dalam skenario nyata, nama tabel akan dikirim sebagai parameter
            df = pd.read_sql_query("SELECT * FROM transactions", conn)
            conn.close()
            return df
        else:
            raise ValueError(f"Tipe file tidak didukung: {type}")

    @staticmethod
    def generate_sample_data(rows: int = 100) -> pd.DataFrame:
        """
        Menghasilkan data sintetis dengan anomali yang disengaja.
        """
        import random
        from datetime import datetime, timedelta

        vendors = ["PT. Maju Jaya", "PT. Maju  Jaya", "CV. Sumber Makmur", "PT. Berdikari", "Dinas Kesehatan"]
        data = []
        
        for i in range(rows):
            # Transaksi normal
            date = datetime(2025, 1, 1) + timedelta(days=random.randint(0, 360))
            amount = random.uniform(1000, 50000)
            vendor = random.choice(vendors)
            sender = "Treasury_Dept"
            
            # Menanamkan Anomali Benford (terlalu banyak angka 5)
            if i % 10 == 0:
                amount = float(f"5{random.randint(0, 9)}{random.randint(0, 9)}000")
            
            # Menanamkan Anomali RSF
            if i == 50:
                amount = 10000000
                vendor = "PT. Berdikari"

            # Menanamkan Fiscal Cliff (dumping Desember)
            if i > 80:
                date = datetime(2025, 12, 28)
                amount = random.uniform(500000, 900000)

            data.append({
                "transaction_id": i,
                "date": date,
                "amount": amount,
                "vendor_name": vendor,
                "vendor_id": vendors.index(vendor),
                "sender_id": sender,
                "receiver_id": vendor
            })

        return pd.DataFrame(data)
