# src/main.py
import os
import pypandoc
import pandas as pd
from datetime import datetime
from analysis_engine import load_data, run_gap_analysis

# Define file paths relative to the project root
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(ROOT_DIR, 'output')

# Report filename includes the date
REPORT_FILE = os.path.join(OUTPUT_DIR, f"Gap_Analysis_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")


def generate_report_pdf(df_report):
    """Creates a Markdown report and converts it to PDF."""
    
    print("Generating report structure...")
    
    # Prepare the DataFrame for presentation
    pdf_df = df_report.copy()
    pdf_df['max_coverage'] = pdf_df['max_coverage'].astype(int).astype(str) + '%'
    
    # Define order for sorting risk priority
    priority_order = ["Critical", "High", "Medium", "Low", "N/A"]
    pdf_df['Risk_Priority'] = pd.Categorical(pdf_df['Risk_Priority'], categories=priority_order, ordered=True)
    pdf_df = pdf_df.sort_values(by='Risk_Priority')

    # Create the detailed markdown table
    markdown_table = pdf_df.to_markdown(index=False, headers=[
        "Standard", "Req. ID", "Description", "Weight", "Status", "Max Cov.", "Priority", "Controls"
    ])
    
    # Calculate executive summary metrics
    critical_high_gaps = len(pdf_df[pdf_df['Risk_Priority'].isin(['Critical', 'High'])])
    
    markdown_content = f"""
# NIS2 / ISO 27001 Control Gap Analysis Report

## Executive Summary
* **Date:** {datetime.now().strftime('%Y-%m-%d')}
* **Total Requirements Analyzed:** {len(df_report)}
* **Critical/High Gaps Identified:** {critical_high_gaps}

This report identifies compliance gaps based on the maximum coverage percentage reported for supporting operational controls. Focus remediation efforts on the **Critical** and **High** priority items below.

## Traceability & Gap Matrix (Sorted by Risk Priority)

{markdown_table}
    """
    
    # Convert Markdown to PDF
    try:
        pypandoc.convert_text(
            markdown_content, 
            'pdf', 
            format='md', 
            outputfile=REPORT_FILE,
            # Arguments for better PDF formatting
            extra_args=['--toc', '-V geometry:margin=1in', '-V links-as-external'] 
        )
        print(f"\n✅ SUCCESS: Audit Report generated at {REPORT_FILE}")
    except Exception as e:
        print(f"\n❌ ERROR: Failed to generate PDF. You must have Pandoc installed on your system. Error: {e}")
        print("Falling back to generating a simple text report in the output folder.")
        with open(REPORT_FILE.replace('.pdf', '.txt'), 'w') as f:
            f.write(markdown_content)


if __name__ == "__main__":
    
    print("Starting Control Gap Analysis Tool...")
    
    # Load Data
    df_standards, df_controls, df_mapping = load_data()
    
    if df_standards is not None and not df_standards.empty:
        print("Running analysis...")
        
        # Run Analysis
        final_report_df = run_gap_analysis(df_standards, df_controls, df_mapping)
        
        # Generate Output
        generate_report_pdf(final_report_df)
    else:
        print("Analysis stopped. Please check if your input files in the 'data' folder are correct and contain data.")
        # src/main.py (Add this line before the report generation block)
# Import os and datetime if not already present
import os
from datetime import datetime

# ... (inside if __name__ == "__main__": block, after final_report_df is calculated)

# Define CSV file path
data_csv_file = os.path.join(OUTPUT_DIR, f"Gap_Analysis_Data_{datetime.now().strftime('%Y%m%d')}.csv")

# Export the final DataFrame to a CSV file
final_report_df.to_csv(data_csv_file, index=False)
print(f"Data saved successfully to {data_csv_file} for external analysis.")

# ... (rest of the generate_report_pdf function continues)