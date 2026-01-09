import json
from datetime import datetime

class ReportGenerator:
    """
    Menghasilkan laporan visual dalam format HTML.
    """
    @staticmethod
    def generate_html(report_data: dict) -> str:
        metadata = report_data.get('metadata', {})
        findings = report_data.get('findings', {})
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        html = f"""
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Laporan Forensik IH-Korupsi</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 1000px; margin: 0 auto; padding: 20px; background-color: #f4f7f6; }}
        header {{ background: #1a3a5f; color: white; padding: 30px; border-radius: 8px; margin-bottom: 30px; text-align: center; }}
        h1 {{ margin: 0; font-size: 2.5em; }}
        .metadata {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 30px; }}
        .card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .card h3 {{ margin-top: 0; color: #1a3a5f; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
        .finding-section {{ margin-bottom: 40px; }}
        .red-flag {{ color: #d9534f; font-weight: bold; border: 1px solid #d9534f; padding: 5px 10px; border-radius: 4px; }}
        .success {{ color: #5cb85c; font-weight: bold; }}
        table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #eee; }}
        th {{ background-color: #f8f9fa; color: #1a3a5f; }}
        .explanation {{ font-style: italic; color: #666; font-size: 0.9em; margin-top: 10px; }}
        footer {{ text-align: center; margin-top: 50px; color: #888; border-top: 1px solid #ddd; padding-top: 20px; }}
    </style>
</head>
<body>
    <header>
        <h1>Laporan IH-Korupsi</h1>
        <p>Indikasi Hukum Korupsi - Toolkit Forensik Data</p>
        <p>Waktu Analisis: {timestamp}</p>
    </header>

    <div class="metadata">
        <div class="card">
            <h3>Total Transaksi</h3>
            <p style="font-size: 1.5em; font-weight: bold;">{metadata.get('total_rows', 0):,}</p>
        </div>
        <div class="card">
            <h3>Total Nilai</h3>
            <p style="font-size: 1.5em; font-weight: bold;">IDR {metadata.get('total_amount', 0):,.2f}</p>
        </div>
        <div class="card">
            <h3>Mata Uang</h3>
            <p style="font-size: 1.5em; font-weight: bold;">{metadata.get('currency', 'IDR')}</p>
        </div>
    </div>
"""

        # Mathematician Section
        math = findings.get('Sang Matematikawan', {})
        if math:
            benford = math.get('uji_benford', {})
            rsf = math.get('uji_rsf', {})
            outliers = math.get('pencilan_statistik', {})
            
            status_color = "red-flag" if benford.get('status_kesesuaian') == "Tidak Sesuai" else "success"
            
            html += f"""
    <div class="finding-section">
        <h2>Deteksi Statistik (Sang Matematikawan)</h2>
        <div class="card">
            <h3>Uji Hukum Benford</h3>
            <p>Status: <span class="{status_color}">{benford.get('status_kesesuaian')}</span> (MAD: {benford.get('mad', 0):.4f})</p>
            <p class="explanation">{benford.get('penjelasan')}</p>
        </div>
        
        <div class="card" style="margin-top:20px;">
            <h3>Entitas Risiko Tinggi (RSF)</h3>
            <table>
                <tr><th>Entitas</th><th>Skor RSF</th><th>Transaksi Terbesar</th><th>Rata-rata Lain</th></tr>
"""
            for e in rsf.get('entitas_risiko_tinggi', []):
                html += f"<tr><td>{e['entitas']}</td><td>{e['nilai_rsf']:.2f}</td><td>{e['transaksi_terbesar']:,.0f}</td><td>{e['rata_rata_lainnya']:,.0f}</td></tr>"
            
            html += f"""
            </table>
            <p class="explanation">{rsf.get('penjelasan')}</p>
        </div>
    </div>
"""

        # Chronologist Section
        chrono = findings.get('Sang Kronolog', {})
        if chrono:
            cliff = chrono.get('fiscal_cliff', {})
            velocity = chrono.get('anomali_kecepatan', {})
            
            status_color = "red-flag" if cliff.get('status') == "Dumping Ekstrem" else "success"
            
            html += f"""
    <div class="finding-section">
        <h2>Deteksi Waktu (Sang Kronolog)</h2>
        <div class="card">
            <h3>Fiscal Cliff (Dumping Anggaran)</h3>
            <p>Status: <span class="{status_color}">{cliff.get('status')}</span> (Rasio: {cliff.get('rasio_desember_vs_rata_rata', 0):.2f}x)</p>
            <p class="explanation">{cliff.get('penjelasan')}</p>
        </div>
        
        <div class="card" style="margin-top:20px;">
            <h3>Kejadian Transaksi Berfrekuensi Tinggi</h3>
            <table>
                <tr><th>Vendor/Entitas</th><th>Tanggal</th><th>Jumlah Transaksi</th></tr>
"""
            for v in velocity.get('kejadian_kecepatan_tinggi', []):
                html += f"<tr><td>{v['vendor_id']}</td><td>{v['date_only']}</td><td>{v['jumlah']}</td></tr>"
            
            html += f"""
            </table>
            <p class="explanation">{velocity.get('penjelasan')}</p>
        </div>
    </div>
"""

        # String Detective Section
        string_det = findings.get('Detektif String', {})
        if string_det:
            ghosts = string_det.get('potensi_vendor_hantu', [])
            html += f"""
    <div class="finding-section">
        <h2>Deteksi Nama (Detektif String)</h2>
        <div class="card">
            <h3>Potensi Vendor Hantu / Duplikasi Nama</h3>
            <table>
                <tr><th>Nama 1</th><th>Nama 2</th><th>Skor Kemiripan</th></tr>
"""
            for g in ghosts:
                html += f"<tr><td>{g['nama_1']}</td><td>{g['nama_2']}</td><td>{g['skor_kemiripan']*100:.1f}%</td></tr>"
            
            html += f"""
            </table>
            <p class="explanation">{string_det.get('penjelasan')}</p>
        </div>
    </div>
"""

        html += """
    <footer>
        <p>Dibuat oleh OurCreativity Edisi Coding - Untuk Indonesia Bebas Korupsi</p>
    </footer>
</body>
</html>
"""
        return html
