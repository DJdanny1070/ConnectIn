"""
AI-based matching service for freelancers and jobs
Uses skill matching, experience level, budget compatibility, and availability
"""

from typing import List, Dict
import math

class MatchingService:
    """Service to match freelancers with jobs using AI algorithms"""
    
    def __init__(self):
        self.skill_weights = {
            'exact_match': 1.0,
            'partial_match': 0.5,
            'related_match': 0.3
        }
        
        # Related skills mapping for better matching
        self.related_skills = {
            'python': ['django', 'flask', 'fastapi', 'pandas', 'numpy'],
            'javascript': ['react', 'node.js', 'vue', 'angular', 'express'],
            'java': ['spring', 'hibernate', 'maven', 'gradle'],
            'react': ['javascript', 'redux', 'next.js', 'typescript'],
            'node.js': ['javascript', 'express', 'mongodb', 'postgresql'],
            'django': ['python', 'postgresql', 'rest api'],
            'flask': ['python', 'rest api', 'sqlalchemy'],
            'aws': ['cloud', 'devops', 'docker', 'kubernetes'],
            'docker': ['kubernetes', 'devops', 'aws', 'linux'],
            'postgresql': ['sql', 'database', 'mysql'],
            'mysql': ['sql', 'database', 'postgresql'],
            'mongodb': ['nosql', 'database', 'node.js'],
        }
    
    def calculate_skill_match_score(self, required_skills: List[str], freelancer_skills: List[str]) -> float:
        """
        Calculate skill match score between job requirements and freelancer skills
        Returns a score between 0 and 1
        """
        if not required_skills or not freelancer_skills:
            return 0.0
        
        # Normalize skills to lowercase
        required_skills_lower = [skill.lower().strip() for skill in required_skills]
        freelancer_skills_lower = [skill.lower().strip() for skill in freelancer_skills]
        
        total_score = 0.0
        max_score = len(required_skills_lower)
        
        for required_skill in required_skills_lower:
            if required_skill in freelancer_skills_lower:
                # Exact match
                total_score += self.skill_weights['exact_match']
            else:
                # Check for partial matches
                partial_match = False
                for freelancer_skill in freelancer_skills_lower:
                    if required_skill in freelancer_skill or freelancer_skill in required_skill:
                        total_score += self.skill_weights['partial_match']
                        partial_match = True
                        break
                
                # Check for related skills
                if not partial_match and required_skill in self.related_skills:
                    for freelancer_skill in freelancer_skills_lower:
                        if freelancer_skill in self.related_skills[required_skill]:
                            total_score += self.skill_weights['related_match']
                            break
        
        return min(total_score / max_score, 1.0) if max_score > 0 else 0.0
    
    def calculate_experience_score(self, required_level: str, freelancer_years: int) -> float:
        """
        Calculate experience match score
        Returns a score between 0 and 1
        """
        experience_requirements = {
            'entry': (0, 2),
            'intermediate': (2, 5),
            'expert': (5, 100)
        }
        
        if not required_level or required_level.lower() not in experience_requirements:
            return 0.5  # Neutral score if not specified
        
        min_exp, max_exp = experience_requirements[required_level.lower()]
        
        if min_exp <= freelancer_years <= max_exp:
            return 1.0
        elif freelancer_years > max_exp:
            # Over-qualified
            return 0.8
        else:
            # Under-qualified
            gap = min_exp - freelancer_years
            return max(0.0, 1.0 - (gap * 0.2))
    
    def calculate_budget_score(self, job_budget: float, freelancer_rate: float, 
                               job_type: str, duration: str = None) -> float:
        """
        Calculate budget compatibility score
        Returns a score between 0 and 1
        """
        if not freelancer_rate or not job_budget:
            return 0.5  # Neutral score if not specified
        
        # Estimate project hours based on duration or assume standard
        estimated_hours = 160  # Default: 1 month full-time
        
        if duration:
            duration_lower = duration.lower()
            if 'week' in duration_lower:
                weeks = int(''.join(filter(str.isdigit, duration_lower)) or '1')
                estimated_hours = weeks * 40
            elif 'month' in duration_lower:
                months = int(''.join(filter(str.isdigit, duration_lower)) or '1')
                estimated_hours = months * 160
        
        if job_type == 'hourly':
            estimated_cost = freelancer_rate * estimated_hours
        else:
            estimated_cost = freelancer_rate * estimated_hours  # Rough estimate
        
        if estimated_cost <= job_budget:
            # Within budget
            utilization = estimated_cost / job_budget
            return 1.0 if utilization >= 0.7 else 0.8 + (utilization * 0.2)
        else:
            # Over budget
            overage = (estimated_cost - job_budget) / job_budget
            return max(0.0, 1.0 - overage)
    
    def calculate_availability_score(self, job_type: str, freelancer_availability: str) -> float:
        """
        Calculate availability match score
        Returns a score between 0 and 1
        """
        compatibility = {
            'project': {'full-time': 1.0, 'part-time': 0.7, 'contract': 1.0},
            'hourly': {'full-time': 0.8, 'part-time': 1.0, 'contract': 0.8},
            'contract': {'full-time': 1.0, 'part-time': 0.6, 'contract': 1.0}
        }
        
        job_type = job_type.lower() if job_type else 'project'
        freelancer_availability = freelancer_availability.lower() if freelancer_availability else 'full-time'
        
        return compatibility.get(job_type, {}).get(freelancer_availability, 0.5)
    
    def calculate_overall_match_score(self, job, freelancer_profile) -> Dict:
        """
        Calculate overall match score combining all factors
        """
        # Individual scores
        skill_score = self.calculate_skill_match_score(
            job.required_skills or [],
            freelancer_profile.skills or []
        )
        
        experience_score = self.calculate_experience_score(
            job.experience_level,
            freelancer_profile.experience_years or 0
        )
        
        budget_score = self.calculate_budget_score(
            job.budget,
            freelancer_profile.hourly_rate or 0,
            job.job_type,
            job.duration
        )
        
        availability_score = self.calculate_availability_score(
            job.job_type,
            freelancer_profile.availability
        )
        
        # Weighted combination
        weights = {
            'skills': 0.4,
            'experience': 0.25,
            'budget': 0.25,
            'availability': 0.1
        }
        
        overall_score = (
            skill_score * weights['skills'] +
            experience_score * weights['experience'] +
            budget_score * weights['budget'] +
            availability_score * weights['availability']
        )
        
        # Calculate match percentage
        match_percentage = round(overall_score * 100, 1)
        
        # Determine match level
        if match_percentage >= 80:
            match_level = 'excellent'
        elif match_percentage >= 60:
            match_level = 'good'
        elif match_percentage >= 40:
            match_level = 'fair'
        else:
            match_level = 'poor'
        
        return {
            'overall_score': overall_score,
            'match_percentage': match_percentage,
            'match_level': match_level,
            'breakdown': {
                'skill_match': round(skill_score * 100, 1),
                'experience_match': round(experience_score * 100, 1),
                'budget_compatibility': round(budget_score * 100, 1),
                'availability_match': round(availability_score * 100, 1)
            }
        }
    
    def match_freelancers_to_job(self, job, freelancers: List) -> List[Dict]:
        """
        Find and rank the best freelancers for a job
        """
        matches = []
        
        for freelancer in freelancers:
            match_data = self.calculate_overall_match_score(job, freelancer)
            
            # Only include matches above a threshold
            if match_data['match_percentage'] >= 30:
                matches.append({
                    'freelancer': freelancer.to_dict(),
                    'match_score': match_data['match_percentage'],
                    'match_level': match_data['match_level'],
                    'score_breakdown': match_data['breakdown'],
                    'recommendation': self._generate_recommendation(match_data, job, freelancer)
                })
        
        # Sort by match score (highest first)
        matches.sort(key=lambda x: x['match_score'], reverse=True)
        
        # Return top 10 matches
        return matches[:10]
    
    def match_jobs_to_freelancer(self, freelancer_profile, jobs: List) -> List[Dict]:
        """
        Find and rank the best jobs for a freelancer
        """
        matches = []
        
        for job in jobs:
            match_data = self.calculate_overall_match_score(job, freelancer_profile)
            
            # Only include matches above a threshold
            if match_data['match_percentage'] >= 30:
                matches.append({
                    'job': job.to_dict(),
                    'match_score': match_data['match_percentage'],
                    'match_level': match_data['match_level'],
                    'score_breakdown': match_data['breakdown'],
                    'recommendation': self._generate_recommendation(match_data, job, freelancer_profile)
                })
        
        # Sort by match score (highest first)
        matches.sort(key=lambda x: x['match_score'], reverse=True)
        
        # Return top 10 matches
        return matches[:10]
    
    def _generate_recommendation(self, match_data: Dict, job, freelancer) -> str:
        """
        Generate a human-readable recommendation based on match data
        """
        breakdown = match_data['breakdown']
        match_level = match_data['match_level']
        
        if match_level == 'excellent':
            base = "Highly recommended match! "
        elif match_level == 'good':
            base = "Good match with strong potential. "
        elif match_level == 'fair':
            base = "Fair match. "
        else:
            base = "Consider carefully. "
        
        details = []
        
        if breakdown['skill_match'] >= 80:
            details.append("Excellent skill alignment")
        elif breakdown['skill_match'] >= 60:
            details.append("Good skill fit")
        else:
            details.append("Some skill gaps to consider")
        
        if breakdown['experience_match'] >= 80:
            details.append("experience level is perfect")
        elif breakdown['experience_match'] < 60:
            details.append("experience level may not be ideal")
        
        if breakdown['budget_compatibility'] >= 80:
            details.append("budget is well-aligned")
        elif breakdown['budget_compatibility'] < 60:
            details.append("budget compatibility needs review")
        
        return base + ", ".join(details) + "."
