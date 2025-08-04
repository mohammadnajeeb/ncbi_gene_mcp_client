#!/usr/bin/env python3
"""
Test script to verify the app works before Vercel deployment.
"""

import sys
import requests
import time
from pathlib import Path

def test_local_server():
    """Test the local development server."""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing NCBI Gene MCP Client before Vercel deployment...\n")
    
    # Test 1: Health check
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/api/health", timeout=10)
        if response.status_code == 200:
            print("   ✅ Health check passed")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
        return False
    
    # Test 2: Home page
    print("2. Testing home page...")
    try:
        response = requests.get(base_url, timeout=10)
        if response.status_code == 200 and "NCBI Gene Explorer" in response.text:
            print("   ✅ Home page loaded successfully")
        else:
            print(f"   ❌ Home page failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Home page error: {e}")
        return False
    
    # Test 3: Gene search API
    print("3. Testing gene search API...")
    try:
        data = {"query": "BRCA1", "max_results": "5"}
        response = requests.post(f"{base_url}/api/search/genes", data=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            if result.get("success") and result.get("data", {}).get("count", 0) > 0:
                print(f"   ✅ Gene search passed (found {result['data']['count']} genes)")
            else:
                print("   ❌ Gene search returned no results")
                return False
        else:
            print(f"   ❌ Gene search failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Gene search error: {e}")
        return False
    
    # Test 4: Symbol search API
    print("4. Testing symbol search API...")
    try:
        data = {"symbol": "TP53", "organism": "human"}
        response = requests.post(f"{base_url}/api/search/symbol", data=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            if result.get("success") and result.get("data", {}).get("count", 0) > 0:
                print(f"   ✅ Symbol search passed (found {result['data']['count']} genes)")
            else:
                print("   ❌ Symbol search returned no results")
                return False
        else:
            print(f"   ❌ Symbol search failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Symbol search error: {e}")
        return False
    
    # Test 5: Gene by ID
    print("5. Testing gene by ID...")
    try:
        response = requests.get(f"{base_url}/api/gene/672", timeout=30)
        if response.status_code == 200:
            result = response.json()
            if result.get("success") and "BRCA1" in str(result.get("data", {})):
                print("   ✅ Gene by ID passed (BRCA1 found)")
            else:
                print(f"   ❌ Gene by ID returned incorrect data: {result}")
                return False
        else:
            print(f"   ❌ Gene by ID failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Gene by ID error: {e}")
        return False
    
    print("\n🎉 All tests passed! Ready for Vercel deployment.")
    print("\n📋 Deployment checklist:")
    print("   □ Push code to Git repository")
    print("   □ Connect repository to Vercel")
    print("   □ Deploy and test live URL")
    print("   □ Update any hardcoded localhost URLs")
    
    return True

def check_deployment_files():
    """Check if all deployment files exist."""
    print("📁 Checking deployment files...\n")
    
    required_files = [
        "vercel.json",
        "requirements.txt", 
        "api/index.py",
        "ncbi_gene_mcp_client/web_app.py",
        "ncbi_gene_mcp_client/templates/index.html"
    ]
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - MISSING")
            return False
    
    print("\n✅ All deployment files present")
    return True

if __name__ == "__main__":
    print("🚀 NCBI Gene MCP Client - Pre-deployment Test\n")
    
    # Check deployment files
    if not check_deployment_files():
        print("❌ Missing deployment files. Fix and try again.")
        sys.exit(1)
    
    print("\n" + "="*50)
    print("Make sure the server is running on localhost:8000")
    print("Run: python -m ncbi_gene_mcp_client.web_app")
    print("="*50 + "\n")
    
    input("Press Enter when server is ready...")
    
    # Run tests
    if test_local_server():
        print("\n🚀 Ready to deploy to Vercel!")
        print("\nNext steps:")
        print("1. git add .")
        print("2. git commit -m 'Add Vercel deployment config'")
        print("3. git push")
        print("4. Connect to Vercel and deploy")
    else:
        print("\n❌ Tests failed. Fix issues before deploying.")
        sys.exit(1)
