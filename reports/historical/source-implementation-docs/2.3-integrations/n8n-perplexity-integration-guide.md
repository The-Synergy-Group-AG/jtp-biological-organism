# N8N + Perplexity Integration Guide for JobTrackerPro

## Executive Summary

This guide details the integration of N8N workflow automation with Perplexity AI to enhance JobTrackerPro's AI-powered job scraping capabilities. The integration provides a visual, no-code approach to complex scraping workflows while maintaining our AI-First principles.

## Current State vs Enhanced State

### Current State (Playwright-based)
- **Technology**: Custom Playwright scripts with anti-detection
- **Maintenance**: High - requires code updates for site changes
- **Scalability**: Limited by browser resource requirements
- **Cost**: High infrastructure costs for browser instances
- **Intelligence**: GPT-4 for extraction only

### Enhanced State (N8N + Perplexity)
- **Technology**: Visual workflow automation with AI orchestration
- **Maintenance**: Low - AI adapts to changes automatically
- **Scalability**: Highly scalable with API-based approach
- **Cost**: 70% reduction in infrastructure costs
- **Intelligence**: Full AI research and understanding capabilities

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                   JobTrackerPro Frontend                      │
│                  (Conversational AI Interface)                │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────┐
│                     MCP Client Layer                          │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
┌───────┴────────┐         ┌───────┴────────┐
│  MCP Servers   │         │ N8N Workflows  │
│                │         │                │
│ • Job Board    │         │ • Discovery    │
│ • Swiss Market │◄────────┤ • Research     │
│ • CV Optimize  │         │ • Analysis     │
└────────────────┘         └───────┬────────┘
                                   │
                           ┌───────┴────────┐
                           │  Perplexity AI │
                           │                │
                           │ • Research     │
                           │ • Intelligence │
                           └────────────────┘
```

## Implementation Phases

### Phase 1: Pilot Integration (Week 1-2)

#### 1.1 Environment Setup

```bash
# Install N8N (self-hosted Swiss instance)
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -e N8N_BASIC_AUTH_ACTIVE=true \
  -e N8N_BASIC_AUTH_USER=jtp_admin \
  -e N8N_BASIC_AUTH_PASSWORD=secure_password \
  -e N8N_ENCRYPTION_KEY=your_encryption_key \
  -v n8n_data:/home/node/.n8n \
  n8nio/n8n:1.98.1

