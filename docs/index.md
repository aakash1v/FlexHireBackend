# FlexHire Backend

The FlexHire backend powers the platform's job posting, user management, and chat features.

## Overview

- **Framework:** Django + Django REST Framework
- **Language:** Python 3.13
- **Database:** PostgreSQL
- **Cache/Queue:** Redis
- **Deployment:** Nginx + Gunicorn + Docker

## Key Apps
- `apps.users`: authentication, user profiles
- `apps.jobs`: job creation and applications
- `apps.chat`: real-time WebSocket chat
