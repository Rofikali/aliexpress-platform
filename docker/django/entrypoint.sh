# #!/bin/sh

# echo "Waiting for database..."

# while ! nc -z db 5432; do
#   sleep 0.5
# done

# echo "Database ready."

# python manage.py migrate
# python manage.py runserver 0.0.0.0:8000

#!/bin/sh

set -e

echo "🚀 Starting AliExpress Platform API"

# Wait for Postgres
echo "⏳ Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 1
done
echo "✅ PostgreSQL is ready"

# Run migrations
python manage.py migrate --noinput

# Collect static (safe even if unused)
python manage.py collectstatic --noinput || true

# Start server
exec python manage.py runserver 0.0.0.0:8000
