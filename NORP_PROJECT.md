# NORP: Non-Profit Organization Project
## CS 6365 Enterprise Computing Semester Project

---

## 📌 Executive Summary

Modern Non-Profit Organizations (NPOs) face unique, complex operational challenges: orchestrating volunteer networks, securing and auditing donor transactions, scaling up digital infrastructure during emergency relief drives, and using modern data tools to optimize outreach. 

The **NORP** project aims to build a modern, high-QoS, cloud-native enterprise platform tailored specifically for NPOs. This platform translates academic principles of Enterprise Computing into practical, reliable, and scalable software solutions that support social impact.

---

## 🛠️ Application of Enterprise Computing Pillars

Our architecture is structured around the four core technical modules of CS 6365:

```
               ┌──────────────────────────────────────────────────┐
               │              NORP Enterprise Portal              │
               └─────────┬──────────────────────────────┬─────────┘
                         │                              │
        ┌────────────────▼────────────────┐    ┌────────▼────────────────────────┐
        │   MT: Transaction Management    │    │      MS: Services & Workflows   │
        │  - ACID donor ledger            │    │ - WED-flow engine               │
        │  - "Conservation of Money"      │    │ - Microservices architecture    │
        │  - Multi-party reconciliation   │    │ - Volunteer dispatching         │
        └─────────────────────────────────┘    └─────────────────────────────────┘
        ┌─────────────────────────────────┐    ┌─────────────────────────────────┐
        │       MQ: QoS & Cloud Scale     │    │         MA: AI/ML Integration   │
        │ - Statistical QoS monitoring    │    │ - LLM-powered donor outreach    │
        │ - Horizontal autoscaling        │    │ - Smart volunteer matching      │
        │ - p99 latency & resilience      │    │ - Situational awareness dashboards│
        └─────────────────────────────────┘    └─────────────────────────────────┘
```

### 1. MT: Transaction Processing (Conservation of Money)
* **Problem:** Auditable financial integrity is paramount for NPOs. Donations, grant distributions, and programmatic spending must be perfectly recorded.
* **Our Solution:** A rigorous ledger system enforcing **ACID transactions**. We implement two-phase commits for donor-to-program allocations to ensure no funds are lost or incorrectly credited, upholding the *Principle of Conservation of Money*.

### 2. MQ: Quality of Service (QoS) & Cloud Scalability
* **Problem:** NPOs experience sudden spikes in traffic during holiday donation campaigns or natural disaster responses. A slow or crashed site translates directly to lost relief funds.
* **Our Solution:** Horizontally scalable cloud infrastructure with built-in **statistical QoS guarantees**. We target **five-nines availability** (99.999% uptime) and a **p99 latency under 200ms** by implementing automated load-balancing, microservice replication, and database read-replicas.

### 3. MS: Services Computing & Workflows (WED-flow)
* **Problem:** NPO operations involve multi-step processes—such as onboarding volunteers, running background checks, and matching them with specific community events.
* **Our Solution:** Implementing a **WED-flow** (Workflows, Events, Data-flows) composition model. By decomposing the system into decentralized microservices, we build decoupled event-driven workflows that track the progression from volunteer sign-up to post-event reporting.

### 4. MA: AI/ML & Situational Awareness
* **Problem:** NPOs have limited administrative staff, making personalized donor engagement and manual resource matching highly inefficient.
* **Our Solution:** Leveraging AI tools for **situational awareness** and operational optimization:
  * **Donor Retention Predictor:** A classifier to flag donors likely to lapse, allowing proactive, personalized outreach.
  * **GenAI Campaign Assistant:** Utilizing LLMs to auto-draft highly personalized campaign newsletters based on a donor’s past giving history.
  * **Smart Matcher:** An optimized recommendation engine matching volunteers to opportunities based on skill-sets, location, and history.

---

## 📈 Project Scope: Moving from [A] to [B]

To satisfy the CS 6365 DevOps checklist, we define our explicit milestones:

### 🏁 **Starting Point [A]**
* A basic web repository with mock volunteer databases.
* Manual, un-orchestrated processes for event management and donation logging.
* No automated scalability, monitoring, or unified workflow engine.

### 🏆 **Ending Point [B]**
* A robust, cloud-deployed backend platform.
* Fully orchestrated microservices with a decoupled event engine (WED-flow).
* High-confidence transaction system with automated unit tests for concurrency.
* Live statistical QoS monitoring dashboard showing p90/p99 latencies under load tests.
* Fully integrated AI models for volunteer-to-event matching and LLM-assisted donor outreach.

---

## 🗂️ Repository & DevOps Structure

To maximize our `#Factual` evaluation, we maintain a highly structured, automated repository layout:

```
CS-6365/
│
├── .gitignore               # Excludes virtual environments and keys
├── README.md                # Project homepage & course summary
├── NORP_PROJECT.md          # Project charter & architectural overview
│
├── checkpoints/             # Contains bi-weekly DevOps reports
│   ├── checkpoint_0.md
│   └── checkpoint_1.md
│
├── src/                     # Core application source code
│   ├── transactions/        # ACID donor ledger service
│   ├── workflows/           # WED-flow volunteer orchestrator
│   ├── ai_engine/           # Smart matcher & GenAI integration
│   └── portal/              # Web/Frontend interface
│
├── tests/                   # Automated validation suites
│   ├── load_testing/        # Locust/JMeter scripts for MQ evaluation
│   └── unit_tests/          # Transaction integrity & workflow tests
│
└── scripts/                 # Automation & Reproducibility scripts
    ├── setup.sh             # One-click environment bootstrap
    └── run_tests.sh         # Executes the complete test suite
```

---

## ⚡ Initial Action Plan

1. **Phase 1: Environment Setup & Checkpoint 0**
   * Perform the reproducibility exercise by cloning and running an exemplar repository from previous semesters.
   * Document and submit the reproducibility report (`checkpoint_0.md`).
2. **Phase 2: System Blueprint & Checkpoint 1**
   * Draft the final database schemas for ACID donation tracking.
   * Detail the API gateway specifications and register our microservices.
   * Complete and submit the initial project proposal (`checkpoint_1.md`) with comprehensive self-evaluations.
