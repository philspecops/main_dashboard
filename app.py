import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Funding by Sector and Year")

data = {
    "Sector": [
        "Farmer Support", "Health", "Education",
        "Water & Sanitation", "Infrastructure", "Other"
    ],
    2024: [42997, 0, 1642, 0, 293, 2287],
    2023: [57462, 0, 27287, 0, 0, 248],
    2022: [19388, 410, 33805, 1049, 331, 1373],
    2021: [13247, 707, 33297, 1454, 0, 2986],
    2020: [29053, 675, 25837, 0, 9949, 5001],
    2019: [45584, 0, 8831, 0, 1777, 38514],
    2018: [15787, 7708, 2432, 0, 6845, 29463],
}

df = pd.DataFrame(data)

year_cols = [col for col in df.columns if isinstance(col, int)]

selected_years = st.multiselect(
    "Select years",
    year_cols,
    default=year_cols
)

filtered = df[["Sector"] + selected_years]

st.dataframe(filtered, use_container_width=True)

long_df = filtered.melt(
    id_vars="Sector",
    var_name="Year",
    value_name="Amount"
)

fig = px.bar(
    long_df,
    x="Year",
    y="Amount",
    color="Sector",
    title="Funding by Sector Over Time",
    barmode="stack"
)

st.plotly_chart(fig, use_container_width=True)

sector = st.selectbox("Select a sector", df["Sector"])

sector_df = long_df[long_df["Sector"] == sector]

line = px.line(
    sector_df,
    x="Year",
    y="Amount",
    markers=True,
    title=f"{sector} Funding Over Time"
)

st.plotly_chart(line, use_container_width=True)
