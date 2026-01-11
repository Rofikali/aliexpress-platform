docker compose exec api python manage.py process_outbox
    docker compose exec api python manage.py run_product_event_consumer
    docker compose exec api python manage.py run_product_consumer 


    something is wrong