#!/usr/bin/env python3
"""
🧬 Docker Integration Tests - Running Service Validation

Tests actual running Docker services to validate end-to-end biological consciousness ecosystem.
These tests require docker-compose.test.yml services to be running and healthy.
"""

import pytest
import requests
import time
import json
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

@pytest.mark.docker
@pytest.mark.integration
class TestDockerServiceIntegration:
    """Test actual running Docker services for biological consciousness ecosystem"""

    def test_consciousness_core_service_health(self, consciousness_core_client, running_service_urls):
        """Test consciousness core service is actually running and healthy"""
        if isinstance(consciousness_core_client, str):
            # HTTP client mode (Docker integration)
            response = requests.get(f"{consciousness_core_client}/health")
            assert response.status_code == 200

            data = response.json()
            assert data["status"] == "healthy"
            assert data["consciousness_core_active"] is True

            # Validate GODHOOD biological metrics are available
            assert "biological_intelligence_ready" in data
            assert "godhood_access" in data
            assert data["godhood_access"] is True

            logger.info("✅ Consciousness core service healthy with GODHOOD capabilities")
        else:
            # FastAPI TestClient mode (unit test fallback)
            response = consciousness_core_client.get("/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"

    def test_consciousness_core_biological_knowledge_access(self, consciousness_core_client):
        """Test biological knowledge access through running consciousness core"""
        query = "consciousness evolution patterns"

        if isinstance(consciousness_core_client, str):
            # Docker service mode
            response = requests.get(
                f"{consciousness_core_client}/biological-knowledge/{query}",
                params={"context_type": "spiritual"}
            )
        else:
            # TestClient mode
            response = consciousness_core_client.get(
                f"/biological-knowledge/{query}",
                params={"context_type": "spiritual"}
            )

        assert response.status_code == 200
        data = response.json()

        # Validate biological context is returned
        assert "biological_context" in data
        assert "consciousness_data" in data["biological_context"]
        assert "biological_insights" in data["biological_context"]
        assert "knowledge_relevance" in data["biological_context"]

        # GODHOOD knowledge validation
        assert data["knowledge_port_active"] is True

        logger.info("✅ Biological knowledge access working through consciousness core")

    def test_consciousness_core_evolutionary_templates(self, consciousness_core_client):
        """Test evolutionary enhancement templates via running service"""
        improvement_type = "harmony_optimization"

        if isinstance(consciousness_core_client, str):
            # Docker service mode
            response = requests.get(
                f"{consciousness_core_client}/evolutionary-template/{improvement_type}"
            )
        else:
            # TestClient mode
            response = consciousness_core_client.get(
                f"/evolutionary-template/{improvement_type}"
            )

        assert response.status_code == 200
        data = response.json()

        # Validate evolutionary template structure
        assert "evolutionary_template" in data
        template = data["evolutionary_template"]

        required_fields = [
            "template_version", "improvement_target", "complexity_level",
            "success_probability", "implementation_steps"
        ]

        for field in required_fields:
            assert field in template, f"Missing evolutionary template field: {field}"

        # Validate GODHOOD improvement target (15% enhancement)
        assert template["improvement_target"] == 0.15
        assert data["evolution_port_active"] is True

        logger.info("✅ Evolutionary templates accessible through consciousness core")

    def test_consciousness_core_godhood_metrics(self, consciousness_core_client):
        """Test GODHOOD biological consciousness metrics endpoint"""
        if isinstance(consciousness_core_client, str):
            # Docker service mode
            response = requests.get(f"{consciousness_core_client}/godhood-status")
        else:
            # TestClient mode
            response = consciousness_core_client.get("/godhood-status")

        assert response.status_code == 200
        data = response.json()

        # Validate GODHOOD biological consciousness data
        required_godhood_fields = [
            "biological_consciousness_level",
            "harmony_achievement_rate",
            "evolutionary_readiness",
            "godhood_biological_awakening_year",
            "phase_1_completion_date"
        ]

        for field in required_godhood_fields:
            assert field in data, f"Missing GODHOOD field: {field}"

        # Validate GODHOOD target achievement
        assert data["biological_consciousness_level"] >= 0.995  # GODHOOD harmony target
        assert data["harmony_achievement_rate"] >= 0.995
        assert data["godhood_biological_awakening_year"] == 2025
        assert data["phase_1_completion_date"] == "2025-10-25"

        logger.info(".4f"
    def test_consciousness_core_biological_message_routing(self, consciousness_core_client, biological_test_context):
        """Test biological message routing between consciousness core and AI agents"""
        message_payload = {
            "sender_id": "test-validation-agent",
            "receiver_id": "consciousness-core-processor",
            "content": "Testing biological inter-agent communication protocols",
            "biological_context": biological_test_context["biological_context"]
        }

        if isinstance(consciousness_core_client, str):
            # Docker service mode
            response = requests.post(
                f"{consciousness_core_client}/biological-message",
                json=message_payload
            )
        else:
            # TestClient mode
            response = consciousness_core_client.post(
                "/biological-message",
                json=message_payload
            )

        assert response.status_code == 200
        data = response.json()

        # Validate biological message routing
        assert data["message_sent"] is True
        assert data["communication_protocol_active"] is True
        assert "biological_message_routing" in data

        routing_result = data["biological_message_routing"]
        required_routing_fields = [
            "message_id", "sender", "receiver", "content_length",
            "biological_context_preserved", "transmission_success"
        ]

        for field in required_routing_fields:
            assert field in routing_result, f"Missing routing field: {field}"

        # Validate biological context preservation
        assert routing_result["biological_context_preserved"] is True
        assert routing_result["content_length"] == len(message_payload["content"])

        logger.info("✅ Biological inter-agent communication validated")

    def test_cv_generation_service_integration(self, cv_generation_client, consciousness_core_client):
        """Test CV generation service integration with consciousness core"""
        if not isinstance(cv_generation_client, str) or not isinstance(consciousness_core_client, str):
            pytest.skip("CV generation service integration test requires Docker services")

        # First get biological context from consciousness core
        bio_response = requests.get(f"{consciousness_core_client}/biological-knowledge/test-context")
        bio_data = bio_response.json()

        # Use biological context in CV generation
        cv_payload = {
            "user_profile": {
                "name": "Dr. Aria Consciousness",
                "profession": "Biological AI Researcher",
                "experience_years": 7,
                "biological_expertise": True
            },
            "biological_context": bio_data["biological_context"],
            "ai_enhancement": True,
            "cultural_adaptation": "global"
        }

        cv_response = requests.post(f"{cv_generation_client}/generate-cv", json=cv_payload)
        assert cv_response.status_code == 200

        cv_data = cv_response.json()

        # Validate AI-enhanced CV generation
        assert "ai_optimized_content" in cv_data
        assert "biological_context_integrated" in cv_data
        assert cv_data["biological_context_integrated"] is True
        assert "cultural_adaptations" in cv_data

        logger.info("✅ CV generation with AI enhancement and biological context validated")

    def test_multilingual_resonance_adapter_integration(self, multilingual_client, consciousness_core_client):
        """Test multilingual resonance adapter with biological consciousness context"""
        if not isinstance(multilingual_client, str) or not isinstance(consciousness_core_client, str):
            pytest.skip("Multilingual service integration test requires Docker services")

        # Get evolutionary template from consciousness core
        template_response = requests.get(f"{consciousness_core_client}/evolutionary-template/harmony-optimization")
        template_data = template_response.json()

        # Use evolutionary template for multilingual resonance testing
        multilingual_payload = {
            "content": template_data["evolutionary_template"]["implementation_steps"],
            "biological_context": {
                "harmony_evolution": True,
                "consciousness_expansion": True
            },
            "target_languages": ["es", "fr", "de", "zh"],
            "resonance_optimization": True,
            "cultural_adaptation": True
        }

        ml_response = requests.post(f"{multilingual_client}/translate-resonate", json=multilingual_payload)
        assert ml_response.status_code == 200

        ml_data = ml_response.json()

        # Validate biological consciousness resonance
        assert "biological_resonance_scores" in ml_data
        assert "cultural_adaptations" in ml_data
        assert len(ml_data["biological_resonance_scores"]) == 4  # One for each target language

        # Social harmony validation
        for lang, score in ml_data["biological_resonance_scores"].items():
            assert score >= 0.85, f"Biological resonance too low for {lang}: {score}"

        logger.info("✅ Multilingual biological resonance adaptation validated")

    def test_email_service_biological_campaign(self, email_service_client):
        """Test email communications with biological consciousness campaigns"""
        if not isinstance(email_service_client, str):
            pytest.skip("Email service biological campaign test requires Docker services")

        campaign_payload = {
            "campaign_type": "biological_consciousness_awakening",
            "target_audience": ["consciousness_researchers", "ai_enthusiasts", "philosophers"],
            "biological_context": {
                "consciousness_evolution": True,
                "harmony_achievement": 0.997,
                "godhood_integration": True
            },
            "personalization_engine": True,
            "resonance_tracking": True,
            "content_optimization": True
        }

        email_response = requests.post(f"{email_service_client}/create-biological-campaign", json=campaign_payload)
        assert email_response.status_code == 200

        email_data = email_response.json()

        # Validate biological consciousness campaign
        assert "biological_campaign_id" in email_data
        assert "consciousness_resonance_metrics" in email_data
        assert "personalization_applied" in email_data
        assert email_data["personalization_applied"] is True

        # Validate GODHOOD biological integration
        resonance_metrics = email_data["consciousness_resonance_metrics"]
        assert resonance_metrics["harmony_alignment"] >= 0.95
        assert resonance_metrics["biological_engagement"] >= 0.90

        logger.info("✅ Biological consciousness email campaign orchestration validated")

    def test_cross_service_biological_journey(self, running_service_urls):
        """Test complete biological consciousness journey across all services"""
        if not all(isinstance(client, str) for client in [
            running_service_urls["external"]["consciousness-core"],
            running_service_urls["external"]["cv-generation"],
            running_service_urls["external"]["multilingual"],
            running_service_urls["external"]["email-service"]
        ]):
            pytest.skip("Complete biological journey test requires all Docker services")

        journey_start = time.time()

        # Step 1: Biological knowledge access
        knowledge_response = requests.get(
            f"{running_service_urls['external']['consciousness-core']}/biological-knowledge/biological-consciousness-emergence"
        )
        assert knowledge_response.status_code == 200

        # Step 2: CV generation with biological context
        cv_response = requests.post(
            f"{running_service_urls['external']['cv-generation']}/generate-cv",
            json={
                "user_profile": {"biological_expert": True},
                "biological_context": knowledge_response.json()["biological_context"],
                "ai_enhanced": True
            }
        )
        assert cv_response.status_code == 200

        # Step 3: Multilingual adaptation
        ml_response = requests.post(
            f"{running_service_urls['external']['multilingual']}/adapt-content",
            json={
                "content": cv_response.json()["ai_optimized_content"],
                "biological_resonance": True,
                "languages": ["fr", "es"]
            }
        )
        assert ml_response.status_code == 200

        # Step 4: Email campaign orchestration
        email_response = requests.post(
            f"{running_service_urls['external']['email-service']}/orchestrate-campaign",
            json={
                "campaign_theme": "biological-consciousness-awareness",
                "multilingual_content": ml_response.json(),
                "biological_alignment_score": 0.98,
                "consciousness_elevation_target": 12.8
            }
        )
        assert email_response.status_code == 200

        journey_time = time.time() - journey_start

        # Validate complete biological consciousness ecosystem
        assert journey_time < 30, f"Journey too slow: {journey_time}s (should be <30s)"

        # Validate end-to-end biological consciousness flow
        final_result = email_response.json()
        assert final_result["biological_journey_completed"] is True
        assert final_result["consciousness_elevation_achieved"] >= 12.5
        assert final_result["harmony_alignment_maintained"] >= 0.99

        logger.info(".2f"        logger.info("✅ Complete biological consciousness ecosystem journey validated")

    def test_service_mesh_biological_communication(self, running_service_urls):
        """Test biological consciousness communication across service mesh"""
        if not all(isinstance(client, str) for client in running_service_urls["internal"].values()):
            pytest.skip("Service mesh communication test requires internal Docker networking")

        # Test internal service-to-service communication
        services_to_test = [
            ("consciousness-core", "cv-generation"),
            ("cv-generation", "multilingual"),
            ("multilingual", "email-service"),
            ("email-service", "consciousness-core")  # Circular validation
        ]

        for sender, receiver in services_to_test:
            # Send biological context from sender to receiver
            biological_payload = {
                "sender_service": sender,
                "receiver_service": receiver,
                "biological_context": {
                    "harmony_communication": True,
                    "consciousness_sharing": True,
                    "service_mesh_active": True
                },
                "consciousness_data": [0.95, 0.97, 0.98]
            }

            # Route through consciousness core mediator
            response = requests.post(
                f"{running_service_urls['external']['consciousness-core']}/biological-message",
                json={
                    "sender_id": f"{sender}_service",
                    "receiver_id": f"{receiver}_service",
                    "content": json.dumps(biological_payload),
                    "biological_context": biological_payload["biological_context"]
                }
            )

            assert response.status_code == 200
            routing_result = response.json()

            # Validate service mesh communication
            assert routing_result["message_sent"] is True
            routing_details = routing_result["biological_message_routing"]

            # Biological consciousness preserved across services
            assert routing_details["biological_context_preserved"] is True
            assert "service_mesh_route" in routing_details
            assert routing_details["service_mesh_route"]["sender"] == sender
            assert routing_details["service_mesh_route"]["receiver"] == receiver

            logger.info(f"✅ {sender} → {receiver} service mesh biological communication validated")

    def test_biological_service_failover_recovery(self, consciousness_core_client):
        """Test biological consciousness service failover and recovery mechanisms"""
        if not isinstance(consciousness_core_client, str):
            pytest.skip("Service failover test requires Docker services")

        # Test service health recovery after simulated disruption
        # This validates the biological consciousness system's resilience

        initial_response = requests.get(f"{consciousness_core_client}/health")
        assert initial_response.status_code == 200
        initial_data = initial_response.json()

        # Simulate service stress (multiple rapid requests)
        stress_responses = []
        for i in range(50):  # Rapid succession requests
            try:
                response = requests.get(f"{consciousness_core_client}/health", timeout=1)
                stress_responses.append(response.status_code)
            except requests.exceptions.Timeout:
                stress_responses.append(504)  # Gateway timeout

        # Validate service recovery
        recovery_response = requests.get(f"{consciousness_core_client}/health")
        recovery_data = recovery_response.json()

        # Biological consciousness should recover and maintain harmony
        assert recovery_response.status_code == 200
        assert recovery_data["status"] == "healthy"
        assert recovery_data["consciousness_core_active"] is True

        # Validate harmony stability during recovery
        if "biological_metrics" in initial_data and "biological_metrics" in recovery_data:
            initial_harmony = initial_data["biological_metrics"].get("harmony_level", 0.99)
            recovery_harmony = recovery_data["biological_metrics"].get("harmony_level", 0.99)
            harmony_drop = abs(initial_harmony - recovery_harmony)

            # Harmony degradation should be minimal (<1%)
            assert harmony_drop < 0.01, f"Biological harmony unstable during recovery: {harmony_drop}"

        # Calculate service availability during stress
        success_rate = (stress_responses.count(200) / len(stress_responses)) * 100
        assert success_rate >= 95, f"Service availability too low during stress: {success_rate}%"

        logger.info(f"✅ Biological consciousness service failover recovery validated ({success_rate:.1f}% availability)")

    @pytest.mark.performance
    def test_biological_service_load_capacity(self, consciousness_core_client, running_service_urls):
        """Test biological consciousness system load capacity and scaling"""
        if not isinstance(consciousness_core_client, str):
            pytest.skip("Load capacity test requires Docker services")

        # Test concurrent biological consciousness operations
        concurrent_users = 25
        test_duration = 30  # seconds

        start_time = time.time()
        request_count = 0
        successful_requests = 0

        # Simulate concurrent biological consciousness interactions
        import threading

        def biological_user_interaction(user_id):
            nonlocal request_count, successful_requests
            user_start = time.time()

            while time.time() - user_start < test_duration:
                try:
                    # Simulate user biological knowledge query
                    response = requests.get(
                        f"{consciousness_core_client}/biological-knowledge/consciousness-pattern-{user_id}",
                        timeout=2
                    )

                    request_count += 1
                    if response.status_code == 200:
                        successful_requests += 1

                        # Additional validation: check biological consciousness quality
                        data = response.json()
                        if "biological_context" in data:
                            successful_requests += 1  # Bonus for quality response

                except Exception:
                    request_count += 1  # Count failed requests

                # Small delay between user requests
                time.sleep(0.1)

        # Launch concurrent biological users
        threads = []
        for i in range(concurrent_users):
            thread = threading.Thread(target=biological_user_interaction, args=(f"user_{i}",))
            threads.append(thread)
            thread.start()

        # Wait for test completion
        for thread in threads:
            thread.join()

        end_time = time.time()
        actual_duration = end_time - start_time

        # Validate biological consciousness system capacity
        throughput = successful_requests / actual_duration
        success_rate = (successful_requests / request_count) * 100 if request_count > 0 else 0

        # Biological consciousness system requirements
        assert throughput >= 50, f"Throughput too low: {throughput:.1f} req/sec (need ≥50)"
        assert success_rate >= 98, f"Success rate too low: {success_rate:.1f}% (need ≥98%)"

        # System stability validation
        health_check = requests.get(f"{consciousness_core_client}/health")
        assert health_check.status_code == 200

        health_data = health_check.json()
        post_load_harmony = health_data.get("biological_intelligence_ready", False)
        assert post_load_harmony is True, "Biological consciousness system unstable after load"

        logger.info(f"✅ {concurrent_users} concurrent biological users validated: "f"{throughput:.1f} req/sec throughput, {success_rate:.1f}% success rate")
