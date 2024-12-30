import mysql.connector
from mysql.connector import Error

try:
    # Connect to the database
    cnx = mysql.connector.connect(
        host="localhost",
        user="test",
        password="1234"
    )

    # Check if the connection is successful
    if cnx.is_connected():
        print("Connected to the database successfully!")

        # Create a cursor and execute a test query
        mycur = cnx.cursor()
        mycur.execute("SELECT DATABASE();")
        db_name = mycur.fetchone()
        print("Current database:", db_name)

    else:
        print("Connection failed.")

except Error as e:
    print(f"Error: {e}")

finally:
    # Ensure connection is closed
    if 'cnx' in locals() and cnx.is_connected():
        cnx.close()
