# errorful_ecommerce_platform
This dummy project helps in the generation of few errors, which will be used for further study by our team.
---
---

# 🛒 E-commerce Platform Dummy Project

Simulates **realistic incidents and failures** in an e-commerce system to generate logs, metrics, and traces for **postmortem analysis**.

This project is ideal for experimenting with **LLM-powered RCA agents, remediation planners, and postmortem generators**.

---

## 🚀 Quick Setup

### 1️⃣ Clone & Setup Project Structure

```bash
mkdir -p ecommerce-platform/{config,services/{user-service,product-service,order-service,payment-service},infrastructure,monitoring,logs,scripts}
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Simulation

```bash
python run_ecommerce_platform.py
```

---

## 📂 Project Overview

### 🔧 Components

* **`run_ecommerce_platform.py`** → Main entry point, simulates incidents & logs
* **`logs/`** → Application, error, and access logs (with timestamped filenames)
* **`services/`** → Placeholder microservices (user, product, order, payment)
* **`monitoring/`** → Metrics & health check generators

### 📝 Log Files

Each run generates timestamped log files in `logs/`:

* `application_YYYYMMDD_HHMMSS.log` → Info & warnings
* `error_YYYYMMDD_HHMMSS.log` → Errors & critical events
* `access_YYYYMMDD_HHMMSS.log` → Simulated HTTP access logs

---

## 💥 Incident Types Simulated

* 🗄 **Database Issues** → Connection pool exhaustion, stuck queries
* 🧠 **Memory Leaks** → OOM errors in product service
* ⚙️ **Configuration Errors** → Wrong timeouts, missing API keys
* 🌐 **Network Issues** → Timeouts, external API failures
* 🔑 **Authentication Failures** → JWT validation problems
* 💻 **Resource Constraints** → High CPU, disk exhaustion
* 🔌 **Third-Party Failures** → Payment gateway (Stripe) downtime

---

## 📊 Data Generated

* **Structured application logs** with timestamps
* **Error logs** with stack traces & service context
* **Access logs** with realistic HTTP request patterns
* **Metrics** → CPU, memory, disk usage, latency, throughput
* **Service health status changes** → Running → Degraded → Critical → Down

---

## 🤖 Use Case: Postmortem Automation

Feed the generated logs into your **LLM-driven incident management pipeline**:

1. **RCA Agent** → Identify root causes (e.g., config errors, resource exhaustion)
2. **Remediation Agent** → Suggest fixes (config rollback, scale infra, retry policies)
3. **Report Generator** → Produce structured postmortem reports (timeline, impact, action items)

---

## 🧪 Example Run

```bash
$ python run_ecommerce_platform.py
🚀 Starting E-commerce Platform Simulation
✅ user-service (port 8001): HEALTHY
📊 Generating baseline metrics...
🌐 Generating access logs...
🎯 Simulating incident scenarios...
🔥 product-service: CRITICAL - Memory leak detected
❌ payment-service: DOWN - Config rollback required
🏁 Simulation completed!
📝 Check logs/ directory for detailed incident logs
🔍 Run your postmortem automation platform on these logs
```

---

## 🎯 Why This Project?

This is a **small but comprehensive sandbox** for practicing:

* Incident simulation & failure injection
* Observability log/metric collection
* LLM-powered **postmortem analysis pipelines**

It deliberately introduces **bugs, misconfigurations, and outages** you’d face in real-world systems.

---
