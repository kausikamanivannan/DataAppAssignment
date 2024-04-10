import streamlit as st
import pandas as pd

st.title("Data App Assignment")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=["Order_Date"])
st.dataframe(df)

selected_category = st.selectbox("Select Category", df["Category"].unique())

selected_sub_categories = st.multiselect("Select Sub-Categories", df[df["Category"] == selected_category]["Sub_Category"].unique())

filtered_df = df[(df["Category"] == selected_category) & df["Sub_Category"].isin(selected_sub_categories)]

if not filtered_df.empty:
    sales_by_date = filtered_df.groupby(pd.Grouper(key="Order_Date", freq="M")).sum()["Sales"]
    st.write("### Line Chart of Sales for Selected Items")
    st.line_chart(sales_by_date)

    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()
    overall_avg_profit_margin = (total_profit / total_sales) * 100

    st.write("### Metrics for Selected Items")
    st.metric("Total Sales", total_sales)
    st.metric("Total Profit", total_profit)
    st.metric("Overall Profit Margin (%)", overall_avg_profit_margin)

    overall_avg_profit_margin_all = (df["Profit"].sum() / df["Sales"].sum()) * 100
    profit_margin_delta = overall_avg_profit_margin - overall_avg_profit_margin_all

    st.write("### Delta with Overall Average Profit Margin")
    st.metric("Delta with Overall Avg Profit Margin (%)", profit_margin_delta)
else:
    st.write("No data available for the selected category and sub-categories.")
