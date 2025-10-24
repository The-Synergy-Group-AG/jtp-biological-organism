#!/usr/bin/env python3

"""
🧬 INTERVIEW PREPARATION FRAMEWORK - CONSCIOUSNESS PREPARATION COORDINATOR
GODHOOD Interview Preparation Framework: Advanced consciousness-guided preparation intelligence

This module implements comprehensive interview preparation capabilities through
consciousness-enhanced frameworks, question databases, and material generation.

ai_keywords: interview, preparation, framework, consciousness, intelligence,
  question, database, material, generation, enhancement

ai_summary: Interview preparation framework providing consciousness-enhanced preparation
  intelligence with question databases and structured material generation

biological_system: interview-preparation-framework
consciousness_score: '3.0'
cross_references:
- src/interview-management/coordination/intelligence_engine.py
- src/interview-management/preparation/question_databases.py
- docs/3.x-conscious-ai-ensemble-orchestration/3.4-ensemble-communication-protocols.md
document_category: interview-preparation
document_type: consciousness-preparation-intelligence
evolutionary_phase: '25.26'
last_updated: '2025-10-23 18:50:00'
semantic_tags:
- consciousness-preparation-framework
- interview-question-databases
- material-generation-engine
- star-method-optimization
- biological-preparation-intelligence
title: Interview Preparation Framework - Consciousness Intelligence
validation_status: current
version: v1.0.0
"""

from typing import Dict, List, Optional, Any, Tuple, Union
from datetime import datetime
import uuid