# Configure Perplexity credentials in N8N
# UI: Settings → Credentials → Add Credential → Perplexity API
```

#### 1.2 First Workflow: Job Discovery

Create this workflow in N8N UI:

```json
{
  "name": "JTP_Job_Discovery_Pilot",
  "nodes": [
    {
      "parameters": {
        "path": "jtp-job-search",
        "responseMode": "responseNode",
        "options": {}
      },
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "position": [250, 300]
    },
    {
      "parameters": {
        "url": "https://api.perplexity.ai/chat/completions",
        "authentication": "predefinedCredentialType",
        "nodeCredentialType": "perplexityApi",
        "method": "POST",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            {
              "name": "model",
              "value": "pplx-70b-online"
            },
            {
              "name": "messages",
              "value": "=[{\"role\": \"user\", \"content\": \"Find current {{$json.role}} job openings in {{$json.location}} Switzerland. Include salary ranges, required skills, and market trends.\"}]"
            }
          ]
        }
      },
      "name": "Perplexity Research",
      "type": "n8n-nodes-base.httpRequest",
      "position": [450, 300]
    },
    {
      "parameters": {
        "agent": "conversationalAgent",
        "promptType": "define",
        "text": "You are a Swiss job market expert. Extract structured job data from the research and format it for our database. Include: title, company, location, salary, requirements, application_url.",
        "hasOutputParser": true
      },
      "name": "AI Agent Parser",
      "type": "@n8n/n8n-nodes-langchain.agent",
      "position": [650, 300]
    },
    {
      "parameters": {
        "url": "={{$env.JTP_MCP_SERVER}}/store-jobs",
        "method": "POST",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            {
              "name": "jobs",
              "value": "={{$json.extracted_jobs}}"
            },
            {
              "name": "source",
              "value": "n8n_perplexity"
            }
          ]
        }
      },
      "name": "Store in JTP",
      "type": "n8n-nodes-base.httpRequest",
      "position": [850, 300]
    }
  ]
}
```

#### 1.3 Integration Code

```python
# Enhanced Job Discovery Agent with N8N
class EnhancedJobDiscoveryAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Enhanced Job Discovery",
            description="AI-powered job discovery with N8N orchestration"
        )
        self.n8n_client = N8NPerplexityClient(
            n8n_base_url="http://localhost:5678"
        )
        
    async def discover_jobs(self, user_context: Dict) -> List[JobListing]:
        """Discover jobs using hybrid approach"""
        
        # Determine search strategy
        if user_context.get("specific_company"):
            # Use Playwright for deep company scraping
            return await self._deep_company_scrape(user_context)
        else:
            # Use N8N + Perplexity for broad market search
            return await self._n8n_market_search(user_context)
            
    async def _n8n_market_search(self, context: Dict) -> List[JobListing]:
        """Use N8N workflow for market search"""
        
        async with self.n8n_client:
            # Execute discovery workflow
            result = await self.n8n_client.execute_workflow(
                WorkflowType.JOB_DISCOVERY,
                {
                    "role": context.get("desired_role"),
                    "location": context.get("location", "Zurich"),
                    "skills": context.get("skills", []),
                    "salary_expectations": context.get("salary_range"),
                    "languages": ["de-CH", "en"]
                }
            )
            
            # Convert to JobListing objects
            jobs = []
            for job_data in result.get("jobs", []):
                listing = JobListing(
                    board_id="n8n_aggregated",
                    external_id=job_data.get("id"),
                    title=job_data.get("title"),
                    company=job_data.get("company"),
                    location=job_data.get("location"),
                    canton=self._extract_canton(job_data.get("location")),
                    description=job_data.get("description"),
                    requirements=job_data.get("requirements", []),
                    salary_range=job_data.get("salary"),
                    posted_date=datetime.now(),
                    application_url=job_data.get("url"),
                    ai_insights=job_data.get("perplexity_insights", {})
                )
                jobs.append(listing)
                
            return jobs
