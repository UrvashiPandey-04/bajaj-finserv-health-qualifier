# 🚀 Bajaj Finserv Health Qualifier – FastAPI Automation System

A production-ready FastAPI backend application built for the **Bajaj Finserv Health Qualifier Challenge**.

This project automates the complete qualifier workflow including:

* Webhook generation
* SQL query selection
* Authentication handling
* Automated query submission
* Startup event execution
* Cloud deployment on Render
* Health monitoring & logging

---

# 🌐 Live Deployment

## 🔗 Live API

https://bajaj-finserv-health-qualifier.onrender.com

## ❤️ Health Endpoint

https://bajaj-finserv-health-qualifier.onrender.com/health

## 📦 GitHub Repository

https://github.com/UrvashiPandey-04/bajaj-finserv-health-qualifier

## ☁️ Render Dashboard

https://dashboard.render.com/web/srv-d8ajdkn7f7vs73d7bna0

---

# 📌 Project Overview

The application automatically executes the following workflow during startup:

1. Sends a POST request to generate a webhook
2. Receives:

   * Webhook URL
   * Access Token
3. Detects whether the registration number is Odd/Even
4. Selects the assigned SQL question
5. Generates the required SQL query
6. Submits the query automatically to the webhook endpoint
7. Logs responses and deployment status

---

# 🛠️ Tech Stack

* Python 3.11
* FastAPI
* Uvicorn
* Requests
* Render
* GitHub
* Environment Variables (.env)

---

# ✨ Features

✅ Automated startup execution
✅ REST API integration
✅ Webhook handling
✅ Authentication token handling
✅ SQL query automation
✅ Structured logging
✅ Health monitoring endpoint
✅ Production-ready deployment
✅ Render auto deployment
✅ GitHub integration

---

# 📂 Project Structure

```bash
.
├── app
│   ├── main.py
│   ├── config.py
│   ├── services
│   │   ├── webhook_service.py
│   │   ├── sql_service.py
│   │   └── submit_service.py
│   ├── utils
│   │   ├── logger.py
│   │   └── helpers.py
│
├── logs
├── requirements.txt
├── render.yaml
├── Procfile
├── runtime.txt
├── .env.example
├── README.md
```

---

# ⚙️ Environment Variables

Create a `.env` file in the project root:

```env
NAME=Your Name
REG_NO=Your Registration Number
EMAIL=your@email.com
```

---

# 🧪 Local Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/UrvashiPandey-04/bajaj-finserv-health-qualifier.git
```

## 2️⃣ Navigate to Project

```bash
cd bajaj-finserv-health-qualifier
```

## 3️⃣ Create Virtual Environment

```bash
python -m venv venv
```

## 4️⃣ Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

---

# 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run Locally

```bash
uvicorn app.main:app --reload
```

---

# ☁️ Render Deployment

## Build Command

```bash
pip install -r requirements.txt
```

## Start Command

```bash
uvicorn app.main:app --host 0.0.0.0 --port 10000
```

---

# ❤️ Health Check Endpoint

Endpoint:

```bash
/health
```

Example Response:

```json
{
  "status": "healthy"
}
```

---

# ✅ Deployment Verification

The deployment was successfully verified with:

* HTTP 200 responses
* Successful FastAPI startup events
* Successful webhook generation
* Successful SQL query submission
* Successful deployment monitoring
* Healthy Render service status

---

# 📖 Learning Outcomes

This project demonstrates practical experience with:

* Backend Development
* FastAPI
* REST APIs
* Webhooks
* Authentication Tokens
* Cloud Deployment
* Render Hosting
* GitHub Workflow
* Environment Variables
* Logging & Monitoring
* Production Debugging

---

# 👩‍💻 Author

## Urvashi Pandey

B.Tech CSE (AI & ML)

Passionate about:

* Backend Development
* APIs
* Data Science
* Machine Learning
* Cloud Deployment

---

# 📜 License

This project was developed for the Bajaj Finserv Health Qualifier Challenge.
