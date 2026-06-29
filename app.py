import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Fair Trade Premium Spending", layout="wide")

st.title("Fair Trade Premium Spending Dashboard")

dropbox_url = "https://www.dropbox.com/scl/fi/ql944vw0bjdk883lj8vjq/Fair-Trade-Premium-Spending.xlsx?rlkey=1ov9apknt53iwwwz72jeuyiyw&st=h2tu1nvd&dl=1"

df = pd.read_excel(dropbox_url)

# Clean data
df = df.dropna(how="all")
df.columns = df.columns.astype(str)

# Rename first column to Sector
df = df.rename(columns={df.columns[0]: "Sector"})

# Remove total row if present
df = df[df["Sector"].astype(str).str.lower() != "total"]

# Convert wide data to long format
long_df = df.melt(
    id_vars="Sector",
    var_name="Year",
    value_name="Amount"
)

long_df["Year"] = pd.to_numeric(long_df["Year"], errors="coerce")
long_df["Amount"] = pd.to_numeric(long_df["Amount"], errors="coerce").fillna(0)

long_df = long_df.dropna(subset=["Year"])
long_df["Year"] = long_df["Year"].astype(int)

st.subheader("Data Table")
st.dataframe(df, use_container_width=True)

st.subheader("Funding Over Time")

sector_options = ["All data"] + sorted(long_df["Sector"].dropna().unique())

selected_sector = st.selectbox("Select data", sector_options)

if selected_sector == "All data":
    chart_df = long_df
    title = "All Funding Over Time"
    color = "Sector"
else:
    chart_df = long_df[long_df["Sector"] == selected_sector]
    title = f"{selected_sector} Funding Over Time"
    color = None

fig = px.line(
    chart_df,
    x="Year",
    y="Amount",
    color=color,
    markers=True,
    title=title
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Funding by Year")

bar_fig = px.bar(
    long_df,
    x="Year",
    y="Amount",
    color="Sector",
    title="Funding by Sector and Year",
    barmode="stack"
)

st.plotly_chart(bar_fig, use_container_width=True)
