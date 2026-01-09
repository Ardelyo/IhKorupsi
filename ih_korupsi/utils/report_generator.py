import json
from datetime import datetime

class ReportGenerator:
    """
    Generates visual reports in HTML format.
    """
    @staticmethod
    def generate_html(report_data: dict) -> str:
        metadata = report_data.get('metadata', {})
        findings = report_data.get('findings', {})
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IH-Korupsi Forensic Report</title>
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
        <h1>IH-Korupsi Report</h1>
        <p>Intelligent Hunting (IH) - Korupsi - Forensic Data Toolkit</p>
        <p>Analysis Time: {timestamp}</p>
    </header>

    <div class="metadata">
        <div class="card">
            <h3>Total Transactions</h3>
            <p style="font-size: 1.5em; font-weight: bold;">{metadata.get('total_rows', 0):,}</p>
        </div>
        <div class="card">
            <h3>Total Amount</h3>
            <p style="font-size: 1.5em; font-weight: bold;">{metadata.get('currency', 'IDR')} {metadata.get('total_amount', 0):,.2f}</p>
        </div>
        <div class="card">
            <h3>Currency</h3>
            <p style="font-size: 1.5em; font-weight: bold;">{metadata.get('currency', 'IDR')}</p>
        </div>
    </div>
"""

        # Mathematician Section
        math = findings.get('The Mathematician', {})
        if math:
            benford = math.get('benford_test', {})
            rsf = math.get('rsf_test', {})
            
            conformity = benford.get('conformity_status')
            status_class = "red-flag" if conformity == "Non-conformity" else "success"
            
            html += f"""
    <div class="finding-section">
        <h2>Statistical Detection (The Mathematician)</h2>
        <div class="card">
            <h3>Benford's Law Test</h3>
            <p>Status: <span class="{status_class}">{conformity}</span> (MAD: {benford.get('mad', 0):.4f})</p>
            <p class="explanation">{benford.get('explanation')}</p>
        </div>
        
        <div class="card" style="margin-top:20px;">
            <h3>High Risk Entities (RSF)</h3>
            <table>
                <tr><th>Entity</th><th>RSF Score</th><th>Largest Transaction</th><th>Average of Others</th></tr>
"""
            for e in rsf.get('high_risk_entities', []):
                html += f"<tr><td>{e['entity']}</td><td>{e['rsf_value']:.2f}</td><td>{e['largest_transaction']:,.0f}</td><td>{e['average_others']:,.0f}</td></tr>"
            
            html += f"""
            </table>
            <p class="explanation">{rsf.get('explanation')}</p>
        </div>
    </div>
"""

        # Chronologist Section
        chrono = findings.get('The Chronologist', {})
        if chrono:
            cliff = chrono.get('fiscal_cliff', {})
            velocity = chrono.get('velocity_anomalies', {})
            
            status = cliff.get('status')
            status_class = "red-flag" if status == "Extreme Dumping" else "success"
            
            html += f"""
    <div class="finding-section">
        <h2>Time-Series Detection (The Chronologist)</h2>
        <div class="card">
            <h3>Fiscal Cliff (Budget Dumping)</h3>
            <p>Status: <span class="{status_class}">{status}</span> (Ratio: {cliff.get('december_vs_avg_ratio', 0):.2f}x)</p>
            <p class="explanation">{cliff.get('explanation')}</p>
        </div>
        
        <div class="card" style="margin-top:20px;">
            <h3>High Frequency Transaction Events</h3>
            <table>
                <tr><th>Vendor/Entity</th><th>Date</th><th>Transaction Count</th></tr>
"""
            for v in velocity.get('high_velocity_events', []):
                html += f"<tr><td>{v['vendor_id']}</td><td>{v['date_only']}</td><td>{v['count']}</td></tr>"
            
            html += f"""
            </table>
            <p class="explanation">{velocity.get('explanation')}</p>
        </div>
    </div>
"""

        # String Detective Section
        string_det = findings.get('String Detective', {})
        if string_det:
            ghosts = string_det.get('potential_ghost_vendors', [])
            html += f"""
    <div class="finding-section">
        <h2>String Detection (String Detective)</h2>
        <div class="card">
            <h3>Potential Ghost Vendors / Name Duplication</h3>
            <table>
                <tr><th>Name 1</th><th>Name 2</th><th>Similarity Score</th></tr>
"""
            for g in ghosts:
                html += f"<tr><td>{g['name_1']}</td><td>{g['name_2']}</td><td>{g['similarity_score']*100:.1f}%</td></tr>"
            
            html += f"""
            </table>
            <p class="explanation">{string_det.get('explanation')}</p>
        </div>
    </div>
"""

        html += """
    <footer>
        <p>Created by OurCreativity Edisi Coding - Towards a More Transparent Future</p>
    </footer>
</body>
</html>
"""
        return html
