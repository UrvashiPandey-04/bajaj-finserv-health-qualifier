# Bajaj Finserv Health Qualifier FastAPI Backend

A complete, production-ready **Python FastAPI** backend application that automatically executes the whole qualifier flow on startup: generates a webhook, selects the correct SQL query depending on the registration number parity, submits the SQL query to the evaluation endpoint, and displays detailed logs.

---

## 📂 Project Architecture

```text
bajaj_qualifier/
│
├── app/
│   ├── __init__.py
│   ├── main.py              # Application core and Lifespan startup workflow
│   ├── config.py            # Environment-variable configs with .env parser
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── webhook_service.py # Hook generation handler with retry logic
│   │   ├── sql_service.py     # SQL query repository & routing
│   │   └── submit_service.py  # Final submission handler
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logger.py          # Colored stdout console + rotating file logs
│       └── helpers.py         # Registration number parsing & parity check
│
├── requirements.txt         # Core dependencies
├── render.yaml              # Render blueprint deployment setup
├── Procfile                 # Uvicorn container start commands
├── runtime.txt              # Standardized python runtime environment
├── .env.example             # Configuration templates
├── .gitignore               # Safe Git exclude paths
└── README.md                # System documentation (This file!)
```

---

## ⚙️ Core Technical Specifications

### 1. Webhook Generation (Phase 1)
Upon application startup, an automated asynchronous context execution triggers an HTTP `POST` request to:
* **Endpoint:** `https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON`
* **JSON Payload:**
  ```json
  {
    "name": "YOUR_NAME",
    "regNo": "YOUR_REG_NO",
    "email": "YOUR_EMAIL"
  }
  ```
The service automatically extracts and returns the **`webhook` URL** and the **`accessToken`**.
* **Resilience Features:** Built-in configurable exponential backoff retry mechanics (defaulting to 3 retries) and request timeout safeguards.

### 2. Registration Number Routing Logic (Phase 2)
The utility extracts the **last numerical digit** of the Candidate Registration Number (`REG_NO`):
* **Odd Digits (e.g. 1, 3, 5, 7, 9):** Routes to **SQL Question 1**.
* **Even Digits (e.g. 0, 2, 4, 6, 8):** Routes to **SQL Question 2**.

---

## 🗄️ SQL Solutions Detailed Walkthrough

### 📊 Question 1 (Odd Last Digit)
**Objective:** Find the highest salary credited to an employee, but only for transactions **NOT** made on the 1st day of any month. Returns `SALARY`, combined `NAME`, `AGE`, and `DEPARTMENT_NAME`.
* **PostgreSQL Solution (Recommended for Production):**
  ```sql
  SELECT 
      p.AMOUNT AS SALARY,
      (e.FIRST_NAME || ' ' || e.LAST_NAME) AS NAME,
      EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.DOB)) AS AGE,
      d.DEPARTMENT_NAME
  FROM PAYMENTS p
  JOIN EMPLOYEE e ON p.EMP_ID = e.EMP_ID
  JOIN DEPARTMENT d ON e.DEPARTMENT = d.DEPARTMENT_ID
  WHERE EXTRACT(DAY FROM p.PAYMENT_TIME) != 1
  ORDER BY p.AMOUNT DESC
  LIMIT 1;
  ```
* **MySQL Alternative (Included in `sql_service.py`):**
  ```sql
  SELECT 
      p.AMOUNT AS SALARY,
      CONCAT(e.FIRST_NAME, ' ', e.LAST_NAME) AS NAME,
      TIMESTAMPDIFF(YEAR, e.DOB, CURDATE()) AS AGE,
      d.DEPARTMENT_NAME
  FROM PAYMENTS p
  JOIN EMPLOYEE e ON p.EMP_ID = e.EMP_ID
  JOIN DEPARTMENT d ON e.DEPARTMENT = d.DEPARTMENT_ID
  WHERE DAY(p.PAYMENT_TIME) != 1
  ORDER BY p.AMOUNT DESC
  LIMIT 1;
  ```

### 📊 Question 2 (Even Last Digit)
**Objective:** For each employee, calculate how many employees in the same department are younger than them. Returns `EMP_ID`, `FIRST_NAME`, `LAST_NAME`, `DEPARTMENT_NAME`, and `YOUNGER_EMPLOYEES_COUNT`. Ordered by `EMP_ID DESC`.
* **Dialect-Agnostic standard SQL Solution (Compatible with SQLite, MySQL, PostgreSQL, etc.):**
  * *Note:* A person is younger than the current employee if their Date of Birth (DOB) is strictly greater (more recent) than the current employee's DOB. By using a direct date comparison (`e2.DOB > e.DOB`), we avoid database-specific age calculations entirely.
  ```sql
  SELECT 
      e.EMP_ID, 
      e.FIRST_NAME, 
      e.LAST_NAME, 
      d.DEPARTMENT_NAME,
      (
          SELECT COUNT(*) 
          FROM EMPLOYEE e2 
          WHERE e2.DEPARTMENT = e.DEPARTMENT 
            AND e2.DOB > e.DOB
      ) AS YOUNGER_EMPLOYEES_COUNT
  FROM EMPLOYEE e
  JOIN DEPARTMENT d ON e.DEPARTMENT = d.DEPARTMENT_ID
  ORDER BY e.EMP_ID DESC;
  ```

---

## 🚀 Execution & Submission (Phase 3)
The app extracts the generated query and automatically posts it:
* **Endpoint:** `https://bfhldevapigw.healthrx.co.in/hiring/testWebhook/PYTHON`
* **Headers:**
  ```http
  Authorization: <accessToken>
  Content-Type: application/json
  ```
