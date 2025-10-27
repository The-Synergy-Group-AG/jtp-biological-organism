# Week 2 MCP Enhancement Deployment Guide

## Overview
This guide covers the deployment of Week 2 MCP Enhancement components: Filesystem (secure document management) and Brave Search (market intelligence) integrated with Week 1 Foundation for JobTrackerPro.

## Architecture

```
Week 2 MCP Enhancement (Building on Week 1)
├── Week 1 Foundation (Existing)
│   ├── Chroma MCP (2 threads)
│   ├── Memory MCP (2 threads)
│   └── Sequential Thinking MCP (2 threads)
└── Week 2 Enhancement (New)
    ├── Filesystem MCP Server (1 thread)
    │   ├── Encrypted document storage
    │   ├── Swiss compliance features
    │   └── GDPR export capabilities
    └── Brave Search MCP Server (1 thread)
        ├── Job market search
        ├── Company research
        └── Swiss regulation lookup
```

## Prerequisites

### System Requirements
- **RAM**: 16GB (Week 1: 12GB + Week 2: 2GB + Reserved: 2GB)
- **Storage**: 100GB+ for documents and search cache
- **Network**: Stable internet for search operations

### Additional Dependencies
```bash
# Week 2 specific packages
pip install aiofiles==23.2.1
pip install python-magic==0.4.27
pip install beautifulsoup4==4.12.2
pip install cryptography==41.0.7

# System dependencies (Linux/macOS)
sudo apt-get install libmagic1  # For file type detection
```

## Installation Steps

### 1. Extend Directory Structure
```bash
# Create Week 2 directories
mkdir -p ./mcp_data/files/documents/{resumes,cover_letters,certificates,portfolios}
mkdir -p ./mcp_data/files/compliance/{rav,permits}
mkdir -p ./mcp_data/files/{temp,archive,.registry}
mkdir -p ./mcp_data/search_cache

# Set secure permissions
chmod -R 700 ./mcp_data/files
chmod 755 ./mcp_data/search_cache
```

### 2. Update Environment Configuration
```bash
# Append to existing .env file
cat >> .env << EOF

# Week 2 Configuration
FILESYSTEM_BASE_PATH=./mcp_data/files
FILESYSTEM_MAX_SIZE_MB=50
FILESYSTEM_ENCRYPTION=true

BRAVE_SEARCH_CACHE_HOURS=24
BRAVE_SEARCH_MAX_CONCURRENT=3
BRAVE_SEARCH_API_KEY=  # Optional, uses mock mode if empty

# Swiss Compliance
GDPR_EXPORT_ENABLED=true
DATA_RETENTION_DAYS=730
AUDIT_TRAIL_ENABLED=true
EOF
```

### 3. Initialize Week 2 MCP Servers

#### Filesystem MCP Server
```python
from filesystem_mcp_integration import FilesystemMCPServer
from cryptography.fernet import Fernet

# Generate encryption key
encryption_key = Fernet.generate_key().decode()

# Initialize filesystem server
filesystem_server = FilesystemMCPServer(
    base_path="./mcp_data/files",
    max_file_size_mb=50,
    encryption_key=encryption_key
)

# Verify setup
compliance = await filesystem_server.verify_compliance()
print(f"Filesystem compliance: {all(compliance.values())}")
```

#### Brave Search MCP Server
```python
from brave_search_mcp_integration import BraveSearchMCPServer

# Initialize search server
search_server = BraveSearchMCPServer(
    api_key=None,  # Using mock mode for testing
    cache_duration_hours=24,
    max_concurrent_searches=3
)

# Test search
results = await search_server.search_jobs(
    "Python developer",
    location="Zurich"
)
print(f"Search test: Found {len(results)} results")
```

### 4. Integrate with Week 1 Foundation
```python
from week2_integration import Week2MCPEnhancement
from week1_integration import Week1MCPFoundation

# Load existing Week 1 foundation
week1_foundation = Week1MCPFoundation()

# Initialize Week 2 enhancement
week2_enhancement = Week2MCPEnhancement(week1_foundation)

# Verify integration
print("Week 2 Enhancement initialized with Week 1 Foundation")
```

## Configuration Options

### Filesystem Configuration
```yaml
filesystem:
  base_path: "./mcp_data/files"
  structure:
    documents:
      - resumes
      - cover_letters  
      - certificates
      - portfolios
    compliance:
      - rav
      - permits
  security:
    encryption: true
    max_file_size_mb: 50
    allowed_types:
      - application/pdf
      - application/msword
      - text/plain
      - image/jpeg
      - image/png
  compliance:
    gdpr_compliant: true
    data_retention_days: 730
    audit_trail: true
    swiss_residency: true
```

