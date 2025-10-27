<?php
/**
 * Community Conversation - Presentation Layer
 * 
 * Conversational interface for AI-driven community building
 */

namespace JTP\Modules\CommunityIntelligence\Presentation;

use JTP\Modules\CommunityIntelligence\Application\CommunityIntelligenceService;

class CommunityConversation {
    private CommunityIntelligenceService $service;
    
    public function __construct(CommunityIntelligenceService $service) {
        $this->service = $service;
    }
    
    /**
     * Connect with community members
     */
    public function findConnections(string $userId, string $message): array {
        $profile = $this->extractProfileFromMessage($message);
        $connections = $this->service->connectMembers($userId, $profile);
        
        return [
            'type' => 'connection_facilitation',
            'message' => $this->createConnectionNarrative($connections),
            'connections' => $this->formatConnections($connections['connection_opportunities']),
            'conversation_starters' => $this->provideConversationStarters($connections),
            'collaboration_ideas' => $connections['collaboration_ideas'],
            'next_prompt' => "Would you like me to introduce you to any of these people?"
        ];
    }
    
    /**
     * Start community discussion
     */
    public function initiateDiscussion(string $topic, string $userId): array {
        $participants = $this->identifyRelevantParticipants($topic, $userId);
        $discussion = $this->service->facilitateDiscussion($topic, $participants);
        
        return [
            'type' => 'discussion_facilitation',
            'opening_message' => $this->craftDiscussionOpening($topic, $discussion),
            'conversation_seeds' => $discussion['discussion_starters'],
            'engagement_tips' => $discussion['facilitator_guidance'],
            'value_focus' => $discussion['value_opportunities'],
            'participation_encouragement' => $this->encourageParticipation($discussion)
        ];
    }
    
    /**
     * Share community wisdom
     */
    public function exploreCommunityWisdom(string $query, string $userId): array {
        $wisdom = $this->service->generateCommunityWisdom();
        $relevantWisdom = $this->filterRelevantWisdom($wisdom, $query);
        
        return [
            'type' => 'community_wisdom',
            'wisdom_response' => $this->narrateWisdom($relevantWisdom),
            'success_examples' => $relevantWisdom['success_patterns'],
            'collective_insights' => $relevantWisdom['community_insights'],
            'actionable_advice' => $this->extractActionableAdvice($relevantWisdom),
            'explore_prompt' => "What aspect of community wisdom interests you most?"
        ];
    }
    
    /**
     * Request community support
     */
    public function seekSupport(string $userId, string $need): array {
        $activity = ['support_request' => $need, 'user_id' => $userId];
        $support = $this->service->provideSupportConnections($userId, $activity);
        
        return [
            'type' => 'support_connection',
            'support_message' => $this->createSupportNarrative($support),
            'support_options' => $this->formatSupportOptions($support),
            'mentorship_opportunities' => $support['mentorship_opportunities'],
            'peer_groups' => $this->describePeerGroups($support['peer_groups']),
            'encouragement' => "You're not alone - our community is here to help!"
        ];
    }
    
    /**
     * Ambassador development conversation
     */
    public function developAmbassadorSkills(string $userId): array {
        $activity = $this->getUserActivity($userId);
        $ambassadorPath = $this->service->developAmbassadors($userId, $activity);
        
        return [
            'type' => 'ambassador_development',
            'recognition_message' => $ambassadorPath['recognition'],
            'growth_opportunities' => $this->narrateGrowthPath($ambassadorPath),
            'impact_ideas' => $ambassadorPath['impact_opportunities'],
            'leadership_story' => $ambassadorPath['leadership_journey'],
            'motivation' => "Your contributions are making a real difference!"
        ];
    }
    
    /**
     * Community growth conversation
     */
    public function discussCommunityGrowth(string $adminId): array {
        $growth = $this->service->strategizeCommunityGrowth();
        
        return [
            'type' => 'growth_strategy',
            'growth_narrative' => $growth['growth_narrative'],
            'engagement_plan' => $this->visualizeEngagementPlan($growth['engagement_initiatives']),
            'value_enhancements' => $growth['value_enhancement'],
            'health_status' => $this->narrateHealthStatus($growth['health_dashboard']),
            'strategic_prompt' => "Which growth area should we focus on first?"
        ];
    }
    
    private function createConnectionNarrative(array $connections): string {
        if (empty($connections['connection_opportunities'])) {
            return "I'm still learning about potential connections for you. Tell me more about your interests and goals!";
        }
        
        $count = count($connections['connection_opportunities']);
        $narrative = "I've found {$count} community members who share your interests! ";
        
        $topConnection = $connections['connection_opportunities'][0];
        $narrative .= "For example, {$topConnection['connection']['display_name']} ";
        $narrative .= "shares your interest in {$topConnection['shared_interests'][0]}. ";
        
        return $narrative;
    }
    
    private function formatConnections(array $opportunities): array {
        return array_map(function($opp) {
            return [
                'member' => $opp['connection'],
                'introduction' => $opp['introduction_message'],
                'common_ground' => $opp['shared_interests'],
                'conversation_hooks' => $opp['conversation_starters'],
                'connection_value' => $opp['connection_value']
            ];
        }, array_slice($opportunities, 0, 5)); // Top 5 connections
    }
    
    private function craftDiscussionOpening(string $topic, array $discussion): string {
        $opening = "Let's explore '{$topic}' together! ";
        
        if (!empty($discussion['discussion_starters'])) {
            $starter = $discussion['discussion_starters'][0];
            $opening .= $starter['thought_provokers'][0] . " ";
        }
        
        $opening .= "I'm excited to hear everyone's perspectives on this.";
        
        return $opening;
    }
    
    private function narrateWisdom(array $wisdom): string {
        $narrative = "Our community has discovered some powerful insights. ";
        
        if (!empty($wisdom['community_insights'])) {
            $topInsight = $wisdom['community_insights'][0];
            $narrative .= $topInsight['story'] . " ";
        }
        
        $narrative .= "These patterns have helped many members succeed.";
        
        return $narrative;
    }
}