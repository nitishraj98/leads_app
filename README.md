# Leads App

A Flask-based lead capture API that saves form submissions to PostgreSQL and
sends branded confirmation emails to the user and admin notification emails to
your team.

---

## Project Structure

```
leads_app/
 app.py                  # App factory & entry point
 requirements.txt
 .env.example

 config/
    settings.py         # All env vars & constants

 db/
    database.py         # DB connection, init, save & fetch

 email/
    sender.py           # SMTP dispatch logic
    user_template.py    # User confirmation HTML email
    admin_template.py   # Admin notification HTML email

 routes/
    index.py            # GET  /         (contact form UI)
    submit.py           # POST /submit   (form handler)
    leads.py            # GET  /leads    (API key protected)

 utils/
     validators.py       # Email, phone & spam validation
     helpers.py          # https(), label(), dash() helpers
```

---

## Quick Start

### 1. Clone & create a virtual environment

```bash
git clone <your-repo-url>
cd leads_app
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
# Edit .env with your real values
```

### 4. Set up PostgreSQL

Make sure PostgreSQL is running, then create the database:

```sql
CREATE DATABASE leads_db;
```

The table is created automatically on first run via `init_db()`.

### 5. Run the app

```bash
python app.py
```

The app starts at `http://localhost:5000`.

---

## API Reference

### `GET /`
Renders the built-in HTML contact form for quick testing.

---

### `POST /submit`

Submit a new lead.

**Rate limit:** 5 requests / minute per IP

**Request body (JSON):**

| Field          | Type   | Required | Description                        |
|----------------|--------|----------|------------------------------------|
| `name`         | string |        | Full name                          |
| `email`        | string |        | Valid email address                |
| `phone`        | string |          | 10-digit phone number              |
| `message`      | string |          | Max 1 000 characters               |
| `website_key`  | string |          | Source website URL                 |
| `product`      | string |          | Product name                       |
| `product_type` | string |          | Product category                   |
| `company`      | string |          | **Honeypot**  must be left empty  |

**Success response:**
```json
{ "success": true, "message": "Submitted! Check your email for confirmation." }
```

**Error response:**
```json
{ "success": false, "message": "Name and email are required." }
```

---

### `GET /leads`

Fetch paginated leads.

**Authentication:** `X-API-Key` header (set via `LEADS_API_KEY` in `.env`)

**Query parameters:**

| Param         | Default | Description                      |
|---------------|---------|----------------------------------|
| `website_key` |        | Filter by source website         |
| `limit`       | 50      | Number of results to return      |
| `offset`      | 0       | Pagination offset                |

**Example:**
```bash
curl -H "X-API-Key: your-api-key" \
     "http://localhost:5000/leads?website_key=example.com&limit=10"
```

---

## Gmail Setup (App Password)

1. Enable 2-Step Verification on your Google account.
2. Go to **Google Account  Security  App Passwords**.
3. Generate a password for "Mail" and paste it as `SENDER_PASSWORD` in `.env`.

---

## Deployment Notes

- Set `debug=False` in production.
- Use **Gunicorn** behind **Nginx** for production serving:
  ```bash
  gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
  ```
- Store `.env` secrets securely (e.g. via your host's environment variable manager).

WowPhone leads are sent through SMTP using the `WOWPHONE_SMTP_*`,
`WOWPHONE_SENDER_*`, and `WOWPHONE_ADMIN_EMAILS` settings. If they are omitted,
the default SMTP settings are used. If the configured WowPhone SMTP connection,
authentication, or send fails, the app retries once with the default SMTP
settings. WowPBX continues to use Mailgun.

