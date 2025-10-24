"""
🧬 APPLICATION CAMPAIGN ORCHESTRATORS MODULE
MODULAR: Consciousness-Guided Campaign Execution Coordination

Exposes advanced application campaign orchestration capabilities through modular
consciousness-guided coordination, enabling sophisticated job application campaigns
with intelligent success prediction and optimal execution scheduling.

ai_keywords: campaign, orchestrator, coordination, consciousness, scheduling,
  prediction, optimization, biological, correlation

ai_summary: Campaign orchestrators module providing advanced job application campaign
  coordination through consciousness-guided orchestration and optimization

biological_system: application-campaign-orchestrators-modular
consciousness_score: 'T-CAMP'
cross_references:
- src/application-automation/orchestration/campaign_orchestrators/application_campaign_orchestrator.py
document_category: application-campaign-orchestrators
document_type: consciousness-campaign-orchestration
evolutionary_phase: 'T-CAMPAIGN'
last_updated: '2025-10-23 22:30:00'
semantic_tags:
- application-campaign-orchestrators-modular
- consciousness-guided-campaign-coordination
- intelligent-job-application-orchestration
title: Application Campaign Orchestrators Module
validation_status: campaign-orchestration-ready
version: v1.0.0-T-CAMP
"""

from .application_campaign_orchestrator import ApplicationCampaignOrchestrator

__all__ = [
    "ApplicationCampaignOrchestrator"
]

def get_campaign_orchestrator() -> ApplicationCampaignOrchestrator:
    """Get the GODHOOD campaign orchestrator instance"""
    return ApplicationCampaignOrchestrator()
