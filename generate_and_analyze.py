"""
Generate and Analyze Dataset Pipeline

This script orchestrates the data generation and analysis workflow for the
Website Carbon API EDA project.
"""

import sys
import os
sys.path.append('.')

from data_collector import CarbonAPICollector
import pandas as pd

def generate_demo_dataset():
    """
    Generate a demo dataset for the EDA project
    This creates a realistic dataset for analysis
    """
    print("=== GENERATING DEMO DATASET ===")
    
    collector = CarbonAPICollector()
    
    try:
        # Try to generate API-based data (if available)
        print("Attempting to fetch real API data...")
        api_data = collector.fetch_from_api("https://example.com")
        
        if api_data:
            print("API data fetched successfully!")
            # Process real API data here if needed
        else:
            print("API not available, generating demo dataset...")
            
    except Exception as e:
        print(f"API fetch failed: {e}")
        print("Generating mock data instead...")
    
    # Generate demo dataset regardless
    output_file = collector.generate_and_save('data', 'demo_carbon_dataset.csv')
    
    # Load and display basic info
    df = pd.read_csv(output_file)
    print(f"\nDataset generated: {len(df):,} records")
    print(f"Columns: {list(df.columns)}")
    print(f"Green hosting: {(df.green == True).sum():,} websites")
    print(f"Average emissions: {df.gco2e.mean():.2f}g CO2")
    
    return output_file

def run_analysis():
    """
    Run basic analysis on the generated dataset
    """
    print("\n=== RUNNING ANALYSIS ===")
    
    data_file = 'data/demo_carbon_dataset.csv'
    
    if not os.path.exists(data_file):
        print("Dataset not found, generating first...")
        generate_demo_dataset()
    
    # Load data
    df = pd.read_csv(data_file)
    
    # Basic analysis
    print(f"\nAnalysis Results:")
    print(f"- Total websites: {len(df):,}")
    print(f"- Green hosting percentage: {(df.green == True).mean()*100:.1f}%")
    print(f"- Average emissions: {df.gco2e.mean():.2f}g CO2")
    print(f"- Size range: {df.size_mb.min():.1f} - {df.size_mb.max():.1f} MB")
    
    return df

def main():
    """Main pipeline execution"""
    print("WEBSITE CARBON API - GENERATE & ANALYZE PIPELINE")
    print("=" * 50)
    
    # Generate dataset
    data_file = generate_demo_dataset()
    
    # Run analysis
    df = run_analysis()
    
    print("\n✅ Pipeline completed successfully!")
    print(f"📊 Data available at: {data_file}")
    print("📋 Next: Run 'python run_notebook_analysis.py' for interactive analysis")

if __name__ == "__main__":
    main()