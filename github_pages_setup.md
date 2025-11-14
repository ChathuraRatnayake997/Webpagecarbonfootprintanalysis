# GitHub Pages Setup Guide

## 🚀 Complete Setup Instructions for GitHub Pages Deployment

### Step 1: Create GitHub Repository

**Option A: Via GitHub Web Interface**
1. Go to [GitHub.com](https://github.com) and sign in
2. Click the green "New" button (or the "+" icon → "New repository")
3. Fill in repository details:
   - **Repository name**: `website-carbon-api-eda` (or your preferred name)
   - **Description**: "Analysis of Website Carbon API data with environmental impact insights"
   - **Visibility**: Public (required for free GitHub Pages)
   - ✅ Check "Add a README file"
   - Click "Create repository"

**Option B: Via Command Line**
```bash
# Create repository on GitHub (requires GitHub CLI)
gh repo create website-carbon-api-eda --public --description "Analysis of Website Carbon API data"

# Clone and setup locally
git clone https://github.com/YOUR_USERNAME/website-carbon-api-eda.git
cd website-carbon-api-eda
```

### Step 2: Local Repository Setup

**Copy Project Files to Repository Root**
```bash
# Copy all essential files from Carbon API to your repository
cp -r /path/to/Carbon_API/site/* /path/to/repository/
cp /path/to/Carbon_API/README.md /path/to/repository/
cp /path/to/Carbon_API/.gitignore /path/to/repository/
```

**Or manually copy these files:**
- `site/index.html` - Landing page
- `site/carbon_eda.html` - Complete analysis
- `site/assets/style.css` - Styling
- `site/plots/` - All visualization files
- `README.md` - Project documentation
- `.gitignore` - Git configuration

### Step 3: Commit and Push

```bash
# Add all files to git
git add .

# Commit with descriptive message
git commit -m "feat: Add Website Carbon API EDA analysis with GitHub Pages

- Professional landing page with project overview
- Complete exploratory data analysis (EDA) 
- Interactive and static data visualizations
- Environmental impact insights
- Modern responsive design"

# Push to GitHub
git push origin main
```

### Step 4: Enable GitHub Pages

1. **Go to Repository Settings**
   - Navigate to your repository on GitHub
   - Click the "Settings" tab (must be repository owner)

2. **Configure Pages**
   - Scroll down to "Pages" section in left sidebar
   - Under "Source", select "Deploy from a branch"
   - Choose "main" branch
   - Select "/ (root)" folder
   - Click "Save"

3. **Wait for Deployment**
   - GitHub will show: "Your site is ready to be published"
   - After a few minutes, it will show: "Your site is published at..."
   - **Note**: First deployment can take 5-10 minutes

### Step 5: Access Your Live Site

**Expected URL**: `https://YOUR_USERNAME.github.io/website-carbon-api-eda/`

**Site Contents**:
- **Home Page**: `/` - Professional landing page with project overview
- **Analysis Page**: `/carbon_eda.html` - Complete interactive EDA
- **Visualizations**: `/plots/` - All charts and interactive plots

## 🎯 What You'll See

Your GitHub Pages site will include:

### 🏠 Professional Landing Page
- Project overview and key environmental findings
- Link to full analysis
- Modern, responsive design
- Environmental impact highlights

### 📊 Complete Data Analysis
- Interactive Jupyter notebook converted to HTML
- Comprehensive exploratory data analysis
- Statistical insights and visualizations
- Environmental impact conclusions

### 🎨 Modern Design
- Clean, professional styling
- Mobile-responsive layout
- Environmental color scheme
- Easy navigation between sections

### 📈 Data Visualizations
- Static plots: emissions analysis, rating distribution, category analysis
- Interactive plots: scatter plots, histograms, box plots
- All plots optimized for web viewing

## 🔧 Troubleshooting

### Common Issues

**1. Pages Not Loading**
- Check repository is public
- Verify files are in repository root (not in subfolder)
- Wait 10-15 minutes for initial deployment

**2. Missing Styling**
- Ensure `assets/style.css` is properly linked
- Check file paths in HTML are correct

**3. Broken Links**
- Verify all plot files exist in `site/plots/`
- Check relative paths in HTML files

### Testing Locally

Before pushing to GitHub, test locally:

```bash
# Serve locally to preview
python -m http.server 8000

# Visit http://localhost:8000 to preview
```

## 🚀 Advanced Options

### Custom Domain (Optional)
1. Add a `CNAME` file with your domain
2. Configure DNS records
3. Enable HTTPS in Pages settings

### Analytics Integration
- Add Google Analytics tracking code
- Monitor site visits and engagement

### Continuous Integration
- Set up GitHub Actions for automatic deployment
- Auto-convert notebook when changes detected

## 📱 Mobile Responsiveness

The site is fully responsive and optimized for:
- **Desktop**: Full feature set with side-by-side layouts
- **Tablet**: Adapted layouts with touch-friendly navigation
- **Mobile**: Stacked layouts with optimized typography

## 🎨 Design Features

- **Modern CSS**: Flexbox and Grid layouts
- **Color Scheme**: Environmental greens and blues
- **Typography**: Clean, readable fonts
- **Accessibility**: Proper contrast and semantic HTML
- **Performance**: Optimized images and minimal dependencies

---

## ✅ Deployment Checklist

- [ ] GitHub repository created
- [ ] All site files copied to repository root
- [ ] Files committed and pushed
- [ ] GitHub Pages enabled (Settings → Pages)
- [ ] Site URL accessible and working
- [ ] All links and navigation functional
- [ ] Mobile responsiveness verified

**🎉 Congratulations! Your Website Carbon API EDA is now live on GitHub Pages!**