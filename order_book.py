import pandas as pd
import numpy as np

df = pd.read_csv("./sample_market_data.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Defining a timestamp to be later used
#timestamp = "2023-11-29 17:01:25.855124"
#timestamp = "2023-11-29 17:30:55.855124"
timestamp = input("Timestamp: ")
timestamp = pd.to_datetime(timestamp)

# Forming a list of orders at a specified timestamp
orders = df[df["timestamp"] <= timestamp]


# Filtering to get the latest order for a corresponding orderid
latest_order_ids = orders.groupby("orderId")['timestamp'].idxmax()
orders = orders.loc[latest_order_ids]
orders = orders[orders["qty"] != 0]

# Forming the order book from the orders
order_book = orders.groupby(['side', 'price']).agg({'qty' : 'sum', 'orderId' : 'count'})
order_book.rename(columns={'orderId' : 'num_orders'}, inplace=True)
order_book.sort_values('price', ascending=False, inplace=True)
order_book.reset_index(inplace=True)

order_book.to_csv('order_book.csv')