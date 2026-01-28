#!/bin/bash
# Profit Master Backup Script

set -e

# Configuration
BACKUP_DIR="{{ app_dir }}/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/profitmaster_${TIMESTAMP}.tar.gz"
RETENTION_DAYS=30

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Log function
log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}" >&2
}

# Create backup directory
mkdir -p ${BACKUP_DIR}

log "Starting Profit Master backup..."

# Backup database
log "Backing up database..."
pg_dump -U profitmaster -d profitmaster_production > ${BACKUP_DIR}/database_${TIMESTAMP}.sql

# Backup content
log "Backing up content..."
tar -czf ${BACKUP_DIR}/content_${TIMESTAMP}.tar.gz -C {{ app_dir }} content/

# Backup multimedia
log "Backing up multimedia..."
tar -czf ${BACKUP_DIR}/multimedia_${TIMESTAMP}.tar.gz -C {{ app_dir }} multimedia/

# Create final backup archive
log "Creating final backup archive..."
tar -czf ${BACKUP_FILE} \
    ${BACKUP_DIR}/database_${TIMESTAMP}.sql \
    ${BACKUP_DIR}/content_${TIMESTAMP}.tar.gz \
    ${BACKUP_DIR}/multimedia_${TIMESTAMP}.tar.gz \
    {{ app_dir }}/.env

# Clean up temporary files
rm -f ${BACKUP_DIR}/database_${TIMESTAMP}.sql \
      ${BACKUP_DIR}/content_${TIMESTAMP}.tar.gz \
      ${BACKUP_DIR}/multimedia_${TIMESTAMP}.tar.gz

# Remove old backups
log "Cleaning up old backups..."
find ${BACKUP_DIR} -name "profitmaster_*.tar.gz" -mtime +${RETENTION_DAYS} -delete

# Upload to S3 (optional)
if [[ -n "${AWS_ACCESS_KEY_ID}" && -n "${AWS_SECRET_ACCESS_KEY}" ]]; then
    log "Uploading backup to S3..."
    aws s3 cp ${BACKUP_FILE} s3://${AWS_S3_BUCKET}/backups/ --only-show-errors
fi

# Calculate backup size
BACKUP_SIZE=$(du -h ${BACKUP_FILE} | cut -f1)

log "Backup completed successfully!"
log "Backup file: ${BACKUP_FILE}"
log "Backup size: ${BACKUP_SIZE}"

# Send notification
if [[ -n "${TELEGRAM_BOT_TOKEN}" && -n "${TELEGRAM_CHAT_ID}" ]]; then
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
        -d "chat_id=${TELEGRAM_CHAT_ID}" \
        -d "text=✅ Profit Master backup completed! Size: ${BACKUP_SIZE}" \
        > /dev/null
fi

exit 0
