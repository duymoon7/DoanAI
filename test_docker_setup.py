"""
Test script to verify Docker setup is working correctly.
Run this after starting docker-compose to verify everything is configured properly.
"""
import requests
import time
import sys

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def test_backend_health():
    """Test if backend is healthy"""
    print("\n🔍 Testing backend health...")
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy" and data.get("database") == "connected":
                print("✅ Backend is healthy and connected to database")
                return True
            else:
                print(f"⚠️  Backend responded but status is: {data}")
                return False
        else:
            print(f"❌ Backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to backend: {e}")
        return False

def test_database_tables():
    """Test if database tables are created"""
    print("\n🔍 Testing database tables...")
    try:
        response = requests.get("http://localhost:8000/debug/tables", timeout=5)
        if response.status_code == 200:
            data = response.json()
            table_count = data.get("actual_count", 0)
            status = data.get("status", "unknown")
            
            if table_count >= 6 and status == "ok":
                print(f"✅ Database has {table_count} tables")
                print(f"   Tables: {', '.join(data.get('actual_tables', []))}")
                return True
            else:
                print(f"⚠️  Expected 6 tables, found {table_count}")
                print(f"   Status: {status}")
                print(f"   Message: {data.get('message', 'N/A')}")
                return False
        else:
            print(f"❌ Tables endpoint returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot check tables: {e}")
        return False

def test_categories():
    """Test if categories are seeded"""
    print("\n🔍 Testing categories...")
    try:
        response = requests.get("http://localhost:8000/api/danh-muc", timeout=5)
        if response.status_code == 200:
            categories = response.json()
            if len(categories) >= 6:
                print(f"✅ Found {len(categories)} categories")
                for cat in categories[:3]:
                    print(f"   - {cat.get('ten_danh_muc', 'N/A')}")
                if len(categories) > 3:
                    print(f"   ... and {len(categories) - 3} more")
                return True
            else:
                print(f"⚠️  Expected at least 6 categories, found {len(categories)}")
                return False
        else:
            print(f"❌ Categories endpoint returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot fetch categories: {e}")
        return False

def test_products():
    """Test if products are seeded"""
    print("\n🔍 Testing products...")
    try:
        response = requests.get("http://localhost:8000/api/san-pham", timeout=5)
        if response.status_code == 200:
            products = response.json()
            if len(products) >= 10:
                print(f"✅ Found {len(products)} products")
                for prod in products[:3]:
                    print(f"   - {prod.get('ten_san_pham', 'N/A')} - {prod.get('gia', 0):,}đ")
                if len(products) > 3:
                    print(f"   ... and {len(products) - 3} more")
                return True
            else:
                print(f"⚠️  Expected at least 10 products, found {len(products)}")
                return False
        else:
            print(f"❌ Products endpoint returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot fetch products: {e}")
        return False

def test_api_docs():
    """Test if API documentation is accessible"""
    print("\n🔍 Testing API documentation...")
    try:
        response = requests.get("http://localhost:8000/docs", timeout=5)
        if response.status_code == 200:
            print("✅ API documentation is accessible")
            return True
        else:
            print(f"❌ API docs returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot access API docs: {e}")
        return False

def test_cors():
    """Test if CORS is configured"""
    print("\n🔍 Testing CORS configuration...")
    try:
        headers = {"Origin": "http://localhost:3000"}
        response = requests.get("http://localhost:8000/api/san-pham", headers=headers, timeout=5)
        
        if "access-control-allow-origin" in response.headers:
            print("✅ CORS is configured")
            print(f"   Allowed origin: {response.headers.get('access-control-allow-origin')}")
            return True
        else:
            print("⚠️  CORS headers not found in response")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot test CORS: {e}")
        return False

def main():
    """Main test function"""
    print_header("🐳 Docker Setup Verification")
    print("\nThis script will verify your Docker setup is working correctly.")
    print("Make sure you have started docker-compose before running this test.")
    print("\nWaiting 5 seconds for services to be ready...")
    time.sleep(5)
    
    # Run all tests
    tests = [
        ("Backend Health", test_backend_health),
        ("Database Tables", test_database_tables),
        ("Categories", test_categories),
        ("Products", test_products),
        ("API Documentation", test_api_docs),
        ("CORS Configuration", test_cors),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test '{test_name}' failed with error: {e}")
            results.append((test_name, False))
    
    # Print summary
    print_header("📊 Test Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\nTests passed: {passed}/{total}")
    print("\nResults:")
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {test_name}")
    
    # Print access URLs
    print_header("🌐 Access URLs")
    print("\n  Backend API:     http://localhost:8000/docs")
    print("  Health Check:    http://localhost:8000/health")
    print("  pgAdmin:         http://localhost:5050")
    print("  Frontend:        http://localhost:3000 (run separately)")
    
    # Print credentials
    print_header("🔐 Credentials")
    print("\n  pgAdmin:")
    print("    Email:    admin@admin.com")
    print("    Password: admin")
    print("\n  PostgreSQL:")
    print("    Host:     postgres (Docker) or localhost (host)")
    print("    Port:     5432")
    print("    Database: electronics_db")
    print("    User:     postgres")
    print("    Password: 123456")
    
    # Exit with appropriate code
    if passed == total:
        print_header("✅ All Tests Passed!")
        print("\nYour Docker setup is working correctly.")
        print("You can now start the frontend with: cd frontend && npm run dev")
        sys.exit(0)
    else:
        print_header("⚠️  Some Tests Failed")
        print("\nPlease check the errors above and try:")
        print("  1. docker-compose logs -f backend")
        print("  2. docker-compose restart backend")
        print("  3. docker-compose down -v && docker-compose up --build")
        sys.exit(1)

if __name__ == "__main__":
    main()
