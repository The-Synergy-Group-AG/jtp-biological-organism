# N8N Workflow Training Guide for JobTrackerPro Team

## Table of Contents
1. [Introduction](#introduction)
2. [N8N Fundamentals](#n8n-fundamentals)
3. [Perplexity Integration](#perplexity-integration)
4. [Building Job Discovery Workflows](#building-job-discovery-workflows)
5. [Debugging and Troubleshooting](#debugging-and-troubleshooting)
6. [Best Practices](#best-practices)
7. [Hands-On Exercises](#hands-on-exercises)
8. [Resources](#resources)

## Introduction

This training guide will help you master N8N workflow automation for JobTrackerPro's enhanced job scraping capabilities. By the end of this training, you'll be able to create, modify, and maintain N8N workflows that integrate with Perplexity AI.

### Training Objectives
- Understand N8N's visual workflow paradigm
- Create job discovery workflows with AI integration
- Debug and optimize workflow performance
- Maintain Swiss compliance in all workflows

## N8N Fundamentals

### What is N8N?
N8N is a workflow automation platform that allows you to:
- Build workflows visually without code
- Connect 400+ apps and services
- Run self-hosted for data privacy
- Create complex automations with AI

### Core Concepts

#### 1. Nodes
Building blocks of workflows:
- **Trigger Nodes**: Start workflows (webhooks, schedules, etc.)
- **Action Nodes**: Perform operations (HTTP requests, data transformation)
- **Logic Nodes**: Control flow (IF, Switch, Merge)

#### 2. Connections
- Connect nodes by dragging from output to input
- Multiple outputs allow branching logic
- Data flows through connections

#### 3. Expressions
- Access data from previous nodes: `{{ $node["NodeName"].json.fieldName }}`
- Use JavaScript: `{{ new Date().toISOString() }}`
- Transform data inline

### N8N Interface Overview

```
┌─────────────────────────────────────────────────────┐
│  N8N Workflow Editor                                │
├─────────────────────────────────────────────────────┤
│  ┌─────────┐     ┌──────────────┐    ┌─────────┐  │
│  │ Sidebar │     │              │    │ Output  │  │
│  │         │     │   Canvas     │    │ Panel   │  │
│  │ - Nodes │     │              │    │         │  │
│  │ - Tools │     │  [Node] ──>  │    │ Results │  │
│  │         │     │              │    │         │  │
│  └─────────┘     └──────────────┘    └─────────┘  │
└─────────────────────────────────────────────────────┘
```

## Perplexity Integration

### Setting Up Perplexity Credentials

1. **Access Credentials**:
   ```
   Settings → Credentials → New → Search "Perplexity"
   ```

2. **Configure API Key**:
   ```json
   {
     "name": "Perplexity API",
     "api_key": "pplx-xxxxxxxxxx"
   }
   ```

### Using Perplexity in Workflows

#### Basic Perplexity Query
```javascript
// Node: HTTP Request
{
  "method": "POST",
  "url": "https://api.perplexity.ai/chat/completions",
  "authentication": "predefinedCredentialType",
  "nodeCredentialType": "perplexityApi",
  "sendBody": true,
  "bodyParameters": {
    "model": "pplx-70b-online",
    "messages": [
      {
        "role": "system",
        "content": "You are a Swiss job market expert."
      },
      {
        "role": "user",
        "content": "{{ $json.query }}"
      }
    ]
  }
}
```

## Building Job Discovery Workflows

### Workflow 1: Basic Job Search

**Objective**: Search for jobs across multiple Swiss job boards

#### Step-by-Step Instructions:

1. **Create Webhook Trigger**
   - Add: Webhook node
   - Set path: `/job-search`
   - Response mode: "On received"

2. **Prepare Search Query**
   - Add: Function node
   - Code:
   ```javascript
   const keywords = $input.item.json.keywords || [];
   const location = $input.item.json.location || "Zurich";
   
   return {
     searchQuery: `${keywords.join(" ")} jobs in ${location}`,
     perplexityPrompt: `Find current ${keywords.join(" ")} job openings in ${location}, Switzerland. Include salary ranges and requirements.`
   };
   ```

3. **Query Perplexity**
   - Add: HTTP Request node
   - Use Perplexity API configuration
   - Body: Use prepared prompt

4. **Parse Results**
   - Add: Code node
   - Extract job listings from Perplexity response

5. **Store in Database**
   - Add: HTTP Request to JTP API
   - Store parsed jobs

### Workflow 2: Market Intelligence

**Objective**: Gather job market trends and insights

```mermaid
graph LR
    A[Daily Schedule] --> B[Define Markets]
    B --> C[Perplexity Research]
    C --> D[Extract Insights]
    D --> E[Generate Report]
    E --> F[Send Notifications]
```

### Workflow 3: Company Deep Dive

**Objective**: Research companies when users show interest

#### Components:
1. Webhook trigger with company name
2. Perplexity company research
3. Glassdoor API integration
4. LinkedIn data enrichment
5. Aggregate and store insights

## Debugging and Troubleshooting

### Common Issues and Solutions

#### 1. Workflow Not Triggering
- **Check**: Is webhook URL correct?
- **Solution**: Test with curl:
  ```bash
  curl -X POST https://n8n.jtp.swiss/webhook/job-search \
    -H "Content-Type: application/json" \
    -d '{"keywords": ["developer"], "location": "Zurich"}'
  ```

#### 2. Perplexity Errors
- **Check**: API key valid?
- **Solution**: Test credentials in isolation
- **Common error**: Rate limiting - implement retry logic

#### 3. Data Not Flowing
- **Check**: Node connections correct?
- **Solution**: Use output panel to inspect data at each step

### Debugging Tools

1. **Execution History**
   - View past executions
   - See exact data at each node
   - Identify failure points

2. **Manual Execution**
   - Test with sample data
   - Step through nodes
   - Modify and retry

3. **Logging**
   ```javascript
   // Add console logs in Function nodes
   console.log('Debug:', $input.item.json);
   ```

## Best Practices

### 1. Swiss Compliance
- **Data Residency**: Ensure workflows process data in Switzerland
- **Privacy**: Don't log personal information
- **Language**: Support all Swiss languages

```javascript
// Language detection in workflows
const detectLanguage = (text) => {
  if (text.includes('Stelle') || text.includes('Arbeit')) return 'de-CH';
  if (text.includes('emploi') || text.includes('poste')) return 'fr-CH';
  if (text.includes('lavoro')) return 'it-CH';
  return 'en';
};
```

### 2. Error Handling
Always implement error handling:

```javascript
// In Code nodes
try {
  // Your logic
} catch (error) {
  return {
    error: true,
    message: error.message,
    timestamp: new Date().toISOString()
  };
}
```

### 3. Performance Optimization
- Use caching for repeated queries
- Implement parallel processing
- Set appropriate timeouts

### 4. Workflow Organization
- Use clear, descriptive node names
- Add sticky notes for documentation
- Group related nodes
- Version control workflow exports

## Hands-On Exercises

### Exercise 1: Create Your First Workflow
**Goal**: Build a simple job search workflow

1. Create webhook trigger
2. Add Perplexity query
3. Parse and display results
4. Test with real data

**Success Criteria**: 
- Workflow executes without errors
- Returns at least 5 job listings
- Data is properly formatted

### Exercise 2: Add Intelligence
**Goal**: Enhance workflow with market insights

1. Extend Exercise 1 workflow
2. Add market analysis branch
3. Aggregate insights
4. Create summary report

### Exercise 3: Multi-Board Integration
**Goal**: Search across multiple job boards

1. Parallel job board queries
2. Merge and deduplicate results
3. Rank by relevance
4. Store in vector database

### Exercise 4: Swiss Localization
**Goal**: Handle Swiss market specifics

1. Detect search language
2. Route to appropriate boards
3. Handle canton-specific searches
4. Format salaries in CHF

## Advanced Topics

### Custom Nodes
Create custom N8N nodes for JTP-specific operations:

```typescript
// Example: JTP Job Ranker Node
import { INodeType, INodeTypeDescription } from 'n8n-workflow';

export class JtpJobRanker implements INodeType {
  description: INodeTypeDescription = {
    displayName: 'JTP Job Ranker',
    name: 'jtpJobRanker',
    group: ['transform'],
    version: 1,
    description: 'Rank jobs using JTP AI',
    defaults: {
      name: 'JTP Job Ranker',
    },
    inputs: ['main'],
    outputs: ['main'],
    properties: [
      // Node properties
    ],
  };

  async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
    // Ranking logic
  }
}
```

### Workflow Templates

#### Template: Daily Job Digest
```json
{
  "name": "Daily Job Digest",
  "nodes": [
    {
      "name": "Schedule",
      "type": "n8n-nodes-base.cron",
      "parameters": {
        "triggerTimes": {
          "item": [{"hour": 8, "minute": 0}]
        }
      }
    },
    // ... rest of workflow
  ]
}
```

### Integration Patterns

#### Pattern 1: Retry with Backoff
```javascript
// Exponential backoff for API calls
const maxRetries = 3;
let retries = 0;

while (retries < maxRetries) {
  try {
    // API call
    break;
  } catch (error) {
    retries++;
    const delay = Math.pow(2, retries) * 1000;
    await new Promise(resolve => setTimeout(resolve, delay));
  }
}
```

#### Pattern 2: Batch Processing
```javascript
// Process items in batches
const batchSize = 10;
const items = $input.all();
const batches = [];

for (let i = 0; i < items.length; i += batchSize) {
  batches.push(items.slice(i, i + batchSize));
}

// Process each batch
for (const batch of batches) {
  // Process batch
  await processJobBatch(batch);
}
```

## Testing Your Workflows

### Unit Testing Approach
1. Test each node in isolation
2. Use mock data for external services
3. Verify data transformations

### Integration Testing
1. Test complete workflow end-to-end
2. Use test webhooks
3. Verify all integrations work

### Load Testing
```bash
# Test webhook performance
ab -n 100 -c 10 -p test_data.json \
  -H "Content-Type: application/json" \
  https://n8n.jtp.swiss/webhook/job-search
```

## Monitoring and Maintenance

### Key Metrics to Track
- Execution success rate
- Average execution time
- API usage and costs
- Error frequency by node

### Maintenance Schedule
- **Daily**: Check execution logs
- **Weekly**: Review performance metrics
- **Monthly**: Update workflows based on feedback
- **Quarterly**: Major workflow optimizations

## Resources

### N8N Documentation
- [Official Docs](https://docs.n8n.io)
- [Community Forum](https://community.n8n.io)
- [YouTube Tutorials](https://youtube.com/n8n-io)

### Perplexity Resources
- [API Documentation](https://docs.perplexity.ai)
- [Best Practices](https://perplexity.ai/best-practices)

### JTP-Specific Resources
- Internal Wiki: `wiki.jtp.swiss/n8n`
- Slack Channel: `#n8n-workflows`
- Office Hours: Thursdays 2-3 PM CET

### Useful Tools
- [JSON Formatter](https://jsonformatter.org)
- [Regex Tester](https://regex101.com)
- [Cron Expression Generator](https://crontab.guru)

## Certification Path

### Level 1: N8N Fundamentals
- Complete all basic exercises
- Build 3 working workflows
- Pass fundamentals quiz

### Level 2: Advanced Automation
- Implement complex logic flows
- Integrate 5+ external services
- Optimize workflow performance

### Level 3: Workflow Architect
- Design system-wide workflows
- Implement custom nodes
- Mentor other team members

## Conclusion

N8N with Perplexity integration represents a significant advancement in our job scraping capabilities. By mastering these tools, you'll be able to:

- Reduce development time by 80%
- Create more intelligent job discovery
- Maintain and modify workflows easily
- Scale our platform efficiently

Remember: The goal is not just to replace Playwright, but to enhance our entire job discovery intelligence. Think creatively about how AI can improve every aspect of the user journey.

### Next Steps
1. Complete Exercise 1 within 24 hours
2. Join the #n8n-workflows Slack channel
3. Schedule 1:1 with workflow architect
4. Start building your first production workflow

**Happy Workflow Building! 🚀**