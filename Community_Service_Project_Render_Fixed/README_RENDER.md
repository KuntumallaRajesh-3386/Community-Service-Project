# Render Deployment

This project uses PostgreSQL on Render when `DATABASE_URL` is set. It falls back to the included SQLite database for local development.

## Render settings

Build command:
```bash
pip install -r requirements.txt
```

Start command:
```bash
gunicorn app:app
```

Set the `DATABASE_URL` environment variable to the **Internal Database URL** from your Render PostgreSQL database (or another PostgreSQL provider). The app creates the `feedback` table automatically on startup.

Do not put database credentials directly in `app.py` or commit a `.env` file.
