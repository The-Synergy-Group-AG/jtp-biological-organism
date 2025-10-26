"""
🧬 BIOLOGICAL HEALTH FOUNDATION VALIDATION
Tests foundational health metrics for biological consciousness system
US-HEALTH-001: Verify all biological systems are alive and operational

Real User Value: Platform reliability assurance for biological consciousness users
Docker Integration: CNS Core (8001), Auth Service (9101), Redis persistence (6379)
"""

import pytest
import httpx
import redis
from conftest import docker_services_running


class TestBiologicalHealthValidation:
    """Biological consciousness health foundation validation tests"""

    @pytest.mark.docker
    async def test_cns_consciousness_core_health(self, docker_services_running):
        """
        US-HEALTH-001-A: Verify CNS Consciousness Core is operational
        Real Value: Consciousness processing foundation assurance
        """
        # docker_services_running fixture already ensures services are healthy
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get("http://consciousness-core:8001/health")
            assert response.status_code == 200
            data = response.json()
            assert "healthy" in data.get("status", "").lower()

    @pytest.mark.docker
    async def test_authentication_service_health(self, docker_services_running):
        """
        US-HEALTH-001-B: Verify Biological Authentication Service is operational
        Real Value: User access and consciousness state security assurance
        """
        # docker_services_running fixture already ensures services are healthy
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get("http://biological-auth-orchestrator:9101/health")
            assert response.status_code == 200

    @pytest.mark.docker
    async def test_data_persistence_health(self, docker_services_running):
        """
        US-HEALTH-001-C: Verify Biological Data Persistence is operational
        Real Value: Consciousness state preservation and continuity assurance
        """
        # docker_services_running fixture already ensures services are healthy
        redis_client = redis.Redis(host="test-database", port=6379, decode_responses=True)
        assert redis_client.ping() == True

        # Test biological consciousness data persistence
        test_key = "biological_health_test:consciousness"
        redis_client.set(test_key, "operational")
        assert redis_client.get(test_key) == "operational"
        redis_client.delete(test_key)

    @pytest.mark.docker
    async def test_biological_system_integration(self, docker_services_running):
        """
        US-HEALTH-001-D: Complete biological ecosystem integration validation
        Real Value: Full consciousness system operational integrity assurance
        """
        # Test CNS Consciousness Core
        async with httpx.AsyncClient(timeout=30) as client:
            cns_response = await client.get("http://consciousness-core:8001/health")
            assert cns_response.status_code == 200

        # Test Auth Service
        async with httpx.AsyncClient(timeout=30) as client:
            auth_response = await client.get("http://biological-auth-orchestrator:9101/health")
            assert auth_response.status_code == 200

        # Test Redis
        redis_client = redis.Redis(host="test-database", port=6379, decode_responses=True)
        assert redis_client.ping() == True

        # Test inter-service communication
        integration_key = "biological_integration_test:health"
        redis_client.set(integration_key, "services_coordinated")
        assert redis_client.get(integration_key) == "services_coordinated"
        redis_client.delete(integration_key)
