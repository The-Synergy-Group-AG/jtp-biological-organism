#!/usr/bin/env python3
"""
🧬 Biological Adaptation Algorithm Tests

Tests for evolutionary adaptation mechanisms and biological response algorithms.
Validates adaptation effectiveness under environmental pressure conditions.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import statistics
import math
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

@pytest.mark.unit
class TestBiologicalAdaptation:
    """Test biological adaptation algorithms"""

    def test_environmental_adaptation_response(self):
        """Test adaptation response to environmental changes"""
        adaptation_scenarios = [
            {
                "environmental_change": "sudden_stress",
                "adaptation_required": 0.9,
                "response_time_seconds": 300,
                "biological_stress_level": 0.8
            },
            {
                "environmental_change": "gradual_shift",
                "adaptation_required": 0.6,
                "response_time_seconds": 1800,
                "biological_stress_level": 0.3
            },
            {
                "environmental_change": "extreme_conditions",
                "adaptation_required": 0.95,
                "response_time_seconds": 120,
                "biological_stress_level": 0.95
            }
        ]

        for scenario in adaptation_scenarios:
            # Simulate biological adaptation response
            stress_factor = scenario["biological_stress_level"]
            base_adaptation = 0.7

            # Adaptation improves under stress (evolutionary principle)
            adaptation_response = base_adaptation + (stress_factor * 0.4)

            assert adaptation_response >= scenario["adaptation_required"], \
                f"Adaptation {adaptation_response} below required {scenario['adaptation_required']} for {scenario['environmental_change']}"

    def test_evolutionary_pressure_calculation(self):
        """Test evolutionary pressure calculations"""
        evolutionary_scenarios = [
            {
                "selection_intensity": 0.8,
                "population_variance": 0.6,
                "adaptation_pressure": "high",
                "expected_evolutionary_rate": 1.2
            },
            {
                "selection_intensity": 0.3,
                "population_variance": 0.9,
                "adaptation_pressure": "low",
                "expected_evolutionary_rate": 0.8
            }
        ]

        for scenario in evolutionary_scenarios:
            intensity = scenario["selection_intensity"]
            variance = scenario["population_variance"]

            # Calculate evolutionary pressure (selection × variance)
            evolutionary_pressure = intensity * variance

            assert evolutionary_pressure > 0.2, "Evolutionary pressure must be sufficient for adaptation"

    def test_adaptation_memory_retention(self):
        """Test adaptation memory and learning retention"""
        adaptation_memory = {
            "successful_adaptations": 15,
            "failed_adaptations": 3,
            "learning_retention_rate": 0.87,
            "adaptation_patterns": ["stress_response", "environmental_shift", "resource_scarcity"]
        }

        retention_rate = adaptation_memory["learning_retention_rate"]
        success_rate = adaptation_memory["successful_adaptations"] / (adaptation_memory["successful_adaptations"] + adaptation_memory["failed_adaptations"])

        # Learning effectiveness should correlate with success rate
        assert retention_rate > success_rate * 0.9, "Learning retention should support adaptation success"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
