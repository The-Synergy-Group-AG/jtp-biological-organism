<?php
/**
 * System Wisdom Conversation - Presentation Layer
 * 
 * Pure conversational interface for system management
 */

namespace JTP\Modules\SystemWisdom\Presentation;

use JTP\Modules\SystemWisdom\Application\SystemWisdomService;

class SystemWisdomConversation {
    private SystemWisdomService $service;
    
    public function __construct(SystemWisdomService $service) {
        $this->service = $service;
    }
    
    /**
     * Handle system conversation through natural language
     */
    public function converse(string $message, string $userId): array {
        // Process the conversation
        $response = $this->service->handleSystemConversation($message, $userId);
        
        // Format for conversational UI
        return [
            'type' => 'system_wisdom',
            'response' => $response['response'],
            'visualizations' => $this->createVisualizations($response),
            'proactive_insights' => $response['proactive_insights'] ?? [],
            'conversation_style' => 'technical_friendly',
            'follow_up_prompts' => $this->generateFollowUpPrompts($response)
        ];
    }
    
    /**
     * Proactive system insights
     */
    public function getProactiveInsights(string $userId): array {
        $insights = $this->service->generateSystemInsights();
        
        return [
            'type' => 'proactive_system_insights',
            'greeting' => $this->createSystemGreeting(),
            'health_status' => $insights['health_narrative'],
            'performance_story' => $insights['performance_story'],
            'optimization_suggestions' => $this->formatOptimizationSuggestions($insights),
            'conversation_starters' => [
                "How's our system performance looking today?",
                "Any optimizations you'd recommend?",
                "What can we do to improve system health?",
                "Show me the performance trends"
            ]
        ];
    }
    
    /**
     * System optimization conversation
     */
    public function discussOptimization(string $userId): array {
        $optimizations = $this->service->optimizeProactively();
        
        if (empty($optimizations['optimizations_applied'])) {
            return [
                'type' => 'optimization_status',
                'message' => "Your system is already running optimally! 🎯",
                'details' => "I'm continuously monitoring for optimization opportunities.",
                'metrics' => $this->getCurrentMetrics()
            ];
        }
        
        return [
            'type' => 'optimization_complete',
            'message' => "I've completed some optimizations for you",
            'optimizations' => $this->narrateOptimizations($optimizations['optimizations_applied']),
            'improvements' => $optimizations['system_improvements'],
            'next_steps' => "I'll keep monitoring and learning from these changes"
        ];
    }
    
    /**
     * Self-healing status conversation
     */
    public function discussSystemHealth(string $userId): array {
        $healing = $this->service->manageSelfHealing();
        
        if (!$healing['healing_performed']) {
            return [
                'type' => 'system_healthy',
                'message' => $healing['system_status'],
                'preventive_tips' => $healing['preventive_measures'],
                'confidence' => "Everything is running smoothly!"
            ];
        }
        
        return [
            'type' => 'healing_performed',
            'message' => "I've detected and resolved some issues",
            'details' => $healing['system_status'],
            'prevention' => $healing['prevention_activated'],
            'assurance' => "Your system is now stable and protected"
        ];
    }
    
    private function createVisualizations(array $response): array {
        $visuals = [];
        
        if (isset($response['performance_data'])) {
            $visuals[] = [
                'type' => 'performance_graph',
                'data' => $response['performance_data'],
                'description' => 'System performance over time'
            ];
        }
        
        if (isset($response['resource_usage'])) {
            $visuals[] = [
                'type' => 'resource_meter',
                'data' => $response['resource_usage'],
                'description' => 'Current resource utilization'
            ];
        }
        
        return $visuals;
    }
    
    private function generateFollowUpPrompts(array $response): array {
        $prompts = [];
        
        if (isset($response['optimization_opportunities'])) {
            $prompts[] = "Would you like me to optimize these areas?";
        }
        
        if (isset($response['performance_patterns'])) {
            $prompts[] = "Should I explain these performance patterns?";
        }
        
        $prompts[] = "Is there anything specific about the system you'd like to know?";
        
        return $prompts;
    }
    
    private function createSystemGreeting(): string {
        $greetings = [
            "Hello! I'm your System Wisdom AI, here to keep everything running smoothly.",
            "Hi there! Ready to discuss how your system is performing?",
            "Welcome! I've been monitoring your system and have some insights to share."
        ];
        
        return $greetings[array_rand($greetings)];
    }
    
    private function narrateOptimizations(array $optimizations): array {
        return array_map(function($opt) {
            return [
                'description' => $opt['narrative'],
                'impact' => $this->describeImpact($opt['result']),
                'visual' => $this->createOptimizationVisual($opt)
            ];
        }, $optimizations);
    }
}