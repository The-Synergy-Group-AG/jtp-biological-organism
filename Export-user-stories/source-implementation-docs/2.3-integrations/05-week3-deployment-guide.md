# Week 3 MCP Advanced Deployment Guide

## Overview
This guide covers the deployment of Week 3 MCP Advanced components: Cloudinary (media processing), RAV Compliance, Swiss Job Board integration, and Canton-Specific services, building on Week 1 Foundation and Week 2 Enhancement.

## Architecture

```
Full MCP Stack (Week 1 + 2 + 3)
├── Week 1 Foundation (6 threads)
│   ├── Chroma MCP (2 threads)
│   ├── Memory MCP (2 threads)
│   └── Sequential Thinking MCP (2 threads)
├── Week 2 Enhancement (2 threads)
│   ├── Filesystem MCP (1 thread)
│   └── Brave Search MCP (1 thread)
└── Week 3 Advanced (4 threads)
    ├── Cloudinary MCP (1 thread)
    │   ├── Photo optimization
    │   ├── Document processing
    │   └── Portfolio management
    ├── RAV Compliance MCP (1 thread)
    │   ├── Application tracking
    │   ├── Monthly reporting
    │   └── Canton requirements
    ├── Swiss Job Board MCP (1 thread)
    │   ├── Multi-board aggregation
    │   ├── Salary benchmarking
    │   └── Application tracking
    └── Canton-Specific MCP (1 thread)
        ├── Canton profiles
        ├── Commute analysis
        └── Regional compliance
```

## Prerequisites

### System Requirements
- **RAM**: 16GB total
  - Week 1: 12GB allocated
  - Week 2: 2GB allocated  
  - Week 3: 2GB allocated
- **Storage**: 200GB+ for media and documents
- **Network**: Stable internet for APIs

### Additional Dependencies
```bash
# Week 3 specific packages
pip install pillow==10.1.0  # Image processing
pip install numpy==1.24.3   # Image analysis
pip install beautifulsoup4==4.12.2  # Web scraping
pip install aiohttp==3.9.1  # Async HTTP

# System dependencies
sudo apt-get install libmagic1  # File type detection
sudo apt-get install imagemagick  # Image processing
```

## Installation Steps

### 1. Extend Directory Structure
```bash
# Create Week 3 directories
mkdir -p ./mcp_data/media/{photos,documents,portfolios}
mkdir -p ./mcp_data/rav/{applications,reports,compliance}
mkdir -p ./mcp_data/job_boards/{cache,applications}
mkdir -p ./mcp_data/cantons/{profiles,statistics}

# Set permissions
chmod -R 700 ./mcp_data/media
chmod -R 700 ./mcp_data/rav
chmod 755 ./mcp_data/job_boards/cache
```

### 2. Update Environment Configuration
```bash
# Append to existing .env file
cat >> .env << EOF

# Week 3 Configuration
# Cloudinary (Media Processing)
CLOUDINARY_CLOUD_NAME=mock_cloud
CLOUDINARY_API_KEY=  # Optional for production
CLOUDINARY_API_SECRET=  # Optional for production
CLOUDINARY_MOCK_MODE=true

# RAV Compliance
RAV_MIN_APPLICATIONS_DEFAULT=10
RAV_COMPLIANCE_STRICT=true
RAV_REPORT_AUTO_SUBMIT=false

# Swiss Job Boards
JOB_BOARD_CACHE_HOURS=6
JOB_BOARD_PARALLEL_SEARCHES=3
JOB_BOARD_MOCK_MODE=true

# Canton Configuration
DEFAULT_CANTON=ZH
LANGUAGE_REQUIREMENTS_STRICT=true
COMMUTE_MAX_HOURS=2

# Swiss Compliance
SWISS_CV_PHOTO_REQUIRED=true
SWISS_PRIVACY_MODE=strict
DATA_RESIDENCY=CH
EOF
```

### 3. Initialize Week 3 MCP Servers

