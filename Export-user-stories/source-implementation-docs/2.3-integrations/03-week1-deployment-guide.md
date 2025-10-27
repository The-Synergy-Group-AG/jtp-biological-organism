# Week 1 MCP Foundation Deployment Guide

## Overview
This guide covers the deployment of Week 1 MCP Foundation components: Chroma (vector storage), Memory (persistent AI memory), and Sequential Thinking (reasoning engine) for JobTrackerPro.

## Architecture

```
Week 1 MCP Foundation (6×2GB threads, 16GB RAM)
├── Chroma MCP Server (2 threads)
│   ├── Vector embeddings for jobs, profiles, documents
│   ├── Semantic search with Swiss filters
│   └── Learning pattern storage
├── Memory MCP Server (2 threads)
│   ├── Knowledge graph-based memory
│   ├── User context management
│   └── Pattern learning and retention
└── Sequential Thinking MCP Server (2 threads)
    ├── Multi-step reasoning
    ├── Decision making strategies
    └── Self-reflection and improvement
```

## Prerequisites

### System Requirements
- **RAM**: 16GB (12GB allocated, 4GB reserved)
- **CPU**: 6+ cores for optimal thread performance
- **Storage**: 50GB+ for vector and graph storage
- **OS**: Linux/macOS (Windows with WSL2)

### Software Dependencies
```bash
# Python 3.9+
python --version

# Required packages
pip install chromadb==0.4.22
pip install networkx==3.2
pip install sentence-transformers==2.2.2
pip install numpy==1.24.3
pip install asyncio
```

## Installation Steps

### 1. Directory Structure Setup
```bash
# Create MCP data directories
mkdir -p ./mcp_data/chroma
mkdir -p ./mcp_data/memory
mkdir -p ./mcp_data/thinking

# Set permissions
chmod -R 755 ./mcp_data
```

### 2. Environment Configuration
```bash
# Create .env file
cat > .env << EOF
# MCP Configuration
MCP_THREADS_CHROMA=2
MCP_THREADS_MEMORY=2
MCP_THREADS_THINKING=2
MCP_MAX_MEMORY_MB=12288

# Swiss Compliance
SWISS_DATA_RESIDENCY=true
GDPR_COMPLIANT=true
ENCRYPTION_ENABLED=true

# Performance
VECTOR_BATCH_SIZE=100
MEMORY_MAX_NODES=100000
THINKING_MAX_DEPTH=10
EOF
```

### 3. Initialize MCP Servers

#### Chroma MCP Server
```python
# Initialize Chroma with Swiss compliance
from chroma_mcp_integration import ChromaMCPServer

chroma_server = ChromaMCPServer(
    persist_directory="./mcp_data/chroma",
    n_threads=2,
    chunk_size=2048  # 2KB chunks
)

# Verify collections
collections = chroma_server.collections
print(f"Initialized {len(collections)} collections")
```

#### Memory MCP Server
```python
# Initialize Memory with persistence
from memory_mcp_integration import MemoryMCPServer

memory_server = MemoryMCPServer(
    persist_path="./mcp_data/memory",
    max_nodes=100000,
    memory_threads=2
)

# Load existing memory
print(f"Loaded {len(memory_server.nodes)} memory nodes")
```

#### Sequential Thinking MCP Server
```python
# Initialize Thinking with strategies
from sequential_thinking_mcp_integration import SequentialThinkingMCPServer

thinking_server = SequentialThinkingMCPServer(
    max_depth=10,
    parallel_sequences=2,
    reflection_enabled=True
)

print(f"Initialized with {len(thinking_server.thinking_strategies)} strategies")
```

### 4. Integration Testing
```bash
# Run integration tests
python week1_integration.py

# Expected output:
# ✅ Job analysis complete
# ✅ Profile enhancement successful
# ✅ System health: operational
# ✅ Swiss compliance: True
```

## Configuration Options

### Chroma Configuration
```yaml
chroma:
  persist_directory: "./mcp_data/chroma"
  anonymized_telemetry: false  # Swiss privacy
  collections:
    - name: "swiss_jobs"
      languages: ["de", "fr", "it", "en"]
    - name: "user_profiles"
      privacy: "encrypted"
    - name: "compliance_docs"
      retention: "permanent"
```

### Memory Configuration
```yaml
memory:
  persist_path: "./mcp_data/memory"
  layers:
    working:
      ttl: "1h"
      max_size: 1000
    short_term:
      ttl: "24h"
      max_size: 10000
    long_term:
      ttl: null
      max_size: 50000
    core:
      ttl: null
      max_size: 10000
```

### Thinking Configuration
```yaml
thinking:
  max_depth: 10
  strategies:
    - career_planning
    - job_matching
    - interview_prep
    - skill_development
  reflection:
    enabled: true
    frequency: "after_each_sequence"
```

## Usage Examples

### 1. Processing Job Opportunities
```python
# Process a job with full MCP integration
result = await foundation.process_job_opportunity(
    job_data={
        "title": "AI Engineer",
        "company": "Swiss Bank",
        "canton": "ZH",
        "languages": ["English", "German"],
        "skills": ["Python", "ML", "Cloud"]
    },
    user_context={
        "user_id": "user_123",
        "skills": ["Python", "Data Science"],
        "preferences": {"remote": True}
    }
)

print(f"Recommendation: {result['analysis']['recommendation']['action']}")
print(f"Confidence: {result['analysis']['recommendation']['confidence']:.0%}")
```

