"""Database access helpers for lead submissions."""

import psycopg2
from config.settings import DB_CONFIG


def get_connection():
    """Create a database connection using configured settings."""
    return psycopg2.connect(**DB_CONFIG)


def init_db():
    """Create or upgrade the form submissions table."""
    conn = get_connection()
    cur  = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS form_submissions (
            id           SERIAL PRIMARY KEY,
            name         VARCHAR(100) NOT NULL,
            email        VARCHAR(150) NOT NULL,
            phone        VARCHAR(20),
            message      TEXT,
            website_key  VARCHAR(255),
            product      VARCHAR(255),
            product_type VARCHAR(255),
            ip_address   VARCHAR(45),
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    for col, dtype in [
        ("website_key",  "VARCHAR(255)"),
        ("product",      "VARCHAR(255)"),
        ("product_type", "VARCHAR(255)"),
        ("ip_address",   "VARCHAR(45)"),
    ]:
        cur.execute(f"""
            DO $$ BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns
                    WHERE table_name='form_submissions' AND column_name='{col}'
                )
                THEN ALTER TABLE form_submissions ADD COLUMN {col} {dtype};
                END IF;
            END$$;
        """)

    conn.commit()
    cur.close()
    conn.close()
    print("PostgreSQL table ready.")


def save_lead(name, email, phone, message, website_key, product, product_type, ip_address):
    """Persist a lead submission."""
    conn = get_connection()
    cur  = conn.cursor()
    cur.execute(
        """INSERT INTO form_submissions
           (name, email, phone, message, website_key, product, product_type, ip_address)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
        (name, email, phone, message, website_key, product, product_type, ip_address),
    )
    conn.commit()
    cur.close()
    conn.close()
    print(f"Saved: {name} <{email}>")


def fetch_leads(website_key=None, limit=50, offset=0):
    """Fetch paginated lead submissions."""
    conn = get_connection()
    cur  = conn.cursor()

    query  = """
        SELECT id, name, email, phone, message,
               website_key, product, product_type, ip_address, submitted_at
        FROM form_submissions
    """
    params = []

    if website_key:
        query += " WHERE website_key = %s"
        params.append(website_key)

    query += " ORDER BY submitted_at DESC LIMIT %s OFFSET %s"
    params += [limit, offset]

    cur.execute(query, params)
    rows = cur.fetchall()

    count_query = "SELECT COUNT(*) FROM form_submissions"
    if website_key:
        count_query += " WHERE website_key = %s"
        cur.execute(count_query, [website_key])
    else:
        cur.execute(count_query)
    total = cur.fetchone()[0]

    cur.close()
    conn.close()

    leads = [
        {
            "id":           row[0],
            "name":         row[1],
            "email":        row[2],
            "phone":        row[3],
            "message":      row[4],
            "website_key":  row[5],
            "product":      row[6],
            "product_type": row[7],
            "ip_address":   row[8],
            "submitted_at": row[9].isoformat() if row[9] else None,
        }
        for row in rows
    ]

    return leads, total


