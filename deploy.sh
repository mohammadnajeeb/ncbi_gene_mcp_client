#!/bin/bash

# NCBI Gene MCP Client - Vercel Deployment Script

echo "🚀 NCBI Gene MCP Client - Vercel Deployment Helper"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "vercel.json" ]; then
    echo "❌ Error: vercel.json not found. Are you in the project root?"
    exit 1
fi

echo "✅ Found vercel.json"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "🔧 Initializing git repository..."
    git init
    echo "✅ Git repository initialized"
fi

# Check if files are staged
if [ -z "$(git status --porcelain)" ]; then
    echo "✅ No changes to commit"
else
    echo "📝 Staging files for deployment..."
    git add .
    echo "✅ Files staged"
    
    echo "💾 Committing changes..."
    git commit -m "Add Vercel deployment configuration

- Added vercel.json for deployment config
- Added requirements.txt for dependencies  
- Added api/index.py as entry point
- Updated .gitignore for Vercel
- Added deployment documentation"
    echo "✅ Changes committed"
fi

# Check if Vercel CLI is installed
if command -v vercel &> /dev/null; then
    echo "✅ Vercel CLI found"
    
    echo ""
    echo "🤔 How would you like to deploy?"
    echo "1) Deploy with Vercel CLI (quick)"
    echo "2) Manual deployment via Vercel Dashboard"
    echo "3) Just prepare files (no deployment)"
    
    read -p "Choose option (1-3): " choice
    
    case $choice in
        1)
            echo ""
            echo "🚀 Deploying with Vercel CLI..."
            vercel --prod
            ;;
        2)
            echo ""
            echo "📋 Manual deployment steps:"
            echo "1. Go to https://vercel.com/dashboard"
            echo "2. Click 'New Project'"
            echo "3. Import your Git repository"
            echo "4. Use these settings:"
            echo "   - Framework Preset: Other"
            echo "   - Root Directory: ./"
            echo "   - Build Command: (leave empty)"
            echo "   - Output Directory: (leave empty)"
            echo "5. Click 'Deploy'"
            ;;
        3)
            echo ""
            echo "✅ Files prepared for deployment"
            echo "📋 Ready for manual deployment to Vercel"
            ;;
        *)
            echo "❌ Invalid choice"
            exit 1
            ;;
    esac
else
    echo "ℹ️  Vercel CLI not found"
    echo ""
    echo "📋 Manual deployment steps:"
    echo "1. Push your code to GitHub/GitLab/Bitbucket"
    echo "2. Go to https://vercel.com/dashboard"
    echo "3. Click 'New Project'"
    echo "4. Import your Git repository"
    echo "5. Use these settings:"
    echo "   - Framework Preset: Other"  
    echo "   - Root Directory: ./"
    echo "   - Build Command: (leave empty)"
    echo "   - Output Directory: (leave empty)"
    echo "6. Click 'Deploy'"
    echo ""
    echo "💡 To install Vercel CLI: npm i -g vercel"
fi

echo ""
echo "📚 For detailed instructions, see DEPLOYMENT.md"
echo "🎉 Good luck with your deployment!"
