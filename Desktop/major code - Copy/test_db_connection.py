import pymysql

print("Attempting to connect to MySQL server using PyMySQL...")
try:
    conn = pymysql.connect(host='127.0.0.1', user='root', password='', port=3306)
    print("Successfully connected to MySQL server using PyMySQL!")
    conn.close()
    print("Connection closed.")
except pymysql.Error as e:
    print(f"PyMySQL Error: {e}")
except Exception as e:
    print(f"General Error: {e}")
print("Script finished.")