* **Body:**
  ```json
  {
    "finalQuery": "YOUR_SQL_QUERY"
  }
  ```
Detailed feedback and evaluation logs are printed and written directly to `logs/app.log`.

---

## 💻 Local Testing & Development

### 1. Copy Environment Configuration
Create a local `.env` file based on `.env.example`:
```bash
cp .env.example .env
```
Fill in your credentials:
```ini
NAME=Your Name
REG_NO=YourRegistrationNumber
EMAIL=your.email@example.com
DB_DIALECT=postgresql
```

### 2. Setup Virtual Environment & Install Dependencies
```bash
# Create environment
python -m venv .venv

# Activate environment (Windows)
.venv\Scripts\activate

# Activate environment (Mac/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run FastAPI Server
```bash
uvicorn app.main:app --reload
```

---

## 📈 Sample Terminal Logs

On startup, your console will output colorful, structured records:

```text
[App] 11:05:00 - INFO - ==================================================
[App] 11:05:00 - INFO - FASTAPI APP LIFESPAN STARTING - RUNNING AUTOMATIC WORKFLOW
[App] 11:05:00 - INFO - ==================================================
[App] 11:05:01 - INFO - ==================================================
[App] 11:05:01 - INFO - PHASE 1: GENERATING WEBHOOK
[App] 11:05:01 - INFO - ==================================================
[App] 11:05:01 - INFO - Target URL: https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON
[App] 11:05:01 - INFO - Sending POST request (Attempt 1/3)...
[App] 11:05:02 - INFO - HTTP Status Code: 200
[App] 11:05:02 - INFO - Successfully generated Webhook credentials:
[App] 11:05:02 - INFO - -> Webhook URL: https://bfhldevapigw.healthrx.co.in/hiring/testWebhook/PYTHON
[App] 11:05:02 - INFO - -> Access Token: eyJhbGciOiJIUzI1... [TRUNCATED]
[App] 11:05:02 - INFO - ==================================================
[App] 11:05:02 - INFO - PHASE 2: RESOLVING SQL QUERY SELECTION
[App] 11:05:02 - INFO - ==================================================
[App] 11:05:02 - INFO - Parsing registration number 'REG12347' to determine odd/even logic...
[App] 11:05:02 - INFO - Extracted last numerical digit: 7
[App] 11:05:02 - INFO - Parity of last digit (7) is ODD.
[App] 11:05:02 - INFO - -> Registration number is ODD. Selecting SQL Question 1.
[App] 11:05:02 - INFO - -> Using PostgreSQL dialect for Question 1.
[App] 11:05:02 - INFO - Selected SQL Query:
SELECT 
    p.AMOUNT AS SALARY,
    (e.FIRST_NAME || ' ' || e.LAST_NAME) AS NAME,
    EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.DOB)) AS AGE,
    d.DEPARTMENT_NAME
FROM PAYMENTS p
JOIN EMPLOYEE e ON p.EMP_ID = e.EMP_ID
JOIN DEPARTMENT d ON e.DEPARTMENT = d.DEPARTMENT_ID
WHERE EXTRACT(DAY FROM p.PAYMENT_TIME) != 1
ORDER BY p.AMOUNT DESC
LIMIT 1;

[App] 11:05:02 - INFO - ==================================================
[App] 11:05:02 - INFO - PHASE 3: SUBMITTING FINAL SQL QUERY
[App] 11:05:02 - INFO - ==================================================
[App] 11:05:02 - INFO - Sending query submission POST request...
[App] 11:05:03 - INFO - HTTP Status Code: 200
[App] 11:05:03 - INFO - Submission Response Text: {"success": true, "message": "Query submitted successfully!"}
[App] 11:05:03 - INFO - Submission SUCCESS: Query successfully validated by server.
[App] 11:05:03 - INFO - ==================================================
[App] 11:05:03 - INFO - QUALIFIER FLOW EXECUTED SUCCESSFULLY
[App] 11:05:03 - INFO - ==================================================
```

---

## 🌐 Production Deployment Guides

### ☁️ Render Deployment
1. **Prepare GitHub Repository:**
   * Initialize git and push to GitHub (see GitHub setup steps).
2. **Deploy via render.yaml Blueprint (Recommended):**
   * Go to **Render Dashboard** -> **New** -> **Blueprint**.
   * Connect your GitHub repository.
   * Render will automatically read the `render.yaml` configuration and provision the service with all settings preconfigured!
3. **Manual Deploy option:**
   * Create a new **Web Service**.
   * Connect your GitHub repo.
   * Set **Build Command** to `pip install -r requirements.txt`.
   * Set **Start Command** to `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
   * Under **Environment Variables**, add: `NAME`, `REG_NO`, `EMAIL`, and `DB_DIALECT`.

### ☁️ Railway Deployment
1. Log in to your **Railway Dashboard**.
2. Click **New Project** -> **Deploy from GitHub repo**.
3. Select your repository.
4. Railway will automatically detect the Python environment and the `Procfile`, then build and deploy the app.
5. In the **Variables** tab, add your environment settings (`NAME`, `REG_NO`, `EMAIL`).

---

## 🛠️ Tool Integration with Antigravity
Using this template alongside modern developer tools maximizes efficiency:
1. **GitHub Continuous Deployment:** Push code changes to trigger automated builds and test query runs on Render or Railway instantly.
2. **Postman & Thunder Client:** Test the `/health` endpoint or mock APIs locally.
3. **VS Code:** Leverage built-in linters and type completion to easily adjust query parameters.
