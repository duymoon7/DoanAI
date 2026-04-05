#!/bin/bash
set -e

echo "🔍 Waiting for PostgreSQL to be ready..."

# Wait for PostgreSQL
until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c '\q' 2>/dev/null; do
  echo "⏳ PostgreSQL is unavailable - sleeping"
  sleep 2
done

echo "✅ PostgreSQL is up and running!"

echo "🔧 Initializing database and seeding data..."
python seed_docker.py

echo "🚀 Starting FastAPI application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
