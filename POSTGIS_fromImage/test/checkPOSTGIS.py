import sys
try:
    import psycopg2
except Exception as e:
    print(e)
    sys.exit('ERROR: cannot find psyconpg2 module')

def check_postgis_installed(database, user, password, host='localhost', port=5432):
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            dbname=database,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cursor = connection.cursor()

        # Check if PostGIS extension is installed
        cursor.execute("SELECT postgis_full_version();")
        result = cursor.fetchone()

        if result:
            print("PostGIS is installed.")
            print("PostGIS Version:", result[0])
        else:
            print("PostGIS is not installed.")

    except psycopg2.Error as e:
        print("Error connecting to the database or executing query:", e)
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

# Replace with your database connection details
check_postgis_installed(
    database="postgis",
    user="usuario",
    password="pass",
)