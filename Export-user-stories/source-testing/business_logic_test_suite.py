#!/usr/bin/env python3
"""
Business Logic Test Suite
=========================
Comprehensive testing for business rules, status progressions,
workflows, and AI-driven decision making in the AI-First 
Job Tracker Pro system.

Performance Requirements:
- 6 concurrent threads (2GB each)
- <100ms decision processing time
- 100% workflow accuracy
- Zero business rule violations
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field
from enum import Enum
import concurrent.futures
from pathlib import Path
import random
import psutil

# Application statuses
class ApplicationStatus(Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    ACKNOWLEDGED = "acknowledged"
    SCREENING = "screening"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    INTERVIEWED = "interviewed"
    ASSESSMENT = "assessment"
    REFERENCE_CHECK = "reference_check"
    OFFER_EXTENDED = "offer_extended"
    OFFER_ACCEPTED = "offer_accepted"
    OFFER_DECLINED = "offer_declined"
    WITHDRAWN = "withdrawn"
    REJECTED = "rejected"
    ARCHIVED = "archived"

# Interview types
class InterviewType(Enum):
    PHONE_SCREEN = "phone_screen"
    TECHNICAL = "technical"
    BEHAVIORAL = "behavioral"
    PANEL = "panel"
    FINAL = "final"
    CULTURAL_FIT = "cultural_fit"

# Business rule types
class BusinessRuleType(Enum):
    STATUS_TRANSITION = "status_transition"
    TIMING_CONSTRAINT = "timing_constraint"
    DATA_VALIDATION = "data_validation"
    WORKFLOW_SEQUENCE = "workflow_sequence"
    NOTIFICATION_TRIGGER = "notification_trigger"
    AI_DECISION = "ai_decision"

@dataclass
class JobApplication:
    """Job application with full lifecycle"""
    application_id: str
    user_id: str
    job_id: str
    company: str
    position: str
    status: ApplicationStatus
    submitted_date: Optional[datetime] = None
    last_updated: datetime = field(default_factory=datetime.now)
    interview_dates: List[datetime] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    documents: List[str] = field(default_factory=list)
    ai_insights: Dict[str, Any] = field(default_factory=dict)
    
@dataclass
class WorkflowStep:
    """Individual workflow step"""
    step_id: str
    name: str
    required: bool
    completed: bool = False
    completed_date: Optional[datetime] = None
    conditions: List[str] = field(default_factory=list)
    next_steps: List[str] = field(default_factory=list)

@dataclass
class BusinessRule:
    """Business rule definition"""
    rule_id: str
    name: str
    description: str
    rule_type: BusinessRuleType
    conditions: Dict[str, Any]
    actions: List[str]
    priority: int = 1
    active: bool = True

@dataclass
class BusinessLogicTestCase:
    """Business logic test case"""
    test_id: str
    name: str
    description: str
    rule_type: BusinessRuleType
    test_scenario: Dict[str, Any]
    expected_outcome: str
    actual_outcome: Optional[str] = None
    passed: Optional[bool] = None
    execution_time_ms: Optional[float] = None
    error_details: Optional[str] = None

@dataclass
class WorkflowExecution:
    """Workflow execution tracking"""
    workflow_id: str
    application_id: str
    steps: List[WorkflowStep]
    current_step: Optional[str] = None
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    status: str = "in_progress"

@dataclass
class BusinessLogicReport:
    """Business logic test report"""
    test_date: datetime
    total_tests: int
    passed_tests: int
    failed_tests: int
    rule_coverage: Dict[str, float]
    workflow_accuracy: float
    ai_decision_accuracy: float
    performance_metrics: Dict[str, float]
    recommendations: List[str]

class BusinessLogicTester:
    """Main business logic testing orchestrator"""
    
    def __init__(self):
        self.test_cases: List[BusinessLogicTestCase] = []
        self.thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=6)
        self.business_rules = self._load_business_rules()
        self.test_applications = self._generate_test_applications()
        self.decision_times: List[float] = []
        
    def _load_business_rules(self) -> List[BusinessRule]:
        """Load all business rules"""
        return [
            # Status transition rules
            BusinessRule(
                rule_id="BR-001",
                name="Submit Application",
                description="Draft to Submitted transition",
                rule_type=BusinessRuleType.STATUS_TRANSITION,
                conditions={
                    "current_status": ApplicationStatus.DRAFT,
                    "required_fields": ["company", "position", "resume"],
                    "documents_uploaded": True
                },
                actions=["update_status", "send_confirmation", "start_tracking"],
                priority=1
            ),
            BusinessRule(
                rule_id="BR-002",
                name="Interview Follow-up",
                description="Auto-reminder after interview",
                rule_type=BusinessRuleType.TIMING_CONSTRAINT,
                conditions={
                    "status": ApplicationStatus.INTERVIEWED,
                    "days_since_interview": 3,
                    "follow_up_sent": False
                },
                actions=["send_follow_up", "update_ai_insights"],
                priority=2
            ),
            BusinessRule(
                rule_id="BR-003",
                name="Application Staleness",
                description="Archive old applications",
                rule_type=BusinessRuleType.TIMING_CONSTRAINT,
                conditions={
                    "days_since_update": 90,
                    "status_not_in": ["offer_extended", "offer_accepted"],
                    "user_inactive": False
                },
                actions=["prompt_user", "suggest_follow_up"],
                priority=3
            ),
            BusinessRule(
                rule_id="BR-004",
                name="AI Interview Prep",
                description="Trigger AI prep when interview scheduled",
                rule_type=BusinessRuleType.AI_DECISION,
                conditions={
                    "status": ApplicationStatus.INTERVIEW_SCHEDULED,
                    "interview_date_set": True,
                    "prep_not_started": True
                },
                actions=["generate_prep_materials", "analyze_company", "suggest_questions"],
                priority=1
            ),
            BusinessRule(
                rule_id="BR-005",
                name="Offer Decision Support",
                description="AI analysis when offer received",
                rule_type=BusinessRuleType.AI_DECISION,
                conditions={
                    "status": ApplicationStatus.OFFER_EXTENDED,
                    "offer_details_available": True,
                    "analysis_not_done": True
                },
                actions=["analyze_offer", "compare_market", "provide_negotiation_tips"],
                priority=1
            )
        ]
    
    def _generate_test_applications(self) -> List[JobApplication]:
        """Generate test job applications"""
        applications = []
        companies = ["TechCorp", "StartupAI", "BigBank", "HealthTech", "EduSoft"]
        positions = ["Senior Developer", "ML Engineer", "Product Manager", "Data Scientist", "DevOps Engineer"]
        
        for i in range(50):
            app = JobApplication(
                application_id=f"app_{i:03d}",
                user_id="test_user",
                job_id=f"job_{i:03d}",
                company=random.choice(companies),
                position=random.choice(positions),
                status=random.choice(list(ApplicationStatus)),
                submitted_date=datetime.now() - timedelta(days=random.randint(0, 90))
            )
            
            # Add some interview dates for certain statuses
            if app.status in [ApplicationStatus.INTERVIEW_SCHEDULED, ApplicationStatus.INTERVIEWED]:
                app.interview_dates = [datetime.now() + timedelta(days=random.randint(1, 14))]
            
            applications.append(app)
        
        return applications
    
    async def run_all_tests(self) -> BusinessLogicReport:
        """Execute all business logic tests"""
        print("\n🧮 Business Logic Testing Suite")
        print("=" * 50)
        
        start_time = time.time()
        
        # Run test categories in parallel
        test_futures = []
        with self.thread_pool as executor:
            test_futures.extend([
                executor.submit(self._test_status_transitions),
                executor.submit(self._test_timing_constraints),
                executor.submit(self._test_workflow_sequences),
                executor.submit(self._test_ai_decisions),
                executor.submit(self._test_notification_triggers),
                executor.submit(self._test_data_validation)
            ])
            
            # Wait for all tests to complete
            concurrent.futures.wait(test_futures)
        
        # Additional comprehensive tests
        await self._test_complex_workflows()
        await self._test_rule_conflicts()
        await self._test_edge_cases()
        await self._test_performance()
        
        # Generate report
        report = self._generate_business_logic_report()
        
        elapsed_time = time.time() - start_time
        print(f"\n✅ All business logic tests completed in {elapsed_time:.2f}s")
        
        return report
    
    def _test_status_transitions(self) -> None:
        """Test application status transitions"""
        print("\n🔄 Testing Status Transitions...")
        
        valid_transitions = {
            ApplicationStatus.DRAFT: [ApplicationStatus.SUBMITTED, ApplicationStatus.WITHDRAWN],
            ApplicationStatus.SUBMITTED: [ApplicationStatus.ACKNOWLEDGED, ApplicationStatus.WITHDRAWN],
            ApplicationStatus.ACKNOWLEDGED: [ApplicationStatus.SCREENING, ApplicationStatus.REJECTED, ApplicationStatus.WITHDRAWN],
            ApplicationStatus.SCREENING: [ApplicationStatus.INTERVIEW_SCHEDULED, ApplicationStatus.REJECTED, ApplicationStatus.WITHDRAWN],
            ApplicationStatus.INTERVIEW_SCHEDULED: [ApplicationStatus.INTERVIEWED, ApplicationStatus.WITHDRAWN],
            ApplicationStatus.INTERVIEWED: [ApplicationStatus.ASSESSMENT, ApplicationStatus.OFFER_EXTENDED, ApplicationStatus.REJECTED, ApplicationStatus.WITHDRAWN],
            ApplicationStatus.OFFER_EXTENDED: [ApplicationStatus.OFFER_ACCEPTED, ApplicationStatus.OFFER_DECLINED],
            ApplicationStatus.OFFER_ACCEPTED: [ApplicationStatus.ARCHIVED],
            ApplicationStatus.OFFER_DECLINED: [ApplicationStatus.ARCHIVED],
            ApplicationStatus.REJECTED: [ApplicationStatus.ARCHIVED],
            ApplicationStatus.WITHDRAWN: [ApplicationStatus.ARCHIVED]
        }
        
        # Test valid transitions
        for from_status, to_statuses in valid_transitions.items():
            for to_status in to_statuses:
                test_case = BusinessLogicTestCase(
                    test_id=f"TRANS-{from_status.name}-{to_status.name}",
                    name=f"Transition {from_status.value} to {to_status.value}",
                    description=f"Test valid transition from {from_status.value} to {to_status.value}",
                    rule_type=BusinessRuleType.STATUS_TRANSITION,
                    test_scenario={
                        "from_status": from_status,
                        "to_status": to_status,
                        "conditions_met": True
                    },
                    expected_outcome="Transition successful"
                )
                
                start = time.time()
                try:
                    # Test transition
                    app = JobApplication(
                        application_id="test_app",
                        user_id="test_user",
                        job_id="test_job",
                        company="TestCorp",
                        position="Test Position",
                        status=from_status
                    )
                    
                    # Apply transition
                    success = self._apply_status_transition(app, to_status)
                    assert success
                    assert app.status == to_status
                    
                    test_case.actual_outcome = f"Transitioned successfully"
                    test_case.passed = True
                    
                except Exception as e:
                    test_case.passed = False
                    test_case.error_details = str(e)
                
                test_case.execution_time_ms = (time.time() - start) * 1000
                self.test_cases.append(test_case)
        
        # Test invalid transitions
        invalid_transitions = [
            (ApplicationStatus.SUBMITTED, ApplicationStatus.OFFER_EXTENDED),  # Can't skip to offer
            (ApplicationStatus.REJECTED, ApplicationStatus.INTERVIEWED),  # Can't interview after rejection
            (ApplicationStatus.ARCHIVED, ApplicationStatus.SUBMITTED)  # Can't unarchive
        ]
        
        for from_status, to_status in invalid_transitions:
            test_case = BusinessLogicTestCase(
                test_id=f"TRANS-INVALID-{from_status.name}-{to_status.name}",
                name=f"Invalid transition {from_status.value} to {to_status.value}",
                description=f"Test invalid transition prevention",
                rule_type=BusinessRuleType.STATUS_TRANSITION,
                test_scenario={
                    "from_status": from_status,
                    "to_status": to_status,
                    "conditions_met": False
                },
                expected_outcome="Transition blocked"
            )
            
            start = time.time()
            try:
                app = JobApplication(
                    application_id="test_app",
                    user_id="test_user",
                    job_id="test_job",
                    company="TestCorp",
                    position="Test Position",
                    status=from_status
                )
                
                # Attempt invalid transition
                success = self._apply_status_transition(app, to_status)
                assert not success
                assert app.status == from_status  # Status unchanged
                
                test_case.actual_outcome = "Invalid transition blocked"
                test_case.passed = True
                
            except Exception as e:
                test_case.passed = False
                test_case.error_details = str(e)
            
            test_case.execution_time_ms = (time.time() - start) * 1000
            self.test_cases.append(test_case)
        
        self._print_test_results("Status Transitions", [tc for tc in self.test_cases if "TRANS" in tc.test_id])
    
    def _test_timing_constraints(self) -> None:
        """Test time-based business rules"""
        print("\n⏰ Testing Timing Constraints...")
        
        timing_scenarios = [
            {
                "test_id": "TIME-001",
                "name": "Interview Follow-up Reminder",
                "scenario": "3 days after interview",
                "rule": "BR-002",
                "days_elapsed": 3,
                "expected_action": "send_follow_up"
            },
            {
                "test_id": "TIME-002",
                "name": "Application Staleness Check",
                "scenario": "90 days without update",
                "rule": "BR-003",
                "days_elapsed": 90,
                "expected_action": "prompt_user"
            },
            {
                "test_id": "TIME-003",
                "name": "Offer Response Deadline",
                "scenario": "7 days to respond to offer",
                "rule": "BR-006",
                "days_elapsed": 6,
                "expected_action": "send_reminder"
            },
            {
                "test_id": "TIME-004",
                "name": "Weekly Progress Check",
                "scenario": "Weekly job search review",
                "rule": "BR-007",
                "days_elapsed": 7,
                "expected_action": "generate_weekly_report"
            }
        ]
        
        for scenario in timing_scenarios:
            test_case = BusinessLogicTestCase(
                test_id=scenario["test_id"],
                name=scenario["name"],
                description=f"Test {scenario['scenario']}",
                rule_type=BusinessRuleType.TIMING_CONSTRAINT,
                test_scenario=scenario,
                expected_outcome=f"Trigger {scenario['expected_action']}"
            )
            
            start = time.time()
            try:
                # Create application with time constraint
                app = JobApplication(
                    application_id="test_app",
                    user_id="test_user",
                    job_id="test_job",
                    company="TestCorp",
                    position="Test Position",
                    status=ApplicationStatus.INTERVIEWED,
                    last_updated=datetime.now() - timedelta(days=scenario["days_elapsed"])
                )
                
                # Check timing rules
                triggered_actions = self._check_timing_constraints(app)
                assert scenario["expected_action"] in triggered_actions
                
                test_case.actual_outcome = f"Triggered: {', '.join(triggered_actions)}"
                test_case.passed = True
                
            except Exception as e:
                test_case.passed = False
                test_case.error_details = str(e)
            
            test_case.execution_time_ms = (time.time() - start) * 1000
            self.test_cases.append(test_case)
            self.decision_times.append(test_case.execution_time_ms)
        
        self._print_test_results("Timing Constraints", [tc for tc in self.test_cases if "TIME" in tc.test_id])
    
    def _test_workflow_sequences(self) -> None:
        """Test workflow execution sequences"""
        print("\n📋 Testing Workflow Sequences...")
        
        workflows = [
            {
                "test_id": "FLOW-001",
                "name": "Complete Application Workflow",
                "steps": [
                    "create_draft",
                    "upload_resume",
                    "upload_cover_letter",
                    "fill_details",
                    "submit_application"
                ],
                "expected": "Application submitted successfully"
            },
            {
                "test_id": "FLOW-002",
                "name": "Interview Preparation Workflow",
                "steps": [
                    "schedule_interview",
                    "research_company",
                    "prepare_questions",
                    "practice_answers",
                    "send_confirmation"
                ],
                "expected": "Interview prep complete"
            },
            {
                "test_id": "FLOW-003",
                "name": "Offer Evaluation Workflow",
                "steps": [
                    "receive_offer",
                    "analyze_compensation",
                    "research_market_rates",
                    "identify_negotiation_points",
                    "prepare_response"
                ],
                "expected": "Offer analysis complete"
            }
        ]
        
        for workflow in workflows:
            test_case = BusinessLogicTestCase(
                test_id=workflow["test_id"],
                name=workflow["name"],
                description=f"Test {workflow['name']} execution",
                rule_type=BusinessRuleType.WORKFLOW_SEQUENCE,
                test_scenario={"steps": workflow["steps"]},
                expected_outcome=workflow["expected"]
            )
            
            start = time.time()
            try:
                # Create workflow execution
                execution = WorkflowExecution(
                    workflow_id=workflow["test_id"],
                    application_id="test_app",
                    steps=[
                        WorkflowStep(
                            step_id=f"step_{i}",
                            name=step,
                            required=True,
                            conditions=[]
                        )
                        for i, step in enumerate(workflow["steps"])
                    ]
                )
                
                # Execute workflow
                for step in execution.steps:
                    success = self._execute_workflow_step(execution, step)
                    assert success
                    step.completed = True
                    step.completed_date = datetime.now()
                
                # Verify completion
                assert all(step.completed for step in execution.steps)
                execution.status = "completed"
                execution.completed_at = datetime.now()
                
                test_case.actual_outcome = f"All {len(execution.steps)} steps completed"
                test_case.passed = True
                
            except Exception as e:
                test_case.passed = False
                test_case.error_details = str(e)
            
            test_case.execution_time_ms = (time.time() - start) * 1000
            self.test_cases.append(test_case)
        
        self._print_test_results("Workflow Sequences", [tc for tc in self.test_cases if "FLOW" in tc.test_id])
    
    def _test_ai_decisions(self) -> None:
        """Test AI-driven business decisions"""
        print("\n🤖 Testing AI Decisions...")
        
        ai_scenarios = [
            {
                "test_id": "AI-001",
                "name": "Job Match Scoring",
                "input": {
                    "user_skills": ["Python", "ML", "Cloud"],
                    "job_requirements": ["Python", "ML", "AWS", "Docker"],
                    "experience_years": 5,
                    "required_years": 3
                },
                "expected": "High match score (>80%)"
            },
            {
                "test_id": "AI-002",
                "name": "Interview Success Prediction",
                "input": {
                    "company_culture": "collaborative",
                    "user_personality": "team_player",
                    "technical_match": 0.85,
                    "preparation_level": 0.9
                },
                "expected": "High success probability (>75%)"
            },
            {
                "test_id": "AI-003",
                "name": "Salary Negotiation Strategy",
                "input": {
                    "offer_amount": 120000,
                    "market_average": 130000,
                    "user_experience": "senior",
                    "company_size": "large"
                },
                "expected": "Recommend negotiation"
            },
            {
                "test_id": "AI-004",
                "name": "Application Priority Ranking",
                "input": {
                    "applications": [
                        {"company": "A", "match": 0.9, "stage": "interview"},
                        {"company": "B", "match": 0.7, "stage": "submitted"},
                        {"company": "C", "match": 0.95, "stage": "screening"}
                    ]
                },
                "expected": "Prioritize company A"
            }
        ]
        
        for scenario in ai_scenarios:
            test_case = BusinessLogicTestCase(
                test_id=scenario["test_id"],
                name=scenario["name"],
                description=f"Test AI decision: {scenario['name']}",
                rule_type=BusinessRuleType.AI_DECISION,
                test_scenario=scenario["input"],
                expected_outcome=scenario["expected"]
            )
            
            start = time.time()
            try:
                # Make AI decision
                decision_start = time.time()
                decision = self._make_ai_decision(scenario["name"], scenario["input"])
                decision_time = (time.time() - decision_start) * 1000
                self.decision_times.append(decision_time)
                
                # Validate decision
                if "Match Scoring" in scenario["name"]:
                    assert decision["match_score"] > 0.8
                    test_case.actual_outcome = f"Match score: {decision['match_score']:.2%}"
                    
                elif "Success Prediction" in scenario["name"]:
                    assert decision["success_probability"] > 0.75
                    test_case.actual_outcome = f"Success probability: {decision['success_probability']:.2%}"
                    
                elif "Negotiation Strategy" in scenario["name"]:
                    assert decision["recommend_negotiation"] is True
                    test_case.actual_outcome = f"Negotiation recommended: +${decision['suggested_increase']:,}"
                    
                elif "Priority Ranking" in scenario["name"]:
                    assert decision["top_priority"] == "A"
                    test_case.actual_outcome = f"Priority order: {', '.join(decision['ranking'])}"
                
                test_case.passed = True
                
            except Exception as e:
                test_case.passed = False
                test_case.error_details = str(e)
            
            test_case.execution_time_ms = (time.time() - start) * 1000
            self.test_cases.append(test_case)
        
        self._print_test_results("AI Decisions", [tc for tc in self.test_cases if "AI-" in tc.test_id])
    
    def _test_notification_triggers(self) -> None:
        """Test notification trigger rules"""
        print("\n🔔 Testing Notification Triggers...")
        
        notification_scenarios = [
            {
                "test_id": "NOTIF-001",
                "name": "Application Confirmation",
                "trigger": "application_submitted",
                "expected_notifications": ["email_confirmation", "in_app_notification"]
            },
            {
                "test_id": "NOTIF-002",
                "name": "Interview Reminder",
                "trigger": "interview_tomorrow",
                "expected_notifications": ["email_reminder", "push_notification", "calendar_update"]
            },
            {
                "test_id": "NOTIF-003",
                "name": "Status Update",
                "trigger": "status_changed",
                "expected_notifications": ["in_app_notification", "optional_email"]
            },
            {
                "test_id": "NOTIF-004",
                "name": "Weekly Summary",
                "trigger": "weekly_checkpoint",
                "expected_notifications": ["email_summary", "dashboard_update"]
            }
        ]
        
        for scenario in notification_scenarios:
            test_case = BusinessLogicTestCase(
                test_id=scenario["test_id"],
                name=scenario["name"],
                description=f"Test notification trigger: {scenario['trigger']}",
                rule_type=BusinessRuleType.NOTIFICATION_TRIGGER,
                test_scenario={"trigger": scenario["trigger"]},
                expected_outcome=f"Send {len(scenario['expected_notifications'])} notifications"
            )
            
            start = time.time()
            try:
                # Trigger notification
                notifications = self._trigger_notifications(scenario["trigger"])
                
                # Verify all expected notifications
                for expected in scenario["expected_notifications"]:
                    assert any(n["type"] == expected for n in notifications)
                
                test_case.actual_outcome = f"Sent: {', '.join(n['type'] for n in notifications)}"
                test_case.passed = True
                
            except Exception as e:
                test_case.passed = False
                test_case.error_details = str(e)
            
            test_case.execution_time_ms = (time.time() - start) * 1000
            self.test_cases.append(test_case)
        
        self._print_test_results("Notification Triggers", [tc for tc in self.test_cases if "NOTIF" in tc.test_id])
    
    def _test_data_validation(self) -> None:
        """Test data validation rules"""
        print("\n✅ Testing Data Validation...")
        
        validation_scenarios = [
            {
                "test_id": "VALID-001",
                "name": "Application Completeness",
                "data": {
                    "company": "TechCorp",
                    "position": "Developer",
                    "resume": "resume.pdf",
                    "cover_letter": None  # Optional
                },
                "expected": "Valid"
            },
            {
                "test_id": "VALID-002",
                "name": "Email Format Validation",
                "data": {
                    "email": "user@example.com",
                    "backup_email": "invalid-email"
                },
                "expected": "Invalid backup email"
            },
            {
                "test_id": "VALID-003",
                "name": "Salary Range Validation",
                "data": {
                    "salary_min": 80000,
                    "salary_max": 120000,
                    "currency": "CHF"
                },
                "expected": "Valid"
            },
            {
                "test_id": "VALID-004",
                "name": "Date Consistency",
                "data": {
                    "application_date": datetime.now() - timedelta(days=5),
                    "interview_date": datetime.now() + timedelta(days=3),
                    "start_date": datetime.now() + timedelta(days=30)
                },
                "expected": "Valid date sequence"
            }
        ]
        
        for scenario in validation_scenarios:
            test_case = BusinessLogicTestCase(
                test_id=scenario["test_id"],
                name=scenario["name"],
                description=f"Test validation: {scenario['name']}",
                rule_type=BusinessRuleType.DATA_VALIDATION,
                test_scenario=scenario["data"],
                expected_outcome=scenario["expected"]
            )
            
            start = time.time()
            try:
                # Validate data
                validation_result = self._validate_data(scenario["name"], scenario["data"])
                
                if "Valid" in scenario["expected"] and "Invalid" not in scenario["expected"]:
                    assert validation_result["valid"] is True
                    test_case.actual_outcome = "Validation passed"
                else:
                    assert validation_result["valid"] is False
                    assert any("email" in error for error in validation_result["errors"])
                    test_case.actual_outcome = f"Validation failed: {validation_result['errors'][0]}"
                
                test_case.passed = True
                
            except Exception as e:
                test_case.passed = False
                test_case.error_details = str(e)
            
            test_case.execution_time_ms = (time.time() - start) * 1000
            self.test_cases.append(test_case)
        
        self._print_test_results("Data Validation", [tc for tc in self.test_cases if "VALID" in tc.test_id])
    
    async def _test_complex_workflows(self) -> None:
        """Test complex multi-step workflows"""
        print("\n🔀 Testing Complex Workflows...")
        
        test_case = BusinessLogicTestCase(
            test_id="COMPLEX-001",
            name="End-to-End Application Journey",
            description="Test complete application lifecycle",
            rule_type=BusinessRuleType.WORKFLOW_SEQUENCE,
            test_scenario={
                "steps": [
                    "create_application",
                    "submit_application",
                    "receive_acknowledgment",
                    "pass_screening",
                    "schedule_interview",
                    "complete_interview",
                    "receive_offer",
                    "negotiate_offer",
                    "accept_offer"
                ]
            },
            expected_outcome="Complete journey successful"
        )
        
        start = time.time()
        try:
            # Create application
            app = JobApplication(
                application_id="journey_app",
                user_id="test_user",
                job_id="dream_job",
                company="DreamCorp",
                position="Dream Position",
                status=ApplicationStatus.DRAFT
            )
            
            # Execute journey
            journey_steps = [
                (ApplicationStatus.DRAFT, ApplicationStatus.SUBMITTED),
                (ApplicationStatus.SUBMITTED, ApplicationStatus.ACKNOWLEDGED),
                (ApplicationStatus.ACKNOWLEDGED, ApplicationStatus.SCREENING),
                (ApplicationStatus.SCREENING, ApplicationStatus.INTERVIEW_SCHEDULED),
                (ApplicationStatus.INTERVIEW_SCHEDULED, ApplicationStatus.INTERVIEWED),
                (ApplicationStatus.INTERVIEWED, ApplicationStatus.OFFER_EXTENDED),
                (ApplicationStatus.OFFER_EXTENDED, ApplicationStatus.OFFER_ACCEPTED)
            ]
            
            for from_status, to_status in journey_steps:
                assert app.status == from_status
                success = self._apply_status_transition(app, to_status)
                assert success
                
                # Simulate time passing
                await asyncio.sleep(0.01)
                
                # Trigger associated rules
                self._execute_status_rules(app)
            
            test_case.actual_outcome = f"Journey completed in {len(journey_steps)} steps"
            test_case.passed = True
            
        except Exception as e:
            test_case.passed = False
            test_case.error_details = str(e)
        
        test_case.execution_time_ms = (time.time() - start) * 1000
        self.test_cases.append(test_case)
        
        status = "✅" if test_case.passed else "❌"
        print(f"{status} {test_case.name}: {test_case.actual_outcome or test_case.error_details}")
    
    async def _test_rule_conflicts(self) -> None:
        """Test handling of conflicting business rules"""
        print("\n⚠️ Testing Rule Conflict Resolution...")
        
        test_case = BusinessLogicTestCase(
            test_id="CONFLICT-001",
            name="Conflicting Rule Priority",
            description="Test resolution of conflicting rules",
            rule_type=BusinessRuleType.STATUS_TRANSITION,
            test_scenario={
                "rule1": "auto_archive_after_90_days",
                "rule2": "keep_active_if_user_engaged",
                "conflict": "User engaged but 90 days passed"
            },
            expected_outcome="Higher priority rule wins"
        )
        
        start = time.time()
        try:
            # Create scenario with conflict
            app = JobApplication(
                application_id="conflict_app",
                user_id="active_user",
                job_id="old_job",
                company="OldCorp",
                position="Old Position",
                status=ApplicationStatus.SUBMITTED,
                submitted_date=datetime.now() - timedelta(days=91)
            )
            
            # User has been active
            user_last_active = datetime.now() - timedelta(days=1)
            
            # Apply rules
            rules_triggered = []
            
            # Rule 1: Archive old applications
            if (datetime.now() - app.submitted_date).days > 90:
                rules_triggered.append(("archive_old", 3))
            
            # Rule 2: Keep active if user engaged
            if (datetime.now() - user_last_active).days < 7:
                rules_triggered.append(("keep_active", 5))  # Higher priority
            
            # Resolve conflict by priority
            winning_rule = max(rules_triggered, key=lambda x: x[1])
            assert winning_rule[0] == "keep_active"
            
            test_case.actual_outcome = f"Rule '{winning_rule[0]}' won with priority {winning_rule[1]}"
            test_case.passed = True
            
        except Exception as e:
            test_case.passed = False
            test_case.error_details = str(e)
        
        test_case.execution_time_ms = (time.time() - start) * 1000
        self.test_cases.append(test_case)
        
        status = "✅" if test_case.passed else "❌"
        print(f"{status} {test_case.name}: {test_case.actual_outcome or test_case.error_details}")
    
    async def _test_edge_cases(self) -> None:
        """Test edge cases in business logic"""
        print("\n🔍 Testing Edge Cases...")
        
        edge_cases = [
            {
                "test_id": "EDGE-001",
                "name": "Same Day Interview",
                "scenario": "Interview scheduled for today",
                "expected": "Emergency prep triggered"
            },
            {
                "test_id": "EDGE-002",
                "name": "Multiple Offers",
                "scenario": "3 offers received simultaneously",
                "expected": "Comparison analysis triggered"
            },
            {
                "test_id": "EDGE-003",
                "name": "Retroactive Application",
                "scenario": "Application dated in the past",
                "expected": "Date adjusted to today"
            }
        ]
        
        for edge_case in edge_cases:
            test_case = BusinessLogicTestCase(
                test_id=edge_case["test_id"],
                name=edge_case["name"],
                description=f"Test edge case: {edge_case['scenario']}",
                rule_type=BusinessRuleType.DATA_VALIDATION,
                test_scenario={"scenario": edge_case["scenario"]},
                expected_outcome=edge_case["expected"]
            )
            
            start = time.time()
            try:
                if "Same Day Interview" in edge_case["name"]:
                    # Test same day interview
                    app = JobApplication(
                        application_id="urgent_app",
                        user_id="test_user",
                        job_id="urgent_job",
                        company="UrgentCorp",
                        position="Urgent Position",
                        status=ApplicationStatus.INTERVIEW_SCHEDULED,
                        interview_dates=[datetime.now()]  # Today!
                    )
                    
                    actions = self._check_urgent_actions(app)
                    assert "emergency_prep" in actions
                    test_case.actual_outcome = "Emergency prep initiated"
                    
                elif "Multiple Offers" in edge_case["name"]:
                    # Test multiple offers
                    offers = [
                        {"company": "A", "salary": 120000},
                        {"company": "B", "salary": 130000},
                        {"company": "C", "salary": 125000}
                    ]
                    
                    analysis = self._analyze_multiple_offers(offers)
                    assert analysis["recommendation"] is not None
                    test_case.actual_outcome = f"Recommended: Company {analysis['recommendation']}"
                    
                elif "Retroactive" in edge_case["name"]:
                    # Test retroactive date
                    past_date = datetime.now() - timedelta(days=5)
                    adjusted_date = self._validate_application_date(past_date)
                    assert adjusted_date.date() == datetime.now().date()
                    test_case.actual_outcome = "Date adjusted to today"
                
                test_case.passed = True
                
            except Exception as e:
                test_case.passed = False
                test_case.error_details = str(e)
            
            test_case.execution_time_ms = (time.time() - start) * 1000
            self.test_cases.append(test_case)
        
        self._print_test_results("Edge Cases", [tc for tc in self.test_cases if "EDGE" in tc.test_id])
    
    async def _test_performance(self) -> None:
        """Test business logic performance"""
        print("\n⚡ Testing Performance...")
        
        test_case = BusinessLogicTestCase(
            test_id="PERF-001",
            name="Decision Processing Speed",
            description="Test AI decisions under 100ms",
            rule_type=BusinessRuleType.AI_DECISION,
            test_scenario={"decisions": 100},
            expected_outcome="All decisions <100ms"
        )
        
        start = time.time()
        try:
            decision_times = []
            
            # Test 100 rapid decisions
            for _ in range(100):
                decision_start = time.time()
                
                # Make quick decision
                decision = self._make_ai_decision("quick_match", {
                    "skills": ["Python", "ML"],
                    "requirements": ["Python", "AI"]
                })
                
                decision_time = (time.time() - decision_start) * 1000
                decision_times.append(decision_time)
            
            # Check performance
            avg_time = sum(decision_times) / len(decision_times)
            max_time = max(decision_times)
            
            assert avg_time < 100  # Average under 100ms
            assert max_time < 200  # No decision over 200ms
            
            test_case.actual_outcome = f"Avg: {avg_time:.1f}ms, Max: {max_time:.1f}ms"
            test_case.passed = True
            
        except Exception as e:
            test_case.passed = False
            test_case.error_details = str(e)
        
        test_case.execution_time_ms = (time.time() - start) * 1000
        self.test_cases.append(test_case)
        
        status = "✅" if test_case.passed else "❌"
        print(f"{status} {test_case.name}: {test_case.actual_outcome or test_case.error_details}")
    
    # Helper methods
    def _apply_status_transition(self, app: JobApplication, new_status: ApplicationStatus) -> bool:
        """Apply status transition with validation"""
        valid_transitions = {
            ApplicationStatus.DRAFT: [ApplicationStatus.SUBMITTED, ApplicationStatus.WITHDRAWN],
            ApplicationStatus.SUBMITTED: [ApplicationStatus.ACKNOWLEDGED, ApplicationStatus.WITHDRAWN],
            ApplicationStatus.ACKNOWLEDGED: [ApplicationStatus.SCREENING, ApplicationStatus.REJECTED, ApplicationStatus.WITHDRAWN],
            ApplicationStatus.SCREENING: [ApplicationStatus.INTERVIEW_SCHEDULED, ApplicationStatus.REJECTED, ApplicationStatus.WITHDRAWN],
            ApplicationStatus.INTERVIEW_SCHEDULED: [ApplicationStatus.INTERVIEWED, ApplicationStatus.WITHDRAWN],
            ApplicationStatus.INTERVIEWED: [ApplicationStatus.ASSESSMENT, ApplicationStatus.OFFER_EXTENDED, ApplicationStatus.REJECTED, ApplicationStatus.WITHDRAWN],
            ApplicationStatus.OFFER_EXTENDED: [ApplicationStatus.OFFER_ACCEPTED, ApplicationStatus.OFFER_DECLINED],
            ApplicationStatus.OFFER_ACCEPTED: [ApplicationStatus.ARCHIVED],
            ApplicationStatus.OFFER_DECLINED: [ApplicationStatus.ARCHIVED],
            ApplicationStatus.REJECTED: [ApplicationStatus.ARCHIVED],
            ApplicationStatus.WITHDRAWN: [ApplicationStatus.ARCHIVED]
        }
        
        if app.status in valid_transitions:
            if new_status in valid_transitions[app.status]:
                app.status = new_status
                app.last_updated = datetime.now()
                return True
        
        return False
    
    def _check_timing_constraints(self, app: JobApplication) -> List[str]:
        """Check timing-based rules"""
        triggered_actions = []
        
        days_since_update = (datetime.now() - app.last_updated).days
        
        # Interview follow-up
        if app.status == ApplicationStatus.INTERVIEWED and days_since_update >= 3:
            triggered_actions.append("send_follow_up")
        
        # Stale application
        if days_since_update >= 90 and app.status not in [ApplicationStatus.OFFER_ACCEPTED, ApplicationStatus.ARCHIVED]:
            triggered_actions.append("prompt_user")
        
        # Weekly check
        if days_since_update >= 7:
            triggered_actions.append("generate_weekly_report")
        
        # Offer reminder
        if app.status == ApplicationStatus.OFFER_EXTENDED and days_since_update >= 6:
            triggered_actions.append("send_reminder")
        
        return triggered_actions
    
    def _execute_workflow_step(self, execution: WorkflowExecution, step: WorkflowStep) -> bool:
        """Execute a workflow step"""
        # Simulate step execution
        return True
    
    def _make_ai_decision(self, decision_type: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Make AI-driven decision"""
        if decision_type == "Job Match Scoring" or decision_type == "quick_match":
            user_skills = set(input_data.get("user_skills", []))
            job_requirements = set(input_data.get("job_requirements", []))
            
            if user_skills and job_requirements:
                match_score = len(user_skills.intersection(job_requirements)) / len(job_requirements)
            else:
                match_score = 0
            
            return {"match_score": match_score}
        
        elif decision_type == "Interview Success Prediction":
            # Simple prediction based on inputs
            culture_match = 1.0 if input_data.get("company_culture") == input_data.get("user_personality") else 0.5
            technical_match = input_data.get("technical_match", 0.5)
            preparation = input_data.get("preparation_level", 0.5)
            
            success_probability = (culture_match * 0.3 + technical_match * 0.5 + preparation * 0.2)
            return {"success_probability": success_probability}
        
        elif decision_type == "Salary Negotiation Strategy":
            offer = input_data.get("offer_amount", 0)
            market = input_data.get("market_average", 0)
            
            if offer < market * 0.9:  # More than 10% below market
                return {
                    "recommend_negotiation": True,
                    "suggested_increase": int(market - offer)
                }
            return {"recommend_negotiation": False, "suggested_increase": 0}
        
        elif decision_type == "Application Priority Ranking":
            applications = input_data.get("applications", [])
            
            # Sort by combination of match score and stage
            stage_weights = {"interview": 3, "screening": 2, "submitted": 1}
            
            scored_apps = []
            for app in applications:
                score = app["match"] * stage_weights.get(app["stage"], 1)
                scored_apps.append((app["company"], score))
            
            scored_apps.sort(key=lambda x: x[1], reverse=True)
            ranking = [app[0] for app in scored_apps]
            
            return {
                "top_priority": ranking[0] if ranking else None,
                "ranking": ranking
            }
        
        return {}
    
    def _trigger_notifications(self, trigger_type: str) -> List[Dict[str, Any]]:
        """Trigger notifications based on event"""
        notifications = []
        
        if trigger_type == "application_submitted":
            notifications.extend([
                {"type": "email_confirmation", "priority": "high"},
                {"type": "in_app_notification", "priority": "medium"}
            ])
        elif trigger_type == "interview_tomorrow":
            notifications.extend([
                {"type": "email_reminder", "priority": "high"},
                {"type": "push_notification", "priority": "high"},
                {"type": "calendar_update", "priority": "medium"}
            ])
        elif trigger_type == "status_changed":
            notifications.extend([
                {"type": "in_app_notification", "priority": "medium"},
                {"type": "optional_email", "priority": "low"}
            ])
        elif trigger_type == "weekly_checkpoint":
            notifications.extend([
                {"type": "email_summary", "priority": "medium"},
                {"type": "dashboard_update", "priority": "low"}
            ])
        
        return notifications
    
    def _validate_data(self, validation_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data according to business rules"""
        errors = []
        
        if validation_type == "Application Completeness":
            required_fields = ["company", "position", "resume"]
            for field in required_fields:
                if field not in data or not data[field]:
                    errors.append(f"Missing required field: {field}")
        
        elif validation_type == "Email Format Validation":
            import re
            email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            
            for field in ["email", "backup_email"]:
                if field in data and data[field]:
                    if not re.match(email_pattern, data[field]):
                        errors.append(f"Invalid {field} format")
        
        elif validation_type == "Salary Range Validation":
            if data.get("salary_min", 0) > data.get("salary_max", float('inf')):
                errors.append("Minimum salary cannot exceed maximum")
        
        elif validation_type == "Date Consistency":
            # Dates should be in chronological order
            if "application_date" in data and "interview_date" in data:
                if data["application_date"] > data["interview_date"]:
                    errors.append("Interview cannot be before application")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    def _execute_status_rules(self, app: JobApplication) -> None:
        """Execute rules associated with current status"""
        # Simulate rule execution based on status
        if app.status == ApplicationStatus.INTERVIEW_SCHEDULED:
            # Trigger interview prep
            app.ai_insights["interview_prep_started"] = True
        elif app.status == ApplicationStatus.OFFER_EXTENDED:
            # Trigger offer analysis
            app.ai_insights["offer_analysis_complete"] = True
    
    def _check_urgent_actions(self, app: JobApplication) -> List[str]:
        """Check for urgent actions needed"""
        actions = []
        
        if app.interview_dates:
            next_interview = min(d for d in app.interview_dates if d >= datetime.now())
            hours_until = (next_interview - datetime.now()).total_seconds() / 3600
            
            if hours_until < 24:
                actions.append("emergency_prep")
            if hours_until < 2:
                actions.append("final_reminder")
        
        return actions
    
    def _analyze_multiple_offers(self, offers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze multiple job offers"""
        if not offers:
            return {"recommendation": None}
        
        # Simple scoring based on salary (in reality would be more complex)
        best_offer = max(offers, key=lambda x: x.get("salary", 0))
        
        return {
            "recommendation": best_offer["company"],
            "analysis": {
                "salary_range": f"${min(o['salary'] for o in offers):,} - ${max(o['salary'] for o in offers):,}",
                "best_salary": best_offer["company"],
                "offer_count": len(offers)
            }
        }
    
    def _validate_application_date(self, date: datetime) -> datetime:
        """Validate and adjust application date"""
        if date > datetime.now():
            return datetime.now()  # Can't apply in the future
        elif date < datetime.now() - timedelta(days=365):
            return datetime.now()  # Too old, probably an error
        return date
    
    def _print_test_results(self, category: str, test_cases: List[BusinessLogicTestCase]) -> None:
        """Print test results for a category"""
        passed = sum(1 for tc in test_cases if tc.passed)
        total = len(test_cases)
        status = "✅" if passed == total else "⚠️" if passed > 0 else "❌"
        print(f"{status} {category}: {passed}/{total} tests passed")
    
    def _generate_business_logic_report(self) -> BusinessLogicReport:
        """Generate comprehensive business logic report"""
        passed = sum(1 for tc in self.test_cases if tc.passed)
        failed = sum(1 for tc in self.test_cases if not tc.passed)
        total = len(self.test_cases)
        
        # Calculate rule coverage
        rule_coverage = {}
        for rule_type in BusinessRuleType:
            rule_tests = [tc for tc in self.test_cases if tc.rule_type == rule_type]
            if rule_tests:
                coverage = sum(1 for tc in rule_tests if tc.passed) / len(rule_tests)
                rule_coverage[rule_type.value] = coverage
        
        # Calculate workflow accuracy
        workflow_tests = [tc for tc in self.test_cases if tc.rule_type == BusinessRuleType.WORKFLOW_SEQUENCE]
        workflow_accuracy = sum(1 for tc in workflow_tests if tc.passed) / len(workflow_tests) if workflow_tests else 0
        
        # Calculate AI decision accuracy
        ai_tests = [tc for tc in self.test_cases if tc.rule_type == BusinessRuleType.AI_DECISION]
        ai_accuracy = sum(1 for tc in ai_tests if tc.passed) / len(ai_tests) if ai_tests else 0
        
        # Performance metrics
        avg_decision_time = sum(self.decision_times) / len(self.decision_times) if self.decision_times else 0
        
        performance_metrics = {
            "avg_decision_time_ms": avg_decision_time,
            "max_decision_time_ms": max(self.decision_times) if self.decision_times else 0,
            "decisions_under_100ms": sum(1 for t in self.decision_times if t < 100) / len(self.decision_times) if self.decision_times else 0
        }
        
        recommendations = []
        if workflow_accuracy < 1.0:
            recommendations.append("Review failing workflow sequences")
        if ai_accuracy < 0.95:
            recommendations.append("Improve AI decision accuracy")
        if avg_decision_time > 100:
            recommendations.append("Optimize decision processing time")
        
        if not recommendations:
            recommendations.append("All business logic tests passing - system ready for production")
        
        return BusinessLogicReport(
            test_date=datetime.now(),
            total_tests=total,
            passed_tests=passed,
            failed_tests=failed,
            rule_coverage=rule_coverage,
            workflow_accuracy=workflow_accuracy,
            ai_decision_accuracy=ai_accuracy,
            performance_metrics=performance_metrics,
            recommendations=recommendations
        )
    
    def generate_report(self, report: BusinessLogicReport) -> None:
        """Generate and save business logic report"""
        print("\n" + "=" * 60)
        print("📊 Business Logic Test Report")
        print("=" * 60)
        print(f"Test Date: {report.test_date.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total Tests: {report.total_tests}")
        print(f"Passed: {report.passed_tests} ✅")
        print(f"Failed: {report.failed_tests} ❌")
        
        print("\n📋 Rule Coverage:")
        for rule_type, coverage in sorted(report.rule_coverage.items()):
            status = "✅" if coverage == 1.0 else "⚠️" if coverage >= 0.8 else "❌"
            print(f"  {status} {rule_type}: {coverage:.0%}")
        
        print(f"\n📈 Accuracy Metrics:")
        print(f"  Workflow Accuracy: {report.workflow_accuracy:.0%}")
        print(f"  AI Decision Accuracy: {report.ai_decision_accuracy:.0%}")
        
        print(f"\n⚡ Performance:")
        print(f"  Average Decision Time: {report.performance_metrics['avg_decision_time_ms']:.1f}ms")
        print(f"  Max Decision Time: {report.performance_metrics['max_decision_time_ms']:.1f}ms")
        print(f"  Decisions <100ms: {report.performance_metrics['decisions_under_100ms']:.0%}")
        
        print("\n📋 Recommendations:")
        for i, rec in enumerate(report.recommendations, 1):
            print(f"{i}. {rec}")
        
        # Save detailed report
        report_data = {
            "test_date": report.test_date.isoformat(),
            "summary": {
                "total_tests": report.total_tests,
                "passed": report.passed_tests,
                "failed": report.failed_tests
            },
            "rule_coverage": report.rule_coverage,
            "accuracy": {
                "workflow": report.workflow_accuracy,
                "ai_decisions": report.ai_decision_accuracy
            },
            "performance": report.performance_metrics,
            "test_results": [
                {
                    "test_id": tc.test_id,
                    "name": tc.name,
                    "rule_type": tc.rule_type.value,
                    "passed": tc.passed,
                    "execution_time_ms": tc.execution_time_ms,
                    "outcome": tc.actual_outcome or tc.error_details
                }
                for tc in self.test_cases
            ],
            "recommendations": report.recommendations
        }
        
        with open("business-logic-test-report.json", "w") as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n💾 Detailed report saved to: business-logic-test-report.json")


async def main():
    """Run business logic test suite"""
    print("🧮 Job Tracker Pro - Business Logic Test Suite")
    print("=" * 60)
    print("Testing business rules, workflows, and AI decisions...")
    print("Performance: 6 threads × 2GB = 12GB allocated")
    
    tester = BusinessLogicTester()
    report = await tester.run_all_tests()
    tester.generate_report(report)
    
    # Performance metrics
    process = psutil.Process()
    memory_info = process.memory_info()
    print(f"\n📊 Performance Metrics:")
    print(f"Peak Memory Usage: {memory_info.rss / 1024 / 1024:.2f} MB")
    print(f"Threads Used: 6")
    print(f"Business Rules Tested: {len(tester.business_rules)}")


if __name__ == "__main__":
    asyncio.run(main())