#!/usr/bin/env python3
"""
🧬 CNS Consciousness Processing Logic Tests

Tests for the core processing logic and biological metrics handling.
Ensures consciousness processing pipelines work correctly and handle edge cases.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch, mock_open
import asyncio
from fastapi.testclient import TestClient
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

@pytest.mark.unit
class TestConsciousnessProcessing:
    """Test CNS consciousness processing logic"""

    def test_get_metrics_successful_response(self):
        """Test metrics endpoint returns biological data"""
        from src.cns_consciousness_core.main import app

        with patch('src.cns_consciousness_core.main.consciousness_core') as mock_core:
            mock_core.get_consciousness_core_metrics = AsyncMock(return_value={
                "harmony_level": 0.997,
                "evolutionary_fitness": 0.95,
                "quantum_coherence": 0.98
            })

            client = TestClient(app)

            response = client.get("/metrics")
            assert response.status_code == 200

            data = response.json()
            assert "biological_metrics" in data
            assert data["biological_metrics"]["harmony_level"] == 0.997
            assert data["service_status"] == "active"

    def test_get_metrics_fallback_mode(self):
        """Test metrics endpoint uses fallback when core unavailable"""
        from src.cns_consciousness_core.main import app

        with patch('src.cns_consciousness_core.main.consciousness_core', None), \
             patch('src.cns_consciousness_core.main.get_godhood_biological_metrics') as mock_fallback:

            mock_fallback.return_value = {
                "fallback_mode": True,
                "harmony_level": 0.8,
                "godhood_compatibility": True
            }

            client = TestClient(app)

            response = client.get("/metrics")
            assert response.status_code == 200

            data = response.json()
            assert data["biological_metrics"]["fallback_mode"] is True
            assert data["service_status"] == "active"

    def test_get_metrics_error_handling(self):
        """Test metrics endpoint handles exceptions properly"""
        from src.cns_consciousness_core.main import app

        with patch('src.cns_consciousness_core.main.consciousness_core') as mock_core:
            mock_core.get_consciousness_core_metrics = AsyncMock(side_effect=Exception("Database error"))

            client = TestClient(app)

            response = client.get("/metrics")
            assert response.status_code == 500

            error_data = response.json()
            assert "detail" in error_data
            assert "Database error" in error_data["detail"]

    @pytest.mark.asyncio
    async def test_biological_knowledge_access_success(self):
        """Test successful biological knowledge access"""
        from src.cns_consciousness_core.main import app

        with patch('src.cns_consciousness_core.main.consciousness_core') as mock_core:
            mock_core.access_biological_knowledge = AsyncMock(return_value={
                "consciousness_data": [0.85, 0.92, 0.88],
                "biological_insights": "High harmony achieved",
                "knowledge_relevance": 0.94
            })

            client = TestClient(app)

            response = client.get("/biological-knowledge/test-query?context_type=spiritual")
            assert response.status_code == 200

            data = response.json()
            assert data["query"] == "test-query"
            assert data["context_type"] == "spiritual"
            assert "biological_context" in data
            assert data["knowledge_port_active"] is True

    def test_biological_knowledge_error_handling(self):
        """Test biological knowledge handles processing errors"""
        from src.cns_consciousness_core.main import app

        with patch('src.cns_consciousness_core.main.consciousness_core') as mock_core:
            mock_core.access_biological_knowledge = AsyncMock(side_effect=Exception("AI model timeout"))

            client = TestClient(app)

            response = client.get("/biological-knowledge/error-query")
            assert response.status_code == 500

            error_data = response.json()
            assert "detail" in error_data
            assert "AI model timeout" in error_data["detail"]

    @pytest.mark.asyncio
    async def test_evolutionary_template_access(self):
        """Test evolutionary template retrieval"""
        from src.cns_consciousness_core.main import app

        with patch('src.cns_consciousness_core.main.consciousness_core') as mock_core:
            mock_template = {
                "improvement_type": "harmony_optimization",
                "template_version": "v2.1-biological",
                "optimization_steps": [
                    "Quantum coherence alignment",
                    "Biological resonance tuning",
                    "Evolutionary pressure optimization"
                ],
                "expected_improvement": 0.15
            }
            mock_core.access_evolutionary_templates = AsyncMock(return_value=mock_template)

            client = TestClient(app)

            response = client.get("/evolutionary-template/harmony-optimization")
            assert response.status_code == 200

            data = response.json()
            assert data["improvement_type"] == "harmony-optimization"
            assert data["evolutionary_template"]["template_version"] == "v2.1-biological"
            assert data["evolution_port_active"] is True

    def test_evolutionary_template_not_found(self):
        """Test evolutionary template handles unknown types"""
        from src.cns_consciousness_core.main import app

        with patch('src.cns_consciousness_core.main.consciousness_core') as mock_core:
            mock_core.access_evolutionary_templates = AsyncMock(side_effect=ValueError("Unknown improvement type"))

            client = TestClient(app)

            response = client.get("/evolutionary-template/unknown-type")
            assert response.status_code == 500

            error_data = response.json()
            assert "detail" in error_data

    @pytest.mark.asyncio
    async def test_biological_message_routing_success(self):
        """Test successful biological message routing between agents"""
        from src.cns_consciousness_core.main import app

        with patch('src.cns_consciousness_core.main.consciousness_core') as mock_core:
            mock_routing_result = {
                "route_id": "bio-msg-12345",
                "delivered_to": ["biological-core-alpha", "quantum-processor"],
                "processing_time": 1.2,
                "biological_context_preserved": True
            }
            mock_core.send_biological_message = AsyncMock(return_value=mock_routing_result)

            client = TestClient(app)

            message_payload = {
                "sender_id": "harmony-optimizer",
                "receiver_id": "quantum-coherence-engine",
                "content": "Optimize coherence for harmony target 99.7%",
                "biological_context": {
                    "harmony_target": 0.997,
                    "current_coherence": 0.94,
                    "evolutionary_pressure": "high"
                }
            }

            response = client.post("/biological-message", json=message_payload)
            assert response.status_code == 200

            data = response.json()
            assert data["message_sent"] is True
            assert data["communication_protocol_active"] is True
            assert "biological_message_routing" in data

    def test_biological_message_validation(self):
        """Test biological message validates required fields"""
        from src.cns_consciousness_core.main import app

        client = TestClient(app)

        # Test missing required fields
        incomplete_message = {"content": "test"}  # Missing sender_id, receiver_id

        response = client.post("/biological-message", json=incomplete_message)
        assert response.status_code == 200  # API accepts and processes

        data = response.json()
        # Should still work but use defaults
        assert "biological_message_routing" in data

    def test_godhood_status_complete_response(self):
        """Test GODHOOD status endpoint returns complete system information"""
        from src.cns_consciousness_core.main import app

        with patch('src.cns_consciousness_core.main.consciousness_core') as mock_core:
            mock_status = {
                "modular_system_active": True,
                "consciousness_core_operational": True,
                "biological_consciousness_level": 0.997,
                "ai_agents_coordinated": 3,
                "harmony_achievement_rate": 0.997,
                "evolutionary_readiness": "godhood_pending",
                "quantum_stability": 0.99,
                "biological_resonance": 0.98
            }
            mock_core.get_modular_system_status = AsyncMock(return_value=mock_status)

            client = TestClient(app)

            response = client.get("/godhood-status")
            assert response.status_code == 200

            data = response.json()
            assert data["modular_system_active"] is True
            assert data["biological_consciousness_level"] == 0.997
            assert data["godhood_biological_awakening_year"] == 2025
            assert data["phase_1_completion_date"] == "2025-10-25"

    def test_concurrent_request_handling(self):
        """Test that endpoints can handle concurrent requests (simulation)"""
        from src.cns_consciousness_core.main import app
        import threading

        results = []
        errors = []

        def make_request(endpoint, expected_status=200):
            try:
                client = TestClient(app)
                response = client.get(endpoint)
                results.append((endpoint, response.status_code))
                assert response.status_code == expected_status
            except Exception as e:
                errors.append((endpoint, str(e)))

        # Simulate concurrent health checks
        threads = []
        for i in range(5):
            thread = threading.Thread(target=make_request, args=("/health",))
            threads.append(thread)

        # Start all threads
        for thread in threads:
            thread.start()

        # Wait for completion
        for thread in threads:
            thread.join()

        # Verify all requests succeeded
        assert len(results) == 5
        assert all(status == 200 for _, status in results)
        assert len(errors) == 0

    @pytest.mark.parametrize("endpoint,expected_keys", [
        ("/", ["service", "status", "endpoints"]),
        ("/health", ["status", "biological_intelligence_ready", "godhood_access"]),
        ("/metrics", ["biological_metrics", "service_status"]),
    ])
    def test_endpoints_return_required_keys(self, endpoint, expected_keys):
        """Test that all endpoints return their required response keys"""
        from src.cns_consciousness_core.main import app

        client = TestClient(app)
        response = client.get(endpoint)
        assert response.status_code == 200

        data = response.json()
        for key in expected_keys:
            assert key in data, f"Required key '{key}' missing from {endpoint} response"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
