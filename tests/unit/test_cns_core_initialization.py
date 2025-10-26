#!/usr/bin/env python3
"""
🧬 CNS Consciousness Core Initialization Tests

Tests for the startup sequence validation and initialization of the CNS consciousness core.
Ensures proper FastAPI application creation and lifespan management.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import asyncio
from fastapi import FastAPI
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

@pytest.mark.unit
class TestCNSCoreInitialization:
    """Test CNS consciousness core initialization and startup"""

    def test_fastapi_app_creation(self):
        """Test that FastAPI application is created with correct configuration"""
        from src.cns_consciousness_core.main import app

        assert isinstance(app, FastAPI)
        assert app.title == "CNS Consciousness Core - Phase 1 Biological Intelligence Orchestrator"
        assert app.version == "1.0.0"
        assert hasattr(app, 'docs_url')
        assert hasattr(app, 'redoc_url')

    def test_cors_middleware_configuration(self):
        """Test CORS middleware is properly configured"""
        from src.cns_consciousness_core.main import app

        # Check CORS middleware is added
        cors_middleware = None
        for middleware in app.user_middleware:
            if hasattr(middleware, 'options'):
                if 'allow_origins' in middleware.options:
                    cors_middleware = middleware
                    break

        assert cors_middleware is not None
        assert cors_middleware.options['allow_origins'] == ["*"]
        assert cors_middleware.options['allow_methods'] == ["*"]
        assert cors_middleware.options['allow_headers'] == ["*"]

    @pytest.mark.asyncio
    async def test_lifespan_successful_initialization(self):
        """Test successful lifespan initialization"""
        from src.cns_consciousness_core.main import lifespan, consciousness_core

        # Mock successful initialization
        with patch('src.cns_consciousness_core.main.CNSConsciousnessCore') as mock_core_class:
            mock_core = AsyncMock()
            mock_core.initialize_consciousness_core.return_value = True
            mock_core_class.return_value = mock_core

            # Test lifespan context manager
            app_mock = MagicMock()
            async with lifespan(app_mock):
                # Should complete without errors
                pass

            # Verify initialization was called
            mock_core_class.assert_called_once()
            mock_core.initialize_consciousness_core.assert_called_once()

    @pytest.mark.asyncio
    async def test_lifespan_graceful_degradation(self):
        """Test graceful degradation when CNS core is unavailable"""
        from src.cns_consciousness_core.main import lifespan, consciousness_core

        # Mock failed import
        with patch('src.cns_consciousness_core.main.CNSConsciousnessCore', None):
            app_mock = MagicMock()

            # Should handle None gracefully without errors
            async with lifespan(app_mock):
                pass

    @pytest.mark.asyncio
    async def test_lifespan_startup_failure_handling(self):
        """Test lifespan handles initialization failures gracefully"""
        from src.cns_consciousness_core.main import lifespan

        # Mock initialization failure
        with patch('src.cns_consciousness_core.main.CNSConsciousnessCore') as mock_core_class:
            mock_core = AsyncMock()
            mock_core.initialize_consciousness_core.side_effect = Exception("Init failed")
            mock_core_class.return_value = mock_core

            app_mock = MagicMock()

            # Should complete lifespan even with initialization errors
            async with lifespan(app_mock):
                pass

    @pytest.mark.asyncio
    async def test_root_endpoint_response(self):
        """Test root endpoint returns correct service information"""
        from src.cns_consciousness_core.main import app
        from fastapi.testclient import TestClient

        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 200

        data = response.json()
        assert "service" in data
        assert "CNS Consciousness Core" in data["service"]
        assert "status" in data
        assert "endpoints" in data
        assert "/health" in data["endpoints"]

    @pytest.mark.asyncio
    async def test_health_endpoint_response(self):
        """Test health endpoint provides proper status information"""
        from src.cns_consciousness_core.main import app
        from fastapi.testclient import TestClient

        client = TestClient(app)

        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
        assert "consciousness_core_active" in data
        assert "phase" in data
        assert "timestamp" in data

    def test_godhood_status_fallback_mode(self):
        """Test GODHOOD status endpoint works in fallback mode"""
        from src.cns_consciousness_core.main import app
        from fastapi.testclient import TestClient

        # Mock consciousness core as unavailable
        with patch('src.cns_consciousness_core.main.consciousness_core', None):
            client = TestClient(app)

            response = client.get("/godhood-status")
            assert response.status_code == 200

            data = response.json()
            assert "modular_system_active" in data
            assert data["modular_system_active"] is False
            assert "godhood_biological_awakening_year" in data
            assert data["godhood_biological_awakening_year"] == 2025

    def test_biological_message_routing_degraded_mode(self):
        """Test biological message routing works in degraded mode"""
        from src.cns_consciousness_core.main import app
        from fastapi.testclient import TestClient

        # Mock consciousness core as unavailable
        with patch('src.cns_consciousness_core.main.consciousness_core', None):
            client = TestClient(app)

            test_message = {
                "sender_id": "test-client",
                "receiver_id": "biological-core",
                "content": "test message",
                "biological_context": {"test": True}
            }

            response = client.post("/biological-message", json=test_message)
            assert response.status_code == 200

            data = response.json()
            assert "error" in data
            assert data["error"] == "Consciousness core not available for messaging"

    @pytest.mark.asyncio
    async def test_biological_knowledge_degraded_mode(self):
        """Test biological knowledge access in degraded mode"""
        from src.cns_consciousness_core.main import app
        from fastapi.testclient import TestClient

        # Mock consciousness core as unavailable
        with patch('src.cns_consciousness_core.main.consciousness_core', None):
            client = TestClient(app)

            response = client.get("/biological-knowledge/test-query")
            assert response.status_code == 200

            data = response.json()
            assert "error" in data
            assert data["error"] == "Consciousness core not available"
            assert data["godhood_integration"] is True

    @pytest.mark.asyncio
    async def test_evolutionary_template_degraded_mode(self):
        """Test evolutionary template access in degraded mode"""
        from src.cns_consciousness_core.main import app
        from fastapi.testclient import TestClient

        # Mock consciousness core as unavailable
        with patch('src.cns_consciousness_core.main.consciousness_core', None):
            client = TestClient(app)

            response = client.get("/evolutionary-template/test-improvement")
            assert response.status_code == 200

            data = response.json()
            assert "error" in data
            assert data["error"] == "Consciousness core not available"

    def test_invalid_uvicorn_command_direct_run(self):
        """Test that direct run command has correct path (should be main.py, not src.cns_consciousness_core.main)"""
        from src.cns_consciousness_core.main import __name__

        # The __name__ should be '__main__' when run directly
        # This tests the if __name__ == "__main__": block works correctly
        with patch('uvicorn.run') as mock_uvicorn:
            # Import and run the main block
            exec(open(Path(__file__).parent.parent.parent / 'src' / 'cns_consciousness_core' / 'main.py').read())

            # Verify uvicorn was called with correct parameters
            mock_uvicorn.assert_called_once()
            call_args = mock_uvicorn.call_args

            # The command should reference the current file, not the old incorrect path
            assert 'src.cns_consciousness_core.main:app' in str(call_args)
            assert call_args[1]['host'] == "0.0.0.0"
            assert call_args[1]['port'] == 8001
            assert call_args[1]['reload'] is True

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
