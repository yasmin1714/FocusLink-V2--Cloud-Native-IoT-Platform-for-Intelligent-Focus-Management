# FocusLink IoT Architecture & Security Specification

## System Overview
FocusLink is an IoT-centric time-series session monitoring application built using Flask, SQLAlchemy, SQLite, and an SSH-inspired host fingerprint registry.

---

## Key Architectural Principles

### 1. Database Snapshot Logging & ID Uniqueness
- **Unique Constraint Policy:** The `FocusLink` database model enforces a `primary_key=True` and `unique=True` constraint **strictly on the `id` column**.
- **Non-Unique Entity Attributes:** `username` and `email` columns explicitly carry `unique=False`.
- **Append-Only Time Series:** Every successful authentication event executes an `INSERT INTO focus_link` operation, maintaining an append-only historical log of hardware telemetry snapshots without causing duplicate key collisions.

---

### 2. Double-Hashed Host Fingerprint Registry (`data/known_hosts.csv`)
FocusLink implements a zero-trust, pseudonymous host registry that avoids exposing raw user identities or plaintext tokens anywhere in HTTP requests or client storage.