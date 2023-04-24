import mysql.connector
import Adafruit_DHT
import time
from datetime import datetime
DHT_SENSOR= Adafruit_DHT.DHT11
DHT_PIN=4




db = mysql.connector.connect(
    host="database-2.co0exmzd6g8a.us-east-1.rds.amazonaws.com",
    user="root",
    password="meditab123",
    database="sys"
)

cursor = db.cursor()

while True:
        hum, temp=Adafruit_DHT.read(DHT_SENSOR,DHT_PIN)
        if hum is not None and temp is not None:
            # Define the data to insert
            now = datetime.now()
            date_time = now.strftime("%Y-%m-%d %H:%M:%S")
            data = (temp,hum,date_time)

            # Define the query to insert the data
            query = "INSERT INTO mytable (temp,hum,time) VALUES (%s, %s , %s)"

            # Execute the query with the data
            cursor.execute(query, data)

            # Commit the changes to the database
            db.commit()

            # Print a message to confirm the data was inserted
            print(cursor.rowcount, "record inserted.")
        else:
            print("fail")
        time.sleep(2)