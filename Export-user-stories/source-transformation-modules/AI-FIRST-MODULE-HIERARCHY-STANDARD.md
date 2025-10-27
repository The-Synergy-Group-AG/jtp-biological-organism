# AI-First Module Hierarchy & Naming Standard

**Version**: 1.0.0  
**Date**: 2025-01-16  
**Status**: Official Standard  
**Supersedes**: All previous module naming conventions

## 1. AI-First Naming Principles

### 1.1 Core Philosophy
- **Human-Centric**: Names describe value to users, not technical implementation
- **Conversation-Focused**: Names imply dialogue and interaction
- **Capability-Oriented**: Names describe what the module enables
- **Memorable**: Single or compound words that stick
- **No Numbers**: Zero numeric prefixes or suffixes

### 1.2 Naming Patterns

#### Pattern A: Companion Modules
For modules that act as conversational partners:
```
CareerCompanion     - Guides career journey
InsightCompanion    - Provides analytical insights  
WelcomeCompanion    - Handles onboarding
InterviewCompanion  - Interview preparation partner
```

#### Pattern B: Intelligence Modules
For modules that provide smart capabilities:
```
NetworkIntelligence    - Understands relationships
PrivacyIntelligence   - Manages data protection
MarketIntelligence    - Analyzes job market
EmotionalIntelligence - Provides emotional support
```

#### Pattern C: Engine Modules
For modules that power core functionality:
```
ConversationEngine  - Powers all dialogues
MotivationEngine    - Drives engagement
WorkflowEngine      - Orchestrates processes
InsightEngine       - Generates understanding
```

#### Pattern D: Single-Word Power Names
For foundational modules:
```
MemoryPalace    - Context and state management
PrivacyVault    - Secure data storage
TrustNetwork    - Authentication system
SystemWisdom    - Self-management capability
```

## 2. Module Hierarchy Structure

### 2.1 Wave-Based Organization
```
JTP-AI-Modules/
├── Wave-1-Foundation/
│   ├── ConversationEngine/
│   ├── PrivacyVault/
│   ├── MemoryPalace/
│   └── ...
├── Wave-2-Core/
│   ├── CareerCompanion/
│   ├── OpportunityNavigator/
│   └── ...
├── Wave-3-Advanced/
│   ├── InterviewMentor/
│   ├── EmotionalCompanion/
│   └── ...
├── Wave-4-Infrastructure/
│   ├── IntegrationFabric/
│   ├── PerformanceOptimizer/
│   └── ...
└── Wave-5-Specialized/
    ├── SearchOptimization/
    ├── ResumeIntelligence/
    └── ...
```

### 2.2 Module Internal Structure
```
ModuleName/
├── manifest.yaml           # Module metadata
├── conversations/         # Dialogue definitions
│   ├── intents/          # User intent handlers
│   ├── flows/            # Conversation flows
│   └── responses/        # Response templates
├── intelligence/         # AI capabilities
│   ├── models/          # AI model configs
│   ├── learning/        # Learning mechanisms
│   └── adaptation/      # Adaptation logic
├── integrations/        # External connections
├── tests/              # Test suites
└── docs/               # Documentation
```

## 3. Module Manifest Standard

Every module must have a `manifest.yaml`:

```yaml
module:
  name: CareerCompanion
  wave: 2
  version: 1.0.0
  description: Natural career journey conversations
  
consolidates:
  - legacy: 2.1-JobTracking
    stories: [US-001, US-015]
  - legacy: 2.1-PersonalEfforts  
    stories: [US-016, US-030]
  - legacy: 2.5-JobTracking
    stories: [US-150, US-165]
    
capabilities:
  - intent: track_application
    description: Track job application progress
  - intent: analyze_efforts
    description: Understand job search efforts
  - intent: suggest_improvements
    description: Provide actionable insights
    
dependencies:
  - ConversationEngine: "^1.0.0"
  - MemoryPalace: "^1.0.0"
  - InsightCompanion: "^1.0.0"
  
performance:
  response_time: 150ms
  memory_usage: 256MB
  concurrent_users: 10000
```

## 4. Naming Rules & Guidelines

### 4.1 Mandatory Rules
1. **No Numbers**: Never use numeric prefixes (❌ 2.1-Module)
2. **No Underscores**: Use CamelCase (❌ career_companion)
3. **No Abbreviations**: Full words only (❌ CarCompanion)
4. **English Only**: All names in English
5. **Unique Names**: No duplicates across waves

### 4.2 Recommended Guidelines
1. **15 Character Limit**: Keep names concise
2. **Descriptive**: Name should hint at function
3. **Positive Tone**: Use uplifting language
4. **Action-Oriented**: Imply capability
5. **User-Focused**: Think user benefit

### 4.3 Examples

#### ✅ Good Names
```
CareerCompanion      - Clear, friendly, purposeful
OpportunityNavigator - Action-oriented, clear benefit
MemoryPalace        - Memorable, implies organization
InsightEngine       - Technical but clear purpose
TrustNetwork        - Security with relationship focus
```