### Search Configuration
```yaml
brave_search:
  cache:
    duration_hours: 24
    max_size_mb: 100
  performance:
    max_concurrent: 3
    timeout_seconds: 30
  swiss_job_boards:
    - jobs.ch
    - jobscout24.ch
    - indeed.ch
    - linkedin.com
    - jobup.ch
  search_params:
    languages: ["German", "French", "Italian", "English"]
    cantons: ["Zurich", "Geneva", "Basel", "Bern"]
```

## Usage Examples

### 1. Complete Job Application Workflow
```python
# Prepare application
job_data = {
    "id": "job_123",
    "title": "Senior Python Developer",
    "company": "Swiss Tech AG",
    "location": "Zurich",
    "languages": ["English", "German"]
}

user_context = {
    "user_id": "user_456",
    "skills": ["Python", "Django", "Docker"],
    "languages": ["English", "German B2"]
}

documents = {
    "resume": resume_bytes,
    "cover_letter": cover_letter_bytes
}

# Process complete workflow
result = await week2_enhancement.process_application_workflow(
    job_data, user_context, documents
)

print(f"Application recommendation: {result['recommendations']['action']}")
print(f"Confidence: {result['recommendations']['overall_fit']:.0%}")
```

### 2. Smart Document Management
```python
# Store documents securely
secure_file = await filesystem_server.store_file(
    file_content=resume_bytes,
    filename="john_doe_resume_2024.pdf",
    owner_id="user_456",
    file_type="resume",
    metadata={
        "version": "2.0",
        "optimized_for": "tech_roles"
    },
    encrypt=True
)

# Search user documents
user_files = await filesystem_server.search_files(
    user_id="user_456",
    search_criteria={
        "file_type": "resume",
        "date_from": datetime.now() - timedelta(days=30)
    }
)

# Export for GDPR
export_data = await filesystem_server.export_user_data("user_456")
```

### 3. Market Intelligence
```python
# Search jobs with filters
jobs = await search_server.search_jobs(
    query="Machine Learning Engineer",
    location="Zurich",
    filters={
        "min_salary": 120000,
        "remote": True,
        "languages": ["English"]
    }
)

# Analyze market trends
insights = await search_server.analyze_job_market(
    role="Data Scientist",
    location="Switzerland"
)

for insight in insights:
    if insight.insight_type == "salary_trend":
        print(f"Average salary: CHF {insight.data['average_salary_chf']:,.0f}")

# Research companies
company_info = await search_server.research_company(
    "Google", "Zurich"
)
print(f"Company sentiment: {company_info.reviews.get('sentiment', 'unknown')}")
```

## Performance Optimization

### Thread Allocation (Week 1 + Week 2)
```python
# Total: 8 threads (6 from Week 1 + 2 from Week 2)
thread_distribution = {
    # Week 1 (6 threads)
    "chroma": 2,
    "memory": 2,
    "thinking": 2,
    # Week 2 (2 threads)
    "filesystem": 1,
    "search": 1
}

# Monitor resource usage
import psutil
process = psutil.Process()
print(f"Total threads: {process.num_threads()}")
print(f"Memory usage: {process.memory_info().rss / 1024 / 1024:.0f} MB")
```

### Caching Strategy
```python
# Configure search caching
search_server.cache_duration = timedelta(hours=24)

# Pre-warm cache with common searches
common_searches = [
    ("Python developer Switzerland", None),
    ("Data scientist Zurich", None),
    ("Remote software engineer", {"remote": True})
]

for query, filters in common_searches:
    await search_server.search_jobs(query, filters=filters)
```

### Batch Operations
```python
# Batch document processing
documents_to_store = [...]  # List of documents
batch_size = 10

results = []
for i in range(0, len(documents_to_store), batch_size):
    batch = documents_to_store[i:i+batch_size]
    batch_results = await asyncio.gather(*[
        filesystem_server.store_file(**doc)
        for doc in batch
    ])
    results.extend(batch_results)
```

## Monitoring & Maintenance

### Health Monitoring
```python
async def monitor_week2_health():
    # Get comprehensive system report
    report = await week2_enhancement.generate_system_report()
    
    # Check Week 2 specific metrics
    week2_metrics = report['week2_enhancement']
    
    # Filesystem health
    fs_health = week2_metrics['filesystem']
    print(f"Files stored: {fs_health['total_files']}")
    print(f"Encryption rate: {fs_health['encryption_operations'] / max(fs_health['total_operations'], 1):.0%}")
    
    # Search health
    search_health = week2_metrics['search']
    print(f"Search cache hit rate: {search_health['cache_hits'] / max(search_health['total_searches'], 1):.0%}")
    print(f"Avg search time: {search_health['avg_search_time_ms']:.0f}ms")
    
    # Compliance status
    compliance_ok = all(fs_health['compliance'].values())
    print(f"Swiss compliance: {'✅' if compliance_ok else '❌'}")
    
    return report['overall_health'] == 'operational'
```

