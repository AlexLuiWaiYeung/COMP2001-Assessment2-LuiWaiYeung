import requests

BASE_URL = "http://localhost:5000"

def test_endpoints():
    """Test all API endpoints"""
    
    print("Testing TrailService API...\n")
    
    # 1. Test home endpoint
    print("1. Testing home endpoint:")
    response = requests.get(f"{BASE_URL}/")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}\n")
    
    # 2. Test health endpoint
    print("2. Testing health endpoint:")
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}\n")
    
    # 3. Test trails endpoint
    print("3. Testing trails endpoint:")
    response = requests.get(f"{BASE_URL}/api/trails")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Found {data.get('count', 0)} trails")
    else:
        print(f"   Error: {response.json()}\n")
    
    print("All tests completed!")

if __name__ == "__main__":
    test_endpoints()