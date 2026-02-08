import pyodbc

try:
    connection_string = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=DIST-6-505.uopnet.plymouth.ac.uk;"
        "DATABASE=COMP2001_HK_WLui;"
        "UID=HK_WLui;"
        "PWD=wiHR0U3a;"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
        "Connection Timeout=30;"
    )

    print("🔗 Testing database connection...")
    print(f"Server: DIST-6-505.uopnet.plymouth.ac.uk")
    print(f"Database: COMP2001_HK_WLui")
    print(f"User: HK_WLui")

    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # Test query
    cursor.execute("SELECT @@VERSION")
    version = cursor.fetchone()[0]
    print(f"✅ Connection successful!")
    print(f"SQL Server version: {version[:100]}...")

    # Test CW2 schema
    print("\n📊 Testing CW2 schema...")
    cursor.execute("SELECT COUNT(*) FROM CW2.Trail")
    trail_count = cursor.fetchone()[0]
    print(f"Trails in CW2.Trail: {trail_count}")

    cursor.execute("SELECT TOP 3 TrailID, TrailName FROM CW2.Trail")
    trails = cursor.fetchall()
    print("First 3 trails:")
    for trail in trails:
        print(f"  ID {trail[0]}: {trail[1]}")

    cursor.close()
    conn.close()

except pyodbc.Error as e:
    print(f"❌ Database error: {e}")
    print("\nTroubleshooting steps:")
    print("1. Check VPN is connected to university network")
    print("2. Verify ODBC Driver 17 is installed")
    print("3. Check credentials in .env file")
except Exception as e:
    print(f"❌ Unexpected error: {e}")