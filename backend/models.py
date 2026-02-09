from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model):
    """User model for both freelancers and employers"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # 'freelancer' or 'employer'
    phone = db.Column(db.String(20))
    location = db.Column(db.String(100))
    profile_image = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    freelancer_profile = db.relationship('FreelancerProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    jobs_posted = db.relationship('Job', backref='employer', foreign_keys='Job.employer_id', cascade='all, delete-orphan')
    applications = db.relationship('Application', backref='freelancer', foreign_keys='Application.freelancer_id', cascade='all, delete-orphan')
    payments_made = db.relationship('Payment', backref='employer', foreign_keys='Payment.employer_id', cascade='all, delete-orphan')
    payments_received = db.relationship('Payment', backref='freelancer', foreign_keys='Payment.freelancer_id')
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'user_type': self.user_type,
            'phone': self.phone,
            'location': self.location,
            'profile_image': self.profile_image,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class FreelancerProfile(db.Model):
    """Freelancer profile with skills and portfolio"""
    __tablename__ = 'freelancer_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    title = db.Column(db.String(200))  # e.g., "Full Stack Developer"
    bio = db.Column(db.Text)
    skills = db.Column(db.JSON)  # List of skills
    experience_years = db.Column(db.Integer, default=0)
    hourly_rate = db.Column(db.Float)  # in INR
    availability = db.Column(db.String(50))  # 'full-time', 'part-time', 'contract'
    portfolio_url = db.Column(db.String(255))
    languages = db.Column(db.JSON)  # Languages spoken
    rating = db.Column(db.Float, default=0.0)
    total_jobs_completed = db.Column(db.Integer, default=0)
    total_earnings = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user': self.user.to_dict() if self.user else None,
            'title': self.title,
            'bio': self.bio,
            'skills': self.skills or [],
            'experience_years': self.experience_years,
            'hourly_rate': self.hourly_rate,
            'availability': self.availability,
            'portfolio_url': self.portfolio_url,
            'languages': self.languages or [],
            'rating': self.rating,
            'total_jobs_completed': self.total_jobs_completed,
            'total_earnings': self.total_earnings,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Job(db.Model):
    """Job posting model"""
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    employer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    required_skills = db.Column(db.JSON, nullable=False)  # List of required skills
    budget = db.Column(db.Float, nullable=False)  # in INR
    duration = db.Column(db.String(100))  # e.g., "2 weeks", "1 month"
    experience_level = db.Column(db.String(50))  # 'entry', 'intermediate', 'expert'
    job_type = db.Column(db.String(50))  # 'project', 'hourly', 'contract'
    location = db.Column(db.String(100))  # Can be 'remote' or specific location
    payment_type = db.Column(db.String(50))  # 'fixed', 'hourly', 'milestone'
    status = db.Column(db.String(50), default='open')  # 'open', 'in_progress', 'completed', 'cancelled'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deadline = db.Column(db.DateTime)
    
    # Relationships
    applications = db.relationship('Application', backref='job', cascade='all, delete-orphan')
    payments = db.relationship('Payment', backref='job', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'employer_id': self.employer_id,
            'employer': self.employer.to_dict() if self.employer else None,
            'title': self.title,
            'description': self.description,
            'required_skills': self.required_skills or [],
            'budget': self.budget,
            'duration': self.duration,
            'experience_level': self.experience_level,
            'job_type': self.job_type,
            'location': self.location,
            'payment_type': self.payment_type,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'applications_count': len(self.applications) if self.applications else 0
        }

class Application(db.Model):
    """Job application model"""
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    freelancer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    cover_letter = db.Column(db.Text)
    proposed_rate = db.Column(db.Float)  # Freelancer's proposed rate
    estimated_duration = db.Column(db.String(100))
    status = db.Column(db.String(50), default='pending')  # 'pending', 'accepted', 'rejected'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'job_id': self.job_id,
            'job': self.job.to_dict() if self.job else None,
            'freelancer_id': self.freelancer_id,
            'freelancer': self.freelancer.to_dict() if self.freelancer else None,
            'cover_letter': self.cover_letter,
            'proposed_rate': self.proposed_rate,
            'estimated_duration': self.estimated_duration,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Payment(db.Model):
    """Payment model for transactions"""
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    employer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    freelancer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default='INR')
    payment_method = db.Column(db.String(50))  # 'upi', 'netbanking', 'card', 'wallet'
    transaction_id = db.Column(db.String(100), unique=True)
    status = db.Column(db.String(50), default='pending')  # 'pending', 'held', 'completed', 'failed', 'refunded'
    payment_gateway = db.Column(db.String(50))  # 'razorpay', 'paytm', 'phonepe', etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    released_at = db.Column(db.DateTime)  # When payment released to freelancer
    
    def to_dict(self):
        return {
            'id': self.id,
            'job_id': self.job_id,
            'employer_id': self.employer_id,
            'freelancer_id': self.freelancer_id,
            'amount': self.amount,
            'currency': self.currency,
            'payment_method': self.payment_method,
            'transaction_id': self.transaction_id,
            'status': self.status,
            'payment_gateway': self.payment_gateway,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'released_at': self.released_at.isoformat() if self.released_at else None
        }
