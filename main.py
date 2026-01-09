import argparse
import sys
import json
from utils.data_loader import DataLoader
from core.engine import FraudEngine
from utils.report_generator import ReportGenerator

def main():
    parser = argparse.ArgumentParser(description="IH-Korupsi: Toolkit Forensik Data Open Source")
    parser.add_argument("--input", type=str, help="Path ke data input (CSV/JSON)")
    parser.add_argument("--type", type=str, choices=['csv', 'json', 'sample'], default='sample', help="Format data")
    parser.add_argument("--output", type=str, default="laporan_fraud.json", help="Path output laporan JSON")
    parser.add_argument("--html", type=str, help="Jika diisi, simpan laporan visual dalam format HTML ke path ini")
    
    args = parser.parse_args()

    print("--- IH-Korupsi Toolkit Forensik ---")
    
    if args.type == 'sample':
        print("Membuat 500 baris data transaksi sintetis...")
        df = DataLoader.generate_sample_data(500)
    else:
        if not args.input:
            print("Error: --input diperlukan untuk data non-sample.")
            sys.exit(1)
        df = DataLoader.load(args.input, args.type)

    engine = FraudEngine()
    report = engine.process(df)
    
    # Simpan JSON
    engine.save_report(report, args.output)
    
    # Simpan HTML jika diminta
    if args.html:
        html_content = ReportGenerator.generate_html(report)
        with open(args.html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Laporan visual HTML disimpan ke {args.html}")

    print("Analisis selesai. Periksa laporan untuk bukti matematis yang terperinci.")

if __name__ == "__main__":
    main()
