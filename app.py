# ------------------------------------
# Packages
# ------------------------------------
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# ------------------------------------
# Page Configuration
# ------------------------------------
st.set_page_config(
    page_title="U.S. Weekly Earnings Dashboard",
    page_icon="💰",
    layout="wide"
)


# ------------------------------------
# Title
# ------------------------------------
st.title("💰 U.S. Weekly Earnings Dashboard")
st.caption(
    "INFO 450 Course Project | Exploring U.S. Weekly Earnings Using CPS Data"
)


# ------------------------------------
# Load CSV File
# ------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Tolu_project_earnings.csv")
    return df


df = load_data()


# ------------------------------------
# Data Cleaning Placeholder
# Add your cleaning code here
# Example:
# df = df[df["UHRSWORKT"] < 200]
# ------------------------------------



# ------------------------------------
# Sidebar Filters
# ------------------------------------
st.sidebar.header("🔎 Dashboard Filters")


# Gender Filter
if "SEX" in df.columns:

    selected_gender = st.sidebar.selectbox(
        "Select Gender",
        ["All"] + list(df["SEX"].unique())
    )

else:
    selected_gender = "All"



# Age Filter
if "AGE" in df.columns:

    selected_age = st.sidebar.slider(
        "Select Age Range",
        int(df["AGE"].min()),
        int(df["AGE"].max()),
        (
            int(df["AGE"].min()),
            int(df["AGE"].max())
        )
    )

else:
    selected_age = (0, 100)



# ------------------------------------
# Apply Filters
# ------------------------------------
filtered_df = df.copy()


if selected_gender != "All":
    filtered_df = filtered_df[
        filtered_df["SEX"] == selected_gender
    ]


if "AGE" in df.columns:

    filtered_df = filtered_df[
        (filtered_df["AGE"] >= selected_age[0]) &
        (filtered_df["AGE"] <= selected_age[1])
    ]



# ------------------------------------
# Summary Statistics
# ------------------------------------
st.divider()

st.header("📊 Summary Statistics")


col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Number of Workers",
    f"{len(filtered_df):,}"
)


if "EARNWEEK" in filtered_df.columns:

    col2.metric(
        "Average Weekly Earnings",
        f"${filtered_df['EARNWEEK'].mean():,.2f}"
    )


    col3.metric(
        "Median Weekly Earnings",
        f"${filtered_df['EARNWEEK'].median():,.2f}"
    )


else:

    col2.metric(
        "Average Weekly Earnings",
        "N/A"
    )

    col3.metric(
        "Median Weekly Earnings",
        "N/A"
    )



if "UHRSWORKT" in filtered_df.columns:

    col4.metric(
        "Average Hours Worked",
        f"{filtered_df['UHRSWORKT'].mean():.1f}"
    )

else:

    col4.metric(
        "Average Hours Worked",
        "N/A"
    )



# ------------------------------------
# Pareto Chart
# ------------------------------------
st.divider()

st.header("📈 Pareto Chart of Workers by Education Level")


if "EDUC_GROUP" in filtered_df.columns:


    pareto = (
        filtered_df["EDUC_GROUP"]
        .value_counts()
        .sort_values(ascending=False)
    )


    cum_percent = (
        pareto.cumsum()
        /
        pareto.sum()
        *
        100
    )


    fig, ax1 = plt.subplots(figsize=(10,6))


    # Bar Chart

    pareto.plot(
        kind="bar",
        ax=ax1
    )


    ax1.set_ylabel(
        "Number of Workers"
    )

    ax1.set_xlabel(
        "Education Group"
    )

    ax1.set_title(
        "Pareto Chart of Workers by Education Level"
    )


    # Cumulative Line

    ax2 = ax1.twinx()


    ax2.plot(
        range(len(cum_percent)),
        cum_percent.values,
        color="red",
        marker="o",
        linewidth=2
    )


    ax2.set_ylabel(
        "Cumulative Percentage (%)"
    )


    ax2.set_ylim(
        0,
        110
    )


    plt.xticks(
        rotation=45
    )


    plt.tight_layout()


    st.pyplot(fig)


    st.success(
        "The Pareto chart highlights which education groups represent the largest portion of workers."
    )


else:

    st.warning(
        "EDUC_GROUP column was not found. Please check your dataset column names."
    )



# ------------------------------------
# Dataset Preview (Optional)
# ------------------------------------
with st.expander("View Dataset Preview"):

    st.dataframe(
        filtered_df.head(10)
    )
