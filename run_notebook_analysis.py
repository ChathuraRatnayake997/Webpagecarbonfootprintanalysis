"""
Interactive Notebook Analysis Runner

This script runs the complete EDA analysis and generates all plots
for the Website Carbon API project.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from datetime import datetime

# Set style for better plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_or_generate_data():
    """Load existing data or generate new dataset"""
    data_file = 'data/demo_carbon_dataset.csv'
    
    if os.path.exists(data_file):
        print(f"Loading existing data from {data_file}")
        df = pd.read_csv(data_file)
    else:
        print("No data found, generating new dataset...")
        from data_collector import CarbonAPICollector
        collector = CarbonAPICollector()
        collector.generate_and_save('data', 'demo_carbon_dataset.csv')
        df = pd.read_csv(data_file)
    
    print(f"Dataset loaded: {len(df):,} records")
    return df

def analyze_green_hosting_impact(df):
    """Analyze the impact of green hosting on emissions"""
    print("\n=== GREEN HOSTING IMPACT ANALYSIS ===")
    
    green_stats = df.groupby('green').agg({
        'gco2e': ['mean', 'median', 'std'],
        'size_mb': 'mean',
        'requests': 'mean'
    }).round(3)
    
    print("Emissions by Hosting Type:")
    print(green_stats)
    
    # Calculate savings
    green_mean = df[df.green == True]['gco2e'].mean()
    non_green_mean = df[df.green == False]['gco2e'].mean()
    savings_pct = ((non_green_mean - green_mean) / non_green_mean) * 100
    
    print(f"\nGreen hosting reduces emissions by {savings_pct:.1f}%")
    return green_stats

def analyze_size_vs_emissions(df):
    """Analyze relationship between website size and emissions"""
    print("\n=== SIZE VS EMISSIONS ANALYSIS ===")
    
    correlation = df['size_mb'].corr(df['gco2e'])
    print(f"Size-Emissions correlation: {correlation:.3f}")
    
    # Create size bins for analysis
    df['size_category'] = pd.cut(df['size_mb'], 
                                bins=[0, 1, 3, 10, float('inf')],
                                labels=['Small (<1MB)', 'Medium (1-3MB)', 
                                       'Large (3-10MB)', 'Very Large (>10MB)'])
    
    size_emissions = df.groupby('size_category')['gco2e'].agg(['mean', 'count'])
    print("\nEmissions by Size Category:")
    print(size_emissions)
    
    return correlation

def analyze_carbon_ratings(df):
    """Analyze distribution of carbon ratings"""
    print("\n=== CARBON RATING ANALYSIS ===")
    
    rating_order = ['A+', 'A', 'B', 'C', 'D']
    rating_counts = df['rating'].value_counts().reindex(rating_order, fill_value=0)
    
    print("Rating Distribution:")
    for rating, count in rating_counts.items():
        pct = (count / len(df)) * 100
        print(f"  {rating}: {count:,} websites ({pct:.1f}%)")
    
    # Rating vs emissions
    rating_emissions = df.groupby('rating')['gco2e'].mean().reindex(rating_order)
    print(f"\nAverage Emissions by Rating:")
    for rating, emissions in rating_emissions.items():
        print(f"  {rating}: {emissions:.2f}g CO2")
    
    return rating_counts

def analyze_categories(df):
    """Analyze different website categories"""
    print("\n=== CATEGORY ANALYSIS ===")
    
    category_stats = df.groupby('category').agg({
        'gco2e': ['mean', 'count'],
        'size_mb': 'mean',
        'green': lambda x: (x == True).mean() * 100
    }).round(2)
    
    print("Statistics by Category:")
    print(category_stats)
    
    # Find greenest categories
    category_emissions = df.groupby('category')['gco2e'].mean().sort_values()
    print(f"\nGreenest Categories (by emissions):")
    for category, emissions in category_emissions.head(3).items():
        print(f"  {category}: {emissions:.2f}g CO2")
    
    return category_stats

def create_visualizations(df):
    """Create all analysis plots"""
    print("\n=== CREATING VISUALIZATIONS ===")
    
    # Ensure plots directory exists
    os.makedirs('plots', exist_ok=True)
    
    # Set up the plotting style
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['font.size'] = 10
    
    # 1. Emissions Analysis
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Website Carbon Emissions Analysis', fontsize=16, fontweight='bold')
    
    # Green vs Non-green hosting
    green_data = [df[df.green == True]['gco2e'], df[df.green == False]['gco2e']]
    axes[0,0].boxplot(green_data, labels=['Green Hosting', 'Non-Green Hosting'])
    axes[0,0].set_title('CO2 Emissions by Hosting Type')
    axes[0,0].set_ylabel('CO2 Emissions (grams)')
    
    # Size vs Emissions scatter
    colors = ['green' if x else 'red' for x in df['green']]
    axes[0,1].scatter(df['size_mb'], df['gco2e'], c=colors, alpha=0.6)
    axes[0,1].set_xlabel('Website Size (MB)')
    axes[0,1].set_ylabel('CO2 Emissions (grams)')
    axes[0,1].set_title('Size vs Emissions')
    
    # Rating distribution
    rating_order = ['A+', 'A', 'B', 'C', 'D']
    rating_counts = df['rating'].value_counts().reindex(rating_order, fill_value=0)
    axes[1,0].bar(rating_counts.index, rating_counts.values)
    axes[1,0].set_title('Carbon Rating Distribution')
    axes[1,0].set_xlabel('Rating')
    axes[1,0].set_ylabel('Number of Websites')
    
    # Category analysis
    category_emissions = df.groupby('category')['gco2e'].mean().sort_values()
    axes[1,1].bar(range(len(category_emissions)), category_emissions.values)
    axes[1,1].set_xticks(range(len(category_emissions)))
    axes[1,1].set_xticklabels(category_emissions.index, rotation=45)
    axes[1,1].set_title('Average Emissions by Category')
    axes[1,1].set_ylabel('CO2 Emissions (grams)')
    
    plt.tight_layout()
    plt.savefig('plots/emissions_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Rating Distribution Plot
    plt.figure(figsize=(10, 6))
    rating_counts = df['rating'].value_counts().reindex(rating_order, fill_value=0)
    bars = plt.bar(rating_counts.index, rating_counts.values, 
                   color=['#2E8B57', '#32CD32', '#FFD700', '#FF8C00', '#DC143C'])
    plt.title('Distribution of Carbon Intensity Ratings', fontsize=14, fontweight='bold')
    plt.xlabel('Carbon Rating')
    plt.ylabel('Number of Websites')
    
    # Add percentage labels on bars
    for bar, count in zip(bars, rating_counts.values):
        height = bar.get_height()
        pct = (count / len(df)) * 100
        plt.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                f'{count}\n({pct:.1f}%)', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('plots/rating_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Category Analysis
    plt.figure(figsize=(12, 8))
    category_stats = df.groupby('category').agg({
        'gco2e': 'mean',
        'green': lambda x: (x == True).mean() * 100
    })
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Average emissions by category
    category_emissions = df.groupby('category')['gco2e'].mean().sort_values()
    bars1 = ax1.bar(range(len(category_emissions)), category_emissions.values)
    ax1.set_xticks(range(len(category_emissions)))
    ax1.set_xticklabels(category_emissions.index, rotation=45)
    ax1.set_title('Average CO2 Emissions by Category')
    ax1.set_ylabel('CO2 Emissions (grams)')
    
    # Green hosting percentage by category
    green_pct = df.groupby('category')['green'].apply(lambda x: (x == True).mean() * 100).sort_values(ascending=False)
    bars2 = ax2.bar(range(len(green_pct)), green_pct.values)
    ax2.set_xticks(range(len(green_pct)))
    ax2.set_xticklabels(green_pct.index, rotation=45)
    ax2.set_title('Green Hosting Adoption by Category')
    ax2.set_ylabel('Green Hosting Percentage')
    
    plt.tight_layout()
    plt.savefig('plots/category_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 4. Interactive plots for HTML
    create_interactive_plots(df)
    
    print("✅ All visualizations created successfully!")
    print("📊 Plots saved to 'plots/' directory")

def create_interactive_plots(df):
    """Create interactive plots for HTML embedding"""
    
    # Create basic interactive HTML plots using simple JavaScript
    # These are lightweight alternatives to heavy plotting libraries
    
    # Interactive scatter plot
    scatter_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Interactive Scatter Plot - Size vs Emissions</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .plot-container {{ width: 100%; height: 500px; }}
        </style>
    </head>
    <body>
        <h1>Interactive Analysis: Website Size vs Carbon Emissions</h1>
        <div class="plot-container" id="scatterPlot"></div>
        
        <script>
        var trace1 = {{
            x: {df['size_mb'].tolist()},
            y: {df['gco2e'].tolist()},
            mode: 'markers',
            type: 'scatter',
            marker: {{
                color: {['green' if x else 'red' for x in df['green']].tolist()},
                size: 8,
                opacity: 0.7
            }},
            text: {['Green: ' + str(x) + ', Rating: ' + str(y) + ', Size: ' + str(z) + 'MB' 
                    for x, y, z in zip(df['green'], df['rating'], df['size_mb'])].tolist()},
            hovertemplate: '%{{text}}<extra></extra>'
        }};
        
        var layout = {{
            title: 'Website Size vs Carbon Emissions',
            xaxis: {{ title: 'Website Size (MB)' }},
            yaxis: {{ title: 'CO2 Emissions (grams)' }}
        }};
        
        Plotly.newPlot('scatterPlot', [trace1], layout);
        </script>
    </body>
    </html>
    """
    
    with open('plots/interactive_scatter.html', 'w') as f:
        f.write(scatter_html)
    
    # Interactive histogram
    histogram_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Interactive Histogram - Emission Distribution</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .plot-container {{ width: 100%; height: 500px; }}
        </style>
    </head>
    <body>
        <h1>Interactive Analysis: Carbon Emission Distribution</h1>
        <div class="plot-container" id="histogram"></div>
        
        <script>
        var trace1 = {{
            x: {df[df['green'] == True]['gco2e'].tolist()},
            type: 'histogram',
            name: 'Green Hosting',
            opacity: 0.7,
            marker: {{ color: 'green' }}
        }};
        
        var trace2 = {{
            x: {df[df['green'] == False]['gco2e'].tolist()},
            type: 'histogram',
            name: 'Non-Green Hosting',
            opacity: 0.7,
            marker: {{ color: 'red' }}
        }};
        
        var layout = {{
            title: 'Carbon Emission Distribution by Hosting Type',
            xaxis: {{ title: 'CO2 Emissions (grams)' }},
            yaxis: {{ title: 'Number of Websites' }},
            barmode: 'overlay'
        }};
        
        Plotly.newPlot('histogram', [trace1, trace2], layout);
        </script>
    </body>
    </html>
    """
    
    with open('plots/interactive_histogram.html', 'w') as f:
        f.write(histogram_html)
    
    # Interactive box plot
    boxplot_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Interactive Box Plot - Rating Analysis</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .plot-container {{ width: 100%; height: 500px; }}
        </style>
    </head>
    <body>
        <h1>Interactive Analysis: Carbon Emissions by Rating</h1>
        <div class="plot-container" id="boxPlot"></div>
        
        <script>
        var data = [
    """
    
    rating_order = ['A+', 'A', 'B', 'C', 'D']
    for rating in rating_order:
        rating_data = df[df['rating'] == rating]['gco2e'].tolist()
        boxplot_html += f"""
        {{
            y: {rating_data},
            type: 'box',
            name: '{rating}',
            marker: {{ color: 'blue' }}
        }},"""
    
    boxplot_html += f"""
        ];
        
        var layout = {{
            title: 'CO2 Emissions Distribution by Carbon Rating',
            yaxis: {{ title: 'CO2 Emissions (grams)' }},
            xaxis: {{ title: 'Carbon Rating' }}
        }};
        
        Plotly.newPlot('boxPlot', data, layout);
        </script>
    </body>
    </html>
    """
    
    with open('plots/interactive_boxplot.html', 'w') as f:
        f.write(boxplot_html)

def main():
    """Main analysis execution"""
    print("WEBSITE CARBON API - INTERACTIVE ANALYSIS")
    print("=" * 50)
    
    # Load or generate data
    df = load_or_generate_data()
    
    # Run all analyses
    analyze_green_hosting_impact(df)
    analyze_size_vs_emissions(df)
    analyze_carbon_ratings(df)
    analyze_categories(df)
    
    # Create visualizations
    create_visualizations(df)
    
    print("\n🎉 Analysis completed successfully!")
    print("📈 Interactive plots available in 'plots/' directory")
    print("📊 Static plots: emissions_analysis.png, rating_distribution.png, category_analysis.png")
    print("💻 Interactive plots: interactive_scatter.html, interactive_histogram.html, interactive_boxplot.html")

if __name__ == "__main__":
    main()