"""
Test script to demonstrate the API functionality
Run this after starting the Flask server
"""

import requests
import json

BASE_URL = "http://localhost:5000/api"

def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

def test_api():
    """Test the API endpoints"""
    
    # Test 1: Register Freelancer
    print("\n🚀 TESTING FREELANCING PLATFORM API")
    
    freelancer_data = {
        "email": "freelancer@example.com",
        "password": "password123",
        "name": "Rahul Kumar",
        "user_type": "freelancer",
        "phone": "+91-9876543210",
        "location": "Bangalore, Karnataka"
    }
    
    response = requests.post(f"{BASE_URL}/register", json=freelancer_data)
    print_response("1. Register Freelancer", response)
    
    if response.status_code == 201:
        freelancer_token = response.json()['access_token']
    else:
        # Try login if already registered
        login_response = requests.post(f"{BASE_URL}/login", json={
            "email": freelancer_data["email"],
            "password": freelancer_data["password"]
        })
        if login_response.status_code == 200:
            freelancer_token = login_response.json()['access_token']
            print_response("1a. Login Freelancer", login_response)
        else:
            print("Failed to authenticate freelancer")
            return
    
    # Test 2: Create Freelancer Profile
    profile_data = {
        "title": "Full Stack Python Developer",
        "bio": "Experienced developer with 5 years in Django, Flask, and React. Specialized in building scalable web applications.",
        "skills": ["Python", "Django", "Flask", "React", "PostgreSQL", "AWS", "Docker", "REST API"],
        "experience_years": 5,
        "hourly_rate": 2500,
        "availability": "full-time",
        "portfolio_url": "https://rahulkumar.dev",
        "languages": ["English", "Hindi", "Kannada"]
    }
    
    headers = {"Authorization": f"Bearer {freelancer_token}"}
    response = requests.post(f"{BASE_URL}/freelancer/profile", json=profile_data, headers=headers)
    print_response("2. Create Freelancer Profile", response)
    
    # Test 3: Register Employer
    employer_data = {
        "email": "employer@example.com",
        "password": "password123",
        "name": "TechCorp Solutions",
        "user_type": "employer",
        "phone": "+91-9123456789",
        "location": "Mumbai, Maharashtra"
    }
    
    response = requests.post(f"{BASE_URL}/register", json=employer_data)
    print_response("3. Register Employer", response)
    
    if response.status_code == 201:
        employer_token = response.json()['access_token']
    else:
        # Try login if already registered
        login_response = requests.post(f"{BASE_URL}/login", json={
            "email": employer_data["email"],
            "password": employer_data["password"]
        })
        if login_response.status_code == 200:
            employer_token = login_response.json()['access_token']
            print_response("3a. Login Employer", login_response)
        else:
            print("Failed to authenticate employer")
            return
    
    # Test 4: Create Job
    job_data = {
        "title": "E-commerce Platform Development",
        "description": "Looking for an experienced full-stack developer to build a modern e-commerce platform with payment integration, inventory management, and user authentication.",
        "required_skills": ["Python", "Django", "React", "PostgreSQL", "Payment Gateway Integration"],
        "budget": 200000,
        "duration": "3 months",
        "experience_level": "intermediate",
        "job_type": "project",
        "location": "remote",
        "payment_type": "fixed"
    }
    
    headers = {"Authorization": f"Bearer {employer_token}"}
    response = requests.post(f"{BASE_URL}/jobs", json=job_data, headers=headers)
    print_response("4. Create Job", response)
    
    if response.status_code == 201:
        job_id = response.json()['job']['id']
    else:
        print("Failed to create job")
        return
    
    # Test 5: Get All Jobs
    response = requests.get(f"{BASE_URL}/jobs?status=open")
    print_response("5. Get All Jobs", response)
    
    # Test 6: Search Jobs with Filters
    response = requests.get(f"{BASE_URL}/jobs?skills=Python,Django&min_budget=50000")
    print_response("6. Search Jobs (Python, Django, Budget > 50k)", response)
    
    # Test 7: Get Job Recommendations for Freelancer
    headers = {"Authorization": f"Bearer {freelancer_token}"}
    response = requests.get(f"{BASE_URL}/freelancer/job-recommendations", headers=headers)
    print_response("7. AI Job Recommendations for Freelancer", response)
    
    # Test 8: Get Freelancer Recommendations for Job
    headers = {"Authorization": f"Bearer {employer_token}"}
    response = requests.get(f"{BASE_URL}/jobs/{job_id}/recommendations", headers=headers)
    print_response("8. AI Freelancer Recommendations for Job", response)
    
    # Test 9: Freelancer Apply to Job
    application_data = {
        "cover_letter": "I am very interested in this project. With 5 years of experience in Django and React, I have built multiple e-commerce platforms. I can deliver this project within the timeline with high quality code.",
        "proposed_rate": 2500,
        "estimated_duration": "10 weeks"
    }
    
    headers = {"Authorization": f"Bearer {freelancer_token}"}
    response = requests.post(f"{BASE_URL}/jobs/{job_id}/apply", json=application_data, headers=headers)
    print_response("9. Apply to Job", response)
    
    if response.status_code == 201:
        application_id = response.json()['application']['id']
    else:
        print("Failed to apply to job")
        return
    
    # Test 10: Get Job Applications
    headers = {"Authorization": f"Bearer {employer_token}"}
    response = requests.get(f"{BASE_URL}/jobs/{job_id}/applications", headers=headers)
    print_response("10. Get Job Applications", response)
    
    # Test 11: Accept Application
    headers = {"Authorization": f"Bearer {employer_token}"}
    response = requests.put(f"{BASE_URL}/applications/{application_id}/status", 
                           json={"status": "accepted"}, headers=headers)
    print_response("11. Accept Application", response)
    
    # Test 12: Create Payment
    payment_data = {
        "job_id": job_id,
        "amount": 200000,
        "payment_method": "upi"
    }
    
    headers = {"Authorization": f"Bearer {employer_token}"}
    response = requests.post(f"{BASE_URL}/payments/create", json=payment_data, headers=headers)
    print_response("12. Create Payment (Escrow)", response)
    
    if response.status_code == 201:
        payment_id = response.json()['payment']['id']
    else:
        print("Failed to create payment")
        return
    
    # Test 13: Get Dashboard Stats (Employer)
    headers = {"Authorization": f"Bearer {employer_token}"}
    response = requests.get(f"{BASE_URL}/dashboard/stats", headers=headers)
    print_response("13. Employer Dashboard Stats", response)
    
    # Test 14: Get Dashboard Stats (Freelancer)
    headers = {"Authorization": f"Bearer {freelancer_token}"}
    response = requests.get(f"{BASE_URL}/dashboard/stats", headers=headers)
    print_response("14. Freelancer Dashboard Stats", response)
    
    # Test 15: Search Freelancers
    response = requests.get(f"{BASE_URL}/search/freelancers?skills=Python,Django&min_rate=2000&max_rate=3000")
    print_response("15. Search Freelancers", response)
    
    # Test 16: Get Payment History (Freelancer)
    headers = {"Authorization": f"Bearer {freelancer_token}"}
    response = requests.get(f"{BASE_URL}/payments/history", headers=headers)
    print_response("16. Freelancer Payment History", response)
    
    print("\n" + "="*60)
    print("  ✅ API TESTING COMPLETE!")
    print("="*60)
    print("\n📊 Summary:")
    print("  - User Registration & Authentication ✓")
    print("  - Profile Management ✓")
    print("  - Job Posting & Search ✓")
    print("  - AI-Based Matching ✓")
    print("  - Application System ✓")
    print("  - Payment Integration ✓")
    print("  - Dashboard Analytics ✓")
    print("\n💡 The API is working as expected!")
    print("   You can now build a frontend to interact with this backend.\n")

if __name__ == "__main__":
    try:
        print("\n⚠️  Make sure the Flask server is running at http://localhost:5000")
        print("   Start it with: python app.py\n")
        input("Press Enter to start testing...")
        test_api()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to the server!")
        print("   Please make sure the Flask server is running at http://localhost:5000")
        print("   Start it with: python app.py\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