### 2. Enhancing User Profiles
```python
# Enhance profile with memory and insights
enhanced = await foundation.enhance_user_profile("user_123")

print(f"Profile Strength: {enhanced['profile_strength']:.0%}")
print(f"Market Alignment: {enhanced['market_alignment']['overall_alignment']:.0%}")
print(f"Improvement Areas: {enhanced['improvement_areas']}")
```

### 3. Semantic Job Search
```python
# Search with natural language
results = await chroma_server.semantic_search(
    query="Python developer roles with AI focus in Zurich",
    collection_name="jobs",
    filters={
        "canton": "ZH",
        "min_salary": 100000
    }
)

for job in results[:3]:
    print(f"{job['metadata']['title']} - Match: {job['similarity_score']:.0%}")
```

## Performance Optimization

### Thread Configuration
```python
# Optimal thread distribution for 6×2GB
thread_config = {
    "chroma": 2,      # Vector operations
    "memory": 2,      # Graph operations
    "thinking": 2     # Reasoning operations
}

# Monitor thread usage
import psutil
process = psutil.Process()
print(f"Threads: {process.num_threads()}")
print(f"Memory: {process.memory_info().rss / 1024 / 1024:.0f} MB")
```

### Batch Processing
```python
# Batch embed documents
documents = [...]  # List of documents
batch_size = 100

for i in range(0, len(documents), batch_size):
    batch = documents[i:i+batch_size]
    await asyncio.gather(*[
        chroma_server.embed_document(doc) 
        for doc in batch
    ])
```

### Memory Management
```python
# Monitor and optimize memory usage
metrics = await foundation.generate_insights_report()

if metrics['system_health']['memory']['memory_usage_mb'] > 10000:
    # Trigger memory optimization
    await memory_server.optimize_memory()
    await memory_server._evict_memories()
```

## Monitoring & Maintenance

### Health Checks
```python
# Regular health check script
async def health_check():
    report = await foundation.generate_insights_report()
    
    # Check each component
    for component in ['chroma', 'memory', 'thinking']:
        health = report['system_health'][component]
        print(f"{component}: {health}")
    
    # Swiss compliance
    compliance = report['swiss_compliance']
    if not all(compliance.values()):
        print("⚠️ Compliance issue detected!")
    
    return report['overall_status'] == 'operational'
```

### Backup & Recovery
```bash
# Backup MCP data
tar -czf mcp_backup_$(date +%Y%m%d).tar.gz ./mcp_data/

# Restore from backup
tar -xzf mcp_backup_20250105.tar.gz

# Verify restoration
python -c "
from week1_integration import Week1MCPFoundation
import asyncio

async def verify():
    foundation = Week1MCPFoundation()
    report = await foundation.generate_insights_report()
    print(f'Status: {report[\"overall_status\"]}')

asyncio.run(verify())
"
```

### Performance Monitoring
```python
# Monitor MCP performance
async def monitor_performance():
    while True:
        metrics = {
            "chroma_search_ms": foundation.chroma_server.metrics["avg_search_time_ms"],
            "memory_recall_ms": foundation.memory_server.metrics["avg_recall_time_ms"],
            "thinking_time_ms": foundation.thinking_server.metrics["avg_completion_time_ms"]
        }
        
        # Alert if performance degrades
        for metric, value in metrics.items():
            if value > 100:  # 100ms threshold
                print(f"⚠️ Performance alert: {metric} = {value}ms")
        
        await asyncio.sleep(60)  # Check every minute
```

## Troubleshooting

### Common Issues

1. **High Memory Usage**
   ```python
   # Force memory cleanup
   await memory_server._evict_memories()
   await memory_server.optimize_memory()
   ```

2. **Slow Vector Search**
   ```python
   # Optimize Chroma indices
   perf = await chroma_server.optimize_performance()
   print(f"Recommendations: {perf['recommendations']}")
   ```

3. **Thinking Timeout**
   ```python
   # Adjust thinking depth
   thinking_server.max_depth = 8  # Reduce depth
   ```

4. **Swiss Compliance Failure**
   ```python
   # Check compliance details
   compliance = await chroma_server.ensure_swiss_compliance()
   for check, status in compliance.items():
       if not status:
           print(f"Failed: {check}")
   ```

## Security Considerations

### Data Encryption
```python
# Ensure encryption at rest
import os
os.environ['CHROMA_ENCRYPTION_KEY'] = 'your-secure-key'

# Encrypt sensitive metadata
from cryptography.fernet import Fernet
key = Fernet.generate_key()
cipher = Fernet(key)

# Encrypt before storing
encrypted_data = cipher.encrypt(json.dumps(sensitive_data).encode())
```

### Access Control
```python
# Implement user-level access control
async def check_access(user_id: str, resource: str) -> bool:
    # Verify user permissions
    user_context = await memory_server.get_user_context(user_id)
    return user_context.get("permissions", {}).get(resource, False)
```

### Audit Logging
```python
# Log all MCP operations
import logging
logging.basicConfig(
    filename='mcp_audit.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(message)s'
)
```

## Next Steps

1. **Week 2 Integration**: Add Filesystem and Brave Search MCPs
2. **Week 3 Advanced**: Implement Cloudinary and custom Swiss MCPs
3. **Week 4 Optimization**: Performance tuning and compliance validation

## Support

For issues or questions:
- Check integration tests: `python week1_integration.py`
- Review logs: `tail -f mcp_audit.log`
- Generate system report: `await foundation.generate_insights_report()`

---
*Last Updated: 2025-01-05*
*Version: 1.0.0*