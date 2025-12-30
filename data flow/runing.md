### docker compose logs -f api ( Django app logs )

    Postgres is up!
    Applying migrations...
    Starting gunicorn...

### docker compose up ( start all services )

    docker compose \
    -f docker-compose.yml \
    -f docker-compose.observability.yml \
    up -d

### get into perticular service shell

    # Product Kafka consumer
    docker compose exec api python manage.py run_product_event_consumer

    # Outbox
    docker compose exec api python manage.py process_outbox
