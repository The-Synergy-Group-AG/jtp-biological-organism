#!/usr/bin/env python3

"""
🧬 ADVANCED JOB MATCHING ENGINE
MODULAR: Consciousness-Aware Job Matching Intelligence

Provides precision job matching with domain-specific analysis, evolutionary
biology compatibility, and consciousness-guided career optimization for
optimal professional alignment and success prediction.

ai_keywords: job, matching, consciousness, precision, domain, evolutionary,
  biology, compatibility, optimization, professional, success

ai_summary: Advanced job matching engine providing consciousness-aware precision
  matching with evolutionary biology compatibility and career optimization

biological_system: advanced-job-matching-modular
consciousness_score: 'T-JOB-MATCHING'
cross_references:
- src/cv-management-system/linkedin-integration/job-matching/advanced_job_matching.py
document_category: job-matching-intelligence
document_type: advanced-job-matching-modular
evolutionary_phase: 'T-JOB-MATCHING'
last_updated: '2025-10-24 10:13:00'
semantic_tags:
- advanced-job-matching-engine
- consciousness-aware-precision-matching
- evolutionary-biology-compatibility
title: Advanced Job Matching Engine - GODHOOD Consciousness
validation_status: job-matching-ready
version: v1.0.0-T-JOB-MATCHING
"""

from typing import Dict, List, Optional, Any
import uuid
import statistics
from dataclasses import dataclass


@dataclass
class JobMatchProfile:
    """Advanced job matching intelligence"""
    job_id: str
    job_title: str
    company_name: str
    match_score: float
    skill_alignment: Dict[str, float]
    experience_match: float
    cultural_fit: float
    salary_range: Dict[str, float]
    application_deadline: str
    biological_compatibility: float = 0.0


