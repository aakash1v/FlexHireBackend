# 💼 FlexHire Backend

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Django](https://img.shields.io/badge/Django-5.0-darkgreen?logo=django)
![License](https://img.shields.io/github/license/Akashace49/flex-hire-backend)
[![Docs](https://img.shields.io/badge/Documentation-Online-success?style=flat&logo=readthedocs)](https://aakash1v.github.io/FlexHireBackend/)

A robust, scalable Django-based backend powering **FlexHire** — a platform for managing job postings, applications, and real-time communication between customers and workers.

---

## 🚀 Live Documentation

👉 **Read the full developer documentation here:**
🔗 [https://aakash1v.github.io/FlexHireBackend/](https://aakash1v.github.io/FlexHireBackend/)

This includes setup instructions, API reference, and architecture overview.

---

## 🧩 Tech Stack

- **Language:** Python 3.13
- **Framework:** Django + Django REST Framework
- **Database:** PostgreSQL
- **Cache/Queue:** Redis
- **Realtime:** Django Channels (WebSockets)
- **Deployment:** Gunicorn + Nginx
- **Docs:** MkDocs + Material Theme

---

## 🏗️ Project Structure
back/
├── apps/
│ ├── users/ # Authentication & user profiles
│ ├── jobs/ # Job posting and applications
│ ├── chat/ # Real-time messaging
│ └── utils/ # Helper utilities (email, etc.)
├── config/ # Django settings, URLs, ASGI/WGSI
├── templates/ # HTML templates
├── static/ # Static assets
└── docs/ # Documentation markdowns (MkDocs)

---

## ⚙️ Setup (Local Development)

1. Clone the repository:
   ```bash
   git clone https://github.com/Akashace49/flex-hire-backend.git
   cd flex-hire-backend
    ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Run migrations and start the server:
    ```bash
    python mange.py migrate
    python mange.py runserver
    ```
## 🧠 Developer Tools

Pre-commit hooks: automatic linting and formatting

Code Formatter: Black + isort

Linter: Flake8

Docs Generator: MkDocs + mkdocstrings

Version Control: Git + github

## 🧰 Environment Variables
Create a .env file in your root directory:
```bash
DJANGO_SECRET_KEY=your_secret_key_here
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost:5432/flexhire
EMAIL_HOST_USER=you@example.com
EMAIL_HOST_PASSWORD=yourpassword

```
## 🧑‍💻 Author

Aakash Kumar
💻 Backend Developer | Python | Django | Cloud
🔗 [GitHub Profile](https://github.com/aakash1v)
