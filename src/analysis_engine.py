# src/analysis_engine.py
import yaml
import pandas as pd
import os # Import os for file path manipulation

# Define the root path relative to the current script location
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'data')

def load_data(req_file='standards_requirements.csv', 
              controls_file='implemented_controls.yaml', 
              mapping_file='control_mapping.csv'):
    """Loads all input data files from the 'data' directory."""
    try:
        # Load CSVs
        df_standards = pd.read_csv(os.path.join(DATA_DIR, req_file))
        df_mapping = pd.read_csv(os.path.join(DATA_DIR, mapping_file)).fillna('')
        
        # Load YAML
        with open(os.path.join(DATA_DIR, controls_file), 'r') as f:
            yaml_data = yaml.safe_load(f)
        df_controls = pd.DataFrame(yaml_data.get('controls', [])).rename(columns={'id': 'Control_ID'})
        
        # Ensure 'Control_ID' is treated as a string to avoid merge issues
        df_controls['Control_ID'] = df_controls['Control_ID'].astype(str) 

        print("Data loaded successfully.")
        return df_standards, df_controls, df_mapping
    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None, None

def run_gap_analysis(df_standards, df_controls, df_mapping):
    """Performs the core gap analysis, calculates coverage, and determines risk status."""
    
    # 1. Melt the mapping table to one row per relationship (Control_ID <-> Requirement_ID)
    df_melt = df_mapping.melt(
        id_vars=['Control_ID'], 
        var_name='Requirement_ID', 
        value_name='Mapping_Type'
    )
    # Filter for actual mappings ('Primary' or 'Supporting')
    df_melt = df_melt[df_melt['Mapping_Type'].isin(['Primary', 'Supporting'])]
    
    # 2. Join the mapping with the operational control data (to get Coverage %)
    df_analysis = df_melt.merge(
        df_controls[['Control_ID', 'coverage_percent', 'owner', 'remediation_plan', 'target_date']],
        on='Control_ID',
        how='left'
    )
    
    # 3. Aggregate: Find the single highest coverage for each requirement
    df_summary = df_analysis.groupby('Requirement_ID').agg(
        max_coverage=('coverage_percent', 'max'),
        all_controls=('Control_ID', lambda x: ', '.join(x.dropna().unique()))
    ).reset_index()
    
    # 4. Determine Status (Business Logic)
    def determine_status(row):
        if row['max_coverage'] is None or row['max_coverage'] == 0:
            return "GAP (0% Coverage)"
        elif row['max_coverage'] == 100:
            return "MET (100% Coverage)"
        elif row['max_coverage'] > 0:
            return f"PARTIAL (Max {int(row['max_coverage'])}%)"
        
    df_summary['Status'] = df_summary.apply(determine_status, axis=1)
    
    # 5. Calculate final risk score
    # Merge summary back with the standards (which contains Risk_Weight)
    df_final = df_standards.merge(df_summary, on='Requirement_ID', how='left')
    
    # Fill gaps for requirements that had NO controls mapped at all
    df_final['Status'] = df_final['Status'].fillna('GAP (NO CONTROL MAPPED)')
    df_final['all_controls'] = df_final['all_controls'].fillna('N/A')
    df_final['max_coverage'] = df_final['max_coverage'].fillna(0)


    def calculate_risk(row):
        weight = row['Risk_Weight (1-10)'] # Note: uses the column name from your CSV
        
        if row['Status'].startswith('MET'):
            return "Low"
        elif row['Status'].startswith('PARTIAL'):
            # High risk if coverage is significantly low (<75%) AND the inherent risk is high (>=8)
            if row['max_coverage'] < 75 and weight >= 8:
                return "High"
            else:
                return "Medium"
        elif row['Status'].startswith('GAP'):
            # Critical risk if it's a gap AND the requirement is highly critical (>=9)
            return "Critical" if weight >= 9 else "High"
        return "N/A"

    df_final['Risk_Priority'] = df_final.apply(calculate_risk, axis=1)
    
# Ensure this list is inside the function and correctly indented
    return df_final[['Standard', 'Requirement_ID', 'Requirement_Description', 'Category', 'Risk_Weight (1-10)', 
                     'Status', 'max_coverage', 'Risk_Priority', 'all_controls']] 
    # ^^^^^^^ This space here must align properly with the open bracket on the first line.