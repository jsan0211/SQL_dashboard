# Live Dashboard Project

A Django-based internal dashboard that supports toggling between SQLite and Microsoft SQL Server (MSSQL) as the backend. Built to make development and deployment seamless, even across environments.

---

## Features

* Toggle between SQLite and MSSQL by editing a `.env` variable
* Start, stop, and restart the Django development server using a custom Python script
* Automatically open browser on server start
* Logs server output to `server.log`
* Tracks process with `server.pid`
* Includes a debug endpoint to confirm environment settings

---

## Setup

### 1. Clone and create your virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Set up your `.env` file

```ini
# Switch between 'sqlite' or 'mssql'
DATABASE_TYPE=sqlite

# Required if DATABASE_TYPE=mssql
DB_NAME=YourDatabaseName
DB_USER=YourUsername
DB_PASSWORD=YourPassword
DB_HOST=YourHostOrIP
DB_DRIVER=ODBC Driver 17 for SQL Server

SECRET_KEY=your-secret-key
```

> If you're using SQLite, it's fine to comment out the DB settings.

---

## Running the Server

Use the `toggle_server.py` script for full control:

```bash
python toggle_server.py start      # Start the server in background
python toggle_server.py stop       # Stop the server
python toggle_server.py restart    # Restart the server
python toggle_server.py status     # Check if server is running
```

* Output is logged to `server.log`
* PID is saved to `server.pid`
* Server opens automatically in your browser

---

## Debugging

Visit this endpoint to check config:

```http
http://127.0.0.1:8000/debug/
```

Example output:

```json
{
  "engine": "django.db.backends.sqlite3",
  "name": ".../db.sqlite3",
  "host": "",
  "driver": null,
  "env_secret_key_loaded": true
}
```

---

## Structure

```bash
live_dashboard/
├── dashboard/           # Your app
├── live_dashboard/      # Main project config
├── toggle_server.py     # Server controller
├── .env                 # Environment config
├── server.log           # Server output
├── server.pid           # PID of running process
├── README.md            # This file
```

---

## Tips

* Always activate your virtual environment before running scripts
* Use `restart` if you're unsure whether the server is running
* Check `server.log` if something isn't working

---

## To Do

* Add authentication and permissions
* Improve front-end dashboard styling
* Support Docker for containerized deployment