#### Complete Stack Initialization
```python
from week3_integration import FullStackMCPOrchestrator

# Initialize full stack (Week 1 + 2 + 3)
orchestrator = FullStackMCPOrchestrator()
await orchestrator.initialize()

print("Full MCP stack initialized with Swiss-specific features")
```

#### Individual Server Testing
```python
# Test Cloudinary
from cloudinary_mcp_integration import CloudinaryMCPServer
cloudinary = CloudinaryMCPServer(mock_mode=True)

# Optimize profile photo
optimization = await cloudinary.optimize_profile_photo(
    photo_bytes, "user_123"
)
print(f"Photo optimization score: {optimization.optimized_score}")

# Test RAV Compliance
from rav_compliance_mcp_integration import RAVComplianceMCPServer
rav = RAVComplianceMCPServer()

# Check compliance
status = await rav.check_compliance_status("user_123")
print(f"RAV compliance: {status['current_status']}")

# Test Job Boards
from swiss_job_board_mcp_integration import SwissJobBoardMCPServer
job_boards = SwissJobBoardMCPServer()

# Search jobs
jobs = await job_boards.search_jobs(
    "Python Developer", 
    canton="ZH"
)
print(f"Found {len(jobs)} jobs across Swiss boards")

# Test Canton Services
from canton_specific_mcp_integration import CantonSpecificMCPServer
cantons = CantonSpecificMCPServer()

# Get recommendations
recs = await cantons.get_canton_recommendations({
    "languages": ["English", "German"],
    "target_industry": "Technology"
})
print(f"Top canton: {recs[0]['canton_name']}")
```

## Configuration Options

### Cloudinary Configuration
```yaml
cloudinary:
  optimization:
    profile_photos:
      target_size: [400, 400]
      quality: 85
      format: "jpg"
      face_detection: true
      background_removal: false
    documents:
      ocr_enabled: true
      languages: ["en", "de", "fr", "it"]
      max_size_mb: 10
  compliance:
    swiss_privacy: true
    metadata_stripping: true
    encryption_at_rest: true
    retention_days: 730
```

### RAV Compliance Configuration
```yaml
rav_compliance:
  cantons:
    ZH:
      min_applications: 10
      proof_required: ["email", "screenshot"]
      language_courses: ["German A2-C1"]
    GE:
      min_applications: 8
      proof_required: ["email", "cover_letter"]
      language_courses: ["French A1-B2"]
  reporting:
    auto_generate_day: 28  # Day of month
    pdf_format: "RAV_standard"
    include_proof: true
```

### Job Board Configuration
```yaml
job_boards:
  enabled_boards:
    - jobs.ch
    - jobscout24.ch
    - indeed.ch
    - jobup.ch
    - michaelpage.ch
  search_settings:
    parallel_searches: 3
    cache_duration_hours: 6
    deduplication: true
  salary_benchmarking:
    min_samples: 3
    outlier_removal: true
    include_benefits: true
```

### Canton Configuration
```yaml
cantons:
  profiles:
    update_frequency: "monthly"
    data_sources: ["official", "statistical"]
  recommendations:
    weight_factors:
      language_match: 0.2
      industry_match: 0.3
      salary_match: 0.2
      quality_of_life: 0.15
      commute_time: 0.15
```

## Usage Examples

### 1. Complete Swiss Job Application
```python
# Prepare application
job_data = {
    "id": "job_123",
    "title": "Senior Python Developer",
    "company": "Swiss Bank AG",
    "canton": "ZH",
    "languages": ["English", "German preferred"],
    "salary_min": 120000
}

user_profile = {
    "user_id": "user_456",
    "canton": "ZH",
    "languages": ["English", "German B2"],
    "work_permit": "Permit B",
    "skills": ["Python", "Django", "Docker"]
}

documents = {
    "resume": resume_bytes,
    "cover_letter": cover_letter_bytes
}

photos = {
    "profile_photo": photo_bytes
}

# Process complete application
result = await orchestrator.process_swiss_job_application(
    "https://jobs.ch/12345",
    user_profile,
    documents,
    photos
)

print(f"Application submitted - RAV compliant: {result['compliance']['rav_registered']}")
print(f"Photo optimized: {result['steps']['photo_optimization']['professional_score']}")
```