```

### Phase 2: Advanced Workflows (Week 3-4)

#### 2.1 Market Intelligence Workflow

```javascript
// N8N Workflow: Swiss Market Intelligence
{
  "nodes": [
    {
      "name": "Daily Trigger",
      "type": "n8n-nodes-base.cron",
      "parameters": {
        "triggerTimes": {
          "item": [{
            "hour": 8,
            "minute": 0
          }]
        }
      }
    },
    {
      "name": "Get User Preferences",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "={{$env.JTP_API}}/users/preferences",
        "method": "GET"
      }
    },
    {
      "name": "Perplexity Market Analysis",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://api.perplexity.ai/chat/completions",
        "method": "POST",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [{
            "name": "messages",
            "value": "={{$json.market_analysis_prompt}}"
          }]
        }
      }
    },
    {
      "name": "Generate Insights",
      "type": "@n8n/n8n-nodes-langchain.agent",
      "parameters": {
        "agent": "planAndExecuteAgent",
        "text": "Analyze market trends and generate personalized insights"
      }
    },
    {
      "name": "Send Notifications",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "={{$env.JTP_API}}/notifications/send",
        "method": "POST"
      }
    }
  ]
}
```

#### 2.2 Company Research Workflow

```python
# N8N Workflow Definition for Company Research
COMPANY_RESEARCH_WORKFLOW = {
    "name": "JTP_Company_Deep_Dive",
    "nodes": [
        {
            "name": "Company Input",
            "type": "webhook",
            "parameters": {
                "path": "company-research"
            }
        },
        {
            "name": "Perplexity Company Research",
            "type": "httpRequest",
            "parameters": {
                "url": "https://api.perplexity.ai/chat/completions",
                "body": {
                    "messages": [{
                        "role": "system",
                        "content": "You are a Swiss job market expert. Research this company thoroughly."
                    }, {
                        "role": "user",
                        "content": "Research {{company_name}} in Switzerland: culture, salaries, reviews, interview process, growth"
                    }]
                }
            }
        },
        {
            "name": "Glassdoor Scraper",
            "type": "httpRequest",
            "parameters": {
                "url": "{{glassdoor_api_endpoint}}",
                "qs": {
                    "company": "{{company_name}}",
                    "location": "Switzerland"
                }
            }
        },
        {
            "name": "LinkedIn Insights",
            "type": "httpRequest",
            "parameters": {
                "url": "{{linkedin_api_endpoint}}",
                "headers": {
                    "Authorization": "Bearer {{linkedin_token}}"
                }
            }
        },
        {
            "name": "AI Synthesis",
            "type": "agent",
            "parameters": {
                "agent": "researchAgent",
                "tools": ["webSearch", "calculator", "textSummarizer"],
                "prompt": "Synthesize all company research into actionable insights"
            }
        },
        {
            "name": "Store Results",
            "type": "httpRequest",
            "parameters": {
                "url": "{{jtp_api}}/company-insights",
                "method": "POST"
            }
        }
    ]
}
```

### Phase 3: Full Integration (Week 5-6)

#### 3.1 Hybrid Orchestration Layer

```python
class HybridJobScrapingSystem:
    """Orchestrates N8N and Playwright for optimal scraping"""
    
    def __init__(self):
        self.n8n = N8NPerplexityClient(os.getenv("N8N_URL"))
        self.playwright = PlaywrightScraper()
        self.decision_engine = ScrapingDecisionEngine()
        
    async def scrape_intelligently(self, request: JobSearchRequest):
        """Choose optimal scraping strategy"""
        
        # Analyze request complexity
        strategy = await self.decision_engine.determine_strategy(request)
        
        if strategy.method == "n8n":
            # Use N8N for:
            # - Broad searches across multiple boards
            # - Research-heavy queries
            # - Trend analysis
            return await self._n8n_scrape(request, strategy)
            
        elif strategy.method == "playwright":
            # Use Playwright for:
            # - Specific company pages
            # - Login-required sites
            # - Complex interactions
            return await self._playwright_scrape(request, strategy)
            
        else:  # hybrid
            # Use both for maximum coverage
            n8n_task = asyncio.create_task(self._n8n_scrape(request, strategy))
            playwright_task = asyncio.create_task(self._playwright_scrape(request, strategy))
            
            n8n_results, playwright_results = await asyncio.gather(
                n8n_task, playwright_task
            )
            
            # Merge and deduplicate
            return self._merge_results(n8n_results, playwright_results)
```

## Performance Metrics

### Expected Improvements

| Metric | Current (Playwright) | Enhanced (N8N+Perplexity) | Improvement |
|--------|---------------------|---------------------------|-------------|
| Scraping Speed | 30s per board | 5s per board | 83% faster |
| Maintenance Hours | 20hrs/month | 2hrs/month | 90% reduction |
| Infrastructure Cost | $500/month | $150/month | 70% savings |
| Data Quality | 85% accuracy | 95% accuracy | 12% improvement |
| Market Insights | Limited | Comprehensive | ∞ |

### Monitoring Dashboard

```python
# N8N Monitoring Integration
class N8NPerformanceMonitor:
    def __init__(self):
        self.metrics = {
            "workflow_executions": Counter("n8n_workflow_executions_total"),
            "workflow_duration": Histogram("n8n_workflow_duration_seconds"),
            "perplexity_api_calls": Counter("perplexity_api_calls_total"),
            "job_discovery_rate": Gauge("job_discovery_rate_per_minute")
        }
        
    async def track_workflow(self, workflow_name: str, duration: float, success: bool):
        """Track workflow execution metrics"""
        
        self.metrics["workflow_executions"].inc({
            "workflow": workflow_name,
            "status": "success" if success else "failure"
        })
        
        self.metrics["workflow_duration"].observe(duration, {
            "workflow": workflow_name
        })
