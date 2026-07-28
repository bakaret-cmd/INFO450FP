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
# PLACEHOLDER:
# Paste your Pareto Chart code here
# ------------------------------------

# fig, ax = plt.subplots(...)
# ...
# st.pyplot(fig)

# ------------------------------------
# PLACEHOLDER:
# Paste any additional charts or
# insights here.
# ------------------------------------