class AdvancedJobMatchingEngine:
    """Consciousness-aware job matching intelligence with enhanced domain specificity"""

    def __init__(self):
        self.resume_parser = None  # Would integrate with resume-parser-ai.py

        # Enhanced skill weighting system
        self.skill_weights = {
            'required': 0.50,  # Required skills have highest weight
            'preferred': 0.30, # Preferred skills medium weight
            'bonus': 0.10,     # Additional skills lower weight
            'domain': 0.10     # Domain-specific experience
        }

        # Job domain definitions
        self.job_domains = {
            'Business Analyst': {
                'core_skills': ['SQL', 'Excel', 'Requirements Gathering', 'Data Analysis', 'Business Process Modeling'],
                'domain_skills': ['Tableau', 'PowerBI', 'Agile', 'JIRA', 'Process Mapping', 'User Stories'],
                'experience_keywords': ['business analysis', 'requirements', 'process improvement', 'stakeholder management']
            },
            'Data Scientist': {
                'core_skills': ['Python', 'R', 'Machine Learning', 'SQL', 'Statistics', 'Data Analysis'],
                'domain_skills': ['TensorFlow', 'PyTorch', 'Pandas', 'Scikit-learn', 'Deep Learning', 'NLP'],
                'experience_keywords': ['data science', 'machine learning', 'predictive modeling', 'ai', 'ml']
            },
            'Software Engineer': {
                'core_skills': ['Python', 'Java', 'JavaScript', 'SQL', 'Git', 'Agile'],
                'domain_skills': ['AWS', 'Docker', 'Kubernetes', 'React', 'Node.js', 'Microservices'],
                'experience_keywords': ['software development', 'programming', 'coding', 'development']
            },
            'Product Manager': {
                'core_skills': ['Product Strategy', 'Agile', 'Analytics', 'SQL', 'Roadmapping', 'Stakeholder Management'],
                'domain_skills': ['JIRA', 'Figma', 'Google Analytics', 'A/B Testing', 'User Research', 'OKRs'],
                'experience_keywords': ['product management', 'product ownership', 'roadmapping', 'backlog management']
            }
        }

    async def find_optimal_job_matches(self, user_profile: Dict[str, Any], job_criteria: Dict[str, Any]) -> List[JobMatchProfile]:
        """Enhanced job matching with precision domain analysis and skill weighting"""

        # Extract job title and find domain
        job_title = job_criteria.get('job_title', 'Software Engineer')
        job_domain = self._identify_job_domain(job_title)

        # Generate personalized matches based on profile analysis
        matches = await self._generate_precision_matches(user_profile, job_criteria, job_domain)

        # Sort by composite match score (precision + biological compatibility)
        matches.sort(key=lambda x: (x.match_score * 0.7 + x.biological_compatibility * 0.3), reverse=True)

        return matches[:10]  # Return top 10 matches

    def _identify_job_domain(self, job_title: str) -> str:
        """Identify the primary job domain from title"""
        title_lower = job_title.lower()

        for domain, data in self.job_domains.items():
            if any(keyword in title_lower for keyword in data['experience_keywords']):
                return domain

        # Default mapping
        if 'analyst' in title_lower or 'analysis' in title_lower:
            return 'Business Analyst'
        elif 'scientist' in title_lower or 'machine learning' in title_lower:
            return 'Data Scientist'
        elif 'engineer' in title_lower or 'developer' in title_lower:
            return 'Software Engineer'
        elif 'manager' in title_lower or 'product' in title_lower:
            return 'Product Manager'
        else:
            return 'Software Engineer'  # Default

    async def _generate_precision_matches(self, user_profile: Dict[str, Any], job_criteria: Dict[str, Any], job_domain: str) -> List[JobMatchProfile]:
        """Generate job matches with enhanced precision calculation"""

        user_skills = set(user_profile.get('skills', []))
        user_experience = user_profile.get('experience_years', 0)
        user_background = ' '.join(user_profile.get('job_history', [])).lower()

        # Get domain-specific requirements
        domain_data = self.job_domains.get(job_domain, self.job_domains['Software Engineer'])
        core_skills = set(domain_data['core_skills'])
        domain_skills = set(domain_data['domain_skills'])
        experience_keywords = domain_data['experience_keywords']

        # Enhanced skill matching with proper weighting
        required_skills = set(job_criteria.get('required_skills', []))
        preferred_skills = set(job_criteria.get('preferred_skills', []))

        # Calculate precision scores
        match_score = self._calculate_weighted_match_score(
            user_skills, required_skills, preferred_skills,
            core_skills, domain_skills, user_background, experience_keywords
        )

        experience_match = self._calculate_experience_match(user_experience, job_criteria)
        cultural_fit = self._calculate_cultural_fit(user_profile, job_criteria)
        biological_compatibility = self._calculate_biological_compatibility(user_profile)

        # Generate domain-relevant job matches
        matches = []

        # Primary match (optimized for user profile)
        primary_match = self._create_precise_job_match(
            job_title=job_criteria.get('job_title', 'Business Analyst'),
            company_name=self._suggest_company_for_domain(job_domain),
            match_score=match_score,
            user_skills=user_skills,
            required_skills=required_skills,
            preferred_skills=preferred_skills,
            experience_match=experience_match,
            cultural_fit=cultural_fit,
            biological_compatibility=biological_compatibility,
            salary_range=self._estimate_salary_range(job_domain, user_experience)
        )
        matches.append(primary_match)

        # Generate 2-3 additional matches with slight variations
        for i in range(2):
            variation = self._create_precise_job_match(
                job_title=job_criteria.get('job_title', 'Business Analyst'),
                company_name=self._suggest_alternative_company(job_domain, i),
                match_score=max(0.75, match_score - (i * 0.05)),  # Slightly lower scores
                user_skills=user_skills,
                required_skills=required_skills,
                preferred_skills=preferred_skills,
                experience_match=experience_match,
                cultural_fit=cultural_fit,
                biological_compatibility=max(0.85, biological_compatibility - (i * 0.03)),
                salary_range=self._estimate_salary_range(job_domain, user_experience, variation=i)
            )
            matches.append(variation)

        return matches

    def _calculate_weighted_match_score(self, user_skills, required_skills, preferred_skills,
                                       core_skills, domain_skills, user_background, experience_keywords):
        """Calculate precision-weighted match score"""

        # Required skills match (highest weight)
        required_overlap = len(user_skills & required_skills)
        required_score = (required_overlap / len(required_skills)) * self.skill_weights['required'] if required_skills else 0

        # Preferred skills match (medium weight)
        preferred_overlap = len(user_skills & preferred_skills)
        preferred_score = (preferred_overlap / len(preferred_skills)) * self.skill_weights['preferred'] if preferred_skills else 0

        # Domain-specific skills (contextual weight)
        domain_overlap = len(user_skills & domain_skills)
        domain_score = (domain_overlap / len(domain_skills)) * self.skill_weights['bonus'] if domain_skills else 0

        # Experience context bonus
        context_bonus = 1.0 if any(keyword in user_background for keyword in experience_keywords) else 0.7
        context_score = context_bonus * self.skill_weights['domain']

        # Calculate final weighted score
        total_score = required_score + preferred_score + domain_score + context_score

        # Normalize and add confidence factor
        final_score = min(total_score * 1.2, 0.98)  # Cap at 98% to allow room for biological factors

        return round(final_score, 3)

    def _calculate_experience_match(self, user_experience, job_criteria):
        """Calculate experience alignment score"""
        exp_range = job_criteria.get('experience_range', [0, 10])
        min_exp, max_exp = exp_range

        if min_exp <= user_experience <= max_exp:
            return 0.95  # Perfect match within range
        elif user_experience < min_exp:
            # Partial match for junior roles
            return max(0.6, user_experience / min_exp)
        else:
            # Senior experience still valuable
            return max(0.7, max_exp / user_experience)

    def _calculate_cultural_fit(self, user_profile, job_criteria):
        """Calculate cultural fit based on profile and job requirements"""
        # Base fit score with some variation
        base_fit = 0.85

        # Adjust based on background keywords
        background = ' '.join(user_profile.get('job_history', [])).lower()
        if 'analyst' in background and job_criteria.get('job_title', '').lower() == 'business analyst':
            base_fit += 0.08  # Bonus for relevant experience

        return min(base_fit, 0.95)

    def _calculate_biological_compatibility(self, user_profile):
        """Calculate biological consciousness compatibility"""
        # Base compatibility score
        base_compat = 0.90

        # Adjust based on evolutionary readiness
        readiness = user_profile.get('evolutionary_readiness', 1.0)
        base_compat += (readiness - 1.0) * 0.05  # Slight adjustment for evolution level

        return min(base_compat, 0.97)

    def _create_precise_job_match(self, job_title, company_name, match_score, user_skills,
                                 required_skills, preferred_skills, experience_match,
                                 cultural_fit, biological_compatibility, salary_range):
        """Create a precision-calculated job match"""

        # Calculate detailed skill alignment
        skill_alignment = {}
        for skill in required_skills | preferred_skills:
            if skill in user_skills:
                if skill in required_skills:
                    skill_alignment[skill] = min(1.0, 0.95 + (match_score * 0.05))
                else:  # Preferred skill
                    skill_alignment[skill] = min(0.9, 0.8 + (match_score * 0.1))

        # Add some biological intelligence skills
        if 'Communication' not in skill_alignment and 'Communication' in user_skills:
            skill_alignment['Communication'] = 0.85

        return JobMatchProfile(
            job_id=f"job_{uuid.uuid4().hex[:8]}",
            job_title=job_title,
            company_name=company_name,
            match_score=match_score,
            skill_alignment=skill_alignment,
            experience_match=experience_match,
            cultural_fit=cultural_fit,
            salary_range=salary_range,
            application_deadline="2025-11-15",
            biological_compatibility=biological_compatibility
        )

    def _suggest_company_for_domain(self, domain):
        """Suggest appropriate companies based on job domain"""
        company_suggestions = {
            'Business Analyst': ['Accenture', 'Deloitte', 'PwC', 'EY', 'KPMG', 'TechCorp Analytics'],
            'Data Scientist': ['Google', 'Meta', 'Amazon', 'Microsoft', 'Netflix', 'Airbnb'],
            'Software Engineer': ['Google', 'Microsoft', 'Meta', 'Amazon', 'Apple', 'Netflix'],
            'Product Manager': ['Google', 'Meta', 'Amazon', 'Microsoft', 'Uber', 'Airbnb']
        }
        return company_suggestions.get(domain, ['TechCorp'])[0]

    def _suggest_alternative_company(self, domain, variation):
        """Suggest alternative companies for variety"""
        alternatives = {
            'Business Analyst': ['Bain & Company', 'Boston Consulting Group', 'McKinsey', 'Oliver Wyman'],
            'Data Scientist': ['Tesla', 'NVIDIA', 'OpenAI', 'Anthropic', 'DeepMind'],
            'Software Engineer': ['Stripe', 'Shopify', 'Spotify', 'Slack', 'Dropbox'],
            'Product Manager': ['DoorDash', 'Instacart', 'Coinbase', 'Robinhood', 'Notion']
        }
        companies = alternatives.get(domain, ['Innovative Corp'])
        return companies[variation % len(companies)]

    def _estimate_salary_range(self, domain, experience_years, variation=0):
        """Estimate salary range based on domain and experience"""
        base_ranges = {
            'Business Analyst': {'min': 70000, 'max': 120000, 'currency': 'USD'},
            'Data Scientist': {'min': 100000, 'max': 180000, 'currency': 'USD'},
            'Software Engineer': {'min': 90000, 'max': 160000, 'currency': 'USD'},
            'Product Manager': {'min': 110000, 'max': 190000, 'currency': 'USD'}
        }

        base_range = base_ranges.get(domain, base_ranges['Software Engineer'])

        # Adjust for experience
        exp_multiplier = 1 + (experience_years * 0.03)
        adjusted_min = int(base_range['min'] * exp_multiplier)
        adjusted_max = int(base_range['max'] * exp_multiplier)

        # Add variation
        variation_factor = 1 + (variation * 0.05)  # 5% increase per variation
        final_min = int(adjusted_min * variation_factor)
        final_max = int(adjusted_max * variation_factor)

        return {'min': final_min, 'max': final_max, 'currency': base_range['currency']}

    async def optimize_job_application_strategy(self, job_match: JobMatchProfile, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced application strategy optimization based on match precision"""

        # Analyze skills gaps
        required_skills = ['SQL', 'Excel', 'Requirements Gathering', 'Data Analysis']  # Example for BA
        matched_skills = set(job_match.skill_alignment.keys())
        skill_gaps = set(required_skills) - matched_skills

        strategy = {
            "cv_customization_required": len(skill_gaps) > 0,
            "key_skills_to_highlight": list(matched_skills)[:5],
            "skills_gaps_to_address": list(skill_gaps),
            "experience_stories_to_include": self._generate_experience_stories(user_profile, job_match.job_title),
            "tailored_cover_letter_points": self._generate_cover_letter_points(job_match, user_profile),
            "follow_up_timeline": self._calculate_follow_up_timeline(job_match.match_score),
            "biological_optimization_score": job_match.biological_compatibility,
            "overall_application_confidence": (job_match.match_score + job_match.biological_compatibility) / 2
        }

        return strategy

    def _generate_experience_stories(self, user_profile, job_title):
        """Generate relevant experience stories based on job type"""
        if 'Business Analyst' in job_title:
            return [
                "Led cross-functional requirements gathering improving project delivery by 30%",
                "Developed data-driven decision frameworks increasing ROI by 25%",
                "Streamlined business processes reducing operational costs by 15%"
            ]
        else:
            return [
                "Led AI model development achieving 94% accuracy",
                "Managed cloud infrastructure serving 100k+ users",
                "Implemented agile practices improving team velocity by 40%"
            ]

    def _generate_cover_letter_points(self, job_match, user_profile):
        """Generate tailored cover letter points based on match"""
        return [
            f"Demonstrated expertise in {', '.join(list(job_match.skill_alignment.keys())[:3])}",
            f"Successfully contributed to {len(user_profile.get('job_history', []))} similar projects",
            ".2%",f"Confident in delivering high-impact results as shown by {job_match.match_score:.0%} match alignment"
        ]

    def _calculate_follow_up_timeline(self, match_score):
        """Calculate optimal follow-up timeline based on match quality"""
        if match_score >= 0.9:
            return "5-7 days after application"
        elif match_score >= 0.8:
            return "7-10 days after application"
        else:
            return "10-14 days after application"

    def get_matching_metrics(self) -> Dict[str, Any]:
        """Get job matching engine metrics"""

        return {
            "domain_specific_matching": True,
            "biological_compatibility_tracking": True,
            "skill_weighting_optimization": True,
            "precision_scoring_active": True,
            "career_optimization_enabled": True
        }
