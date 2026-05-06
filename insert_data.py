import os
import json
import mysql.connector

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="phonepe"
)

cursor = conn.cursor()

# Path to data
base_path = "C:/Users/91921/OneDrive/Desktop/pulse-master/pulse-master/data/aggregated/transaction/country/india/state"
for state in os.listdir(base_path):
    state_path = os.path.join(base_path, state)

    for year in os.listdir(state_path):
        year_path = os.path.join(state_path, year)
        year_int = int(year) 
         
        for file in os.listdir(year_path):
            if file.endswith(".json"):
                quarter = int(file.strip(".json"))

                with open(os.path.join(year_path, file)) as f:
                    data = json.load(f)

                    if "data" in data and data["data"] != None:
                        for item in data["data"]["transactionData"]:
                            name = item["name"]
                            count = item["paymentInstruments"][0]["count"]
                            amount = item["paymentInstruments"][0]["amount"]

                            cursor.execute("""
                                INSERT INTO aggregated_transaction 
                                VALUES (%s,%s,%s,%s,%s,%s)
                            """, (state, year, quarter, name, count, amount))

conn.commit()
print("All Data Inserted ")