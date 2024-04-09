import streamlit as st
import pandas as pd

st.title("Data App Assignment")

# Read data
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=["Order_Date"])

# Step 1: Dropdown for Category Selection
selected_category = st.selectbox("Select a Category", df["Category"].unique())

# Step 2: Multi-select for Sub_Category within the Selected Category
sub_categories = df[df["Category"] == selected_category]["Sub_Category"].unique()
selected_sub_categories = st.multiselect("Select Sub-Categories", sub_categories)

# Step 3: Show a Line Chart of Sales for the Selected Items
filtered_df = df[(df["Category"] == selected_category) & (df["Sub_Category"].isin(selected_sub_categories))]
sales_by_date = filtered_df.groupby(pd.Grouper(key='Order_Date', freq='D')).sum()  # Grouping by day
st.line_chart(sales_by_date["Sales"])

# Step 4: Show Three Metrics for the Selected Items
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
overall_profit_margin = (total_profit / total_sales) * 100

st.write("## Metrics")
st.metric("Total Sales", total_sales)
st.metric("Total Profit", total_profit)
st.metric("Overall Profit Margin (%)", overall_profit_margin, delta=overall_avg_profit_margin)

# Step 5: Calculate Overall Average Profit Margin
overall_avg_profit_margin = (df["Profit"].sum() / df["Sales"].sum()) * 100
