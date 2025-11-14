"""
Jupyter Notebook to HTML Converter for GitHub Pages

This script converts the carbon_eda.ipynb notebook to a GitHub Pages-compatible
HTML file with embedded images and proper styling.
"""

import os
import sys
import nbformat
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExtractOutputPreprocessor
import shutil

def convert_notebook_to_html():
    """Convert Jupyter notebook to HTML for GitHub Pages"""
    
    notebook_file = 'carbon_eda.ipynb'
    output_dir = 'site'
    
    # Check if notebook exists
    if not os.path.exists(notebook_file):
        print(f"❌ Error: {notebook_file} not found!")
        return False
    
    # Check if output directory exists
    if not os.path.exists(output_dir):
        print(f"📁 Creating output directory: {output_dir}")
        os.makedirs(output_dir)
    
    try:
        # Read the notebook
        print(f"📖 Reading notebook: {notebook_file}")
        with open(notebook_file, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, as_version=4)
        
        # Configure HTML exporter
        html_exporter = HTMLExporter()
        html_exporter.template_name = 'classic'
        
        # Extract outputs (images, etc.)
        extract_output = ExtractOutputPreprocessor()
        resources = {}
        notebook, resources = extract_output.preprocess(notebook, resources)
        
        # Convert to HTML
        print("🔄 Converting to HTML...")
        (body, resources) = html_exporter.from_notebook_cell(notebook, resources)
        
        # Add custom CSS for GitHub Pages styling
        custom_css = """
        <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
            background-color: #f8f9fa;
        }
        
        .container {
            background: white;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        
        h2 {
            color: #34495e;
            margin-top: 30px;
        }
        
        h3 {
            color: #7f8c8d;
        }
        
        code {
            background-color: #f1f2f6;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
        
        pre {
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 5px;
            padding: 15px;
            overflow-x: auto;
        }
        
        .output_subarea {
            margin: 10px 0;
        }
        
        .output_area img {
            max-width: 100%;
            height: auto;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .cell {
            margin: 20px 0;
        }
        
        .input {
            margin-bottom: 10px;
        }
        
        .output {
            margin-top: 10px;
        }
        
        .markdown {
            color: #2c3e50;
        }
        
        .markdown h1, .markdown h2, .markdown h3 {
            margin-top: 25px;
        }
        
        .markdown p {
            margin: 10px 0;
        }
        
        .markdown ul, .markdown ol {
            margin: 10px 0;
            padding-left: 25px;
        }
        
        .markdown code {
            color: #e74c3c;
        }
        
        .highlight {
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 5px;
            padding: 15px;
            margin: 15px 0;
        }
        
        .nav-links {
            position: fixed;
            top: 20px;
            right: 20px;
            background: #3498db;
            color: white;
            padding: 10px;
            border-radius: 5px;
            z-index: 1000;
        }
        
        .nav-links a {
            color: white;
            text-decoration: none;
            margin: 0 5px;
            font-weight: bold;
        }
        
        .nav-links a:hover {
            text-decoration: underline;
        }
        </style>
        """
        
        # Create complete HTML document
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Website Carbon API - EDA Analysis</title>
            {custom_css}
        </head>
        <body>
            <div class="nav-links">
                <a href="index.html">← Back to Home</a>
            </div>
            <div class="container">
                {body}
            </div>
        </body>
        </html>
        """
        
        # Save HTML file
        output_file = os.path.join(output_dir, 'carbon_eda.html')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        # Copy any output images to the site/plots directory
        if 'outputs' in resources:
            plots_dir = os.path.join(output_dir, 'plots')
            os.makedirs(plots_dir, exist_ok=True)
            
            for output_path in resources['outputs']:
                if os.path.exists(output_path):
                    filename = os.path.basename(output_path)
                    dest_path = os.path.join(plots_dir, filename)
                    shutil.copy2(output_path, dest_path)
                    print(f"📁 Copied plot: {filename}")
        
        print(f"✅ Conversion successful!")
        print(f"📄 HTML file saved to: {output_file}")
        print(f"📊 File size: {os.path.getsize(output_file):,} bytes")
        
        return True
        
    except Exception as e:
        print(f"❌ Conversion failed: {str(e)}")
        return False

def main():
    """Main function"""
    print("🚀 Jupyter Notebook to HTML Converter")
    print("=" * 50)
    print("Converting carbon_eda.ipynb for GitHub Pages...")
    print()
    
    success = convert_notebook_to_html()
    
    if success:
        print("\n🎉 Conversion completed successfully!")
        print("📱 Your analysis is now ready for GitHub Pages!")
        print("🔗 Access it at: /site/carbon_eda.html")
    else:
        print("\n❌ Conversion failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()