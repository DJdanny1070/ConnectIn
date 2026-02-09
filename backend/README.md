# Indian Freelancing Platform - Backend API

A Flask-based backend for a localized freelancing platform tailored to the Indian market. Features AI-driven matching, support for Indian payment methods (UPI, Net Banking, Cards, Wallets), and escrow payment system.

## 🚀 Features

### Core Functionality
- **User Authentication**: JWT-based authentication for freelancers and employers
- **Freelancer Profiles**: Detailed profiles with skills, experience, portfolio, and rates
- **Job Posting & Search**: Advanced job search with filters (skills, budget, location, experience)
- **AI-Based Matching**: Intelligent matching algorithm that scores freelancers for jobs based on:
  - Skill compatibility (exact, partial, and related skills)
  - Experience level alignment
  - Budget compatibility
  - Availability matching
- **Application System**: Freelancers can apply to jobs with cover letters and proposed rates
- **Payment Integration**: Support for Indian payment methods with escrow system
- **Dashboard Stats**: Analytics for both freelancers and employers

### Indian Market Features
- ✅ UPI payment support (GPay, PhonePe, Paytm, BHIM)
- ✅ Net Banking integration
- ✅ Card payments (Visa, Mastercard, RuPay)
- ✅ Digital Wallets (Paytm, PhonePe, Mobikwik)
- ✅ INR currency by default
- ✅ Regional language support ready
- ✅ Escrow payment system for secure transactions

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## 🛠️ Installation

1. **Clone or download the project files**

2. **Create a virtual environment** (recommended):
```bash
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Mac/Linux
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:
```bash
cp .env.example .env
# Edit .env and add your configuration
```

5. **Initialize the database**:
```bash
python app.py
```
The database will be created automatically on first run.

## 🚀 Running the Application

Start the Flask server:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## 📚 API Documentation

### Authentication

#### Register User
```http
POST /api/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword",
  "name": "John Doe",
  "user_type": "freelancer",  // or "employer"
  "phone": "+91-9876543210",
  "location": "Mumbai, Maharashtra"
}
```

**Response:**
```json
{
  "message": "User registered successfully",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "user_type": "freelancer"
  }
}
```

#### Login
```http
POST /api/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

#### Get Profile
```http
GET /api/profile
Authorization: Bearer <token>
```

### Freelancer Profile

#### Create/Update Profile
```http
POST /api/freelancer/profile
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Full Stack Developer",
  "bio": "Experienced developer specializing in Python and React",
  "skills": ["Python", "Django", "React", "PostgreSQL", "AWS"],
  "experience_years": 5,
  "hourly_rate": 2000,
  "availability": "full-time",
  "portfolio_url": "https://myportfolio.com",
  "languages": ["English", "Hindi", "Marathi"]
}
```

#### Get Freelancer Profile
```http
GET /api/freelancer/profile/<user_id>
```

### Jobs

#### Create Job
```http
POST /api/jobs
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "E-commerce Website Development",
  "description": "Need a full-stack developer to build an e-commerce platform",
  "required_skills": ["Python", "Django", "React", "PostgreSQL"],
  "budget": 150000,
  "duration": "2 months",
  "experience_level": "intermediate",
  "job_type": "project",
  "location": "remote",
  "payment_type": "fixed"
}
```

#### Get All Jobs (with filters)
```http
GET /api/jobs?skills=Python,React&job_type=project&min_budget=50000&max_budget=200000&location=Mumbai&status=open
```

#### Get Specific Job
```http
GET /api/jobs/<job_id>
```

#### Update Job
```http
PUT /api/jobs/<job_id>
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Updated title",
  "status": "open"
}
```

### AI Matching

#### Get Recommended Freelancers for Job
```http
GET /api/jobs/<job_id>/recommendations
Authorization: Bearer <token>
```

**Response:**
```json
{
  "job": { ... },
  "recommendations": [
    {
      "freelancer": { ... },
      "match_score": 87.5,
      "match_level": "excellent",
      "score_breakdown": {
        "skill_match": 90.0,
        "experience_match": 85.0,
        "budget_compatibility": 88.0,
        "availability_match": 87.0
      },
      "recommendation": "Highly recommended match! Excellent skill alignment, experience level is perfect, budget is well-aligned."
    }
  ]
}
```

#### Get Recommended Jobs for Freelancer
```http
GET /api/freelancer/job-recommendations
Authorization: Bearer <token>
```

### Applications

#### Apply to Job
```http
POST /api/jobs/<job_id>/apply
Authorization: Bearer <token>
Content-Type: application/json

{
  "cover_letter": "I am very interested in this project...",
  "proposed_rate": 2500,
  "estimated_duration": "6 weeks"
}
```

#### Get Job Applications
```http
GET /api/jobs/<job_id>/applications
Authorization: Bearer <token>
```

#### Update Application Status
```http
PUT /api/applications/<application_id>/status
Authorization: Bearer <token>
Content-Type: application/json

{
  "status": "accepted"  // or "rejected"
}
```

### Payments

#### Create Payment
```http
POST /api/payments/create
Authorization: Bearer <token>
Content-Type: application/json

{
  "job_id": 1,
  "amount": 150000,
  "payment_method": "upi"  // upi, netbanking, card, wallet
}
```

