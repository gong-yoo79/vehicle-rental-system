import mysql.connector

def connect_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Yumi@1234",  
        database="vehicle_rental"
    )
    return conn
