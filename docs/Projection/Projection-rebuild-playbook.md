# Read Model Rebuild (Product Search Projection)

## 📌 Purpose

This folder contains **finite, deterministic rebuild logic** for the Product **read model** (Elasticsearch projections).

A rebuild exists to **reconstruct query-side state** from already-published domain events when:

- an index schema changes
- a bug corrupted the projection
- historical data must be re-indexed
- a new read model is introduced

⚠️ **This is NOT a normal Kafka consumer.**

---

## 🧠 Key Concept: What a Rebuild Is (and Is Not)

### ✅ A rebuild **IS**

- A **one-time or manual operation**
- Deterministic and replayable
- Scoped to a **single read model**
- Safe to re-run
- Owned by the **read model**

### ❌ A rebuild is **NOT**

- A long-running service
- Part of a Kafka consumer group
- Allowed to commit offsets
- Allowed to affect live consumers
- Infrastructure or messaging logic

---

## 📁 Why This Lives Under `read_model/rebuild/`

This location is **intentional and non-negotiable**.

read_model/
├── documents/ # Shape of read data
├── projections/ # Event → document logic
├── indices/ # Index mappings & versions
├── rebuild/ # ← YOU ARE HERE

yaml
Copy code

### Architectural Rule

> Any code whose sole purpose is to **create, fix, or replay a read model**
> must live inside the **read_model boundary**.

A rebuild is a **read concern**, not a messaging concern.

Placing rebuild logic under:

- `messaging/`
- `consumers/`
- `infrastructure/`

would be **architecturally incorrect** and dangerous.

---

## 🚨 Why Rebuilds Must Be Isolated

Putting rebuild logic near normal consumers causes:

- accidental offset commits
- rebuilds joining live consumer groups
- production consumers skipping events
- non-deterministic state

To prevent this, rebuild logic:

- uses **explicit offset control**
- runs in **finite loops**
- exits cleanly
- never auto-commits

---

## 🔄 Data Source: Kafka or Database?

This rebuild **replays Kafka events**, not the database.

### Why Kafka?

- Kafka is the **source of truth for facts**
- Events represent *what happened*, not *current state*
- Database reads reintroduce coupling and bugs
- Kafka replay guarantees correctness

👉 **Rule**:  
**Read models are rebuilt from events, never from write databases.**

---

## 🧪 Rebuild Guarantees

A correct rebuild must be:

| Property | Guaranteed |
|--------|-----------|
| Deterministic | Same events → same index |
| Idempotent | Re-run safe |
| Finite | Always terminates |
| Isolated | No impact on live traffic |
| Versioned | Writes to versioned indices |

---

## 🏷️ Index Versioning & Aliases

Rebuilds always write to **new versioned indices**:

product_search_v1_<hash>

yaml
Copy code

After a successful rebuild:

- alias `product_search_current` is atomically switched
- zero downtime
- instant rollback possible

❌ Rebuilds must **never** write to a live alias directly.

---

## ▶️ How This Is Run

Rebuilds are executed via **explicit management commands**:

```bash
python manage.py rebuild_product_search_projection

### *********  2️⃣ Run outbox ************************ ###

    python manage.py process_outbox


    3️⃣ Run rebuild

    python manage.py rebuild_product_search_projection


    4️⃣ Start live consumer

    python manage.py run_product_projection_consumer
