import pandas as pd
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="phonepe"
)
# Step 2: SQL se data uthao (YAHI KARNA HAI 🔥)
df = pd.read_sql("SELECT * FROM aggregated_transaction", conn)

# Step 3: Check data
print(df.head())
print(df.shape)
import matplotlib.pyplot as plt

plt.figure(figsize=(12,5))

# Graph 1
plt.subplot(1,2,1)
top_states = df.groupby('state')['amount'].sum().sort_values(ascending=False).head(10)
top_states.plot(kind='bar')
plt.title("Top States")
plt.xticks(rotation=45)

# Graph 2
plt.subplot(1,2,2)
yearly = df.groupby('year')['amount'].sum()
yearly.plot(marker='o')
plt.title("Year-wise Growth")

plt.tight_layout()
plt.show()
plt.show()