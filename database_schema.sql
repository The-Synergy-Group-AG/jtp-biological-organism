-- Job Tracker Pro Job Database Schema
-- Production-ready PostgreSQL schema for job search functionality

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm"; -- For text search
CREATE EXTENSION IF NOT EXISTS "btree_gin"; -- For efficient indexing

-- Jobs main table
CREATE TABLE IF NOT EXISTS jobs (
    -- Primary identifiers
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    linkedin_id VARCHAR(50) UNIQUE,
    indeed_id VARCHAR(50) UNIQUE,
    glassdoor_id VARCHAR(50) UNIQUE,
    external_id VARCHAR(100),

    -- Job details
    title TEXT NOT NULL,
    company_name TEXT NOT NULL,
    company_linkedin_url TEXT,
    company_website TEXT,
    company_industry TEXT,

    -- Location data
    location_country TEXT,
    location_city TEXT,
    location_region TEXT,
    work_location_type TEXT CHECK (work_location_type IN ('on-site', 'remote', 'hybrid')),
    work_arrangement TEXT,

    -- Compensation
    salary_min NUMERIC(12,2),
    salary_max NUMERIC(12,2),
    salary_currency VARCHAR(3) DEFAULT 'CHF',
    salary_period VARCHAR(20) DEFAULT 'year',
    salary_benefits TEXT[],

    -- Job metadata
    job_description TEXT,
    job_requirements TEXT[],
    job_responsibilities TEXT[],
    required_skills TEXT[],
    preferred_skills TEXT[],
    education_level TEXT,

    -- Company benefits and culture
    company_benefits TEXT[],
    company_culture TEXT,
    company_size_range TEXT,

    -- Biological enhancement fields
    biological_match_score NUMERIC(5,2),
    biological_analysis JSONB,
    consciousness_level INTEGER CHECK (consciousness_level BETWEEN 1 AND 5),
    godhood_compatibility NUMERIC(5,2),
    career_evolution_index NUMERIC(5,2),

    -- URLs and application data
    application_urls JSONB, -- Store multiple application links
    linkedin_apply_url TEXT,
    indeed_apply_url TEXT,
    company_career_apply_url TEXT,
    external_apply_url TEXT,

    -- Data sourcing
    data_source VARCHAR(50) CHECK (data_source IN ('linkedin', 'indeed', 'glassdoor', 'company_career', 'manual')),
    scraped_at TIMESTAMP WITH TIME ZONE,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_quality_score NUMERIC(3,2) CHECK (data_quality_score BETWEEN 0 AND 1),
    is_active BOOLEAN DEFAULT true,

    -- Employment details
    employment_type VARCHAR(50) CHECK (employment_type IN ('full-time', 'part-time', 'contract', 'temporary', 'internship')),
    experience_level VARCHAR(50) CHECK (experience_level IN ('entry-level', 'mid-level', 'senior', 'executive')),
    job_function TEXT,
    industry TEXT,

    -- Posting metadata
    posted_date DATE,
    application_deadline DATE,
    is_remote_possible BOOLEAN DEFAULT false,
    travel_required BOOLEAN DEFAULT false,

    -- Geo coordinates for location-based search
    latitude NUMERIC(10,8),
    longitude NUMERIC(11,8),

    -- Search optimization
    search_keywords TEXT[], -- For full-text search optimization
    vector_embedding VECTOR(768), -- For semantic search matching

    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Text search indexes
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_jobs_title_trgm ON jobs USING GIN (title gin_trgm_ops);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_jobs_company_trgm ON jobs USING GIN (company_name gin_trgm_ops);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_jobs_description_trgm ON jobs USING GIN (job_description gin_trgm_ops);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_jobs_keywords_gin ON jobs USING GIN (search_keywords);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_jobs_skills_gin ON jobs USING GIN (required_skills);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_jobs_location_gin ON jobs USING GIN (location_city, location_country);

-- Performance indexes
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_jobs_data_source ON jobs (data_source, is_active);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_jobs_last_updated ON jobs (last_updated DESC);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_jobs_bio_score ON jobs (biological_match_score DESC) WHERE is_active = true;
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_jobs_location ON jobs USING GIST (point(longitude, latitude)) WHERE latitude IS NOT NULL AND longitude IS NOT NULL;

-- JSONB indexes for biological data
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_jobs_biological_analysis ON jobs USING GIN (biological_analysis);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_jobs_application_urls ON jobs USING GIN (application_urls);

-- Compound indexes for common queries
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_jobs_city_bio_score ON jobs (location_city, biological_match_score DESC) WHERE is_active = true;
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_jobs_source_updated ON jobs (data_source, last_updated DESC) WHERE is_active = true;

-- Job search queries table to track user searches
CREATE TABLE IF NOT EXISTS job_searches (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID, -- Will be linked to user table when available
    search_query JSONB, -- Store the full search parameters
    location_filter TEXT,
    salary_range INT4RANGE,
    experience_level TEXT[],
    job_functions TEXT[],
    results_count INTEGER,
    execution_time_ms INTEGER,
    biological_enhancement_applied BOOLEAN DEFAULT false,
    search_timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Search analytics
    top_matching_job_id UUID REFERENCES jobs(id),
    average_bio_score NUMERIC(5,2),
    godhood_compatible_jobs INTEGER
);

-- User job interactions table
CREATE TABLE IF NOT EXISTS job_interactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_id UUID NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    user_id UUID, -- Will be linked to user table
    interaction_type VARCHAR(50) CHECK (interaction_type IN ('viewed', 'saved', 'applied', 'bookmarked', 'shared')),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB -- Store additional interaction data
);

