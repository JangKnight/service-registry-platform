#!/bin/bash
set -e

BACKUP_DIR="./backups"
DATE=$(date +%Y%m%d-%H%M%S)
BACKUP_FILE="$BACKUP_DIR/backup-$DATE.sql.gz"

mkdir -p "$BACKUP_DIR"

echo "Starting backup..."

# pg_dump with gzip compress
docker-compose exec -T db pg_dump -U platform registry | gzip > "$BACKUP_FILE"

if [ $? -eq 0 ]; then
  echo "Backup successful: $BACKUP_FILE"

  ls -lh "$BACKUP_FILE"

  cd "$BACKUP_DIR"
  ls -t backup-*.sql.gz | tail -n +4 | xargs -r rm
  echo "Backup successful!"
else
  echo "Backup failed!"
  exit 1
fi