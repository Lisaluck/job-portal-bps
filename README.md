# 🏦 IBPS Job Portal - Django REST API

A complete Django REST Framework API for managing IBPS job listings with JWT authentication and secure endpoints.

![Django](https://img.shields.io/badge/Django-4.2.7-green)
![DRF](https://img.shields.io/badge/Django_REST_Framework-3.14.0-blue)
![Python](https://img.shields.io/badge/Python-3.8+-yellow)

## 🚀 Features

- **RESTful API** with Django REST Framework
- **JWT Authentication** for secure access
- **CRUD Operations** for job management
- **SQLite Database** with Django ORM
- **API Documentation** with Postman collection
- **CORS Enabled** for frontend integration

## 📋 API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/status/` | API health check | ❌ |
| `POST` | `/api/login/` | JWT token generation | ❌ |
| `GET` | `/api/jobs/` | Get all job listings | ✅ |
| `POST` | `/api/jobs/add/` | Add new job listing | ✅ |

## 🛠️ Installation

### 1. Clone Repository
```bash
git clone https://github.com/lisaluck/ibps-job-portal.git
cd ibps-job-portal/ibps_api
