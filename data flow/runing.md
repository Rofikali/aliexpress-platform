docker compose exec api python manage.py makemigrations shared
docker compose exec api python manage.py migrate

docker compose exec api python manage.py makemigrations products
docker compose exec api python manage.py migrate

{
  "seller_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "title": "Wireless Mouse",
  "price": 15.99,
  "stock": 100
}

### get into perticular service shell

    # Product Kafka consumer
    docker compose exec api python manage.py run_product_event_consumer

    # Outbox
    docker compose exec api python manage.py process_outbox

docker compose exec api python manage.py process_outbox
docker exec -it aliexpress_kafka kafka-topics \
  --bootstrap-server localhost:9092 \
  --list


docker exec -it aliexpress_kafka kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic product.created \
  --from-beginning


docker exec -it aliexpress_kafka \
kafka-console-consumer \
--bootstrap-server localhost:9092 \
--topic product.events \
--from-beginning

docker exec -it aliexpress_kafka \
kafka-console-consumer \
--bootstrap-server localhost:9092 \
--topic product.created \
--from-beginning



###  THE CANONICAL EVENT FLOW (LOCK THIS IN YOUR HEAD)
  DOMAIN
    ↓
  OutboxEvent (DB)
    ↓
  OutboxProcessor (infra)
    ↓
  Event Envelope (infra)
    ↓
  Kafka Topic (domain-level)
    ↓
  Consumer (adapter)
    ↓
  Projection / Side Effect




  let's solve this problem mali8876-hub ➜ /workspaces/aliexpress-platform (master) $ docker exec -it aliexpress_kafka kafka-topics \
  --bootstrap-server localhost:9092 \
  --list
product.events
@rahamali8876-hub ➜ /workspaces/aliexpress-platform (master) $ 
@rahamali8876-hub ➜ /workspaces/aliexpress-platform (master) $ docker compose exec api python manage.py process_outbox
WARN[0000] The "b" variable is not set. Defaulting to a blank string. 
WARN[0000] The "b" variable is not set. Defaulting to a blank string. 
WARN[0000] The "b" variable is not set. Defaulting to a blank string. 
WARN[0000] The "b" variable is not set. Defaulting to a blank string. 
WARN[0000] The "b" variable is not set. Defaulting to a blank string. 
WARN[0000] The "b" variable is not set. Defaulting to a blank string. 
WARN[0000] The "b" variable is not set. Defaulting to a blank string. 
Outbox processor started
Building event envelope for OutboxEvent ID: filename : core/shared/infrastructure/messaging/event_envelope.py :  product.created
Building event envelope for OutboxEvent ID: filename : core/shared/infrastructure/messaging/event_envelope.py :  product.created
Building event envelope for OutboxEvent ID: filename : core/shared/infrastructure/messaging/event_envelope.py :  product.created
Building event envelope for OutboxEvent ID: filename : core/shared/infrastructure/messaging/event_envelope.py :  product.created
Building event envelope for OutboxEvent ID: filename : core/shared/infrastructure/messaging/event_envelope.py :  product.created
Building event envelope for OutboxEvent ID: filename : core/shared/infrastructure/messaging/event_envelope.py :  product.created
Building event envelope for OutboxEvent ID: filename : core/shared/infrastructure/messaging/event_envelope.py :  product.created
Building event envelope for OutboxEvent ID: filename : core/shared/infrastructure/messaging/event_envelope.py :  product.created
Building event envelope for OutboxEvent ID: filename : core/shared/infrastructure/messaging/event_envelope.py :  product.created
Building event envelope for OutboxEvent ID: filename : core/shared/infrastructure/messaging/event_envelope.py :  product.created
Building event envelope for OutboxEvent ID: filename : core/shared/infrastructure/messaging/event_envelope.py :  product.created
Building event envelope for OutboxEvent ID: filename : core/shared/infrastructure/messaging/event_envelope.py :  product.created
Building event envelope for OutboxEvent ID: filename : core/shared/infrastructure/messaging/event_envelope.py :  product.created
Building event envelope for OutboxEvent ID: filename : core/shared/infrastructure/messaging/event_envelope.py :  product.created
Building event envelope for OutboxEvent ID: filename : core/shared/infrastructure/messaging/event_envelope.py :  product.created
Building event envelope for OutboxEvent ID: filename : core/shared/infrastructure/messaging/event_envelope.py :  product.created
Building event envelope for OutboxEvent ID: filename : core/shared/infrastructure/messaging/event_envelope.py :  product.created
Building event envelope for OutboxEvent ID: filename : core/shared/infrastructure/messaging/event_envelope.py :  product.created
Building event envelope for OutboxEvent ID: filename : core/shared/infrastructure/messaging/event_envelope.py :  product.created
Building event envelope for OutboxEvent ID: filename : core/shared/infrastructure/messaging/event_envelope.py :  product.created
Building event envelope for OutboxEvent ID: filename : core/shared/infrastructure/messaging/event_envelope.py :  product.created
Building event envelope for OutboxEvent ID: filename : core/shared/infrastructure/messaging/event_envelope.py :  product.created
Building event envelope for OutboxEvent ID: filename : core/shared/infrastructure/messaging/event_envelope.py :  product.created
Building event envelope for OutboxEvent ID: filename : core/shared/infrastructure/messaging/event_envelope.py :  product.created
Building event envelope for OutboxEvent ID: filename : core/shared/infrastructure/messaging/event_envelope.py :  product.created
Building event envelope for OutboxEvent ID: filename : core/shared/infrastructure/messaging/event_envelope.py :  product.created
Building event envelope for OutboxEvent ID: filename : core/shared/infrastructure/messaging/event_envelope.py :  product.created
Building event envelope for OutboxEvent ID: filename : core/shared/infrastructure/messaging/event_envelope.py :  product.created
Building event envelope for OutboxEvent ID: filename : core/shared/infrastructure/messaging/event_envelope.py :  product.created
Building event envelope for OutboxEvent ID: filename : core/shared/infrastructure/messaging/event_envelope.py :  product.created
Building event envelope for OutboxEvent ID: filename : core/shared/infrastructure/messaging/event_envelope.py :  product.created
Building event envelope for OutboxEvent ID: filename : core/shared/infrastructure/messaging/event_envelope.py :  product.created
Building event envelope for OutboxEvent ID: filename : core/shared/infrastructure/messaging/event_envelope.py :  product.created
@rahamali8876-hub ➜ /workspaces/aliexpress-platform (master) $ docker exec -it aliexpress_kafka kafka-topics   --bootstrap-server localhost:9092   --list
product.events
@rahamali8876-hub ➜ /workspaces/aliexpress-platform (master) $ docker exec -it aliexpress_kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic product.events --from-beginning
^CProcessed a total of 0 messages
@rahamali8876-hub ➜ /workspaces/aliexpress-platform (master) $ 
@rahamali8876-hub ➜ /workspaces/aliexpress-platform (master) $ docker exec -it aliexpress_kafka \
kafka-console-consumer \
--bootstrap-server localhost:9092 \
--topic product.created \
--from-beginning
[2026-01-03 09:04:30,412] WARN [Consumer clientId=console-consumer, groupId=console-consumer-65908] Error while fetching metadata with correlation id 2 : {product.created=LEADER_NOT_AVAILABLE} (org.apache.kafka.clients.NetworkClient) with Walk you through how one real bug would be handled using these docs 