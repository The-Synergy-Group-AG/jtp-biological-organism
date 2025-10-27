#!/usr/bin/env python3
"""
LinkedIn Jobs API Client
Integration with LinkedIn Jobs API for real job search and application link generation
"""

import os
import json
import time
import requests
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import sqlite3
from pathlib import Path

logger = logging.getLogger(__name__)

class LinkedInJobsAPI:
    """
    LinkedIn Jobs API Client with OAuth2 authentication and rate limiting
    """

    def __init__(self, client_id: Optional[str] = None, client_secret: Optional[str] = None, db_path: str = "jtp_jobs.db"):
        """
        Initialize LinkedIn API client

        Args:
            client_id: LinkedIn Partner App Client ID
            client_secret: LinkedIn Partner App Client Secret
            db_path: Path to jobs database
        """
        self.client_id = client_id or os.environ.get('LINKEDIN_CLIENT_ID')
        self.client_secret = client_secret or os.environ.get('LINKEDIN_CLIENT_SECRET')

        if not self.client_id or not self.client_secret:
            logger.warning("⚠️ LinkedIn API credentials not found. Using demo mode with mock data.")
            self.demo_mode = True
        else:
            self.demo_mode = False

        self.db_path = db_path
        self.session = None
        self.access_token = None
        self.token_expires_at = None

        # Rate limiting setup
        self.rate_limiter = RateLimiter(max_calls_per_hour=1000)

        # API endpoints
        self.base_url = "https://api.linkedin.com"

        # Initialize database connection
        self.ensure_database_tables()

    def authenticate(self) -> bool:
        """
        Authenticate with LinkedIn using OAuth2 Client Credentials flow

        Returns:
            bool: True if authentication successful
        """
        if self.demo_mode:
            logger.info("Demo mode: Skipping real authentication")
            return True

        try:
            # LinkedIn OAuth2 Client Credentials flow
            client = BackendApplicationClient(client_id=self.client_id)
            oauth = OAuth2Session(client=client)

            # Get access token
            token_url = "https://www.linkedin.com/oauth/v2/accessToken"
            token_data = {
                'grant_type': 'client_credentials',
                'scope': 'r_liteprofile,r_emailaddress,w_member_social'
            }

            auth = requests.auth.HTTPBasicAuth(self.client_id, self.client_secret)
            token_response = requests.post(token_url, data=token_data, auth=auth)

            if token_response.status_code == 200:
                token_data = token_response.json()
                self.access_token = token_data['access_token']
                self.token_expires_at = datetime.now() + timedelta(seconds=token_data['expires_in'] - 300)  # 5 min buffer

                # Create session with token
                self.session = OAuth2Session(client_id=self.client_id, token={'access_token': self.access_token})
                logger.info("✅ LinkedIn API authentication successful")
                return True
            else:
                logger.error(f"❌ LinkedIn API authentication failed: {token_response.text}")
                return False

        except Exception as e:
            logger.error(f"❌ LinkedIn API authentication error: {str(e)}")
            return False

    def is_token_valid(self) -> bool:
        """Check if current access token is still valid"""
        return (self.token_expires_at and
                datetime.now() < self.token_expires_at and
                self.access_token is not None)

    def refresh_token_if_needed(self) -> bool:
        """Refresh access token if expired"""
        if not self.is_token_valid():
            logger.info("🔄 Refreshing LinkedIn API token")
            return self.authenticate()
        return True

    def search_jobs(self, keywords: str = "Business Analyst", location: str = "Zurich",
                   experience_level: str = "", remote_filter: bool = False,
                   limit: int = 25) -> List[Dict[str, Any]]:
        """
        Search for jobs using LinkedIn Jobs API

        Args:
            keywords: Job search keywords
            location: Geographic location
            experience_level: Experience filter (ENTRY_LEVEL, MID_SENIOR, DIRECTOR, etc.)
            remote_filter: Filter for remote jobs
            limit: Maximum results to return

        Returns:
            List of job dictionaries with enriched data
        """
        if self.demo_mode:
            return self._get_demo_jobs(keywords, location, limit)

        # Rate limiting check
        if not self.rate_limiter.can_make_request():
            logger.warning("⚠️ Rate limit exceeded, returning cached results")
            return self._get_cached_results(keywords, location, limit)

        self.refresh_token_if_needed()

        try:
            # LinkedIn Jobs Search API endpoint
            search_endpoint = f"{self.base_url}/v2/jobSearch"
            params = {
                'keywords': keywords,
                'location': location,
                'count': min(limit, 50),  # LinkedIn API limit is 50
                'sort': 'DD'  # DD = Date Descending
            }

            if experience_level:
                params['experience'] = experience_level

            if remote_filter:
                params['f_WT'] = 2  # 2 = Remote work

            # Make API request
            response = self.session.get(search_endpoint, params=params)

            if response.status_code == 200:
                data = response.json()
                jobs = self._process_linkedin_results(data, keywords)

                # Update rate limiter
                self.rate_limiter.record_request()

                logger.info(f"✅ LinkedIn Jobs API: Found {len(jobs)} positions for '{keywords}' in {location}")
                return jobs
            else:
                logger.error(f"❌ LinkedIn Jobs API error: {response.status_code} - {response.text}")
                return []

        except Exception as e:
            logger.error(f"❌ LinkedIn Jobs API request failed: {str(e)}")
            return []

    def get_job_details(self, job_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information for a specific job

        Args:
            job_id: LinkedIn job ID

        Returns:
            Job details dictionary or None if not found
        """
        if self.demo_mode:
            return self._get_demo_job_details(job_id)

        try:
            details_endpoint = f"{self.base_url}/v2/jobs/{job_id}"
            response = self.session.get(details_endpoint)

            if response.status_code == 200:
                job_data = response.json()
                return self._enrich_job_details(job_data)
            else:
                logger.warning(f"❌ Could not fetch job details for {job_id}: {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"❌ Error fetching job details: {str(e)}")
            return None

    def _process_linkedin_results(self, api_response: Dict, search_keywords: str) -> List[Dict]:
        """Process LinkedIn API response into standardized job format"""
        processed_jobs = []

        jobs = api_response.get('elements', [])
        for job in jobs:
            try:
                processed_job = self._standardize_linkedin_job(job, search_keywords)

                # Enrich with additional data if needed
                if processed_job.get('linkedin_id'):
                    job_details = self.get_job_details(processed_job['linkedin_id'])
                    if job_details:
                        processed_job.update(job_details)

                processed_jobs.append(processed_job)

            except Exception as e:
                logger.warning(f"❌ Error processing job: {str(e)}")
                continue

        return processed_jobs

    def _standardize_linkedin_job(self, raw_job: Dict, search_keywords: str) -> Dict:
        """Convert LinkedIn job API response to standardized format"""
        try:
            job = {
                'linkedin_id': raw_job.get('id'),
                'title': raw_job.get('title'),
                'company_name': raw_job.get('companyDetails', {}).get('companyName'),
                'location_city': raw_job.get('locationName', {}).get('preferredGeoPlace', {}).get('cityName'),
                'location_country': raw_job.get('locationName', {}).get('preferredGeoPlace', {}).get('country'),
                'job_description': raw_job.get('description', {}).get('text'),
                'employment_type': raw_job.get('employmentStatus'),
                'experience_level': raw_job.get('experienceLevel'),
                'work_location_type': raw_job.get('workplaceType'),
                'application_method': raw_job.get('applicationMethod'),
                'posted_date': raw_job.get('listedAt'),
                'external_apply_url': raw_job.get('applyMethod', {}).get('companyApplyUrl'),
                'data_source': 'linkedin',
                'scraped_at': datetime.now(),
                'is_active': True,
                'search_keywords': json.dumps([word.strip() for word in search_keywords.split() if word.strip()])
            }

            # Generate LinkedIn apply URL if available
            if job.get('linkedin_id'):
                job['linkedin_apply_url'] = f"https://linkedin.com/jobs/view/{job['linkedin_id']}"
                job['application_urls'] = json.dumps({
                    'linkedin': job['linkedin_apply_url'],
                    'external': job.get('external_apply_url')
                })

            # Extract compensation data if available
            compensation = raw_job.get('compensation', {})
            if compensation:
                job['salary_min'] = compensation.get('startingAmount')
                job['salary_max'] = compensation.get('endingAmount')
                job['salary_currency'] = compensation.get('currencyCode', 'CHF')
                job['salary_period'] = compensation.get('unitReference', 'YEAR')

            # Extract skills if available
            skills = raw_job.get('skills', [])
            if skills:
                job['required_skills'] = json.dumps([skill.get('skill') for skill in skills])

            return job

        except Exception as e:
            logger.error(f"❌ Error standardizing LinkedIn job: {str(e)}")
            return {}

    def _enrich_job_details(self, job_data: Dict) -> Dict:
        """Enrich job with additional details"""
        enriched = {}

        # Extract company industry
        company = job_data.get('companyDetails', {})
        enriched['company_industry'] = company.get('industries', [{}])[0].get('localizedName')
        enriched['company_website'] = company.get('companyPageUrl')
        enriched['company_size_range'] = company.get('employeeCountRange')

        # Extract job benefits and requirements
        enriched['job_benefits'] = job_data.get('benefits')
        enriched['job_functions'] = [func.get('localizedName') for func in job_data.get('jobFunctions', [])]

        # Extract seniority and pay information
        enriched['seniority'] = job_data.get('seniority')

        return enriched

    def _get_demo_jobs(self, keywords: str, location: str, limit: int) -> List[Dict]:
        """Return demo job data when API credentials are unavailable"""
        logger.info("🔄 Returning demo job data for testing")

        demo_jobs = [
            {
                'title': f'Senior {keywords}',
                'company_name': 'Demo Company',
                'location_city': location,
                'location_country': 'Switzerland',
                'job_description': f'Demo job description for {keywords} position in {location}',
                'linkedin_apply_url': f'https://linkedin.com/jobs/view/demo-{keywords.lower().replace(" ", "-")}-{location.lower()}-2025',
                'application_urls': json.dumps({
                    'linkedin': f'https://linkedin.com/jobs/view/demo-{keywords.lower().replace(" ", "-")}-{location.lower()}-2025'
                }),
                'biological_match_score': 92.5,
                'godhood_compatibility': 89.5,
                'data_source': 'linkedin',
                'is_active': True
            }
        ]

        return demo_jobs[:limit]

    def _get_demo_job_details(self, job_id: str) -> Dict:
        """Return demo job details"""
        return {
            'company_industry': 'Technology',
            'company_website': 'https://demo.company.com',
            'job_benefits': ['Health Insurance', 'Remote Work', 'Flexible Hours']
        }

    def _get_cached_results(self, keywords: str, location: str, limit: int) -> List[Dict]:
        """Return cached results when rate limited"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            query = """
            SELECT * FROM jobs
            WHERE title LIKE ? AND location_city LIKE ?
            AND is_active = 1
            ORDER BY biological_match_score DESC
            LIMIT ?
            """

            cursor.execute(query, (f'%{keywords}%', f'%{location}%', limit))
            rows = cursor.fetchall()

            # Convert to dictionaries
            columns = [desc[0] for desc in cursor.description]
            jobs = [dict(zip(columns, row)) for row in rows]

            conn.close()

            if jobs:
                logger.info(f"📋 Returned {len(jobs)} cached job results")
            else:
                logger.info("📋 No cached results available")

            return jobs

        except Exception as e:
            logger.error(f"❌ Error fetching cached results: {str(e)}")
            return []

    def ensure_database_tables(self):
        """Ensure required database tables exist"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Ensure api_limits table exists
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS api_limits (
                    api_provider TEXT PRIMARY KEY,
                    hourly_limit INTEGER,
                    daily_limit INTEGER,
                    current_hourly INTEGER DEFAULT 0,
                    current_daily INTEGER DEFAULT 0,
                    hour_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    day_start DATE DEFAULT CURRENT_DATE
                )
            """)

            # Insert LinkedIn limit if not exists
            cursor.execute("""
                INSERT OR IGNORE INTO api_limits (api_provider, hourly_limit, daily_limit)
                VALUES ('linkedin', 1000, 100000)
            """)

            conn.commit()
            conn.close()
            logger.info("✅ Database tables verified")

        except Exception as e:
            logger.warning(f"Couldn't ensure database tables: {e}")

class RateLimiter:
    """Simple rate limiter for API calls"""

    def __init__(self, max_calls_per_hour: int = 1000):
        self.max_calls_per_hour = max_calls_per_hour
        self.calls_this_hour = 0
        self.hour_start = datetime.now()

    def can_make_request(self) -> bool:
        """Check if we can make another API request"""
        now = datetime.now()

        # Reset counters if hour has changed
        if now - self.hour_start >= timedelta(hours=1):
            self.calls_this_hour = 0
            self.hour_start = now

        return self.calls_this_hour < self.max_calls_per_hour

    def record_request(self):
        """Record that a request was made"""
        self.calls_this_hour += 1


def test_linkedin_api():
    """Test function for LinkedIn Jobs API client"""
    client = LinkedInJobsAPI()

    if not client.demo_mode:
        print("🔍 Testing LinkedIn Jobs API...")
        jobs = client.search_jobs("Business Analyst", "Zurich", limit=3)

        print(f"📊 Found {len(jobs)} job results:")
        for job in jobs:
            print(f"   • {job.get('title', 'Unknown')} at {job.get('company_name', 'Unknown')}")
            if job.get('linkedin_apply_url'):
                print(f"     Apply: {job['linkedin_apply_url']}")
    else:
        print("🔍 Running in demo mode - no real API calls")
        jobs = client.search_jobs("Business Analyst", "Zurich", limit=3)

        print(f"📊 Found {len(jobs)} demo job results:")
        for job in jobs:
            print(f"   • {job.get('title', 'Unknown')} at {job.get('company_name', 'Unknown')}")

if __name__ == "__main__":
    test_linkedin_api()
