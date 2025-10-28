# Developer Quick Reference: Module Changes

**Date**: 2025-01-16  
**IMPORTANT**: All module names have changed. Use this guide for migration.

## 🚨 Critical Changes

### No More Numbers!
- ❌ OLD: `2.1-JobTracking`
- ✅ NEW: `CareerCompanion`

### Wave-Based Organization
- ❌ OLD: `/modules/2.x-Features/2.1-JobTracking/`
- ✅ NEW: `/modules/Wave-2-Core/CareerCompanion/`

## 📋 Quick Lookup Table

### Most Used Modules

| You're Looking For | Old Name | New Name | Wave |
|-------------------|----------|----------|------|
| Job tracking | 2.1-JobTracking | CareerCompanion | 2 |
| Applications | 2.2-Applications | OpportunityNavigator | 2 |
| Analytics | 2.3-Analytics | InsightCompanion | 2 |
| Gamification | 2.4-Gamification | MotivationEngine | 2 |
| Authentication | 1.2-Security | PrivacyVault | 1 |
| Admin panel | 1.5-Admin | SystemWisdom | 1 |
| Onboarding | 3.2-Onboarding | WelcomeCompanion | 1 |
| Network/LinkedIn | 2.4a-LinkedInIntegration | NetworkIntelligence | 2 |
| Interview prep | 2.9-InterviewPrep | InterviewMentor | 3 |
| Emotional support | 3.8-EmotionalIntelligence | EmotionalCompanion | 3 |

### Complete Module Mapping

#### Wave 1: Foundation (9 modules)
```
1.1-Core                → ConversationEngine
1.2-Security            → PrivacyVault
1.2a-Authentication     → TrustNetwork (consolidated)
1.2b-Authorization      → TrustNetwork (consolidated)
1.3-Configuration       → ConfigurationIntelligence
1.5-Admin              → SystemWisdom
1.6-NotificationCenter  → NotificationCompanion
1.7-EventBus           → EventOrchestrator
3.2/4.5-Onboarding     → WelcomeCompanion
NEW                    → MemoryPalace
```

#### Wave 2: Core Experience (8 modules)
```
2.1/2.5-JobTracking    → CareerCompanion
2.2-Applications       → OpportunityNavigator
All Analytics modules  → InsightCompanion
All Gamification      → MotivationEngine
All Network modules   → NetworkIntelligence
2.6-RAVCompliance     → ComplianceGuide
2.7-UserMarketing     → BrandEvolution
2.10-FeedbackMode     → FeedbackWhisperer
```

#### Wave 3: Advanced Features (13 modules)
```
2.9-InterviewPrep      → InterviewMentor
2.11-TimelineSupport   → TimelineStoryteller
3.8-EmotionalIntel     → EmotionalCompanion
3.1/3.4-Ambassador     → CommunityOrchestrator
NEW                    → LearningPathfinder
3.9-EmailIntegration   → CommunicationBridge
3.3-ThemeCustom        → ExperienceDesigner
3.4-International      → UniversalTranslator
3.5-DragDrop          → GestureInterpreter
3.3/3.6-AIAssets      → CreativeCompanion
3.7-LegalDocs         → LegalAdvisor
3.5/4.3-Trends        → MarketIntelligence
2.3/4.4-Portals       → PortalUnifier
```

## 🔧 Code Migration

### Import Updates
```php
// OLD
use JobTrackerPro\Modules\Features\JobTracking\Services\JobService;
use JobTrackerPro\Modules\Features\Gamification\Models\Achievement;

// NEW
use JobTrackerPro\Modules\Wave2\CareerCompanion\Services\CareerService;
use JobTrackerPro\Modules\Wave2\MotivationEngine\Models\Achievement;
```

### Configuration Updates
```php
// OLD
define('JTP_MODULE_PATH', 'modules/2.1-JobTracking');

// NEW
define('JTP_MODULE_PATH', 'modules/Wave-2-Core/CareerCompanion');
```

### Event Names
```php
// OLD
do_action('jtp_job_tracking_update', $data);

// NEW
do_action('jtp_career_companion_update', $data);
```

## 📁 Directory Structure

### Old Structure
```
modules/
├── 1.x-Core/
│   ├── 1.1-Core/
│   ├── 1.2-Security/
│   └── ...
├── 2.x-Features/
│   ├── 2.1-JobTracking/
│   ├── 2.2-Applications/
│   └── ...
```

### New Structure
```
modules/
├── Wave-1-Foundation/
│   ├── ConversationEngine/
│   ├── PrivacyVault/
│   └── ...
├── Wave-2-Core/
│   ├── CareerCompanion/
│   ├── OpportunityNavigator/
│   └── ...
```

## 🔍 Finding Your Module

### By Functionality
- **Job/Career**: CareerCompanion (Wave 2)
- **Applications**: OpportunityNavigator (Wave 2)
- **Analytics/Reports**: InsightCompanion (Wave 2)
- **Games/Points**: MotivationEngine (Wave 2)
- **Login/Security**: PrivacyVault + TrustNetwork (Wave 1)
- **Admin**: SystemWisdom (Wave 1)
- **Onboarding**: WelcomeCompanion (Wave 1)
- **LinkedIn**: NetworkIntelligence (Wave 2)
- **Email**: CommunicationBridge (Wave 3)
- **UI/Theme**: ExperienceDesigner (Wave 3)

### By Old Module Number
Just remove the number and look for the descriptive name:
- Had number 2.x? → Check Wave 2
- Had number 3.x? → Check Wave 3
- Had number 1.x? → Check Wave 1

## ⚠️ Breaking Changes

### Consolidated Modules
These old modules no longer exist separately:
- All analytics modules → InsightCompanion
- All gamification modules → MotivationEngine
- All onboarding modules → WelcomeCompanion
- All networking modules → NetworkIntelligence

### Deprecated Patterns
```php
// ❌ Don't use module numbers
$module = '2.1-JobTracking';

// ✅ Use module names
$module = 'CareerCompanion';

// ❌ Don't use category paths
require_once '/modules/2.x-Features/module.php';

// ✅ Use wave paths
require_once '/modules/Wave-2-Core/module.php';
```

## 📚 Resources

### Documentation
- Full reorganization plan: `AI-FIRST-MODULE-REORGANIZATION-PLAN.md`
- Naming standard: `AI-FIRST-MODULE-HIERARCHY-STANDARD.md`
- Module registry: `MODULE_REGISTRY.yaml`

### Migration Tools
```bash
# Find old module references
grep -r "2\.1-JobTracking" .

# Update imports (example)
find . -name "*.php" -exec sed -i 's/2\.1-JobTracking/CareerCompanion/g' {} \;

# Validate module names
./scripts/validate-module-reference.sh "CareerCompanion"
```

## 🆘 Need Help?

1. **Can't find a module?** Check `MODULE_REGISTRY.yaml`
2. **Import errors?** Update to wave-based paths
3. **Missing functionality?** Module was likely consolidated
4. **Story mapping?** Check module's `manifest.yaml`

---

**Remember**: All modules now have AI-First conversational names. No more numbers!

*Quick tip: If you remember the old number, just look for a descriptive name that matches what that module did.*