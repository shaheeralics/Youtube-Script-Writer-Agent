import requests
import json

def test_backend(base_url="http://localhost:8000"):
    """Test the FastAPI backend endpoints"""
    
    print(f"🧪 Testing YouTube Script Writer Backend at {base_url}")
    print("-" * 60)
    
    # Test health endpoint
    try:
        print("1️⃣ Testing health endpoint...")
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['status']}")
            print(f"   OpenAI configured: {data['openai_configured']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    print()
    
    # Test script generation
    try:
        print("2️⃣ Testing script generation...")
        test_data = {
            "topic": "Python Programming for Beginners",
            "style": "educational",
            "duration": "medium",
            "target_audience": "beginners"
        }
        
        response = requests.post(
            f"{base_url}/generate-script",
            headers={"Content-Type": "application/json"},
            json=test_data
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Script generation successful!")
            print(f"   Word count: {data['word_count']}")
            print(f"   Duration: {data['estimated_duration']}")
            print(f"   Sections: {len(data['sections'])}")
            print(f"   Script preview: {data['script'][:100]}...")
        else:
            print(f"❌ Script generation failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Script generation error: {e}")
    
    print()
    print("🏁 Testing complete!")

if __name__ == "__main__":
    test_backend()
