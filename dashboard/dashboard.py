import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

def create_sum_sharing(df):
    sumshare_df = df.resample(rule='D', on='dteday').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    sumshare_df = sumshare_df.reset_index()
    return sumshare_df

def create_monthly_sharing(df):
    monthlyshare_df = df.resample(rule='M', on='dteday').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    monthlyshare_df.index = monthlyshare_df.index.strftime('%B %Y')
    monthlyshare_df = monthlyshare_df.reset_index()
    return monthlyshare_df

def create_workingday(df):
    workday_df = df.groupby(by="workingday").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    return workday_df

def create_weathersit(df):
    weathersit_df = df.groupby(by="weathersit").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    return weathersit_df

clean_df = pd.read_csv("https://raw.githubusercontent.com/naskaj/Proyek-AnalisisData/main/dashboard/main_data.csv")
clean_df["dteday"] = pd.to_datetime(clean_df["dteday"])

min_date = clean_df["dteday"].min()
max_date = clean_df["dteday"].max()

with st.sidebar:
    st.subheader("Filter data")
    start_date, end_date = st.date_input(
        label='Time span',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = clean_df[(clean_df["dteday"] >= str(start_date)) &
                   (clean_df["dteday"] <= str(end_date))]

sumsharing_df = create_sum_sharing(main_df)
monthlysum_df = create_monthly_sharing(main_df)
byday_df = create_workingday(main_df)
byweather_df = create_weathersit(main_df)

st.header("Bike Sharing Summary")

# Tampilan grafik perhari
st.subheader("Total bike shared")
col1, col2, col3 = st.columns(3)
with col1:
    sharesum = sumsharing_df.cnt.sum()
    st.metric("Total user", value=sharesum)
with col2:
    sharesum = sumsharing_df.casual.sum()
    st.metric("Casual user", value=sharesum)
with col3:
    sharesum = sumsharing_df.registered.sum()
    st.metric("Registered user", value=sharesum)

fig, ax = plt.subplots(figsize=(16, 8))
x = sumsharing_df['dteday']
ax.plot(x, sumsharing_df['casual'], marker='o')
ax.plot(x, sumsharing_df['registered'], marker='o')
ax.legend(["Casual", "Registered"])
st.pyplot(fig)

# Tampilan grafik berdasarkan hari
st.subheader("Performance based on day")
fig, ax = plt.subplots(figsize=(7, 5))
x = np.arange(2)
width = 0.40
ax.bar(x-width/2, byday_df['casual'], width)
ax.bar(x+width/2, byday_df['registered'], width)
ax.set_xticks(x+0, (["Holiday", "Weekday"]))
ax.legend(["Casual", "Registered"])
st.pyplot(fig)

# Tampilan grafik berdasarkan cuaca
st.subheader("Performance based on weather")
fig, ax = plt.subplots(figsize=(7, 5))
x = np.arange(3)
width = 0.30
ax.bar(x-width/2, byweather_df['casual'], width)
ax.bar(x+width/2, byweather_df['registered'], width)
ax.set_xticks(x+0, (["Clear,\nFew clouds,\nPartly cloudy",
                     "Mist + Cloudy,\nMist + Broken clouds,\nMist + Few clouds,\nMist",
                     "Light Snow,\nLight Rain + Thunderstorm\n+ Scattered clouds,\nLight Rain + Scattered clouds"]))
ax.legend(["Casual", "Registered"])
st.pyplot(fig)

# Tampilan grafik perbulan
st.subheader("Monthly bike shared")
fig, ax = plt.subplots(figsize=(16, 8))
x = monthlysum_df['dteday']
ax.plot(x, monthlysum_df['casual'], marker='o')
ax.plot(x, monthlysum_df['registered'], marker='o')
ax.tick_params(axis='x', rotation=45)
ax.legend(["Casual", "Registered"])
st.pyplot(fig)