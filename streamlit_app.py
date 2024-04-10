import streamlit as st
import pandas as pd

st.title("Data App Assignment")

# Displaying input data and examples
st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=["Order_Date"])
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.line_chart(df.groupby("Category").sum()["Sales"])

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set it as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df["Sales"].resample("M").sum()

# Plotting sales by month
st.line_chart(sales_by_month)

'''
st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
st.write("### (3) show a line chart of sales for the selected items in (2)")
st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
'''

# 1. Dropdown for selecting category
selected_category = st.selectbox("Select Category", df["Category"].unique())

# 2. Multiselect for selecting sub-categories within the selected category
selected_sub_categories = st.multiselect("Select Sub-Categories", df[df["Category"] == selected_category]["Sub_Category"].unique())

# 3. Filter the dataframe based on selected category and sub-categories
filtered_df = df[(df["Category"] == selected_category) & df["Sub_Category"].isin(selected_sub_categories)]

# 4. Line chart of sales for selected items
if not filtered_df.empty:
    sales_by_date = filtered_df.groupby(pd.Grouper(key="Order_Date", freq="M")).sum()["Sales"]
    st.write("### Line Chart of Sales for Selected Items")
    st.line_chart(sales_by_date)

    # 5. Metrics for selected items
    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()
    overall_avg_profit_margin = (total_profit / total_sales) * 100

    st.write("### Metrics for Selected Items")
    st.metric("Total Sales", total_sales)
    st.metric("Total Profit", total_profit)
    st.metric("Overall Profit Margin (%)", overall_avg_profit_margin)

    # Overall average profit margin for all products across all categories
    overall_avg_profit_margin_all = (df["Profit"].sum() / df["Sales"].sum()) * 100
    profit_margin_delta = overall_avg_profit_margin - overall_avg_profit_margin_all

    st.write("### Delta with Overall Average Profit Margin")
    st.metric("Delta with Overall Avg Profit Margin (%)", profit_margin_delta)
else:
    st.write("No data available for the selected category and sub-categories.")