#### Release Payment
```http
POST /api/payments/<payment_id>/release
Authorization: Bearer <token>
```

#### Get Payment History
```http
GET /api/payments/history
Authorization: Bearer <token>
```

### Dashboard

#### Get Dashboard Stats
```http
GET /api/dashboard/stats
Authorization: Bearer <token>
```

**For Employers:**
```json
{
  "jobs_posted": 15,
  "active_jobs": 8,
  "total_spent": 450000
}
```

**For Freelancers:**
```json
{
  "applications_sent": 25,
  "jobs_won": 12,
  "total_earned": 380000
}
```

### Search

#### Search Freelancers
```http
GET /api/search/freelancers?skills=Python,React&location=Mumbai&min_rate=1500&max_rate=3000&availability=full-time
```

## 🧠 AI Matching Algorithm

The matching system uses a sophisticated scoring algorithm:

### Scoring Components

1. **Skill Match (40% weight)**
   - Exact match: 100% score
   - Partial match: 50% score
   - Related skills: 30% score
   - Uses skill relationship mapping for better matches

2. **Experience Match (25% weight)**
   - Entry level: 0-2 years
   - Intermediate: 2-5 years
   - Expert: 5+ years
   - Over-qualification penalty: 20%

3. **Budget Compatibility (25% weight)**
   - Considers hourly rate vs project budget
   - Estimates project hours from duration
   - Optimal range: 70-100% budget utilization

4. **Availability Match (10% weight)**
   - Matches job type with freelancer availability
   - Full-time, part-time, contract compatibility matrix

### Match Levels
- **Excellent**: 80%+ match
- **Good**: 60-79% match
- **Fair**: 40-59% match
- **Poor**: <40% match

## 💳 Payment Flow

1. **Job Acceptance**: Employer accepts freelancer application
2. **Payment Creation**: Employer creates payment and funds are held in escrow
3. **Work Completion**: Freelancer completes the project
4. **Payment Release**: Employer releases payment to freelancer
5. **Payout**: Funds transferred to freelancer's bank account

### Supported Payment Methods

- **UPI**: GPay, PhonePe, Paytm, BHIM (instant, 0 fees)
- **Net Banking**: All major Indian banks
- **Cards**: Visa, Mastercard, RuPay
- **Wallets**: Paytm, PhonePe, Mobikwik, Amazon Pay

## 🔒 Security Features

- JWT-based authentication
- Password hashing with Werkzeug
- CORS protection
- SQL injection protection via SQLAlchemy ORM
- Escrow payment system

## 🗄️ Database Schema

### Users
- Authentication and basic info
- User type (freelancer/employer)

### FreelancerProfiles
- Skills, experience, rates
- Portfolio, availability
- Rating and earnings

### Jobs
- Job details and requirements
- Budget, duration, type
- Status tracking

### Applications
- Cover letter and proposals
- Status (pending/accepted/rejected)

### Payments
- Transaction tracking
- Escrow management
- Multiple payment methods

## 📊 Example Use Cases

### 1. Freelancer Finding Jobs
```python
# 1. Login
POST /api/login

# 2. Create profile
POST /api/freelancer/profile

# 3. Get personalized job recommendations
GET /api/freelancer/job-recommendations

# 4. Apply to a job
POST /api/jobs/5/apply
```

### 2. Employer Hiring Freelancer
```python
# 1. Register as employer
POST /api/register

# 2. Post a job
POST /api/jobs

# 3. Get AI-recommended freelancers
GET /api/jobs/5/recommendations

# 4. Review applications
GET /api/jobs/5/applications

# 5. Accept application
PUT /api/applications/12/status

# 6. Create payment
POST /api/payments/create
```

## 🚧 Future Enhancements

- [ ] Real payment gateway integration (Razorpay, Paytm, PhonePe)
- [ ] Email notifications
- [ ] Real-time chat between freelancers and employers
- [ ] Review and rating system
- [ ] Dispute resolution system
- [ ] Multi-language support (Hindi, Tamil, Telugu, etc.)
- [ ] Mobile app APIs
- [ ] Advanced analytics dashboard
- [ ] Milestone-based payments
- [ ] Contract generation
- [ ] Tax invoice generation (GST compliant)

## 🐛 Error Handling

All endpoints return appropriate HTTP status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `409`: Conflict (e.g., duplicate email)
- `500`: Internal Server Error

Error response format:
```json
{
  "error": "Error message here"
}
```

## 🧪 Testing

Test the API using:
- **Postman**: Import endpoints and test
- **cURL**: Command-line testing
- **Python requests**: Automated testing

Example cURL:
```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "name": "Test User",
    "user_type": "freelancer"
  }'
```

## 📝 Notes

- This is a development version with SQLite database
- For production, use PostgreSQL or MySQL
- Replace mock payment processing with actual gateway integration
- Add proper email service for notifications
- Implement rate limiting for API endpoints
- Add comprehensive logging
- Set up proper error monitoring (Sentry, etc.)

## 🤝 Contributing

Feel free to extend this platform with:
- Additional payment methods
- Enhanced matching algorithms
- More sophisticated search filters
- Regional language support
- Mobile-specific endpoints

## 📄 License

This project is open-source and available for educational purposes.

## 📧 Support

For issues or questions, please check the API documentation or review the code comments.
