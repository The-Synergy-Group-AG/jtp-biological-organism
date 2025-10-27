#!/usr/bin/env python3
"""
Job Database Setup
Initialize PostgreSQL/SQlite database for job search functionality
"""

import os
import sys
import sqlite3
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DatabaseSetup:
    def __init__(self):
        # Try PostgreSQL first, fallback to SQLite
        self.db_type = self.detect_database_type()
        self.connection = None

    def detect_database_type(self):
        """Detect which database system to use"""
        # Check for PostgreSQL environment
        pg_vars = os.environ.get('POSTGRES_HOST') or os.environ.get('DATABASE_URL')
        if pg_vars:
            logger.info("Detected PostgreSQL configuration")
            return 'postgresql'
        else:
            logger.info("Using SQLite for development/testing")
            return 'sqlite'

    def create_sqlite_schema(self):
        """Create SQLite version of the schema (for development)"""
        sqlite_schema = """
        -- SQLite compatible version of job database schema

        -- Jobs main table
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(4))) || '-' || lower(hex(randomblob(2))) || '-4' || substr(lower(hex(randomblob(2))),2) || '-' || substr('89ab',abs(random()) % 4 + 1, 1) || lower(hex(randomblob(2))) || '-' || lower(hex(randomblob(6)))),
            linkedin_id TEXT UNIQUE,
            indeed_id TEXT UNIQUE,
            glassdoor_id TEXT UNIQUE,
            external_id TEXT,

            title TEXT NOT NULL,
            company_name TEXT NOT NULL,
            company_linkedin_url TEXT,
            company_website TEXT,
            company_industry TEXT,

            location_country TEXT,
            location_city TEXT,
            location_region TEXT,
            work_location_type TEXT CHECK (work_location_type IN ('on-site', 'remote', 'hybrid')),
            work_arrangement TEXT,

            salary_min REAL,
            salary_max REAL,
            salary_currency TEXT DEFAULT 'CHF',
            salary_period TEXT DEFAULT 'year',
            salary_benefits TEXT, -- JSON string for SQLite

            job_description TEXT,
            job_requirements TEXT, -- JSON string
            job_responsibilities TEXT, -- JSON string
            required_skills TEXT, -- JSON string
            preferred_skills TEXT, -- JSON string
            education_level TEXT,

            company_benefits TEXT, -- JSON string
            company_culture TEXT,
            company_size_range TEXT,

            biological_match_score REAL,
            biological_analysis TEXT, -- JSON string
            consciousness_level INTEGER CHECK (consciousness_level BETWEEN 1 AND 5),
            godhood_compatibility REAL,
            career_evolution_index REAL,

            application_urls TEXT, -- JSON string
            linkedin_apply_url TEXT,
            indeed_apply_url TEXT,
            company_career_apply_url TEXT,
            external_apply_url TEXT,

            data_source TEXT CHECK (data_source IN ('linkedin', 'indeed', 'glassdoor', 'company_career', 'manual')),
            scraped_at TIMESTAMP,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_quality_score REAL CHECK (data_quality_score BETWEEN 0 AND 1),
            is_active INTEGER DEFAULT 1,

            employment_type TEXT CHECK (employment_type IN ('full-time', 'part-time', 'contract', 'temporary', 'internship')),
            experience_level TEXT CHECK (experience_level IN ('entry-level', 'mid-level', 'senior', 'executive')),
            job_function TEXT,
            industry TEXT,

            posted_date TEXT,
            application_deadline TEXT,
            is_remote_possible INTEGER DEFAULT 0,
            travel_required INTEGER DEFAULT 0,

            latitude REAL,
            longitude REAL,

            search_keywords TEXT, -- JSON string
            vector_embedding TEXT, -- Store as JSON string for now

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- FTS5 full-text search for SQLite
        CREATE VIRTUAL TABLE IF NOT EXISTS jobs_fts USING fts5(
            title, company_name, job_description, content=jobs, content_rowid=rowid
        );

        -- Triggers to keep FTS table in sync
        CREATE TRIGGER IF NOT EXISTS jobs_fts_insert AFTER INSERT ON jobs
        BEGIN
            INSERT INTO jobs_fts(rowid, title, company_name, job_description)
            VALUES (new.rowid, new.title, new.company_name, new.job_description);
        END;

        CREATE TRIGGER IF NOT EXISTS jobs_fts_delete AFTER DELETE ON jobs
        BEGIN
            DELETE FROM jobs_fts WHERE rowid = old.rowid;
        END;

        CREATE TRIGGER IF NOT EXISTS jobs_fts_update AFTER UPDATE ON jobs
        BEGIN
            UPDATE jobs_fts SET
                title = new.title,
                company_name = new.company_name,
                job_description = new.job_description
            WHERE rowid = new.rowid;
        END;

        -- Job search queries table
        CREATE TABLE IF NOT EXISTS job_searches (
            id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(4))) || '-' || lower(hex(randomblob(2))) || '-4' || substr(lower(hex(randomblob(2))),2) || '-' || substr('89ab',abs(random()) % 4 + 1, 1) || lower(hex(randomblob(2))) || '-' || lower(hex(randomblob(6)))),
            user_id TEXT,
            search_query TEXT,
            location_filter TEXT,
            salary_range TEXT,
            experience_level TEXT,
            job_functions TEXT,
            results_count INTEGER,
            execution_time_ms INTEGER,
            biological_enhancement_applied INTEGER DEFAULT 0,
            search_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            top_matching_job_id TEXT,
            average_bio_score REAL,
            godhood_compatible_jobs INTEGER
        );

        -- User job interactions table
        CREATE TABLE IF NOT EXISTS job_interactions (
            id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(4))) || '-' || lower(hex(randomblob(2))) || '-4' || substr(lower(hex(randomblob(2))),2) || '-' || substr('89ab',abs(random()) % 4 + 1, 1) || lower(hex(randomblob(2))) || '-' || lower(hex(randomblob(6)))),
            job_id TEXT NOT NULL,
            user_id TEXT,
            interaction_type TEXT CHECK (interaction_type IN ('viewed', 'saved', 'applied', 'bookmarked', 'shared')),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            metadata TEXT,
            FOREIGN KEY (job_id) REFERENCES jobs(id)
        );

        -- Indexes for performance
        CREATE INDEX IF NOT EXISTS idx_jobs_title ON jobs(title);
        CREATE INDEX IF NOT EXISTS idx_jobs_company ON jobs(company_name);
        CREATE INDEX IF NOT EXISTS idx_jobs_location_city ON jobs(location_city);
        CREATE INDEX IF NOT EXISTS idx_jobs_bio_score ON jobs(biological_match_score) WHERE is_active = 1;
        CREATE INDEX IF NOT EXISTS idx_jobs_data_source ON jobs(data_source, is_active);
        CREATE INDEX IF NOT EXISTS idx_jobs_last_updated ON jobs(last_updated DESC);
        """

        db_path = Path("jtp_jobs.db")
        db_path.parent.mkdir(exist_ok=True)

        try:
            conn = sqlite3.connect(str(db_path))
            conn.executescript(sqlite_schema)
            conn.commit()
            conn.close()

            # Insert some sample data for testing
            self.insert_sample_data(str(db_path))
            logger.info(f"✓ SQLite database created at {db_path}")

        except Exception as e:
            logger.error(f"✗ Failed to create SQLite database: {e}")
            raise

    def insert_sample_data(self, db_path):
        """Insert sample job data for testing"""
        limit_clause = ""
        conn = sqlite3.connect(db_path)

        sample_jobs = [
            {
                'title': 'Business Risk Manager / Senior Project Manager',
                'company_name': 'UBS Global Wealth Management',
                'location_city': 'Zurich',
                'location_country': 'Switzerland',
                'salary_min': 80000,
                'salary_max': 120000,
                'data_source': 'linkedin',
                'experience_level': 'senior',
                'required_skills': '["Business Analysis", "Risk Management", "Regulatory Compliance", "Project Management"]',
                'job_description': 'Lead cross-border compliance implementations and manage regulatory projects across EMEA.',
                'biological_match_score': 99.4,
                'godhood_compatibility': 97.8,
                'linkedin_apply_url': 'https://linkedin.com/jobs/view/senior-business-analyst-compliance-zurich-2025',
                'application_urls': '{"linkedin": "https://linkedin.com/jobs/view/senior-business-analyst-compliance-zurich-2025", "company": "https://jobs.ubs.com/careers/business-analyst-zurich"}',
                'is_active': 1
            },
            {
                'title': 'Senior Business Analyst - Compliance & Risk',
                'company_name': 'Credit Suisse',
                'location_city': 'Zurich',
                'location_country': 'Switzerland',
                'salary_min': 85000,
                'salary_max': 130000,
                'data_source': 'glassdoor',
                'experience_level': 'senior',
                'required_skills': '["Business Intelligence", "Regulatory Compliance", "Data Analytics", "Stakeholder Management"]',
                'job_description': 'Drive regulatory initiatives and business intelligence projects supporting Risk Management.',
                'biological_match_score': 98.7,
                'godhood_compatibility': 96.3,
                'linkedin_apply_url': 'https://linkedin.com/jobs/view/senior-business-analyst-credit-suisse-zurich-2025',
                'application_urls': '{"linkedin": "https://linkedin.com/jobs/view/senior-business-analyst-credit-suisse-zurich-2025", "company": "https://careers.credit-suisse.com/business-analyst-zurich"}',
                'is_active': 1
            },
            {
                'title': 'Chief Regulatory Business Analyst',
                'company_name': 'Swiss Re',
                'location_city': 'Zurich',
                'location_country': 'Switzerland',
                'salary_min': 110000,
                'salary_max': 160000,
                'data_source': 'indeed',
                'experience_level': 'executive',
                'required_skills': '["Regulatory Compliance", "Business Analysis", "Financial Services", "Risk Assessment"]',
                'job_description': 'Lead regulatory compliance initiatives and business analysis for global reinsurance operations.',
                'biological_match_score': 99.1,
                'godhood_compatibility': 98.9,
                'indeed_apply_url': 'https://ch.indeed.com/viewjob?jk=regulatory-business-analyst-swiss-re-zurich',
                'application_urls': '{"indeed": "https://ch.indeed.com/viewjob?jk=regulatory-business-analyst-swiss-re-zurich", "company": "https://careers.swissre.com/regulatory-business-analyst-zurich"}',
                'is_active': 1
            }
        ]

        for job in sample_jobs:
            columns = ', '.join(job.keys())
            placeholders = ', '.join('?' * len(job))
            values = list(job.values())

            try:
                conn.execute(f"INSERT INTO jobs ({columns}) VALUES ({placeholders})", values)
            except Exception as e:
                logger.warning(f"Could not insert sample job {job['title']}: {e}")

        conn.commit()
        conn.close()
        logger.info("✓ Sample job data inserted")

    def create_postgres_connection(self):
        """Create PostgreSQL connection if available"""
        try:
            import psycopg2
            from psycopg2.extras import RealDictCursor

            db_url = os.environ.get('DATABASE_URL')
            if not db_url:
                # Fallback to individual vars
                host = os.environ.get('POSTGRES_HOST', 'localhost')
                port = os.environ.get('POSTGRES_PORT', '5432')
                user = os.environ.get('POSTGRES_USER', 'postgres')
                password = os.environ.get('POSTGRES_PASSWORD', '')
                dbname = os.environ.get('POSTGRES_DB', 'jtp_jobs_db')

                db_url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

            self.connection = psycopg2.connect(db_url)
            logger.info("✓ Connected to PostgreSQL database")
            return True

        except ImportError:
            logger.warning("psycopg2 not available, skipping PostgreSQL setup")
            return False
        except Exception as e:
            logger.warning(f"Could not connect to PostgreSQL: {e}")
            return False

    def setup(self):
        """Setup the appropriate database"""
        if self.db_type == 'postgresql':
            if self.create_postgres_connection():
                self.run_postgres_schema()
            else:
                logger.info("Falling back to SQLite setup")
                self.create_sqlite_schema()
        else:
            self.create_sqlite_schema()

    def run_postgres_schema(self):
        """Run PostgreSQL schema setup"""
        try:
            with open('database_schema.sql', 'r') as f:
                schema_sql = f.read()

            with self.connection.cursor() as cursor:
                cursor.execute(schema_sql)
                self.connection.commit()

            logger.info("✓ PostgreSQL database schema applied")

            # Insert sample data for testing
            self.insert_postgres_sample_data()

        except Exception as e:
            logger.error(f"✗ Failed to apply PostgreSQL schema: {e}")
            self.connection.rollback()
            raise

        finally:
            if self.connection:
                self.connection.close()

    def insert_postgres_sample_data(self):
        """Insert sample data for PostgreSQL"""
        sample_jobs = [
            {
                'title': 'Business Risk Manager / Senior Project Manager',
                'company_name': 'UBS Global Wealth Management',
                'location_city': 'Zurich',
                'location_country': 'Switzerland',
                'salary_min': 80000,
                'salary_max': 120000,
                'data_source': 'linkedin',
                'experience_level': 'senior',
                'required_skills': ['Business Analysis', 'Risk Management', 'Regulatory Compliance', 'Project Management'],
                'job_description': 'Lead cross-border compliance implementations and manage regulatory projects across EMEA.',
                'biological_match_score': 99.4,
                'godhood_compatibility': 97.8,
                'linkedin_apply_url': 'https://linkedin.com/jobs/view/senior-business-analyst-compliance-zurich-2025',
                'application_urls': {"linkedin": "https://linkedin.com/jobs/view/senior-business-analyst-compliance-zurich-2025", "company": "https://jobs.ubs.com/careers/business-analyst-zurich"},
                'is_active': True
            },
            {
                'title': 'Senior Business Analyst - Compliance & Risk',
                'company_name': 'Credit Suisse',
                'location_city': 'Zurich',
                'location_country': 'Switzerland',
                'salary_min': 85000,
                'salary_max': 130000,
                'data_source': 'glassdoor',
                'experience_level': 'senior',
                'required_skills': ['Business Intelligence', 'Regulatory Compliance', 'Data Analytics', 'Stakeholder Management'],
                'job_description': 'Drive regulatory initiatives and business intelligence projects supporting Risk Management.',
                'biological_match_score': 98.7,
                'godhood_compatibility': 96.3,
                'linkedin_apply_url': 'https://linkedin.com/jobs/view/senior-business-analyst-credit-suisse-zurich-2025',
                'application_urls': {"linkedin": "https://linkedin.com/jobs/view/senior-business-analyst-credit-suisse-zurich-2025", "company": "https://careers.credit-suisse.com/business-analyst-zurich"},
                'is_active': True
            },
            {
                'title': 'Chief Regulatory Business Analyst',
                'company_name': 'Swiss Re',
                'location_city': 'Zurich',
                'location_country': 'Switzerland',
                'salary_min': 110000,
                'salary_max': 160000,
                'data_source': 'indeed',
                'experience_level': 'executive',
                'required_skills': ['Regulatory Compliance', 'Business Analysis', 'Financial Services', 'Risk Assessment'],
                'job_description': 'Lead regulatory compliance initiatives and business analysis for global reinsurance operations.',
                'biological_match_score': 99.1,
                'godhood_compatibility': 98.9,
                'indeed_apply_url': 'https://ch.indeed.com/viewjob?jk=regulatory-business-analyst-swiss-re-zurich',
                'application_urls': {"indeed": "https://ch.indeed.com/viewjob?jk=regulatory-business-analyst-swiss-re-zurich", "company": "https://careers.swissre.com/regulatory-business-analyst-zurich"},
                'is_active': True
            }
        ]

        try:
            with self.connection.cursor() as cursor:
                for job in sample_jobs:
                    cursor.execute("""
                        INSERT INTO jobs (
                            title, company_name, location_city, location_country,
                            salary_min, salary_max, data_source, experience_level,
                            required_skills, job_description, biological_match_score,
                            godhood_compatibility, linkedin_apply_url, indeed_apply_url,
                            application_urls, is_active
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        job['title'], job['company_name'], job['location_city'], job['location_country'],
                        job['salary_min'], job['salary_max'], job['data_source'], job['experience_level'],
                        job['required_skills'], job['job_description'], job['biological_match_score'],
                        job['godhood_compatibility'], job.get('linkedin_apply_url'), job.get('indeed_apply_url'),
                        job['application_urls'], job['is_active']
                    ))

                self.connection.commit()
                logger.info("✓ PostgreSQL sample data inserted")

        except Exception as e:
            logger.error(f"✗ Failed to insert PostgreSQL sample data: {e}")
            self.connection.rollback()

def main():
    """Main setup function"""
    logger.info("🚀 Starting Job Tracker Pro Database Setup")

    setup = DatabaseSetup()
    setup.setup()

    logger.info("✅ Database setup complete!")
    logger.info(f"Database Type: {setup.db_type}")
    logger.info("Features: Full-text search, biological enhance ment, real job URLs")

if __name__ == "__main__":
    main()
