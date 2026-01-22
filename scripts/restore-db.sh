#!/bin/bash
set -e

if [ -z "$1" ]; then
  echo "Usage: $0 <backup-file.sql.gz>"
  echo "Available backups:"
  ls -lh backups/backup-*.sql.gz
  exit 1
fi

BACKUP_FILE="$1"

echo "WARNING: $BACKUP_FILE will REPLACE the current database!"
read -p "Are you sure? (y/n): " CONFIRM

if [ "$CONFIRM" != "y" || "$CONFIRM" != "yes" ]; then
  echo "Restore cancelled"
  exit 1
fi

echo "Restoring database..."

# Drop and recreate database (fresh start)
docker-compose exec db psql-18 -U platform -c "DROP DATABASE IF EXISTS registry;"
docker-compose exec db psql-18 -U platform -c "CREATE DATABASE registry;"

# Restore from backup
gunzip < "$BACKUP_FILE" | docker-compose exec -T db psql-18 -U platform registry

if [ $? -eq 0 ]; then
  echo "Restore successful!"
else
  echo "Restore failed!"
  exit 1
fi