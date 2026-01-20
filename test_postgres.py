import psycopg2

try:
    # Test connection to default PostgreSQL
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",  # Default database
        user="postgres",
        password="telegram_pass",
        port="5432"
    )
    print("✅ Connected to PostgreSQL!")
    
    cursor = conn.cursor()
    
    # Create database if not exists
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'medical_warehouse'")
    if not cursor.fetchone():
        cursor.execute("CREATE DATABASE medical_warehouse")
        print("✅ Created database: medical_warehouse")
    else:
        print("✅ Database already exists: medical_warehouse")
    
    conn.close()
    
except Exception as e:
    print(f"❌ PostgreSQL connection failed: {e}")
    print("\nInstall PostgreSQL from: https://www.postgresql.org/download/windows/")
    print("Use password: telegram_pass")
    print("Port: 5432")