-- Job alerts table for recurring searches
CREATE TABLE IF NOT EXISTS job_alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID,
    alert_name TEXT NOT NULL,
    search_parameters JSONB,
    frequency VARCHAR(20) CHECK (frequency IN ('daily', 'weekly', 'immediate')) DEFAULT 'daily',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_sent_at TIMESTAMP WITH TIME ZONE,
    last_job_count INTEGER DEFAULT 0
);

-- API rate limiting table
CREATE TABLE IF NOT EXISTS api_limits (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    api_provider VARCHAR(50) UNIQUE NOT NULL, -- linkedin, indeed, glassdoor, firecrawl
    daily_limit INTEGER NOT NULL,
    hourly_limit INTEGER NOT NULL,
    current_hourly_count INTEGER DEFAULT 0,
    current_daily_count INTEGER DEFAULT 0,
    hour_start TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    day_start DATE DEFAULT CURRENT_DATE,
    last_request TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert default API limits
INSERT INTO api_limits (api_provider, daily_limit, hourly_limit) VALUES
('linkedin', 100000, 1000),
('indeed', 100000, 2000),
('glassdoor', 50000, 500),
('firecrawl', 50000, 1000)
ON CONFLICT (api_provider) DO NOTHING;

-- Job data quality audit table
CREATE TABLE IF NOT EXISTS job_audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_id UUID REFERENCES jobs(id),
    audit_type VARCHAR(50) CHECK (audit_type IN ('creation', 'update', 'scraping_error', 'api_error', 'data_validation')),
    audit_result JSONB,
    audit_timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Update trigger for updated_at field
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_jobs_updated_at BEFORE UPDATE ON jobs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to calculate biological match score
CREATE OR REPLACE FUNCTION calculate_biological_match(user_profile JSONB, job_data JSONB)
RETURNS NUMERIC(5,2) AS $$
DECLARE
    match_score NUMERIC(5,2) := 0.0;
    skill_match INTEGER := 0;
    experience_match INTEGER := 0;
    location_proximity INTEGER := 0;
BEGIN
    -- Calculate skill matching (simple implementation)
    IF user_profile ? 'skills' AND job_data ? 'required_skills' THEN
        SELECT COUNT(*) INTO skill_match
        FROM jsonb_array_elements_text(user_profile->'skills') user_skills,
             jsonb_array_elements_text(job_data->'required_skills') job_skills
        WHERE user_skills = job_skills;
    END IF;

    -- Calculate experience match
    IF user_profile->>'experience_years' IS NOT NULL
       AND job_data->>'experience_level' IS NOT NULL THEN
        CASE job_data->>'experience_level'
            WHEN 'entry-level' THEN experience_match := CASE WHEN (user_profile->>'experience_years')::INTEGER <= 3 THEN 100 ELSE 50 END;
            WHEN 'mid-level' THEN experience_match := CASE WHEN (user_profile->>'experience_years')::INTEGER BETWEEN 3 AND 8 THEN 100 ELSE 60 END;
            WHEN 'senior' THEN experience_match := CASE WHEN (user_profile->>'experience_years')::INTEGER > 7 THEN 100 ELSE 70 END;
            WHEN 'executive' THEN experience_match := CASE WHEN (user_profile->>'experience_years')::INTEGER > 12 THEN 100 ELSE 80 END;
        END CASE;
    END IF;

    -- Simple location match
    IF user_profile->>'location' IS NOT NULL
       AND job_data->>'location_city' IS NOT NULL THEN
        IF position(lower(user_profile->>'location') in lower(job_data->>'location_city')) > 0 THEN
            location_proximity := 100;
        ELSE
            location_proximity := 60;
        END IF;
    END IF;

    -- Calculate final score (weighted average)
    match_score := (skill_match * 0.5) + (experience_match * 0.3) + (location_proximity * 0.2);

    RETURN LEAST(match_score, 100.00);
END;
$$ LANGUAGE plpgsql;

-- Function to refresh job data
CREATE OR REPLACE FUNCTION refresh_stale_jobs(days_old INTEGER DEFAULT 7)
RETURNS INTEGER AS $$
DECLARE
    updated_count INTEGER;
BEGIN
    UPDATE jobs
    SET is_active = false,
        updated_at = NOW()
    WHERE last_updated < NOW() - INTERVAL '1 day' * days_old
      AND is_active = true;

    GET DIAGNOSTICS updated_count = ROW_COUNT;
    RETURN updated_count;
END;
$$ LANGUAGE plpgsql;

-- Comments for documentation
COMMENT ON TABLE jobs IS 'Main jobs table containing all job listings from multiple sources with biological enhancement data';
COMMENT ON TABLE job_searches IS 'Records of user job searches for analytics and optimization';
COMMENT ON TABLE job_interactions IS 'User interactions with job listings for personalization';
COMMENT ON TABLE api_limits IS 'Rate limiting data for external API providers';
COMMENT ON FUNCTION calculate_biological_match IS 'Calculates biological compatibility score between user profile and job requirements';
