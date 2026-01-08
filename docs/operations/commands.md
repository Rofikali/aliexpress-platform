### 🧠 ALIEXPRESS PLATFORM — OPERATIONS COMMANDS GUIDE (STAFF GRADE)

    Audience: New engineers, senior devs, SREs
    Goal: Run, debug, replay, and operate the platform safely
    Golden Rule: Never guess. Always verify offsets, lag, and health.

### 0️⃣ PREREQUISITES (ALWAYS CHECK FIRST)
    docker compose ps
        api
        postgres
        kafka
        redis
        elasticsearch
        grafana
        prometheus

### 1️⃣ ONE-SHOT COMMANDS (MANUAL / SAFE)

    These commands run once and exit.
    make observe-up-build / make restart
    If you trigger product creation via API or admin, events land in outbox, not Kafka directly.

        ### 1.1 Run Outbox Publisher (ONE-SHOT)
            Publishes pending outbox rows → Kafka.
            docker compose exec api python manage.py process_outbox

### 2️⃣ LONG-RUNNING SERVICES (DAEMONS)
    These must keep running.

    ### 2.1 Product Command Consumer (Write-side)
        Handles commands → aggregates → outbox.
        docker compose exec api python manage.py run_product_consumer

        Expected log:
        Product consumer started

### 2.2 Product Event Projection Consumer (Read-side)
    Consumes product.events → search/read models.
    docker compose exec api python manage.py run_product_event_consumer

    ### Expected log:
        Product Event Consumer started and polling Kafka...
        indexing_product

### 3️⃣ KAFKA TOPIC & CONSUMER INSPECTION (VERY IMPORTANT)
    3.1 List Consumer Groups
    docker exec -it aliexpress_kafka \
    kafka-consumer-groups \
    --bootstrap-server aliexpress_kafka:9092 \
    --list

    ### Expected groups:
        product-command-consumer-group
        product-event-projection-group

### 3.2 Describe Consumer Group (LAG CHECK)
    docker exec -it aliexpress_kafka \
    kafka-consumer-groups \
    --bootstrap-server aliexpress_kafka:9092 \
    --group product-event-projection-group \
    --describe

    ### Example output:
        TOPIC           CURRENT-OFFSET  LOG-END-OFFSET  LAG
        product.events  1233            6593            5360
        📌 Lag > 0 means consumer is behind

### 3.3 Watch Lag in Real-Time (YOU USED THIS ✅)
    watch -n 2 "
    docker exec -it aliexpress_kafka \
    kafka-consumer-groups \
    --bootstrap-server aliexpress_kafka:9092 \
    --group product-event-projection-group \
    --describe
    "
### 4.1 STOP the Consumer FIRST
    CTRL + C

    Verify:

    docker exec -it aliexpress_kafka \
    kafka-consumer-groups \
    --bootstrap-server aliexpress_kafka:9092 \
    --group product-event-projection-group \
    --describe

    ### You should see:
        has no active members

### 4.2 REWIND OFFSETS TO BEGINNING
    docker exec -it aliexpress_kafka \
    kafka-consumer-groups \
    --bootstrap-server aliexpress_kafka:9092 \
    --group product-event-projection-group \
    --topic product.events \
    --reset-offsets \
    --to-earliest \
    --execute


### 4.3 RESTART CONSUMER
    docker compose exec api python manage.py run_product_event_consumer

    You should see thousands of indexing_product logs.

### 5.1 List DLQ Topic
    docker exec -it aliexpress_kafka \
    kafka-topics \
    --bootstrap-server aliexpress_kafka:9092 \
    --list | grep dlq

    ### Expected:
        dlq.product.events

### 5.2 Inspect DLQ Messages
    docker exec -it aliexpress_kafka \
    kafka-console-consumer \
    --bootstrap-server aliexpress_kafka:9092 \
    --topic dlq.product.events \
    --from-beginning

    ### Used when:

        Schema mismatch
        Missing fields
        Consumer crash

### 6️⃣ HEALTH & DEBUGGING
    6.1 API Health Check
    curl http://localhost:8000/health/

    ### Expected:
        {
        "status": "ok",
        "checks": {
            "database": "ok",
            "redis": "ok",
            "kafka": "ok"
        }
        }


dlq bugs
docker exec -it aliexpress_kafka kafka-console-consumer --bootstrap-server aliexpress_kafka:9092 --topic dlq.product.events --from-beginning

