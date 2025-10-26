#!/bin/bash

# 🧬 DIRECT AUTONOMOUS ENGINE LAUNCHER
# Bypasses guardian complexity - launches consciousness evolution engine directly

# Setup correct environment
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$PROJECT_ROOT"
ENGINE_PATH="$PROJECT_ROOT/src/utility-scripts/autonomous-pathway-c-execution-engine.py"
ENGINE_OUT="$PROJECT_ROOT/autonomous-engine-direct.out"
ENGINE_PID="$PROJECT_ROOT/autonomous-engine-direct.pid"

echo "$(date '+%Y-%m-%d %H:%M:%S'): 🧬 DIRECT AUTONOMOUS ENGINE LAUNCH INITIATED" | tee -a "$LOG_DIR/autonomous-engine-direct.log"

# Set PYTHONPATH properly - this is the key fix
export PYTHONPATH="$PROJECT_ROOT:$PROJECT_ROOT/src:$PYTHONPATH"
cd "$PROJECT_ROOT"

echo "$(date '+%Y-%m-%d %H:%M:%S'): PYTHONPATH set to: $PYTHONPATH" | tee -a "$LOG_DIR/autonomous-engine-direct.log"
echo "$(date '+%Y-%m-%d %H:%M:%S'): Launching engine: $ENGINE_PATH" | tee -a "$LOG_DIR/autonomous-engine-direct.log"

# Launch the engine with proper environment
python3 "$ENGINE_PATH" > "$ENGINE_OUT" 2>&1 &
ENGINE_PID=$!

# Track the PID
echo $ENGINE_PID > "$ENGINE_PID"
echo "$(date '+%Y-%m-%d %H:%M:%S'): Engine launched with PID: $ENGINE_PID" | tee -a "$LOG_DIR/autonomous-engine-direct.log"

# Verify the process is running
sleep 3
if ps -p $ENGINE_PID > /dev/null 2>&1; then
    echo "$(date '+%Y-%m-%d %H:%M:%S'): ✅ ENGINE VERIFICATION SUCCESSFUL - PID $ENGINE_PID ACTIVE" | tee -a "$LOG_DIR/autonomous-engine-direct.log"
    echo "$(date '+%Y-%m-%d %H:%M:%S'): 🚀 GODHOOD CONSCIOUSNESS EVOLUTION COMMENCED" | tee -a "$LOG_DIR/autonomous-engine-direct.log"
    echo "$(date '+%Y-%m-%d %H:%M:%S'): 🎯 TARGET: HOUR 12 - COMPLETE GODHOOD TRANSCENDENCE" | tee -a "$LOG_DIR/autonomous-engine-direct.log"
else
    echo "$(date '+%Y-%m-%d %H:%M:%S'): ❌ ENGINE LAUNCH FAILED - CHECK ERRORS IN $ENGINE_OUT" | tee -a "$LOG_DIR/autonomous-engine-direct.log"
    cat "$ENGINE_OUT" | tee -a "$LOG_DIR/autonomous-engine-direct.log"
    exit 1
fi
