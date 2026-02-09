from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///freelance_platform.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Import models and services after app initialization
from models import User, FreelancerProfile, Job, Application, Payment
from matching_service import MatchingService
from payment_service import PaymentService

matching_service = MatchingService()
payment_service = PaymentService()

# ============= AUTHENTICATION ROUTES =============
@app.route('/', methods=['GET'])
def hello():
    return "Hello "


@app.route('/api/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    # Validation
    if not all(k in data for k in ['email', 'password', 'name', 'user_type']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if data['user_type'] not in ['freelancer', 'employer']:
        return jsonify({'error': 'Invalid user type'}), 400
    
    # Check if user exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 409
    
    # Create user
    user = User(
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        name=data['name'],
        user_type=data['user_type'],
        phone=data.get('phone'),
        location=data.get('location')
    )
    
    db.session.add(user)
    db.session.commit()
    
    # Create access token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'message': 'User registered successfully',
        'access_token': access_token,
        'user': user.to_dict()
    }), 201

@app.route('/api/login', methods=['POST'])
def login():
    """User login"""
    data = request.get_json()
    
    if not all(k in data for k in ['email', 'password']):
        return jsonify({'error': 'Missing email or password'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'access_token': access_token,
        'user': user.to_dict()
    }), 200

@app.route('/api/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200

# ============= FREELANCER PROFILE ROUTES =============

@app.route('/api/freelancer/profile', methods=['POST', 'PUT'])
@jwt_required()
def create_update_freelancer_profile():
    """Create or update freelancer profile"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.user_type != 'freelancer':
        return jsonify({'error': 'Only freelancers can create profiles'}), 403
    
    data = request.get_json()
    
    profile = FreelancerProfile.query.filter_by(user_id=user_id).first()
    
    if profile:
        # Update existing profile
        profile.title = data.get('title', profile.title)
        profile.bio = data.get('bio', profile.bio)
        profile.skills = data.get('skills', profile.skills)
        profile.experience_years = data.get('experience_years', profile.experience_years)
        profile.hourly_rate = data.get('hourly_rate', profile.hourly_rate)
        profile.availability = data.get('availability', profile.availability)
        profile.portfolio_url = data.get('portfolio_url', profile.portfolio_url)
        profile.languages = data.get('languages', profile.languages)
    else:
        # Create new profile
        profile = FreelancerProfile(
            user_id=user_id,
            title=data.get('title'),
            bio=data.get('bio'),
            skills=data.get('skills', []),
            experience_years=data.get('experience_years', 0),
            hourly_rate=data.get('hourly_rate'),
            availability=data.get('availability', 'full-time'),
            portfolio_url=data.get('portfolio_url'),
            languages=data.get('languages', ['English', 'Hindi'])
        )
        db.session.add(profile)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Profile saved successfully',
        'profile': profile.to_dict()
    }), 200

@app.route('/api/freelancer/profile/<int:user_id>', methods=['GET'])
def get_freelancer_profile(user_id):
    """Get a freelancer's public profile"""
    profile = FreelancerProfile.query.filter_by(user_id=user_id).first()
    
    if not profile:
        return jsonify({'error': 'Profile not found'}), 404
    
    return jsonify(profile.to_dict()), 200

# ============= JOB ROUTES =============

@app.route('/api/jobs', methods=['POST'])
@jwt_required()
def create_job():
    """Create a new job posting"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.user_type != 'employer':
        return jsonify({'error': 'Only employers can post jobs'}), 403
    
    data = request.get_json()
    
    # Validation
    required_fields = ['title', 'description', 'budget', 'required_skills']
    if not all(k in data for k in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    job = Job(
        employer_id=user_id,
        title=data['title'],
        description=data['description'],
        required_skills=data['required_skills'],
        budget=data['budget'],
        duration=data.get('duration'),
        experience_level=data.get('experience_level', 'intermediate'),
        job_type=data.get('job_type', 'project'),
        location=data.get('location'),
        payment_type=data.get('payment_type', 'fixed')
    )
    
    db.session.add(job)
    db.session.commit()
    
    return jsonify({
        'message': 'Job created successfully',
        'job': job.to_dict()
    }), 201

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    """Get all jobs with optional filtering"""
    # Query parameters
    skills = request.args.get('skills')
    job_type = request.args.get('job_type')
    experience_level = request.args.get('experience_level')
    min_budget = request.args.get('min_budget', type=float)
    max_budget = request.args.get('max_budget', type=float)
    location = request.args.get('location')
    status = request.args.get('status', 'open')
    
    query = Job.query.filter_by(status=status)
    
    # Apply filters
    if skills:
        skill_list = skills.split(',')
        for skill in skill_list:
            query = query.filter(Job.required_skills.contains([skill.strip()]))
    
    if job_type:
        query = query.filter_by(job_type=job_type)
    
    if experience_level:
        query = query.filter_by(experience_level=experience_level)
    
    if min_budget:
        query = query.filter(Job.budget >= min_budget)
    
    if max_budget:
        query = query.filter(Job.budget <= max_budget)
    
    if location:
        query = query.filter(Job.location.ilike(f'%{location}%'))
    
    jobs = query.order_by(Job.created_at.desc()).all()
    
    return jsonify({
        'jobs': [job.to_dict() for job in jobs],
        'count': len(jobs)
    }), 200

@app.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """Get a specific job"""
    job = Job.query.get(job_id)
    
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify(job.to_dict()), 200

@app.route('/api/jobs/<int:job_id>', methods=['PUT'])
@jwt_required()
def update_job(job_id):
    """Update a job posting"""
    user_id = get_jwt_identity()
    job = Job.query.get(job_id)
    
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    if job.employer_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    # Update fields
    job.title = data.get('title', job.title)
    job.description = data.get('description', job.description)
    job.required_skills = data.get('required_skills', job.required_skills)
    job.budget = data.get('budget', job.budget)
    job.duration = data.get('duration', job.duration)
    job.status = data.get('status', job.status)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Job updated successfully',
        'job': job.to_dict()
    }), 200

# ============= AI MATCHING ROUTES =============

@app.route('/api/jobs/<int:job_id>/recommendations', methods=['GET'])
@jwt_required()
def get_job_recommendations(job_id):
    """Get AI-recommended freelancers for a job"""
    user_id = get_jwt_identity()
    job = Job.query.get(job_id)
    
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    if job.employer_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get all freelancer profiles
    freelancers = FreelancerProfile.query.all()
    
    # Get recommendations using AI matching
    recommendations = matching_service.match_freelancers_to_job(job, freelancers)
    
    return jsonify({
        'job': job.to_dict(),
        'recommendations': recommendations
    }), 200

@app.route('/api/freelancer/job-recommendations', methods=['GET'])
@jwt_required()
def get_freelancer_job_recommendations():
    """Get AI-recommended jobs for a freelancer"""
    user_id = get_jwt_identity()
    profile = FreelancerProfile.query.filter_by(user_id=user_id).first()
    
    if not profile:
        return jsonify({'error': 'Freelancer profile not found'}), 404
    
    # Get open jobs
    jobs = Job.query.filter_by(status='open').all()
    
    # Get recommendations using AI matching
    recommendations = matching_service.match_jobs_to_freelancer(profile, jobs)
    
    return jsonify({
        'recommendations': recommendations
    }), 200

# ============= APPLICATION ROUTES =============

@app.route('/api/jobs/<int:job_id>/apply', methods=['POST'])
@jwt_required()
def apply_to_job(job_id):
    """Apply to a job"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.user_type != 'freelancer':
        return jsonify({'error': 'Only freelancers can apply to jobs'}), 403
    
    job = Job.query.get(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    if job.status != 'open':
        return jsonify({'error': 'Job is not open for applications'}), 400
    
    # Check if already applied
    existing = Application.query.filter_by(job_id=job_id, freelancer_id=user_id).first()
    if existing:
        return jsonify({'error': 'Already applied to this job'}), 409
    
    data = request.get_json()
    
    application = Application(
        job_id=job_id,
        freelancer_id=user_id,
        cover_letter=data.get('cover_letter'),
        proposed_rate=data.get('proposed_rate'),
        estimated_duration=data.get('estimated_duration')
    )
    
    db.session.add(application)
    db.session.commit()
    
    return jsonify({
        'message': 'Application submitted successfully',
        'application': application.to_dict()
    }), 201

@app.route('/api/jobs/<int:job_id>/applications', methods=['GET'])
@jwt_required()
def get_job_applications(job_id):
    """Get all applications for a job"""
    user_id = get_jwt_identity()
    job = Job.query.get(job_id)
    
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    if job.employer_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    applications = Application.query.filter_by(job_id=job_id).all()
    
    return jsonify({
        'applications': [app.to_dict() for app in applications],
        'count': len(applications)
    }), 200

@app.route('/api/applications/<int:application_id>/status', methods=['PUT'])
@jwt_required()
def update_application_status(application_id):
    """Update application status (accept/reject)"""
    user_id = get_jwt_identity()
    application = Application.query.get(application_id)
    
    if not application:
        return jsonify({'error': 'Application not found'}), 404
    
    job = Job.query.get(application.job_id)
    if job.employer_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    new_status = data.get('status')
    
    if new_status not in ['accepted', 'rejected']:
        return jsonify({'error': 'Invalid status'}), 400
    
    application.status = new_status
    
    if new_status == 'accepted':
        job.status = 'in_progress'
    
    db.session.commit()
    
    return jsonify({
        'message': 'Application status updated',
        'application': application.to_dict()
    }), 200

# ============= PAYMENT ROUTES =============

@app.route('/api/payments/create', methods=['POST'])
@jwt_required()
def create_payment():
    """Create a payment for a job"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    job_id = data.get('job_id')
    job = Job.query.get(job_id)
    
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    if job.employer_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get accepted application
    application = Application.query.filter_by(
        job_id=job_id,
        status='accepted'
    ).first()
    
    if not application:
        return jsonify({'error': 'No accepted application found'}), 404
    
    # Create payment
    payment = Payment(
        job_id=job_id,
        employer_id=user_id,
        freelancer_id=application.freelancer_id,
        amount=data.get('amount', job.budget),
        payment_method=data.get('payment_method', 'upi'),
        currency='INR'
    )
    
    db.session.add(payment)
    db.session.commit()
    
    # Process payment (mock integration)
    result = payment_service.process_payment(payment)
    
    return jsonify({
        'message': 'Payment created',
        'payment': payment.to_dict(),
        'payment_result': result
    }), 201

@app.route('/api/payments/<int:payment_id>/release', methods=['POST'])
@jwt_required()
def release_payment(payment_id):
    """Release payment to freelancer"""
    user_id = get_jwt_identity()
    payment = Payment.query.get(payment_id)
    
    if not payment:
        return jsonify({'error': 'Payment not found'}), 404
    
    if payment.employer_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if payment.status != 'held':
        return jsonify({'error': 'Payment cannot be released'}), 400
    
    payment.status = 'completed'
    payment.released_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'message': 'Payment released successfully',
        'payment': payment.to_dict()
    }), 200

@app.route('/api/payments/history', methods=['GET'])
@jwt_required()
def get_payment_history():
    """Get payment history for current user"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.user_type == 'employer':
        payments = Payment.query.filter_by(employer_id=user_id).all()
    else:
        payments = Payment.query.filter_by(freelancer_id=user_id).all()
    
    return jsonify({
        'payments': [p.to_dict() for p in payments],
        'count': len(payments)
    }), 200

# ============= DASHBOARD ROUTES =============

@app.route('/api/dashboard/stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    """Get dashboard statistics"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.user_type == 'employer':
        jobs_posted = Job.query.filter_by(employer_id=user_id).count()
        active_jobs = Job.query.filter_by(employer_id=user_id, status='open').count()
        total_spent = db.session.query(db.func.sum(Payment.amount)).filter_by(
            employer_id=user_id, status='completed'
        ).scalar() or 0
        
        return jsonify({
            'jobs_posted': jobs_posted,
            'active_jobs': active_jobs,
            'total_spent': total_spent
        }), 200
    else:
        applications = Application.query.filter_by(freelancer_id=user_id).count()
        accepted = Application.query.filter_by(freelancer_id=user_id, status='accepted').count()
        total_earned = db.session.query(db.func.sum(Payment.amount)).filter_by(
            freelancer_id=user_id, status='completed'
        ).scalar() or 0
        
        return jsonify({
            'applications_sent': applications,
            'jobs_won': accepted,
            'total_earned': total_earned
        }), 200

# ============= SEARCH ROUTES =============

@app.route('/api/search/freelancers', methods=['GET'])
def search_freelancers():
    """Search freelancers by skills, location, etc."""
    skills = request.args.get('skills')
    location = request.args.get('location')
    min_rate = request.args.get('min_rate', type=float)
    max_rate = request.args.get('max_rate', type=float)
    availability = request.args.get('availability')
    
    query = FreelancerProfile.query
    
    if skills:
        skill_list = skills.split(',')
        for skill in skill_list:
            query = query.filter(FreelancerProfile.skills.contains([skill.strip()]))
    
    if min_rate:
        query = query.filter(FreelancerProfile.hourly_rate >= min_rate)
    
    if max_rate:
        query = query.filter(FreelancerProfile.hourly_rate <= max_rate)
    
    if availability:
        query = query.filter_by(availability=availability)
    
    if location:
        query = query.join(User).filter(User.location.ilike(f'%{location}%'))
    
    profiles = query.all()
    
    return jsonify({
        'freelancers': [p.to_dict() for p in profiles],
        'count': len(profiles)
    }), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