### 2. Smart Job Search with Canton Analysis
```python
# Search with Swiss context
search_result = await orchestrator.smart_job_search(
    "Machine Learning Engineer Zurich remote",
    user_profile
)

print(f"Found {len(search_result['jobs'])} matching jobs")
print(f"Canton insights: {search_result['canton_insights']}")
print(f"RAV tips: {search_result['rav_tips']}")

# Get canton recommendations
canton_recs = await week3.canton_server.get_canton_recommendations(user_profile)

for rec in canton_recs[:3]:
    print(f"{rec['canton_name']}: {rec['match_score']}/100")
    print(f"  Reasons: {', '.join(rec['reasons'])}")
```

### 3. RAV Compliance Management
```python
# Register application
await week3.rav_server.register_application({
    "user_id": "user_456",
    "job_title": "Data Scientist",
    "company_name": "Pharma Co",
    "application_method": "online",
    "documents": ["cv", "cover_letter", "certificates"]
})

# Check monthly status
compliance_status = await week3.rav_server.check_compliance_status("user_456")
print(f"Applications: {compliance_status['submitted_applications']}/{compliance_status['required_applications']}")

# Generate monthly report
report = await week3.generate_rav_monthly_report("user_456")
print(f"Report ID: {report['report_id']}")
print(f"Compliance: {report['compliance_status']}")

# Submit to RAV
submission = await week3.rav_server.submit_report_to_rav(report['report_id'])
print(f"Submission status: {submission['status']}")
```

## Performance Optimization

### Thread Distribution (12 threads total)
```python
# Optimal distribution for 6×2GB configuration
thread_config = {
    # Week 1 (6 threads)
    "chroma": 2,
    "memory": 2,
    "thinking": 2,
    # Week 2 (2 threads)
    "filesystem": 1,
    "search": 1,
    # Week 3 (4 threads)
    "cloudinary": 1,
    "rav": 1,
    "job_boards": 1,
    "cantons": 1
}

# Monitor usage
import psutil
process = psutil.Process()
print(f"Threads: {process.num_threads()}")
print(f"Memory: {process.memory_info().rss / 1024 / 1024:.0f} MB")
```

### Caching Strategy
```python
# Configure multi-level caching
cache_config = {
    "job_searches": {
        "duration_hours": 6,
        "max_entries": 1000
    },
    "canton_profiles": {
        "duration_hours": 168,  # 1 week
        "max_entries": 26  # All cantons
    },
    "media_optimizations": {
        "duration_hours": 720,  # 30 days
        "max_size_mb": 500
    }
}

# Pre-warm caches
await week3._warmup_caches()
```

## Monitoring & Maintenance

### Swiss Compliance Dashboard
```python
async def monitor_swiss_compliance():
    report = await orchestrator.generate_complete_system_report()
    
    # Swiss-specific metrics
    swiss_score = report['swiss_compliance_score']
    rav_compliance = report['week3_advanced']['rav_compliance']
    
    print(f"📊 Swiss Compliance Dashboard")
    print(f"Overall Score: {swiss_score:.1f}%")
    print(f"RAV Applications: {rav_compliance['validated_applications']}/{rav_compliance['total_applications']}")
    print(f"Compliance Warnings: {rav_compliance['compliance_warnings']}")
    
    # Canton distribution
    canton_queries = report['week3_advanced']['cantons']['queries']
    print(f"\nCanton Activity:")
    for canton, count in canton_queries.items():
        print(f"  {canton}: {count} queries")
    
    # Job board efficiency
    boards = report['week3_advanced']['job_boards']
    cache_rate = boards['cache_hits'] / max(boards['total_searches'], 1)
    print(f"\nJob Board Performance:")
    print(f"  Cache Hit Rate: {cache_rate:.1%}")
    print(f"  Jobs Found: {boards['jobs_found']}")
    
    return swiss_score > 70  # Healthy threshold
```

