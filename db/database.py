import psycopg2
from config.settings import DB_CONFIG


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def init_db():
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
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Idempotent column additions (safe on existing tables)
    for col, dtype in [
        ("website_key",  "VARCHAR(255)"),
        ("product",      "VARCHAR(255)"),
        ("product_type", "VARCHAR(255)"),
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
    print("✅ PostgreSQL table ready.")


def save_lead(name, email, phone, message, website_key, product, product_type):
    conn = get_connection()
    cur  = conn.cursor()
    cur.execute(
        """INSERT INTO form_submissions
           (name, email, phone, message, website_key, product, product_type)
           VALUES (%s, %s, %s, %s, %s, %s, %s)""",
        (name, email, phone, message, website_key, product, product_type),
    )
    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Saved: {name} <{email}>")


def fetch_leads(website_key=None, limit=50, offset=0):
    conn = get_connection()
    cur  = conn.cursor()

    query  = """
        SELECT id, name, email, phone, message,
               website_key, product, product_type, submitted_at
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
            "submitted_at": row[8].isoformat() if row[8] else None,
        }
        for row in rows
    ]

    return leads, total