### Backup Strategy
```bash
# Backup Week 2 data
tar -czf week2_backup_$(date +%Y%m%d).tar.gz \
    ./mcp_data/files \
    ./mcp_data/search_cache

# Restore Week 2 data
tar -xzf week2_backup_20250105.tar.gz
```

### Maintenance Tasks
```python
# Clean up old files
async def maintenance_cleanup():
    # Clean old files based on retention policy
    cleanup_result = await filesystem_server.cleanup_old_files()
    print(f"Archived {cleanup_result['archived']} old files")
    
    # Clear expired search cache
    expired_count = 0
    for key, (results, timestamp) in list(search_server.search_cache.items()):
        if datetime.now() - timestamp > search_server.cache_duration:
            del search_server.search_cache[key]
            expired_count += 1
    print(f"Cleared {expired_count} expired cache entries")
    
    # Optimize storage
    storage_info = await filesystem_server.get_user_storage_info("admin")
    if storage_info['quota_used_percent'] > 80:
        print("⚠️ Storage usage high - consider archiving")
```

## Troubleshooting

### Common Issues

1. **File Upload Failures**
   ```python
   # Check file size limit
   if len(file_content) > filesystem_server.max_file_size_bytes:
       print(f"File too large: {len(file_content)} bytes")
   
   # Verify MIME type
   mime = magic.Magic(mime=True)
   mime_type = mime.from_buffer(file_content)
   if mime_type not in filesystem_server.allowed_mime_types:
       print(f"Unsupported file type: {mime_type}")
   ```

2. **Search Performance Issues**
   ```python
   # Increase cache duration
   search_server.cache_duration = timedelta(hours=48)
   
   # Reduce concurrent searches
   search_server.max_concurrent_searches = 2
   
   # Check cache efficiency
   if search_server.metrics['cache_hits'] < search_server.metrics['total_searches'] * 0.3:
       print("Low cache hit rate - review search patterns")
   ```

3. **Encryption Errors**
   ```python
   # Regenerate encryption key if needed
   new_key = Fernet.generate_key()
   filesystem_server.cipher = Fernet(new_key)
   
   # Test encryption/decryption
   test_data = b"test"
   encrypted = filesystem_server.cipher.encrypt(test_data)
   decrypted = filesystem_server.cipher.decrypt(encrypted)
   assert decrypted == test_data
   ```

## Security Best Practices

### Document Security
```python
# Always encrypt sensitive documents
sensitive_types = ["resume", "cover_letter", "certificate"]
encrypt = file_type in sensitive_types

# Implement access logging
async def log_file_access(file_id: str, user_id: str, action: str):
    await filesystem_server._log_operation(
        FileOperation(
            operation_id=f"audit_{datetime.now().timestamp()}",
            operation_type=action,
            file_id=file_id,
            user_id=user_id
        )
    )
```

### Search Privacy
```python
# Don't log sensitive search queries
sensitive_keywords = ["salary", "termination", "discrimination"]

def should_log_search(query: str) -> bool:
    return not any(keyword in query.lower() for keyword in sensitive_keywords)
```

### GDPR Compliance
```python
# Regular GDPR audit
async def gdpr_audit():
    # Check data retention
    all_files = list(filesystem_server.file_registry.values())
    old_files = [
        f for f in all_files
        if (datetime.now() - f.created_at).days > 730
    ]
    
    if old_files:
        print(f"⚠️ {len(old_files)} files exceed retention period")
    
    # Verify export capability
    test_export = await filesystem_server.export_user_data("test_user")
    assert len(test_export) > 0, "Export functionality broken"
    
    print("✅ GDPR audit complete")
```

## Integration with Main Application

### Module Registration
```python
# In main application startup
from week2_integration import EnhancedWeek2Orchestrator

orchestrator = EnhancedWeek2Orchestrator()
await orchestrator.initialize()

# Register with conversation router
router.register_handler("filesystem", orchestrator.week2_enhancement.filesystem_agent)
router.register_handler("search", orchestrator.week2_enhancement.search_agent)
```

### Route Configuration
```python
# Update conversation routes
router.route_map.update({
    "upload": ["filesystem"],
    "my documents": ["filesystem"],
    "search jobs": ["search"],
    "market trends": ["search"],
    "apply": ["filesystem", "search", "memory", "thinking"]
})
```

## Next Steps

1. **Week 3 Integration**: Add Cloudinary MCP for media processing
2. **Custom Swiss MCPs**: Develop specialized Swiss compliance MCPs
3. **Week 4 Optimization**: Performance tuning and final validation

---
*Last Updated: 2025-01-05*
*Version: 1.0.0*