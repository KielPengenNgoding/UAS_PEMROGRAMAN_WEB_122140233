import psycopg2
import configparser
import os

def test_postgres_connection(manual_password=None):
    """Test connection to PostgreSQL database."""
    try:
        # Read database URL from development.ini
        config = configparser.ConfigParser()
        here = os.path.dirname(os.path.abspath(__file__))
        config_file = os.path.join(here, 'development.ini')
        config.read(config_file)
        
        # Get database connection parameters from the URL
        db_url = config.get('app:main', 'sqlalchemy.url')
        print(f"Database URL: {db_url}")
        
        # Parse the URL to get connection parameters
        # Format: postgresql://username:password@host:port/dbname
        db_url = db_url.replace('postgresql://', '')
        user_pass, host_db = db_url.split('@')
        
        if ':' in user_pass:
            username, password = user_pass.split(':')
        else:
            username = user_pass
            password = ''
            
        # Use manual password if provided
        if manual_password:
            password = manual_password
            
        if '/' in host_db:
            host_port, dbname = host_db.split('/')
        else:
            host_port = host_db
            dbname = ''
            
        if ':' in host_port:
            host, port = host_port.split(':')
        else:
            host = host_port
            port = '5432'  # Default PostgreSQL port
        
        # Connect to the database
        print(f"Connecting to PostgreSQL database: {dbname} on {host}:{port} as {username}")
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=dbname,
            user=username,
            password=password
        )
        
        # Create a cursor
        cur = conn.cursor()
        
        # Execute a test query
        cur.execute('SELECT version();')
        
        # Get the result
        db_version = cur.fetchone()
        print(f"PostgreSQL database version: {db_version[0]}")
        
        # Close the cursor and connection
        cur.close()
        conn.close()
        print("Database connection test successful!")
        return True
        
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return False

if __name__ == "__main__":
    # Get password from user input
    password = input("Enter PostgreSQL password for user 'postgres': ")
    test_postgres_connection(manual_password=password)
