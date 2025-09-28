# Task Manager with CRUD & Dashboard 📊

This is a **Task Management project (Tasks, Users, Projects)** built with **FastAPI (backend)** and **Streamlit (frontend)**.  
The main goal is to practice **Data Engineer** concepts, exploring CRUD operations, APIs, and interactive dashboards.

---

## 🚀 Features

- **Full CRUD**
  - Users
  - Projects
  - Tasks
- **Interactive Dashboard with**:
  - Filters by user and project
  - Pie chart showing task percentage by status
  - Grouped bar chart (user × task status)
  - Additional insights through charts
- **Frontend-Backend Integration**
  - Streamlit consuming the FastAPI endpoints
  - Communication via `requests`

---

## 🏗️ Project Structure

```bash
task-manager/
│
├── backend/                # FastAPI
│   ├── main.py              # backend entrypoint
│   ├── models/              # data models (SQLAlchemy/Pydantic)
│   ├── routers/             # organized routes (users, projects, tasks)
│   └── db/                  # database connection and initialization
│
├── frontend/               # Streamlit
│   ├── main.py              # main app (navigation and sessions)
│   ├── user_page.py         # user management section
│   ├── project_page.py      # project management section
│   ├── task_page.py         # task management section
│   └── dashboard.py         # dashboards with charts
│
├── docker-compose.yml       # container orchestration
├── requirements.txt         # dependencies (backend + frontend)
└── README.md
```

## 🖼️ Architecture

  - **Frontend (Streamlit)** → calls the API

  - **Backend (FastAPI)** → exposes CRUD endpoints

  - **Database (PostgreSQL)** → persists data

  - **Docker Compose** → orchestrates all services

## ⚙️ How to Run

### 1️⃣ Requirements

  - Docker + Docker Compose
  - Git

### 2️⃣ Clone the repository
``` 
git clone https://github.com/marceloaugusto453/task_manager_using_crud.git
cd task-manager
``` 

### 3️⃣ Build and run containers

``` 
docker compose up --build
``` 

### 4️⃣ Access

  - Frontend (Streamlit): http://localhost:8501

  - Backend (FastAPI docs): http://localhost:8000/docs

## 📚 What I Wanted to Learn

  - **FastAPI** → building RESTful routes and Pydantic schemas

  - **Streamlit** → creating interactive applications for analytics

  - **API + Frontend Integration** → real-time data consumption

  - **Docker Compose** → orchestrating multiple services (frontend, backend, db)

  - **Data Visualization** → building dashboards with relevant metrics

  - **Portfolio Best Practices** → organized README, modularized code

## 🔮 Next Steps

  -  Deploy to AWS

## 👨‍💻 Author

Developed by **Marcelo Ribeiro.**