#### ❌ Bad Names
```
2.1-JobTracker      - Has numbers
JobMgmt             - Abbreviated
job_tracker         - Has underscores
TrackingModule      - Too generic
JTPJobHandler       - Technical, not user-focused
```

## 5. Module Categories (Semantic, Not Structural)

### 5.1 Journey Modules
Support user's career journey:
- CareerCompanion
- OpportunityNavigator
- InterviewMentor
- TransitionGuide

### 5.2 Intelligence Modules  
Provide smart insights:
- InsightCompanion
- MarketIntelligence
- NetworkIntelligence
- PredictiveAdvisor

### 5.3 Experience Modules
Shape user experience:
- MotivationEngine
- EmotionalCompanion
- ExperienceDesigner
- PersonalizationEngine

### 5.4 Foundation Modules
Core infrastructure:
- ConversationEngine
- MemoryPalace
- PrivacyVault
- SystemWisdom

### 5.5 Bridge Modules
Connect to external world:
- IntegrationFabric
- CommunicationBridge
- PortalUnifier
- APITransformer

## 6. Module Relationships

### 6.1 Dependency Types
```yaml
dependencies:
  required:          # Won't function without
    - ConversationEngine: "^1.0.0"
  recommended:       # Better with these
    - InsightCompanion: "^1.0.0"
  optional:          # Enhanced features
    - EmotionalCompanion: "^1.0.0"
```

### 6.2 Communication Patterns
```yaml
communications:
  publishes:
    - event: career_milestone_reached
    - event: application_status_changed
  subscribes:
    - event: user_mood_detected
    - event: market_conditions_changed
```

## 7. Migration Mapping

### 7.1 Quick Reference Table
| Old Module | New Module | Wave |
|------------|------------|------|
| 1.1-Core | ConversationEngine | 1 |
| 1.2-Security | PrivacyVault | 1 |
| 1.5-Admin | SystemWisdom | 1 |
| 2.1/2.5-JobTracking | CareerCompanion | 2 |
| 2.2-Applications | OpportunityNavigator | 2 |
| 2.3-Analytics + others | InsightCompanion | 2 |
| 2.4-Gamification + others | MotivationEngine | 2 |
| 2.6-RAVCompliance | ComplianceGuide | 2 |
| 2.8-NetworkProspecting | NetworkIntelligence | 2 |
| 2.9-InterviewPrep | InterviewMentor | 3 |
| 3.2/4.5-Onboarding | WelcomeCompanion | 1 |
| 3.8-EmotionalIntelligence | EmotionalCompanion | 3 |

### 7.2 Consolidation Rules
When multiple old modules become one:
1. Combine all user stories
2. Merge overlapping capabilities
3. Preserve all business logic
4. Document in manifest
5. Create migration guide

## 8. Implementation Checklist

### 8.1 For New Modules
- [ ] Choose name following patterns
- [ ] Verify name uniqueness
- [ ] Create manifest.yaml
- [ ] Define wave placement
- [ ] Document capabilities
- [ ] Map user stories
- [ ] Set up structure

### 8.2 For Migration
- [ ] Identify all legacy modules
- [ ] Map to new names
- [ ] Create consolidation plan
- [ ] Update story mappings
- [ ] Document in manifest
- [ ] Create migration scripts
- [ ] Update references

## 9. Governance & Compliance

### 9.1 Review Process
1. Developer proposes module name
2. Check against naming rules
3. Verify uniqueness
4. Review with team
5. Update module registry
6. Document decision

### 9.2 Module Registry
Central registry location: `/modules/MODULE_REGISTRY.yaml`

```yaml
registry:
  version: 1.0.0
  updated: 2025-01-16
  modules:
    ConversationEngine:
      wave: 1
      status: active
      added: 2025-01-16
    CareerCompanion:
      wave: 2
      status: active
      added: 2025-01-16
      consolidates: [2.1-JobTracking, 2.5-JobTracking]
```

### 9.3 Validation Tools
```bash
# Validate module name
./scripts/validate-module-name.sh "ProposedName"

# Check uniqueness
./scripts/check-module-unique.sh "ProposedName"

# Validate manifest
./scripts/validate-manifest.sh /path/to/manifest.yaml
```

## 10. FAQ

**Q: Can I use numbers in any form?**  
A: No. Zero numbers allowed. Use descriptive names.

**Q: What about versioning?**  
A: Versions go in manifest.yaml, not module names.

**Q: How do I indicate sub-modules?**  
A: Use capability namespacing within the module, not separate modules.

**Q: Can modules have similar names?**  
A: Yes, if they serve different purposes (e.g., InsightCompanion vs InsightEngine).

**Q: What about technical modules?**  
A: Give them user-friendly names (e.g., CacheModule → PerformanceOptimizer).

---

*"From 2.1-JobTracking to CareerCompanion. From technical features to human experiences. This is the AI-First way."*