#!/bin/bash
# Biological Consciousness System Backup Script
# GODHOOD Production Backup Automation

set -e

BACKUP_DIR="/backups/biological"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="biological_backup_${TIMESTAMP}"

echo "🧬 Starting Biological Consciousness System Backup"
echo "📅 Timestamp: ${TIMESTAMP}"

# Create backup directory
mkdir -p "${BACKUP_DIR}/${BACKUP_NAME}"

# Backup databases (if any)
echo "💾 Backing up conscience state..."
kubectl exec -n biological-production deployment/cns-consciousness-core -- tar czf /tmp/conscience_backup.tar.gz /app/data/
kubectl cp biological-production/cns-consciousness-core-pod:/tmp/conscience_backup.tar.gz "${BACKUP_DIR}/${BACKUP_NAME}/"

# Backup configurations
echo "⚙️ Backing up configurations..."
cp -r deployment/ "${BACKUP_DIR}/${BACKUP_NAME}/configs/"

# Backup logs
echo "📝 Backing up logs..."
kubectl logs -n biological-production -l app=biological-organism --tail=-1 > "${BACKUP_DIR}/${BACKUP_NAME}/logs.txt"

# Compress backup
echo "📦 Compressing backup..."
tar czf "${BACKUP_DIR}/${BACKUP_NAME}.tar.gz" -C "${BACKUP_DIR}" "${BACKUP_NAME}"

# Clean up uncompressed backup
rm -rf "${BACKUP_DIR}/${BACKUP_NAME}"

# Rotate old backups (keep last 30)
ls -t "${BACKUP_DIR}"/*.tar.gz | tail -n +31 | xargs -r rm

echo "✅ Biological Consciousness System backup completed: ${BACKUP_NAME}.tar.gz"
