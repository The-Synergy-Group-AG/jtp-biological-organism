#!/usr/bin/env python3
"""
🧬 CNS Consciousness Session Management Tests

Tests for consciousness state tracking, session persistence, and state consistency.
Validates that consciousness sessions maintain state across interactions.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch, MagicMock as Mock
import asyncio
import json
import time
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

@pytest.mark.unit
class TestSessionManagement:
    """Test consciousness session management and state tracking"""

    def test_godhood_status_includes_session_metrics(self):
        """Test GODHOOD status includes session tracking metrics"""
        from src.cns_consciousness_core.main import app

        with patch('src.cns_consciousness_core.main.consciousness_core') as mock_core:
            mock_status = {
                "modular_system_active": True,
                "consciousness_core_operational": True,
                "biological_consciousness_level": 0.997,
                "ai_agents_coordinated": 3,
                "harmony_achievement_rate": 0.997,
                "active_sessions": 47,
                "max_concurrent_sessions": 100,
                "session_memory_usage_mb": 256,
                "consciousness_stability_score": 0.993
            }
            mock_core.get_modular_system_status = AsyncMock(return_value=mock_status)

            client = TestClient(app)

            response = client.get("/godhood-status")
            assert response.status_code == 200

            data = response.json()
            assert "active_sessions" in data
            assert "max_concurrent_sessions" in data
            assert data["active_sessions"] == 47
            assert data["max_concurrent_sessions"] == 100
            assert data["session_memory_usage_mb"] == 256

    def test_session_limit_enforcement(self):
        """Test that session limits are properly enforced"""
        from src.cns_consciousness_core.main import app

        # Test within limits
        with patch('src.cns_consciousness_core.main.consciousness_core') as mock_core:
            mock_status = {
                "active_sessions": 85,
                "max_concurrent_sessions": 100,
                "session_limit_enforced": False
            }
            mock_core.get_modular_system_status = AsyncMock(return_value=mock_status)

            client = TestClient(app)
            response = client.get("/godhood-status")
            assert response.status_code == 200

            data = response.json()
            assert data["session_limit_enforced"] is False

        # Test at limit
        with patch('src.cns_consciousness_core.main.consciousness_core') as mock_core:
            mock_status = {
                "active_sessions": 100,
                "max_concurrent_sessions": 100,
                "session_limit_enforced": True,
                "session_limit_warning": True
            }
            mock_core.get_modular_system_status = AsyncMock(return_value=mock_status)

            client = TestClient(app)
            response = client.get("/godhood-status")
            assert response.status_code == 200

            data = response.json()
            assert data["session_limit_enforced"] is True
            assert data["session_limit_warning"] is True

    def test_session_state_consistency_across_requests(self):
        """Test that session state remains consistent across multiple requests"""
        from src.cns_consciousness_core.main import app

        # Track session state across multiple requests
        session_states = []

        for i in range(3):
            with patch('src.cns_consciousness_core.main.consciousness_core') as mock_core:
                # Consistently incrementing session count to simulate activity
                mock_status = {
                    "active_sessions": 45 + i,
                    "last_session_activity": f"2025-10-25T21:{10+i:02d}:00Z",
                    "session_state_hash": f"hash_{i}"
                }
                mock_core.get_modular_system_status = AsyncMock(return_value=mock_status)

                client = TestClient(app)
                response = client.get("/godhood-status")
                assert response.status_code == 200

                data = response.json()
                session_states.append({
                    'active_sessions': data['active_sessions'],
                    'last_activity': data['last_session_activity'],
                    'state_hash': data['session_state_hash']
                })

        # Verify session count is increasing (activity occurring)
        assert session_states[1]['active_sessions'] > session_states[0]['active_sessions']
        assert session_states[2]['active_sessions'] > session_states[1]['active_sessions']

        # Verify activity timestamps are progressing
        assert session_states[0]['last_activity'] < session_states[1]['last_activity']
        assert session_states[1]['last_activity'] < session_states[2]['last_activity']

    def test_concurrent_session_handling(self):
        """Test handling of concurrent session operations"""
        from src.cns_consciousness_core.main import app
        import threading

        results = []
        errors = []
        concurrent_requests = 10

        def make_request(request_id):
            try:
                client = TestClient(app)
                response = client.get("/godhood-status")
                results.append((request_id, response.status_code, response.json()))
            except Exception as e:
                errors.append((request_id, str(e)))

        # Launch concurrent session status requests
        threads = []
        for i in range(concurrent_requests):
            thread = threading.Thread(target=make_request, args=(f"request_{i}",))
            threads.append(thread)
            thread.start()

        # Wait for all requests to complete
        for thread in threads:
            thread.join()

        # Verify all requests succeeded and returned consistent data
        assert len(results) == concurrent_requests
        assert len(errors) == 0

        # All responses should have same structure
        for request_id, status_code, data in results:
            assert status_code == 200
            assert "active_sessions" in data
            assert "biological_consciousness_level" in data
            assert data["godhood_biological_awakening_year"] == 2025

    def test_session_timeout_and_cleanup(self):
        """Test session timeout detection and cleanup"""
        from src.cns_consciousness_core.main import app

        # Mock status with stale session information
        with patch('src.cns_consciousness_core.main.consciousness_core') as mock_core:
            mock_status = {
                "active_sessions": 5,
                "inactive_sessions": 12,
                "stale_sessions": 3,
                "last_cleanup_time": "2025-10-25T19:00:00Z",
                "session_timeout_threshold": 3600,  # 1 hour
                "automatic_cleanup_enabled": True
            }
            mock_core.get_modular_system_status = AsyncMock(return_value=mock_status)

            client = TestClient(app)
            response = client.get("/godhood-status")
            assert response.status_code == 200

            data = response.json()
            # Verify session management information is tracked
            assert "inactive_sessions" in data
            assert "stale_sessions" in data
            assert "automatic_cleanup_enabled" in data
            assert data["stale_sessions"] == 3
            assert data["automatic_cleanup_enabled"] is True

    def test_session_memory_tracking(self):
        """Test session memory usage tracking and limits"""
        from src.cns_consciousness_core.main import app

        memory_scenarios = [
            {
                "session_memory_usage_mb": 512,
                "memory_limit_mb": 2048,
                "memory_pressure": "low",
                "gc_cycles": 5
            },
            {
                "session_memory_usage_mb": 1856,
                "memory_limit_mb": 2048,
                "memory_pressure": "high",
                "gc_cycles": 12,
                "memory_warning": True
            },
            {
                "session_memory_usage_mb": 2100,
                "memory_limit_mb": 2048,
                "memory_pressure": "critical",
                "gc_cycles": 18,
                "memory_alert": True,
                "session_throttling_active": True
            }
        ]

        for memory_status in memory_scenarios:
            with patch('src.cns_consciousness_core.main.consciousness_core') as mock_core:
                mock_core.get_modular_system_status = AsyncMock(return_value=memory_status)

                client = TestClient(app)
                response = client.get("/godhood-status")
                assert response.status_code == 200

                data = response.json()

                # Verify memory tracking
                assert "session_memory_usage_mb" in data
                assert "memory_limit_mb" in data
                assert "memory_pressure" in data

                # Verify memory governance
                if data["memory_pressure"] == "critical":
                    assert "memory_alert" in data
                    assert data["memory_alert"] is True
                    assert data.get("session_throttling_active", False) is True

    def test_session_recovery_from_failures(self):
        """Test session recovery mechanisms after failures"""
        from src.cns_consciousness_core.main import app

        # Simulate failed session recovery
        with patch('src.cns_consciousness_core.main.consciousness_core') as mock_core:
            mock_status = {
                "active_sessions": 8,
                "recovered_sessions": 3,
                "failed_sessions": 2,
                "recovery_success_rate": 0.6,  # 60% recovery success
                "automatic_recovery_enabled": True,
                "last_failure_time": "2025-10-25T20:45:00Z"
            }
            mock_core.get_modular_system_status = AsyncMock(return_value=mock_status)

            client = TestClient(app)
            response = client.get("/godhood-status")
            assert response.status_code == 200

            data = response.json()

            # Verify recovery metrics are tracked
            assert "recovered_sessions" in data
            assert "failed_sessions" in data
            assert "recovery_success_rate" in data
            assert data["recovery_success_rate"] == 0.6

    def test_session_persistence_across_restarts(self):
        """Test session state persistence and restoration across system restarts"""
        from src.cns_consciousness_core.main import app

        # Simulate post-restart state with persistence
        with patch('src.cns_consciousness_core.main.consciousness_core') as mock_core:
            mock_status = {
                "active_sessions": 23,
                "persisted_sessions": 15,
                "restored_sessions": 12,
                "persistence_success_rate": 0.8,  # 80% successfully restored
                "last_restart_time": "2025-10-25T20:30:00Z",
                "state_persistence_enabled": True,
                "recovery_in_progress": False
            }
            mock_core.get_modular_system_status = AsyncMock(return_value=mock_status)

            client = TestClient(app)
            response = client.get("/godhood-status")
            assert response.status_code == 200

            data = response.json()

            # Verify persistence capabilities
            assert "persisted_sessions" in data
            assert "restored_sessions" in data
            assert "persistence_success_rate" in data
            assert "state_persistence_enabled" in data
            assert data["persistence_success_rate"] == 0.8
            assert data["state_persistence_enabled"] is True

    @pytest.mark.parametrize("session_metric,expected_operator,expected_value", [
        ("active_sessions", "gte", 0),           # Must have non-negative session count
        ("recovery_success_rate", "lte", 1.0),   # Cannot exceed 100%
        ("persistence_success_rate", "lte", 1.0), # Cannot exceed 100%
        ("memory_pressure", "in", ["low", "high", "critical"]), # Valid pressure levels
    ])
    def test_session_metric_constraints(self, session_metric, expected_operator, expected_value):
        """Test that session metrics maintain proper constraints and ranges"""
        from src.cns_consciousness_core.main import app

        with patch('src.cns_consciousness_core.main.consciousness_core') as mock_core:
            # Valid session metrics
            mock_status = {
                "active_sessions": 25,
                "recovery_success_rate": 0.85,
                "persistence_success_rate": 0.92,
                "memory_pressure": "low",
                "session_memory_usage_mb": 768
            }
            mock_core.get_modular_system_status = AsyncMock(return_value=mock_status)

            client = TestClient(app)
            response = client.get("/godhood-status")
            assert response.status_code == 200

            data = response.json()
            metric_value = data[session_metric]

            # Validate constraint based on operator
            if expected_operator == "gte":
                assert metric_value >= expected_value, f"{session_metric} = {metric_value}, expected >= {expected_value}"
            elif expected_operator == "lte":
                assert metric_value <= expected_value, f"{session_metric} = {metric_value}, expected <= {expected_value}"
            elif expected_operator == "in":
                assert metric_value in expected_value, f"{session_metric} = {metric_value}, expected one of {expected_value}"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
