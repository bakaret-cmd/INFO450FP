# Packages
import streamlit as st
import matplotlib.pyplot as plit
import pandas as pd
# ------------------------------------
# Page Configuration
# ------------------------------------
st.set_page_config(
    page_title="U.S. Weekly Earnings Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 U.S. Weekly Earnings Dashboard")
st.write("Explore Current Population Survey (CPS) data interactively.")

# ------------------------------------
# Load CSV File
# Make sure cps_project_data.csv is in
# the same folder as app.py
# ------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Tolu_project_earnings.csv")
    return df

df = load_data()

# Display the first few rows (optional)
st.subheader("Dataset Preview")
st.dataframe(df.head())

# ====================================
# PLACEHOLDER:
# Paste your data cleaning/analysis
# code here.
#
# Example:
# df = df[df["UHRSWORKT"] < 200]
# df["weekly_income"] = ...
# pareto_df = ...
# summary_stats = ...
# ====================================


# ------------------------------------
# Interactive Widgets
# ------------------------------------
st.sidebar.header("Filters")

# Replace these column names with the
# ones used in your dataset.
selected_gender = st.sidebar.selectbox(
    "Gender",
    ["All"] + list(df["SEX"].unique())
)

selected_age = st.sidebar.slider(
    "Age Range",
    int(df["AGE"].min()),
    int(df["AGE"].max()),
    (
        int(df["AGE"].min()),
        int(df["AGE"].max())
    )
)

# ------------------------------------
# Apply Filters
# ------------------------------------
filtered_df = df.copy()

if selected_gender != "All":
    filtered_df = filtered_df[
        filtered_df["SEX"] == selected_gender
    ]

filtered_df = filtered_df[
    (filtered_df["AGE"] >= selected_age[0]) &
    (filtered_df["AGE"] <= selected_age[1])
]

# ------------------------------------
# Summary Statistics
# Replace with your own statistics
# ------------------------------------
st.header("Summary Statistics")

st.write(filtered_df.describe())

# ------------------------------------
# ------------------------------------
# Pareto Chart
# ------------------------------------
st.header("Pareto Chart of Workers by Education Level")

# Create Pareto data from the filtered dataset
pareto = (
    filtered_df["EDUC_GROUP"]
    .value_counts()
    .sort_values(ascending=False)
)

# Calculate cumulative percentage
cum_percent = pareto.cumsum() / pareto.sum() * 100

# Create the figure
fig, ax1 = plt.subplots(figsize=(10, 6))

# Bar chart
pareto.plot(
    kind="bar",
    ax=ax1,
    color="steelblue"
)

ax1.set_ylabel("Number of Workers")
ax1.set_xlabel("Education Group")
ax1.set_title("Pareto Chart of Workers by Education Level")

# Cumulative percentage line
ax2 = ax1.twinx()

ax2.plot(
    range(len(cum_percent)),
    cum_percent.values,
    color="red",
    marker="o",
    linewidth=2
)

ax2.set_ylabel("Cumulative Percentage (%)")
ax2.set_ylim(0, 110)

plt.xticks(rotation=45)
plt.tight_layout()

# Display in Streamlit
st.pyplot(fig)
# ------------------------------------

# fig, ax = plt.subplots(...)
# ...
# st.pyplot(fig)

# ------------------------------------
# PLACEHOLDER:
# Paste any additional charts or
# insights here.
# ------------------------------------
