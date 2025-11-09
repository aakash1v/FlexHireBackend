# Architecture Overview

```mermaid
flowchart TD
    A[Client App] -->|REST API| B(Django Backend)
    B --> C[(PostgreSQL)]
    B --> D[(Redis)]
    B --> E[Celery Worker]
```
