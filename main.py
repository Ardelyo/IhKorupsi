import argparse
import sys
import json
from ih_korupsi.utils.data_loader import DataLoader
from ih_korupsi.core.engine import FraudEngine
from ih_korupsi.utils.report_generator import ReportGenerator

def main():
    parser = argparse.ArgumentParser(description="IH-Korupsi: Open Source Forensic Data Toolkit")
    parser.add_argument("--input", type=str, help="Path to input data (CSV/JSON)")
    parser.add_argument("--type", type=str, choices=['csv', 'json', 'sample'], default='sample', help="Data format")
    parser.add_argument("--output", type=str, default="fraud_report.json", help="Path to JSON report output")
    parser.add_argument("--html", type=str, help="If provided, save a visual HTML report to this path")
    
    args = parser.parse_args()

    print("--- IH-Korupsi Forensic Toolkit ---")
    
    if args.type == 'sample':
        print("Generating 500 rows of synthetic transaction data...")
        df = DataLoader.generate_sample_data(500)
    else:
        if not args.input:
            print("Error: --input is required for non-sample data.")
            sys.exit(1)
        df = DataLoader.load(args.input, args.type)

    engine = FraudEngine()
    report = engine.process(df)
    
    # Save JSON
    engine.save_report(report, args.output)
    
    # Save HTML if requested
    if args.html:
        html_content = ReportGenerator.generate_html(report)
        with open(args.html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Visual HTML report saved to {args.html}")

    print("Analysis complete. Check the report for detailed mathematical evidence.")

if __name__ == "__main__":
    main()
