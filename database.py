import pymysql


def connect_to_mysql():
    try:
        # Establish the connection
        connection = pymysql.connect(
            host='localhost',          # e.g., 'localhost' or IP address
            user='root',      # Your MySQL username
            password='10312018',   # Your MySQL password
            database='sixFold'   # Name of the database you want to connect to
        )

        print("Successfully connected to the database")
        return connection

    except pymysql.MySQLError as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

def main():
    connection = connect_to_mysql()
    
    if connection:
        # Do something with the connection
        cursor = connection.cursor()
        
        # Example: Fetch data from a table
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        
        for row in rows:
            print(row)
        
        cursor.close()
        connection.close()

if __name__ == "__main__":
    main()