```

## Swiss Market Optimizations

### Multi-language Support

```javascript
// N8N Sub-workflow: Language Detection and Translation
{
  "name": "Swiss_Language_Handler",
  "nodes": [
    {
      "name": "Detect Language",
      "type": "function",
      "parameters": {
        "functionCode": `
          const text = $input.item.json.text;
          const languages = ['de-CH', 'fr-CH', 'it-CH', 'rm-CH', 'en'];
          
          // Simple detection logic
          if (text.includes('Stelle') || text.includes('Arbeit')) return 'de-CH';
          if (text.includes('emploi') || text.includes('poste')) return 'fr-CH';
          if (text.includes('lavoro') || text.includes('impiego')) return 'it-CH';
          
          return 'en';
        `
      }
    },
    {
      "name": "Translate if Needed",
      "type": "if",
      "parameters": {
        "conditions": {
          "string": [{
            "value1": "={{$json.detected_language}}",
            "operation": "notEquals",
            "value2": "={{$json.target_language}}"
          }]
        }
      }
    }
  ]
}
```

### Canton-Specific Workflows

```python
# Canton-specific job board configurations
CANTON_JOB_BOARDS = {
    "ZH": {
        "primary": ["jobs.ch", "jobscout24.ch"],
        "local": ["stadt-zuerich.ch/jobs", "zh.ch/jobs"],
        "language": "de-CH"
    },
    "GE": {
        "primary": ["jobup.ch", "indeed.ch"],
        "local": ["ge.ch/emploi", "ville-geneve.ch"],
        "language": "fr-CH"
    },
    "TI": {
        "primary": ["jobs.ch", "ticino.ch"],
        "local": ["ti.ch/lavoro"],
        "language": "it-CH"
    }
}
```

## Security and Compliance

### Data Privacy

```python
# Swiss-compliant data handling in N8N
class SwissCompliantN8NClient(N8NPerplexityClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.encryption = SwissDataEncryption()
        
    async def execute_workflow(self, workflow_type, payload):
        """Execute with Swiss privacy compliance"""
        
        # Encrypt sensitive data
        encrypted_payload = self.encryption.encrypt_pii(payload)
        
        # Execute in Swiss data center
        result = await super().execute_workflow(
            workflow_type,
            encrypted_payload
        )
        
        # Decrypt results
        return self.encryption.decrypt_response(result)
```

## Rollout Plan

### Week 1-2: Pilot
- Deploy N8N in Swiss data center
- Implement job discovery workflow
- A/B test against current system
- Monitor performance metrics

### Week 3-4: Expansion
- Add market research workflows
- Implement company analysis
- Integrate with MCP servers
- Train AI agents on Swiss data

### Week 5-6: Full Production
- Migrate all job boards to hybrid system
- Implement monitoring and alerting
- Document workflows for maintenance
- Conduct performance review

## Cost-Benefit Analysis

### Costs
- N8N Enterprise License: $99/month
- Perplexity API: ~$200/month (estimated)
- Development: 80 hours
- Training: 20 hours

### Benefits
- Infrastructure savings: $350/month
- Maintenance reduction: 18 hours/month
- Improved job discovery: 20% more relevant matches
- Market insights: Previously unavailable

### ROI
- Break-even: 3 months
- Annual savings: $4,200
- Productivity gain: 216 hours/year

## Conclusion

The N8N + Perplexity integration represents a significant advancement in JobTrackerPro's scraping capabilities. By combining visual workflow automation with AI intelligence, we can:

1. Reduce complexity and maintenance overhead
2. Improve data quality and insights
3. Scale more efficiently
4. Maintain Swiss compliance
5. Enhance user experience with better job matches

The hybrid approach ensures we leverage the best of both worlds - N8N's efficiency for standard scraping and Playwright's power for complex scenarios.