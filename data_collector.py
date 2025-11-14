"""
Website Carbon API Data Collector

This module provides functionality to collect and generate data from the Website Carbon API.
It includes both API data fetching and sample data generation capabilities.
"""

import requests
import pandas as pd
import numpy as np
import os
from datetime import datetime
import json

class CarbonAPICollector:
    """Class to collect data from Website Carbon API or generate sample data"""
    
    def __init__(self):
        self.base_url = "https://api.websitecarbon.com"
        self.sample_data_size = 1000
        
    def fetch_from_api(self, url):
        """
        Fetch carbon data for a specific URL from the Website Carbon API
        
        Args:
            url (str): The URL to check
            
        Returns:
            dict: API response data or None if failed
        """
        try:
            response = requests.get(f"{self.base_url}?url={url}", timeout=10)
            response.raise_for_status()
            return response.json()
        except (requests.RequestException, json.JSONDecodeError) as e:
            print(f"Error fetching data for {url}: {e}")
            return None
    
    def generate_sample_dataset(self, size=None):
        """
        Generate a sample dataset for demonstration purposes
        
        Args:
            size (int): Number of records to generate
            
        Returns:
            pd.DataFrame: Generated dataset
        """
        if size is None:
            size = self.sample_data_size
            
        np.random.seed(42)  # For reproducible results
        
        # Generate sample data
        data = {
            'url': [f'https://example{i}.com' for i in range(size)],
            'green': np.random.choice([True, False], size, p=[0.3, 0.7]),
            'gco2e': np.random.exponential(2.5, size),  # grams of CO2
            'rating': np.random.choice(['A+', 'A', 'B', 'C', 'D'], size, p=[0.1, 0.2, 0.3, 0.3, 0.1]),
            'category': np.random.choice(['ecommerce', 'blog', 'portfolio', 'corporate', 'news'], size),
            'size_mb': np.random.lognormal(0, 1, size),  # Website size in MB
            'requests': np.random.poisson(50, size)  # Number of requests
        }
        
        return pd.DataFrame(data)
    
    def save_dataset(self, df, filepath):
        """
        Save dataset to CSV file
        
        Args:
            df (pd.DataFrame): Dataset to save
            filepath (str): Output file path
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        df.to_csv(filepath, index=False)
        print(f"Dataset saved to {filepath}")
        
    def generate_and_save(self, output_dir='data', filename='carbon_dataset.csv'):
        """
        Generate sample dataset and save it
        
        Args:
            output_dir (str): Output directory
            filename (str): Output filename
            
        Returns:
            str: Path to saved file
        """
        df = self.generate_sample_dataset()
        filepath = os.path.join(output_dir, filename)
        self.save_dataset(df, filepath)
        return filepath

def main():
    """Main function to demonstrate usage"""
    collector = CarbonAPICollector()
    
    # Generate sample dataset
    output_file = collector.generate_and_save()
    print(f"Sample dataset generated: {output_file}")
    
    # Display basic info about the dataset
    df = pd.read_csv(output_file)
    print(f"\nDataset Info:")
    print(f"- Size: {len(df):,} records")
    print(f"- Columns: {list(df.columns)}")
    print(f"- Green hosting: {(df.green == True).sum():,} websites")
    print(f"- Average CO2 emissions: {df.gco2e.mean():.2f}g")

if __name__ == "__main__":
    main()