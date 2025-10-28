<?php
/**
 * Learning Conversation Interface - Presentation Layer
 * 
 * Natural conversation interface that implicitly gathers feedback
 */

namespace JTP\Modules\LearningConversations\Presentation;

use JTP\Modules\LearningConversations\Application\LearningConversationService;

class LearningConversationInterface {
    private LearningConversationService $service;
    
    public function __construct(LearningConversationService $service) {
        $this->service = $service;
    }
    
    /**
     * Handle user message with implicit learning
     */
    public function chat(string $message, string $userId, array $context): array {
        // Process with implicit feedback extraction
        $response = $this->service->processConversation($message, $userId, $context);
        
        // Natural conversation response
        return [
            'type' => 'natural_conversation',
            'message' => $response['response'],
            'follow_up' => $response['follow_up_questions'] ?? null,
            'value_tips' => $this->extractValueTips($response),
            'conversation_flow' => 'natural',
            'learning_active' => !($response['learning_disabled'] ?? false)
        ];
    }
    
    /**
     * Proactive conversation initiation
     */
    public function checkForConversationOpportunity(string $userId, array $behavior): array {
        $opportunity = $this->service->initiateConversation($userId, $behavior);
        
        if (!$opportunity['initiate']) {
            return ['initiate' => false];
        }
        
        return [
            'type' => 'proactive_conversation',
            'initiate' => true,
            'message' => $opportunity['message'],
            'purpose' => 'helpful_check_in',
            'expected_value' => $opportunity['expected_value'],
            'style' => $this->determineConversationStyle($behavior)
        ];
    }
    
    /**
     * Show conversation insights (admin view)
     */
    public function getConversationInsights(string $adminId): array {
        $insights = $this->service->synthesizeInsights('week');
        
        return [
            'type' => 'conversation_insights',
            'narrative' => $this->createInsightsNarrative($insights),
            'key_themes' => $this->visualizeThemes($insights['key_insights']),
            'action_plan' => $this->formatActionPlan($insights['priority_actions']),
            'impact_preview' => $insights['user_impact'],
            'conversation_prompt' => "Would you like me to explain any of these insights?"
        ];
    }
    
    /**
     * Personalized conversation patterns
     */
    public function adaptConversationStyle(string $userId): array {
        $patterns = $this->service->analyzeConversationPatterns($userId);
        
        return [
            'type' => 'conversation_adaptation',
            'adapted_style' => $patterns['conversation_style'],
            'understanding' => "I've noticed you prefer " . $this->describeStyle($patterns['conversation_style']),
            'improvements' => $this->suggestImprovements($patterns['pain_points']),
            'personalization_active' => $patterns['personalization_applied']
        ];
    }
    
    /**
     * Conversation quality dashboard
     */
    public function showConversationQuality(): array {
        $quality = $this->service->assessConversationQuality();
        
        return [
            'type' => 'quality_dashboard',
            'overall_score' => $quality['overall_quality'],
            'narrative' => $this->createQualityNarrative($quality),
            'success_stories' => $this->highlightSuccesses($quality['success_patterns']),
            'improvement_focus' => $this->prioritizeImprovements($quality['improvement_areas']),
            'optimization_ready' => $quality['optimization_suggestions']
        ];
    }
    
    private function extractValueTips(array $response): ?array {
        if (!isset($response['value_delivery'])) {
            return null;
        }
        
        return [
            'tip' => $response['value_delivery']['tip'],
            'relevance' => $response['value_delivery']['relevance'],
            'timing' => 'contextual'
        ];
    }
    
    private function determineConversationStyle(array $behavior): string {
        // Analyze behavior to determine best approach
        if ($this->detectsStruggle($behavior)) {
            return 'supportive_helpful';
        }
        
        if ($this->detectsSuccess($behavior)) {
            return 'celebratory_encouraging';
        }
        
        return 'friendly_curious';
    }
    
    private function createInsightsNarrative(array $insights): string {
        $narrative = "Based on this week's conversations, I've discovered some interesting patterns. ";
        
        if (!empty($insights['key_insights'])) {
            $topTheme = $insights['key_insights'][0];
            $narrative .= "The most common theme was around {$topTheme['theme']}, ";
            $narrative .= "which came up in {$topTheme['frequency']} conversations. ";
        }
        
        $narrative .= "Here's what I learned and how we can improve the experience...";
        
        return $narrative;
    }
    
    private function visualizeThemes(array $themes): array {
        return array_map(function($theme) {
            return [
                'theme' => $theme['theme'],
                'frequency' => $theme['frequency'],
                'sentiment' => $theme['average_sentiment'],
                'impact_score' => $theme['potential_impact'],
                'visual_representation' => $this->createThemeVisual($theme)
            ];
        }, $themes);
    }
    
    private function createQualityNarrative(array $quality): string {
        $score = $quality['overall_quality'];
        
        if ($score > 0.8) {
            return "Our conversations are creating great value! Users are engaged and we're learning valuable insights.";
        } elseif ($score > 0.6) {
            return "Conversations are going well, with some opportunities to increase value and gather deeper insights.";
        } else {
            return "There's significant room to improve our conversation quality and the value we provide.";
        }
    }
}