### Backup Strategy
```bash
#!/bin/bash
# Backup Week 3 data

BACKUP_DIR="./backups/week3_$(date +%Y%m%d)"
mkdir -p $BACKUP_DIR

# Backup media assets
tar -czf $BACKUP_DIR/media.tar.gz ./mcp_data/media

# Backup RAV data (critical for compliance)
tar -czf $BACKUP_DIR/rav.tar.gz ./mcp_data/rav

# Backup job board cache
tar -czf $BACKUP_DIR/job_boards.tar.gz ./mcp_data/job_boards

# Backup canton data
tar -czf $BACKUP_DIR/cantons.tar.gz ./mcp_data/cantons

echo "Week 3 backup completed: $BACKUP_DIR"
```

## Troubleshooting

### Common Issues

1. **RAV Compliance Warnings**
```python
# Check application quality
apps = await rav_server.get_user_applications(user_id)
for app in apps:
    if not app.rav_validated:
        print(f"Invalid: {app.job_title}")
        print(f"Issues: {app.metadata.get('validation', {}).get('issues')}")
```

2. **Photo Optimization Failures**
```python
# Verify image format
from PIL import Image
import io

try:
    img = Image.open(io.BytesIO(photo_bytes))
    print(f"Format: {img.format}, Size: {img.size}")
    if img.format not in ['JPEG', 'PNG']:
        # Convert to JPEG
        buffer = io.BytesIO()
        img.convert('RGB').save(buffer, format='JPEG')
        photo_bytes = buffer.getvalue()
except Exception as e:
    print(f"Invalid image: {e}")
```

3. **Canton Mismatch**
```python
# Check language requirements
compliance = await canton_server.check_canton_compliance(
    job_canton, user_profile
)
if not compliance['compliant']:
    print("Issues found:")
    for issue in compliance['issues']:
        print(f"  - {issue}")
    print("\nRecommendations:")
    for rec in compliance['recommendations']:
        print(f"  - {rec}")
```

## Security Best Practices

### Media Privacy
```python
# Always strip metadata from photos
cloudinary_server.compliance_settings['metadata_stripping'] = True

# Encrypt sensitive documents
cloudinary_server.compliance_settings['encryption_required'] = [
    'passport', 'permit', 'certificate'
]
```

### RAV Data Protection
```python
# Anonymize reports for analysis
def anonymize_rav_data(report):
    report_copy = report.copy()
    report_copy['user_id'] = hashlib.sha256(
        report['user_id'].encode()
    ).hexdigest()[:8]
    return report_copy
```

### API Key Management
```python
# Use environment variables
import os
api_keys = {
    'cloudinary': os.getenv('CLOUDINARY_API_KEY'),
    'job_boards': os.getenv('JOB_BOARD_API_KEY')
}

# Rotate keys periodically
if datetime.now().day == 1:  # First of month
    print("⚠️ Remember to rotate API keys")
```

## Integration with Main Application

### Module Registration
```python
# In main application
from week3_integration import FullStackMCPOrchestrator

# Initialize orchestrator
orchestrator = FullStackMCPOrchestrator()
await orchestrator.initialize()

# Register conversation handlers
router.register_module("media", orchestrator.week3_advanced.cloudinary_agent)
router.register_module("rav", orchestrator.week3_advanced.rav_agent)
router.register_module("jobs", orchestrator.week3_advanced.job_board_agent)
router.register_module("cantons", orchestrator.week3_advanced.canton_agent)

# Register routes
router.route_map.update({
    "optimize photo": ["media"],
    "rav compliance": ["rav"],
    "search jobs": ["jobs", "cantons"],
    "which canton": ["cantons"],
    "complete application": ["media", "rav", "jobs", "filesystem", "memory"]
})
```

## Next Steps

1. **Week 4 Optimization**: Performance tuning and final Swiss compliance validation
2. **Production Deployment**: Remove mock modes, add real API integrations
3. **Monitoring Setup**: Implement comprehensive Swiss compliance monitoring
4. **User Training**: Create guides for Swiss job market features

---
*Last Updated: 2025-01-05*
*Version: 1.0.0*