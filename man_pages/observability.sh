📊 Observability Stack (Prometheus + Grafana)

This document explains what docker-compose.observability.yml is, why we use it, and how to run it.

1️⃣ What is docker-compose.observability.yml?

docker-compose.observability.yml runs the monitoring stack for the platform.

It starts:

Prometheus → collects metrics

Grafana → visualizes metrics with dashboards

It does NOT run business services (API, Orders, Products, etc.).

👉 Think of it as “system health tools”, not application logic.

2️⃣ Why do we keep observability separate?
❌ Bad approach (everything in one file)

Hard to understand

Hard to turn monitoring on/off

Everyone forced to run Grafana

✅ Good approach (separate file)

Clean separation of concerns

Developers can run app only

Ops/QA can run observability anytime

Production-like setup

This is how real companies structure Docker Compose.

3️⃣ When should I run it?

Run observability when you want to:

See CPU / memory usage

Debug slow APIs

Detect memory leaks

Monitor Python runtime

Prepare for production readiness

You do NOT need it for basic coding.

4️⃣ How to run observability only

From the project root:

docker compose -f docker-compose.observability.yml up

This will:

Start Prometheus

Start Grafana

Expose dashboards

Access URLs
Tool URL
Prometheus <http://localhost:9090>

Grafana <http://localhost:3000>

Default Grafana login:

username: admin
password: admin

5️⃣ How to run app + observability together
docker compose \
  -f docker-compose.yml \
  -f docker-compose.observability.yml \
  up

What happens here?

Docker merges both files into one stack:

App services

Databases

Kafka

Redis

Prometheus

Grafana

👉 One command → full platform

6️⃣ Why this matters (simple explanation)

Without observability:

You don’t know if your service is healthy

You don’t see memory leaks

You don’t know why something is slow

With observability:

You see problems before users do

You debug faster

You build production confidence

This is mandatory for real systems.

7️⃣ Folder structure (expected)
aliexpress-platform/
├── docker-compose.yml
├── docker-compose.observability.yml
├── observability/
│   ├── prometheus/
│   │   └── prometheus.yml
│   └── grafana/
│       ├── dashboards/
│       └── provisioning/
└── core/

8️⃣ TL;DR (remember this)

docker-compose.yml → run the app

docker-compose.observability.yml → monitor the app

Use both together for production-like setup

🏁 Final staff-level takeaway

Observability is not optional.
If you don’t measure it, you can’t trust it.

You’re building this the right way 👏
