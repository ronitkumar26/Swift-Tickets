# SwiftTicket 🎫
**A Support Ticketing System Backend built with FastAPI and PostgreSQL.**

SwiftTicket is a robust backend solution designed to handle customer support workflows. It features secure user authentication, role-based access control, and efficient ticket management, all packaged within a scalable Dockerized environment.

---

## 🚀 Features
* **Authentication:** Secure user signup and login using **OAuth2 with JWT (JSON Web Tokens)**.
* **Ticket Management:** Full CRUD operations (Create, Read, Update, Delete) for support tickets.
* **Database Integration:** Relational data modeling with **PostgreSQL** and **SQLAlchemy ORM**.
* **Schema Validation:** Strict data validation using **Pydantic** models.
* **API Documentation:** Automatically generated interactive docs via **Swagger UI**.
* **Containerization:** Fully Dockerized setup for consistent development and deployment.
* **Database Migrations:** Managed schema changes using **Alembic**.

---

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Framework:** FastAPI
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **DevOps:** Docker, Docker Compose
* **Security:** Passlib (Bcrypt), Python-Jose (JWT)

---

## 📂 Project Structure
```text
.
├── alembic/             # Database migration scripts
├── app/                 # Main application source code
│   ├── core/            # Security (JWT) and Global Settings
│   ├── database/        # Session and Engine configuration
│   ├── models/          # SQLAlchemy database entities
│   ├── routers/         # API endpoint definitions
│   ├── schemas/         # Pydantic data validation models
│   ├── services/        # Core business logic
│   ├── __init__.py
│   └── main.py          # FastAPI application entry point
├── .env                 # Local environment variables
├── .gitignore           # Files to exclude from Git
├── alembic.ini          # Alembic configuration
├── docker-compose.yml   # Multi-container setup (App + DB)
├── Dockerfile           # Backend container instructions
├── README.md            # Project documentation
└── requirements.txt     # Python dependencies

```

---

## 📦 Getting Started

### Prerequisites

* Docker and Docker Compose installed on your machine.

### Installation & Setup

1. **Clone the repository:**
```bash
git clone [https://github.com/ronitkumar26/Swift-Tickets.git](https://github.com/ronitkumar26/Swift-Tickets.git)
cd Swift-Tickets

```


2. **Configure Environment:**
Create a `.env` file in the root directory and add:
```env
DATABASE_URL=postgresql://user:password@db:5432/swiftticket
SECRET_KEY=your_generated_secret_key
ALGORITHM=HS256

```


3. **Spin up with Docker:**
```bash
docker-compose up --build

```


The server will start at `http://localhost:8000`.

---


