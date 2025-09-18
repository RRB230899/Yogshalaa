# 🧘 YogShalaa — A Wellness & Yoga Platform

**YogShalaa** is a **full-stack Django web application** designed to make yoga and wellness more accessible.  
It offers an engaging platform where users can explore yoga sessions, track their progress, and connect with holistic wellness practices.  

The project is **fully built using Django**, configured and hosted on **Render**, with **Stripe** for payments and **Google Firebase Auth** for OTP-based authentication.

---

## ✨ Features
- 🌐 **Full Django Web App** — robust backend with clean frontend integration  
- 🧘 **Yoga & Wellness Modules** — curated practices, sessions, and progress tracking  
- 👤 **User-Friendly UI** — responsive, modern design for seamless experience  
- 🔒 **Secure Authentication** — OTP login via Google Firebase  
- 💳 **Integrated Payment Gateway** — Stripe for session purchases  
- 📊 **Scalable Architecture** — API-driven for future enhancements  

---

## 🛠️ Tech Stack
- **Frontend & Backend**: Django, Django Templates, HTML, CSS, JavaScript  
- **Database**: SQLite (development) / PostgreSQL (production-ready)  
- **Authentication**: Google Firebase OTP  
- **Payment Gateway**: Stripe  
- **Hosting/Deployment**: Render  

---

## 🚀 Live Demo
- **Gallery**: [https://yogshalaa.onrender.com/gallery](https://yogshalaa.onrender.com/gallery)  
- **Class Coverage**: [https://yogshalaa.onrender.com/coverage](https://yogshalaa.onrender.com/coverage)
- **Landing Page**: [https://yogshalaa.onrender.com](https://yogshalaa.onrender.com)

---

## 🚀 Getting Started

### 1. Clone the Repository
git clone https://github.com/RRB230899/Yogshalaa.git
cd Yogshalaa

### 2. Project Structure

```text
YogShalaa/
├─ yogshalaa/ # Django project settings
│ ├─ init.py
│ ├─ settings.py
│ ├─ urls.py
│ └─ wsgi.py
├─ landing_page/ # Core Django app for landing pages and main features
│ ├─ migrations/
│ ├─ templates/
│ ├─ static/
│ ├─ admin.py
│ ├─ apps.py
│ ├─ models.py
│ ├─ views.py
│ └─ urls.py
├─ templates/ # Global templates
├─ static/ # Global static files (CSS, JS, images)
├─ manage.py # Django management script
└─ requirements.txt # Python dependencies