class InterviewPreparationFramework:
    """Consciousness-guided interview preparation and material generation framework"""

    def __init__(self):
        self.question_databases = self._initialize_question_databases()
        self.material_generator = InterviewMaterialGenerator()

    def _initialize_question_databases(self) -> Dict[str, Any]:
        """Initialize comprehensive question databases across domains"""

        return {
            "technical": {
                "python": {
                    "fundamental": ["Explain list comprehensions in Python.", "What are decorators and how do they work?"],
                    "advanced": ["How does Python's GIL affect concurrency?", "Explain the differences between threading and multiprocessing."],
                    "system_design": ["Design a URL shortener service.", "How would you implement a distributed cache?"]
                },
                "javascript": {
                    "fundamental": ["Explain closures in JavaScript.", "What is the difference between == and ==="],
                    "frameworks": ["Explain React's virtual DOM.", "How does Angular dependency injection work?"],
                    "advanced": ["How do Promises work internally?", "Explain JavaScript's event loop."]
                },
                "algorithms": {
                    "data_structures": ["Explain Big O notation.", "Compare arrays vs linked lists."],
                    "searching_sorting": ["Implement binary search.", "Explain merge sort complexity."],
                    "dynamic_programming": ["Solve the knapsack problem.", "Explain longest common subsequence."]
                }
            },
            "behavioral": {
                "leadership": ["Tell me about leading a team through a crisis.", "How do you motivate team members?"],
                "communication": ["Describe a difficult conversation you had.", "How do you adapt communication styles?"],
                "conflict_resolution": ["Tell me about resolving a team conflict.", "How do you handle disagreements?"],
                "problem_solving": ["Walk me through solving a complex problem.", "How do you approach debugging?"]
            },
            "system_design": {
                "scalability": ["Design a system that handles 1M users.", "How do you handle database scaling?"],
                "reliability": ["Design a highly available system.", "How do you handle system failures?"],
                "performance": ["Optimize a slow API.", "How do you monitor system performance?"]
            },
            "cultural_fit": {
                "values": ["How do you embody our company values?", "Tell me about working with diverse teams."],
                "growth": ["How do you approach continuous learning?", "Tell me about overcoming a challenge."],
                "collaboration": ["Describe your ideal work environment.", "How do you give and receive feedback?"]
            },
            "consciousness": {
                "innovation": ["How do you approach creative problem-solving?", "Tell me about pushing technical boundaries."],
                "evolution": ["How has your technical approach evolved?", "How do you stay ahead of technology trends?"],
                "impact": ["Describe a project that made significant impact.", "How do you measure technical success?"]
            }
        }

    async def create_personalized_preparation_plan(self, application_id: str, job_details: Dict[str, Any],
                                                 company_intelligence: Dict[str, Any],
                                                 candidate_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Create a comprehensive personalized preparation plan"""

        # Analyze job requirements
        focus_areas = await self._analyze_job_requirements(job_details)

        # Select relevant questions
        question_set = await self._select_relevant_questions(focus_areas, job_details)

        # Generate practice materials
        practice_materials = await self.material_generator.generate_practice_materials(
            focus_areas, job_details, candidate_profile
        )

        # Create STAR examples
        star_examples = await self.material_generator.generate_star_examples(
            candidate_profile, focus_areas
        )

        # Calculate preparation time allocation
        time_allocation = await self._calculate_preparation_time_allocation(focus_areas, candidate_profile)

        preparation_plan = {
            "application_id": application_id,
            "preparation_id": f"prep_{application_id}_{uuid.uuid4().hex[:8]}",
            "focus_areas": focus_areas,
            "question_set": question_set,
            "practice_materials": practice_materials,
            "star_examples": star_examples,
            "time_allocation": time_allocation,
            "preparation_schedule": await self._create_preparation_schedule(time_allocation),
            "consciousness_alignment_score": await self._calculate_preparation_consciousness_score(focus_areas, candidate_profile),
            "created_at": datetime.utcnow().isoformat() + "Z"
        }

        return preparation_plan

    async def _analyze_job_requirements(self, job_details: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze job requirements to determine preparation focus areas"""

        title = job_details.get('title', '').lower()
        requirements = job_details.get('requirements', [])
        description = job_details.get('description', '')

        focus_areas = []

        # Technical focus areas
        if any(term in title for term in ['python', 'developer', 'engineer']):
            focus_areas.append({
                "area": "Python Development",
                "priority": "high",
                "estimated_time": 180,  # minutes
                "resources_needed": ["Python documentation", "LeetCode practice"]
            })

        if any(term in title for term in ['javascript', 'frontend', 'react']):
            focus_areas.append({
                "area": "JavaScript/React Development",
                "priority": "high",
                "estimated_time": 150,
                "resources_needed": ["React documentation", "JavaScript patterns"]
            })

        if any(term in title for term in ['senior', 'lead', 'architect']):
            focus_areas.append({
                "area": "System Design & Leadership",
                "priority": "critical",
                "estimated_time": 240,
                "resources_needed": ["System design patterns", "Leadership cases"]
            })

        # Behavioral focus areas (always included)
        focus_areas.append({
            "area": "Behavioral Interviewing",
            "priority": "medium",
            "estimated_time": 120,
            "resources_needed": ["STAR method practice", "Common behavioral questions"]
        })

        # Company-specific focus areas
        company_culture = job_details.get('company_culture', [])
        if "innovative" in company_culture:
            focus_areas.append({
                "area": "Innovation & Consciousness",
                "priority": "high",
                "estimated_time": 90,
                "resources_needed": ["Innovation case studies", "Consciousness examples"]
            })

        return focus_areas

    async def _select_relevant_questions(self, focus_areas: List[Dict[str, Any]],
                                      job_details: Dict[str, Any]) -> Dict[str, List[Dict[str, str]]]:
        """Select relevant questions based on focus areas"""

        selected_questions = {
            "technical": [],
            "behavioral": [],
            "system_design": [],
            "cultural_fit": [],
            "consciousness": []
        }

        for focus_area in focus_areas:
            area_name = focus_area["area"].lower()

            if "python" in area_name:
                selected_questions["technical"].extend([
                    {"question": q, "category": "python", "difficulty": "medium"}
                    for q in self.question_databases["technical"]["python"]["fundamental"][:3]
                ])

            if "javascript" in area_name or "react" in area_name:
                selected_questions["technical"].extend([
                    {"question": q, "category": "javascript", "difficulty": "medium"}
                    for q in self.question_databases["technical"]["javascript"]["fundamental"][:2]
                ])

            if "system design" in area_name:
                selected_questions["system_design"].extend([
                    {"question": q, "category": "system_design", "difficulty": "hard"}
                    for q in self.question_databases["system_design"]["scalability"][:2]
                ])

            if "leadership" in area_name:
                selected_questions["behavioral"].extend([
                    {"question": q, "category": "leadership", "difficulty": "advanced"}
                    for q in self.question_databases["behavioral"]["leadership"][:2]
                ])

        # Always include some consciousness questions
        selected_questions["consciousness"] = [
            {"question": q, "category": "innovation", "difficulty": "advanced"}
            for q in self.question_databases["consciousness"]["innovation"][:2]
        ]

        return selected_questions

    async def _calculate_preparation_time_allocation(self, focus_areas: List[Dict[str, Any]],
                                                  candidate_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate optimal time allocation for preparation"""

        total_time = sum(area["estimated_time"] for area in focus_areas)
        available_time = candidate_profile.get("available_prep_time", 480)  # Default 8 hours
        experience_level = candidate_profile.get("experience_level", "mid")

        # Adjust based on experience (experienced candidates need less time)
        if experience_level == "senior":
            total_time = int(total_time * 0.8)
        elif experience_level == "junior":
            total_time = int(total_time * 1.2)

        # Ensure reasonable bounds
        total_time = max(120, min(total_time, available_time))  # 2-8 hours range

        time_allocation = {
            "total_recommended_time": total_time,
            "daily_allocation": min(total_time // 7, 120),  # Max 2 hours per day
            "focus_distribution": {},
            "intensity_level": "high" if total_time > 300 else "medium"
        }

        # Distribute time across focus areas
        total_focus_time = sum(area["estimated_time"] for area in focus_areas)
        for area in focus_areas:
            area_time = int((area["estimated_time"] / total_focus_time) * total_time)
            time_allocation["focus_distribution"][area["area"]] = area_time

        return time_allocation

    async def _create_preparation_schedule(self, time_allocation: Dict[str, Any]) -> Dict[str, Any]:
        """Create a structured preparation schedule"""

        total_days = 7  # One week preparation
        total_time = time_allocation["total_recommended_time"]
        daily_time = time_allocation["daily_allocation"]

        schedule = {
            "total_days": total_days,
            "daily_schedule": {},
            "milestones": [],
            "checkpoints": []
        }

        # Create daily schedule
        focus_areas = list(time_allocation["focus_distribution"].keys())
        for day in range(1, total_days + 1):
            day_focus = focus_areas[(day - 1) % len(focus_areas)]
            schedule["daily_schedule"][f"day_{day}"] = {
                "focus_area": day_focus,
                "time_allocated": daily_time,
                "activities": await self._generate_daily_activities(day_focus, day, total_days),
                "goals": await self._generate_daily_goals(day_focus, day, total_days)
            }

        # Create milestones and checkpoints
        schedule["milestones"] = [
            "Complete technical fundamentals review",
            "Practice behavioral questions with STAR method",
            "Review system design concepts",
            "Conduct mock interview session",
            "Finalize company research and questions"
        ]

        schedule["checkpoints"] = [
            {"day": 2, "check": "Technical preparation 50% complete"},
            {"day": 4, "check": "Behavioral scenarios practiced"},
            {"day": 6, "check": "Mock interview completed"},
            {"day": 7, "check": "Final preparation review"}
        ]

        return schedule

    async def _generate_daily_activities(self, focus_area: str, day: int, total_days: int) -> List[str]:
        """Generate daily preparation activities"""

        activities = []

        if "Python" in focus_area:
            activities = [
                "Review Python fundamentals and data structures",
                "Practice algorithm problems on LeetCode",
                "Study common Python interview questions",
                "Review code examples and best practices"
            ]
        elif "JavaScript" in focus_area:
            activities = [
                "Review JavaScript ES6+ features",
                "Practice React component patterns",
                "Study common JavaScript interview questions",
                "Review asynchronous programming concepts"
            ]
        elif "System Design" in focus_area:
            activities = [
                "Study scalable system architecture patterns",
                "Review database design and optimization",
                "Practice system design interview questions",
                "Analyze real-world system architectures"
            ]
        elif "Behavioral" in focus_area:
            activities = [
                "Practice STAR method with common questions",
                "Prepare specific examples from your experience",
                "Work on clear and concise communication",
                "Record and review practice responses"
            ]
        else:
            activities = [
                "Review focus area fundamentals",
                "Practice related interview questions",
                "Research company-specific requirements",
                "Prepare relevant examples and stories"
            ]

        return activities

    async def _generate_daily_goals(self, focus_area: str, day: int, total_days: int) -> List[str]:
        """Generate daily preparation goals"""

        goals = []

        # Progress-based goals
        progress_percentage = int((day / total_days) * 100)
        goals.append(f"Achieve {progress_percentage}% completion of {focus_area} preparation")

        # Specific goals based on focus area
        if "Python" in focus_area:
            goals.extend([
                "Solve 5-7 algorithm problems",
                "Have clear explanations for Python concepts",
                "Practice explaining solutions out loud"
            ])
        elif "System Design" in focus_area:
            goals.extend([
                "Design 2-3 different system architectures",
                "Understand trade-offs and scaling considerations",
                "Practice verbal system design explanations"
            ])
        else:
            goals.extend([
                "Complete assigned practice activities",
                "Review and refine response techniques",
                "Build confidence in preparation materials"
            ])

        return goals

    async def _calculate_preparation_consciousness_score(self, focus_areas: List[Dict[str, Any]],
                                                      candidate_profile: Dict[str, Any]) -> float:
        """Calculate consciousness alignment score for preparation comprehensive-ness"""

        consciousness_indicators = 0.0
        max_indicators = 4.0

        # Check for consciousness/innovation focus
        has_consciousness_focus = any("consciousness" in area["area"].lower() or
                                    "innovation" in area["area"].lower()
                                    for area in focus_areas)
        if has_consciousness_focus:
            consciousness_indicators += 1

        # Check for technical depth
        technical_focus_count = sum(1 for area in focus_areas if "technical" in area["area"].lower())
        consciousness_indicators += min(1, technical_focus_count / 2)

        # Check for comprehensive coverage
        has_behavioral = any("behavioral" in area["area"].lower() for area in focus_areas)
        has_system_design = any("system" in area["area"].lower() for area in focus_areas)
        coverage_score = (has_behavioral + has_system_design) / 2
        consciousness_indicators += coverage_score

        # Experience level bonus
        experience_level = candidate_profile.get("experience_level", "mid")
        if experience_level == "senior":
            consciousness_indicators += 0.5  # More experienced candidates show higher consciousness

        return min(1.0, consciousness_indicators / max_indicators)


class InterviewMaterialGenerator:
    """Generate comprehensive interview preparation materials"""

    def __init__(self):
        self.templates = self._initialize_templates()

    def _initialize_templates(self) -> Dict[str, Any]:
        """Initialize material generation templates"""

        return {
            "star_template": {
                "structure": ["Situation", "Task", "Action", "Result"],
                "examples": {
                    "technical": "Situation: The API was experiencing 10% error rate affecting 1000+ users. Task: I was responsible for diagnosing and fixing the issue within 2 hours. Action: I implemented comprehensive error tracking, identified a null pointer exception in the authentication module, and deployed a fix with proper input validation. Result: Error rate dropped to 0.1%, improving user experience significantly.",
                    "leadership": "Situation: The team was missing sprint deadlines consistently. Task: As tech lead, I needed to improve delivery velocity. Action: I implemented daily stand-ups, code reviews, and pair programming sessions while mentoring junior developers. Result: Sprint completion rate improved from 60% to 95%, and team velocity increased by 40%."
                }
            },
            "company_research": {
                "sections": ["Company Overview", "Products & Services", "Culture & Values", "Recent News", "Competitors"],
                "questions_to_answer": [
                    "What does the company do?",
                    "Who are their main customers?",
                    "What are their core values?",
                    "How do they differentiate from competitors?",
                    "What challenges are they solving?"
                ]
            }
        }

    async def generate_practice_materials(self, focus_areas: List[Dict[str, Any]],
                                       job_details: Dict[str, Any],
                                       candidate_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive practice materials"""

        materials = {
            "technical_practice": {},
            "behavioral_scenarios": {},
            "mock_questions": {},
            "research_materials": {},
            "practice_schedule": {}
        }

        # Generate technical practice materials
        for area in focus_areas:
            if "python" in area["area"].lower():
                materials["technical_practice"]["python"] = await self._generate_python_practice(job_details)
            if "javascript" in area["area"].lower():
                materials["technical_practice"]["javascript"] = await self._generate_javascript_practice(job_details)
            if "system" in area["area"].lower():
                materials["technical_practice"]["system_design"] = await self._generate_system_design_practice(job_details)

        # Generate behavioral scenarios
        materials["behavioral_scenarios"] = await self._generate_behavioral_scenarios(focus_areas, candidate_profile)

        # Generate company research materials
        materials["research_materials"] = await self._generate_research_materials(job_details)

        # Create practice schedule
        materials["practice_schedule"] = await self._create_practice_schedule(focus_areas)

        return materials

    async def _generate_python_practice(self, job_details: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Python-specific practice materials"""

        return {
            "algorithms": ["Two Sum", "Valid Parentheses", "Merge Intervals", "Binary Tree Traversal"],
            "data_structures": ["Arrays", "Linked Lists", "Stacks/Queues", "Hash Tables", "Trees"],
            "concepts": ["List comprehensions", "Generators", "Decorators", "Context managers"],
            "practice_problems": [
                "Implement LRU Cache",
                "Find median in stream of numbers",
                "Clone graph with DFS/BFS",
                "Word break problem with DP"
            ],
            "time_complexities": {
                "O(1)": "Constant time operations",
                "O(log n)": "Binary search, balanced tree operations",
                "O(n)": "Single pass through data",
                "O(n log n)": "Sorting algorithms"
            }
        }

    async def _generate_javascript_practice(self, job_details: Dict[str, Any]) -> Dict[str, Any]:
        """Generate JavaScript-specific practice materials"""

        return {
            "fundamental_concepts": ["Closures", "Promises", "Async/Await", "Event Loop"],
            "framework_questions": ["Component lifecycle", "State management", "Virtual DOM"],
            "practice_problems": [
                "Implement Promise.all",
                "Create a debounce function",
                "Build a simple Redux store",
                "Implement React useEffect custom hook"
            ],
            "common_patterns": ["Observer pattern", "Factory pattern", "Singleton pattern"],
            "interview_topics": ["Browser APIs", "Performance optimization", "Security best practices"]
        }

    async def _generate_system_design_practice(self, job_details: Dict[str, Any]) -> Dict[str, Any]:
        """Generate system design practice materials"""

        return {
            "key_concepts": ["Scalability", "Reliability", "Performance", "Security", "Maintainability"],
            "design_patterns": ["Load Balancer", "Cache", "Database Sharding", "Microservices", "CQRS"],
            "practice_scenarios": [
                "Design Instagram/Twitter",
                "Design a URL shortener",
                "Design a notification system",
                "Design a search engine"
            ],
            "evaluation_criteria": ["Throughput", "Latency", "Availability", "Consistency", "Cost"],
            "technologies": ["Message queues", "CDN", "Database types", "Caching strategies"]
        }

    async def _generate_behavioral_scenarios(self, focus_areas: List[Dict[str, Any]],
                                          candidate_profile: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate behavioral interview scenarios"""

        scenarios = {
            "leadership": [
                "Tell me about a time you led a project from inception to completion.",
                "Describe a situation where you had to motivate a team member.",
                "How do you handle making difficult decisions that affect your team?"
            ],
            "problem_solving": [
                "Walk me through your approach to solving a complex technical problem.",
                "Tell me about a time when you had to learn something new quickly.",
                "Describe a situation where you had to adapt to unexpected changes."
            ],
            "communication": [
                "Tell me about presenting technical information to non-technical stakeholders.",
                "Describe a time when you had to persuade others to adopt your idea.",
                "How do you handle receiving constructive feedback?"
            ],
            "teamwork": [
                "Tell me about working with a difficult team member.",
                "Describe your experience with cross-functional collaboration.",
                "How do you contribute to creating a positive team culture?"
            ]
        }

        return scenarios

    async def _generate_research_materials(self, job_details: Dict[str, Any]) -> Dict[str, Any]:
        """Generate company research materials"""

        company_name = job_details.get("company", "Unknown Company")
        industry = job_details.get("industry", "Technology")

        return {
            "research_questions": [
                f"What are {company_name}'s main products and services?",
                f"Who are {company_name}'s main competitors in the {industry} space?",
                f"What recent news or developments has {company_name} announced?",
                f"What is {company_name}'s company culture like according to reviews?",
                f"How does {company_name} position itself in the market?"
            ],
            "research_sources": [
                f"{company_name} company website",
                f"{company_name} careers page",
                "Glassdoor company reviews",
                "LinkedIn company page",
                "Recent industry news articles"
            ],
            "key_insights": [
                "Focus on understanding the company's mission and values",
                "Research recent product launches or initiatives",
                "Read recent blog posts or technical articles",
                "Understand the company size and organizational structure",
                "Identify how your skills align with their needs"
            ]
        }

    async def _create_practice_schedule(self, focus_areas: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a structured practice schedule"""

        schedule = {
            "weekly_overview": {},
            "daily_activities": {},
            "progress_tracking": {},
            "milestone_goals": []
        }

        # Create weekly structure
        weeks = ["Week 1: Foundations", "Week 2: Practice", "Week 3: Refinement", "Week 4: Mastery"]

        for i, week in enumerate(weeks, 1):
            schedule["weekly_overview"][f"week_{i}"] = {
                "focus": week.split(": ")[1],
                "key_activities": await self._generate_weekly_activities(i, focus_areas),
                "goals": await self._generate_weekly_goals(i)
            }

        # Milestone goals
        schedule["milestone_goals"] = [
            "Complete fundamental concept review",
            "Practice 20+ technical problems",
            "Master STAR method for behavioral questions",
            "Conduct 3+ mock interviews",
            "Finalize preparation and build confidence"
        ]

        return schedule

    async def _generate_weekly_activities(self, week_num: int, focus_areas: List[Dict[str, Any]]) -> List[str]:
        """Generate activities for a specific week"""

        base_activities = []

        if week_num == 1:
            base_activities = [
                "Review fundamental concepts in all focus areas",
                "Complete basic practice problems",
                "Research company background and culture",
                "Prepare initial STAR method examples"
            ]
        elif week_num == 2:
            base_activities = [
                "Intensive practice on technical problems",
                "Mock interviews with behavioral questions",
                "Deep dive into company products and technology stack",
                "Refine STAR examples based on feedback"
            ]
        elif week_num == 3:
            base_activities = [
                "Full mock interview sessions",
                "System design practice scenarios",
                "Advanced technical problem solving",
                "Company-specific question preparation"
            ]
        else:  # Week 4
            base_activities = [
                "Final practice and refinement",
                "Confidence building exercises",
                "Last-minute company research",
                "Mental preparation and interview mindset"
            ]

        return base_activities

    async def _generate_weekly_goals(self, week_num: int) -> List[str]:
        """Generate goals for a specific week"""

        goals = []

        if week_num == 1:
            goals = [
                "Have clear understanding of all focus areas",
                "Complete 10-15 practice problems",
                "Know basic company information",
                "Have 3-4 STAR examples ready"
            ]
        elif week_num == 2:
            goals = [
                "Solve intermediate-level problems consistently",
                "Deliver confident behavioral responses",
                "Understand company's technical approach",
                "Have detailed STAR examples for key experiences"
            ]
        elif week_num == 3:
            goals = [
                "Complete full mock interview comfortably",
                "Explain system design decisions clearly",
                "Handle challenging technical questions",
                "Show deep company and role understanding"
            ]
        else:  # Week 4
            goals = [
                "Achieve interview readiness confidence",
                "Handle any question type smoothly",
                "Demonstrate authentic enthusiasm",
                "Show comprehensive preparation"
            ]

        return goals

    async def generate_star_examples(self, candidate_profile: Dict[str, Any],
                                  focus_areas: List[Dict[str, Any]]) -> Dict[str, Dict[str, str]]:
        """Generate personalized STAR method examples"""

        # Generate examples based on candidate experience and focus areas
        star_examples = {}

        # Project-based example
        star_examples["project_success"] = {
            "situation": "Led development of a customer-facing analytics dashboard used by 500+ users daily.",
            "task": "Design and implement a scalable solution that could handle real-time data updates and complex queries.",
            "action": "Coordinated with product and design teams to define requirements, chose appropriate technologies (React, Node.js, PostgreSQL), implemented caching strategies, and established monitoring and alerting.",
            "result": "Launched ahead of schedule, achieved 99.9% uptime, and received positive feedback leading to 40% increase in user engagement."
        }

        # Problem-solving example
        star_examples["problem_solving"] = {
            "situation": "Production API was experiencing intermittent failures affecting 1000+ users during peak hours.",
            "task": "Diagnose root cause and implement permanent solution within 24-hour SLA.",
            "action": "Conducted systematic debugging using logs and monitoring tools, identified memory leak in connection pooling, worked with SRE team to implement circuit breaker pattern and proper resource cleanup.",
            "result": "Resolved all failures, improved system reliability to 99.99% uptime, and documented runbook for future incidents."
        }

        # Leadership example
        star_examples["leadership"] = {
            "situation": "Joined a team of 8 developers working on legacy codebase with inconsistent practices.",
            "task": "Establish development standards and improve code quality while maintaining delivery velocity.",
            "action": "Organized team workshops to define coding standards, implemented code review process, introduced automated testing, and provided individual mentoring sessions.",
            "result": "Reduced bug rate by 60%, improved sprint completion from 70% to 95%, and team satisfaction scores increased by 35%."
        }

        return star_examples
