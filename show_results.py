import pandas as pd
import os

# Load the generated data
df = pd.read_csv('data/demo_carbon_dataset.csv')
print('=== WEBSITE CARBON API EDA - ANALYSIS COMPLETE ===\n')
print(f'Dataset Size: {len(df):,} records')
print(f'Columns: {list(df.columns)}')
print(f'Categories: {list(df.category.unique())}')
print()

# Key Statistics
print('=== KEY FINDINGS ===')
print(f'Green vs Non-Green Hosting:')
print(f'  - Green hosting: {(df.green==True).sum():,} websites ({(df.green==True).mean()*100:.1f}%)')
print(f'  - Non-green hosting: {(df.green==False).sum():,} websites ({(df.green==False).mean()*100:.1f}%)')
print()

print(f'Average CO2 Emissions (grams):')
green_emissions = df[df.green==True]['gco2e'].mean()
non_green_emissions = df[df.green==False]['gco2e'].mean()
print(f'  - Green hosting: {green_emissions:.6f}g CO2')
print(f'  - Non-green hosting: {non_green_emissions:.6f}g CO2')
print(f'  - Green hosting saves: {((non_green_emissions-green_emissions)/non_green_emissions*100):.1f}% emissions')
print()

print(f'Carbon Ratings Distribution:')
rating_counts = df['rating'].value_counts().sort_index()
for rating, count in rating_counts.items():
    print(f'  - {rating}: {count:,} websites ({count/len(df)*100:.1f}%)')
print()

print(f'Website Size Distribution (MB):')
print(f'  - Min: {df["size_mb"].min():.3f} MB')
print(f'  - Max: {df["size_mb"].max():.3f} MB')
print(f'  - Mean: {df["size_mb"].mean():.3f} MB')
print()

print('=== FILES GENERATED ===')
data_files = os.listdir('data')
print(f'Data files: {data_files}')
print()
print('✅ Analysis complete! All data saved to data/ folder.')
print('📊 Open carbon_eda.ipynb to explore the interactive analysis!')