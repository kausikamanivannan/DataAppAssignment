import matplotlib
matplotlib.use('agg')  # Set Matplotlib to use the 'agg' backend

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Data App Assignment")

# Read data
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=["Order_Date"])

st.write("### Input Data and Examples")
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
plt.bar(df["Category"], df["Sales"])
st.pyplot()

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
df_grouped = df.groupby("Category").sum()
plt.bar(df_grouped.index, df_grouped["Sales"], color="#04f")
st.pyplot()

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

# Plotting with Matplotlib
plt.plot(sales_by_month.index, sales_by_month["Sales"])
plt.xlabel("Month")
plt.ylabel("Sales")
plt.title("Monthly Sales")
st.pyplot()

st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
st.write("### (3) show a line chart of sales for the selected items in (2)")
st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
