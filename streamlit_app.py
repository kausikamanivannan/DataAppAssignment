import streamlit as st
import pandas as pd

st.title("Data App Assignment")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=["Order_Date"])
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.line_chart(df.groupby("Category").sum()["Sales"])

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

# Plotting sales by month
st.line_chart(sales_by_month, use_container_width=True)

st.write("## Your additions")

# 1. Dropdown for selecting category
selected_category = st.selectbox("Select Category", df["Category"].unique())

# 2. Multiselect for selecting sub-categories within the selected category
selected_sub_categories = st.multiselect("Select Sub-Categories", df[df["Category"] == selected_category]["Sub_Category"].unique())

# Filter the dataframe based on selected category and sub-categories
filtered_df = df[(df["Category"] == selected_category) & df["Sub_Category"].isin(selected_sub_categories)]

# 3. Line chart of sales for selected items
if not filtered_df.empty:
    sales_by_subcategory = filtered_df.groupby(pd.Grouper(freq='M'))["Sales"].sum()
    st.line_chart(sales_by_subcategory, use_container_width=True)
else:
    st.write("No data available for the selected category and sub-categories.")

# 4. Metrics for selected items
if not filtered_df.empty:
    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()
    overall_profit_margin = (total_profit / total_sales) * 100

    st.write("### Metrics for Selected Items")
    st.metric("Total Sales", total_sales)
    st.metric("Total Profit", total_profit)
    st.metric("Overall Profit Margin (%)", overall_profit_margin)

    # Overall average profit margin for all products across all categories
    overall_avg_profit_margin_all = (df["Profit"].sum() / df["Sales"].sum()) * 100
    profit_margin_delta = overall_profit_margin - overall_avg_profit_margin_all

    # 5. Delta option in the overall profit margin metric
    st.write("### Delta with Overall Average Profit Margin")
    st.metric("Delta with Overall Avg Profit Margin (%)", profit_margin_delta)
