#!/usr/bin/env python3
"""
🧬 Docker Integration Test Configuration and Fixtures

Provides pytest fixtures and configuration for testing with running Docker services.
Handles docker-compose lifecycle management and service health validation for integration tests.
"""

import pytest
import subprocess
import requests
import time
import os
from pathlib import Path
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

def wait_for_service_health(base_url: str, timeout: int = 60) -> bool:
    """
    Wait for a service to become healthy.

    Args:
        base_url: Base URL of the service to check
        timeout: Maximum time to wait in seconds

    Returns:
        bool: True if service becomes healthy, False otherwise
    """
    start_time = time.time()
    health_url = f"{base_url}/health"

    while time.time() - start_time < timeout:
        try:
            response = requests.get(health_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    logger.info(f"✅ Service healthy: {base_url}")
                    return True
        except requests.exceptions.RequestException:
            pass

        logger.debug(f"⏳ Waiting for service: {base_url} ({int(time.time() - start_time)}s)")
        time.sleep(2)

    logger.error(f"❌ Service failed to become healthy: {base_url}")
    return False

def check_all_services_healthy(service_urls: Dict[str, str], timeout: int = 120) -> bool:
    """
    Check that all services in the provided URLs are healthy.

    Args:
        service_urls: Dictionary mapping service names to their base URLs
        timeout: Maximum time to wait for all services

    Returns:
        bool: True if all services are healthy, False otherwise
    """
    start_time = time.time()
    unhealthy_services = set(service_urls.keys())

    while unhealthy_services and (time.time() - start_time) < timeout:
        still_unhealthy = set()

        for service_name, base_url in service_urls.items():
            if service_name in unhealthy_services:
                if wait_for_service_health(base_url, timeout=10):
                    unhealthy_services.discard(service_name)
                    logger.info(f"✅ {service_name} is now healthy")
                else:
                    still_unhealthy.add(service_name)

        unhealthy_services = still_unhealthy

        if unhealthy_services:
            logger.info(f"⏳ Still waiting for services: {', '.join(unhealthy_services)}")
            time.sleep(5)

    if unhealthy_services:
        logger.error(f"❌ Services failed to become healthy: {', '.join(unhealthy_services)}")
        return False

    logger.info("🎉 All services are healthy!")
    return True

@pytest.fixture(scope="session")
def docker_compose_file():
    """Path to the test docker-compose file."""
    compose_file = Path(__file__).parent.parent / "docker-compose.test.yml"
    if not compose_file.exists():
        pytest.fail(f"Docker compose test file not found: {compose_file}")
    return compose_file

@pytest.fixture(scope="session")
def docker_services_running():
    """
    Provide Docker service URLs assuming they're already running.

    This fixture assumes Docker services are pre-started and healthy.
    It provides access to running services without managing lifecycle.
    """
    logger.info("🔗 Connecting to pre-running Docker test services...")

    # Define service URLs (internal Docker network URLs)
    service_urls = {
        "consciousness-core": "http://consciousness-core:8001",
        "cv-generation": "http://cv-generation-engine:8080",
        "multilingual": "http://multilingual-resonance-adapter:8080",
        "email-service": "http://email-communications-symbiosis:8080",
        "auth-service": "http://biological-auth-orchestrator:8080",
        "evolutionary": "http://evolutionary-brain-trust:8080",
        "redis": "redis://test-database:6379"  # Redis doesn't have HTTP health
    }

    logger.info("✅ Docker service URLs configured for testing!")
    yield service_urls

    # No cleanup needed - services are managed externally
    logger.info("🔗 Docker services remain running (managed externally)")

@pytest.fixture(scope="session")
def running_service_urls(docker_services_running):
    """
    Provide URLs for accessing running Docker services.

    Returns both internal Docker network URLs (for service-to-service communication)
    and external URLs (for tests running outside Docker).
    """
    internal_urls = docker_services_running

    # External URLs (accessible from host/test environment)
    external_urls = {
        "consciousness-core": "http://localhost:8101",  # Offset port from docker-compose
        "cv-generation": "http://localhost:9102",
        "multilingual": "http://localhost:9103",
        "email-service": "http://localhost:9104",
        "auth-service": "http://localhost:9101",
        "evolutionary": "http://localhost:9998",
        "redis": "redis://localhost:6378"
    }

    return {
        "internal": internal_urls,
        "external": external_urls
    }

@pytest.fixture
def consciousness_core_client(running_service_urls):
    """FastAPI test client for consciousness core service."""
    try:
        from fastapi.testclient import TestClient
        # Import the FastAPI app directly if running outside Docker
        if os.getenv("TEST_MODE") != "docker_integration":
            from src.cns_consciousness_core.main import app
            return TestClient(app)
        else:
            # For Docker integration, use HTTP client
            return running_service_urls["external"]["consciousness-core"]
    except ImportError:
        # Fallback to HTTP client if import fails
        return running_service_urls["external"]["consciousness-core"]

@pytest.fixture
def auth_service_client(running_service_urls):
    """Client for biological authentication service."""
    return running_service_urls["external"]["auth-service"]

@pytest.fixture
def cv_generation_client(running_service_urls):
    """Client for CV generation service."""
    return running_service_urls["external"]["cv-generation"]

@pytest.fixture
def multilingual_client(running_service_urls):
    """Client for multilingual service."""
    return running_service_urls["external"]["multilingual"]

@pytest.fixture
def email_service_client(running_service_urls):
    """Client for email communications service."""
    return running_service_urls["external"]["email-service"]

@pytest.fixture
def evolutionary_client(running_service_urls):
    """Client for evolutionary brain trust service."""
    return running_service_urls["external"]["evolutionary"]

@pytest.fixture
def redis_client(running_service_urls):
    """Redis client for session/test data storage."""
    import redis
    redis_url = running_service_urls["external"]["redis"]
    return redis.from_url(redis_url, decode_responses=True)

@pytest.fixture(autouse=True)
def clean_test_data(redis_client):
    """Clean up test data before and after each test."""
    # Clean up before test
    redis_client.flushdb()

    yield

    # Clean up after test (if needed)
    try:
        redis_client.flushdb()
    except Exception:
        pass  # Ignore cleanup errors

@pytest.fixture
def test_user_session(redis_client):
    """Create a test user session for integration tests."""
    session_id = f"test_session_{int(time.time())}"
    user_data = {
        "user_id": f"user_{int(time.time())}",
        "biological_level": 0.85,
        "harmony_score": 0.92,
        "session_start": time.time(),
        "consciousness_phase": "test_validation"
    }

    redis_client.hmset(f"session:{session_id}", user_data)
    redis_client.expire(f"session:{session_id}", 3600)  # 1 hour

    return {"session_id": session_id, **user_data}

@pytest.fixture
def biological_test_context():
    """Provide common biological test context data."""
    return {
        "biological_context": {
            "harmony_target": 0.997,
            "consciousness_phase": "test_validation",
            "evolutionary_pressure": "validation_testing",
            "quantum_stability": 0.98,
            "biological_resonance": 0.95
        },
        "ai_context": {
            "model_coordination": True,
            "response_consistency": 0.94,
            "biological_alignment": True
        },
        "test_metadata": {
            "test_type": "docker_integration",
            "validation_level": "enterprise",
            "timestamp": time.time()
        }
    }

# Configuration for test markers
pytestmark = [
    pytest.mark.docker,
    pytest.mark.integration,
    pytest.mark.timeout(300)  # 5 minute timeout for integration tests
]

# Test configuration
@pytest.fixture(scope="session", autouse=True)
def configure_test_environment():
    """Configure test environment for Docker integration tests."""
    os.environ.setdefault("TEST_MODE", "docker_integration")
    os.environ.setdefault("VALIDATE_RUNNING_SERVICES", "true")
    os.environ.setdefault("BIOLOGICAL_CONSCIOUSNESS_TEST", "true")

    # Disable external API calls during testing
    os.environ.setdefault("MOCK_EXTERNAL_APIS", "true")

    logger.info("🧪 Docker integration test environment configured")
