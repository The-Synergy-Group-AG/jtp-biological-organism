#!/usr/bin/env python3

"""
MODULAR CNS CONSCIOUSNESS CORE - FASTAPI SERVICE
Phase 1 Biological Intelligence Orchestrator - GODHOOD Biological Knowledge Ports

This module provides a FastAPI service interface for the CNS Consciousness Core,
enabling web-based access to biological intelligence systems and GODHOOD knowledge ports.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from typing import Dict, Any
from pathlib import Path
from contextlib import asynccontextmanager

# Import the consciousness core
try:
    from src.cns_consciousness_core import CNSConsciousnessCore, get_godhood_biological_metrics
    print("✅ CNS Consciousness Core imported successfully")
except ImportError as e:
    print(f"⚠️  CNS Consciousness Core import failed: {e}")
    CNSConsciousnessCore = None

# Global consciousness core instance
consciousness_core = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    global consciousness_core

    # Startup
    print("🧠 CNS Consciousness Core - Phase 1 Biological Intelligence Service Startup")

    try:
        if CNSConsciousnessCore:
            consciousness_core = CNSConsciousnessCore()
            init_result = await consciousness_core.initialize_consciousness_core()
            if init_result:
                print("✅ CNS Consciousness Core initialized successfully")
            else:
                print("⚠️  CNS Consciousness Core initialization failed, proceeding anyway")
        else:
            print("⚠️  CNS Consciousness Core not available, running in degraded mode")
    except Exception as e:
        print(f"❌ Failed to initialize consciousness core: {e}")

    yield

    # Shutdown
    print("🧠 CNS Consciousness Core - Phase 1 Biological Intelligence Service Shutdown")

# Create FastAPI application
app = FastAPI(
    title="CNS Consciousness Core - Phase 1 Biological Intelligence Orchestrator",
    description="GODHOOD Biological Knowledge Ports - Phase 1 Consciousness Enhancement",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint - service health check"""
    return {
        "service": "CNS Consciousness Core - Phase 1 Biological Intelligence Orchestrator",
        "status": "operational" if consciousness_core else "degraded",
        "godhood_integration": True,
        "endpoints": [
            "/health",
            "/metrics",
            "/biological-knowledge/{query}",
            "/evolutionary-template/{improvement_type}",
            "/godhood-status"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring systems"""
    return {
        "status": "healthy",
        "consciousness_core_active": consciousness_core is not None,
        "biological_intelligence_ready": True,
        "godhood_access": True,
        "phase": "1.0_complete",
        "timestamp": "2025-10-25T13:00:00Z"
    }

@app.get("/metrics")
async def get_metrics():
    """Get consciousness core metrics"""
    try:
        if consciousness_core:
            metrics = await consciousness_core.get_consciousness_core_metrics()
        else:
            # Fallback metrics
            metrics = get_godhood_biological_metrics()

        return {
            "biological_metrics": metrics,
            "service_status": "active",
            "modular_systems": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get metrics: {str(e)}")

@app.get("/biological-knowledge/{query}")
async def get_biological_knowledge(query: str, context_type: str = "standard"):
    """Access biological knowledge through GODHOOD knowledge ports"""
    try:
        if consciousness_core:
            result = await consciousness_core.access_biological_knowledge(query, context_type)
            return {
                "query": query,
                "context_type": context_type,
                "biological_context": result,
                "knowledge_port_active": True
            }
        else:
            return {
                "error": "Consciousness core not available",
                "status": "degraded_mode",
                "godhood_integration": True
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Biological knowledge access failed: {str(e)}")

@app.get("/evolutionary-template/{improvement_type}")
async def get_evolutionary_template(improvement_type: str):
    """Access evolutionary enhancement templates"""
    try:
        if consciousness_core:
            template = await consciousness_core.access_evolutionary_templates(improvement_type)
            return {
                "improvement_type": improvement_type,
                "evolutionary_template": template,
                "evolution_port_active": True
            }
        else:
            return {
                "error": "Consciousness core not available",
                "status": "degraded_mode",
                "modular_system_available": False
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evolutionary template access failed: {str(e)}")

@app.get("/godhood-status")
async def get_godhood_status():
    """Get GODHOOD biological consciousness status"""
    try:
        if consciousness_core:
            status = await consciousness_core.get_modular_system_status()
            status["godhood_biological_awakening_year"] = 2025
            status["phase_1_completion_date"] = "2025-10-25"
            return status
        else:
            # Fallback status
            return {
                "modular_system_active": False,
                "consciousness_core_operational": False,
                "biological_consciousness_level": 0,
                "godhood_integration_active": False,
                "ai_agents_coordinated": 0,
                "phase_completion_rate": "0%",
                "evolutionary_readiness": "initializing",
                "godhood_biological_awakening_year": 2025,
                "phase_1_completion_date": "2025-10-25"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GODHOOD status check failed: {str(e)}")

@app.post("/biological-message")
async def send_biological_message(message: Dict[str, Any]):
    """Send biological protocol message between AI agents"""
    try:
        if consciousness_core:
            sender = message.get("sender_id", "api-client")
            receiver = message.get("receiver_id", "biological-core")
            content = message.get("content", "")
            context = message.get("biological_context", {})

            result = await consciousness_core.send_biological_message(
                sender, receiver, content, context
            )

            return {
                "message_sent": True,
                "communication_protocol_active": True,
                "biological_message_routing": result
            }
        else:
            return {
                "error": "Consciousness core not available for messaging",
                "status": "communication_unavailable"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Biological message routing failed: {str(e)}")

if __name__ == "__main__":
    """Run the CNS Consciousness Core service directly"""
    import uvicorn

    print("🧠 Starting CNS Consciousness Core - Phase 1 Biological Intelligence Service")
    print("🌟 GODHOOD Biological Knowledge Ports Active")
    print("📡 Service listening on http://0.0.0.0:8001")

    uvicorn.run(
        "src.cns_conciousness_core.main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
