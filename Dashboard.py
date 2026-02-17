import streamlit as st
import pandas as pd
import numpy as np   
import yfinance as yf                   
import matplotlib.pyplot as plt
from streamlit_autorefresh import st_autorefresh
import time

st.header(" Stock Market Dashboard")
st.markdown("""
<h3 style='color:red; text-align:center; margin-bottom:5px;'>📊 Real-Time Stock Market Dashboard</h3>
<p style='text-align:center; color:black; margin-top:0;'>Welcome to My Interactive Stock Monitoring App!</p>
""", unsafe_allow_html=True)

#markdown for my Dashboard
st.markdown(" <span style='color:green'>The market is up today!</span> ", unsafe_allow_html=True)

#Adding an image to my Dashboard
st.image("Dashboard.png", caption="Stock Market Overview",width=100,)

with st.sidebar.expander("📊 Dashboard", expanded=True):
    st.write("Overview of stock market metrics")

with st.sidebar.expander("⚙️ Components"):
    st.radio("Choose component:", ["Charts", "Tables"])

with st.sidebar.expander("📋 Tables & Forms"):
    st.checkbox("Show recent transactions")
    st.checkbox("Show alerts")

with st.sidebar.expander("📄 Pages"):
    page = st.radio("Choose page:", ["Dashboard", "Mailbox", "To Do List", "Notes", "Calendar"])

with st.sidebar.expander("🛠 Apps"):
    st.selectbox("Select App:", ["App 1", "App 2", "App 3"])
# Refresh every 5 seconds
st_autorefresh(interval=5000, key="datarefresh")
page = st.sidebar.radio("Choose for stock:", ["Dashboard", "Mailbox", "To Do List", "Notes", "Calendar"])
#Data for my Dashboard
st.write("Data will be displayed here:")

# Sidebar to select stock
symbol = st.sidebar.text_input("Enter Stock Symbol", value="AAPL")
if symbol:
    stock = yf.Ticker(symbol)
    hist = stock.history(period="100d") # last 100 days
    
    # DataFrames for price and volume
    data = hist[['Close']].rename(columns={'Close':'Price'})
    data2 = hist[['Volume']]

    # Reset index to datetime for charts
    data.index = pd.to_datetime(data.index)
    data2.index = pd.to_datetime(data2.index)

# --- Dashboard Page ---
if page == "Dashboard":
    if symbol:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1d", interval="1m")  # Real-time intraday data
        data = hist[['Close']].rename(columns={'Close': 'Price'})
        data2 = hist[['Volume']]
        data.index = pd.to_datetime(data.index)
        data2.index = pd.to_datetime(data2.index)
        #col5,col6=st.columns(2)
        #with col5:
           # st.
        # Layout: two columns for price
        col1, col2,col3,col4 = st.columns(4)
        with col1:
            st.markdown(f"#### {symbol} Price Over Time")
            fig, ax = plt.subplots(figsize=(1,1))
            st.line_chart(data)
            st.markdown(
                "<p style='text-align:center; color:black; font-size:10px;'>Stock Price Distribution</p>",
                unsafe_allow_html=True)
            
        with col2:
            st.warning("Not enough valid price data to display pie chart.")

            st.markdown("#### Current Stock Price Distribution (Pie Chart)")
            apps = ["Mailbox", "To Do List", "Whatsapp", "Facebook"]
            latest_prices = data['Price'].tail(4).tolist()
            if len(latest_prices) < 4:
                latest_prices += [0] * (4 - len(latest_prices))
            fig, ax = plt.subplots(figsize=(2,2))
            
            ax.pie(latest_prices, labels=apps, autopct='%1.1f%%',startangle=90,
                pctdistance=0.8,
            colors=['skyblue','lightgreen','salmon','orange'])
            st.pyplot(fig)

        with col3:
            st.markdown(f"#### {symbol} Trading Volume Over Time")
            fig,ax = plt.subplots(figsize=(1, 1))
            st.line_chart(data2)
            #st.pyplot(fig)
    
        with col4:
            st.markdown("#### Current Trading Volume Distribution (Bar Chart)")
            fig, ax = plt.subplots(figsize=(1, 2))
            latest_volumes = data2['Volume'].tail(4).tolist()
            if len(latest_volumes) < 4:
                latest_volumes += [0] * (4 - len(latest_volumes))
            fig, ax = plt.subplots()
            ax.bar(apps, latest_volumes, color=['skyblue','lightgreen','salmon','orange'])
            st.pyplot(fig)

# --- Mailbox Page ---
elif page == "Mailbox":
    st.header("Mailbox Overview")
    st.write("Here you can see Mailbox-related metrics or charts.")
    # Example dummy chart
    df = pd.DataFrame({'Emails Sent': [5, 10, 7, 12], 'Emails Received': [8, 9, 6, 11]},
                      index=['Mon','Tue','Wed','Thu'])
    st.bar_chart(df)
    col1,col2=st.columns(2)
    
# --- To Do List Page ---
elif page == "To Do List":
    st.header("To Do List Overview")
    st.write("Here you can see To Do List status.")
    tasks = pd.DataFrame({
        "Task": ["Task 1", "Task 2", "Task 3"],
        "Status": ["Done", "Pending", "Pending"]
    })
    st.table(tasks)

# --- Notes Page ---
elif page == "Notes":
    st.header("Notes Overview")
    st.write("Here you can see Notes analytics or summaries.")
    notes_df = pd.DataFrame({
        "Title": ["Meeting", "Ideas", "Report"],
        "Word Count": [120, 350, 200]
    })
    st.bar_chart(notes_df.set_index("Title"))

# --- Calendar Page ---
elif page == "Calendar":
    st.header("Calendar Overview")
    st.write("Here you can see Calendar events or activity.")
    events = pd.DataFrame({
        "Event": ["Meeting", "Deadline", "Appointment"],
        "Day": ["Mon", "Wed", "Fri"]
    })
    st.table(events)
#footer for my Dashboard
st.markdown("<footer style='color:grey; text-align:center; background-color:lightblue;'>© 2025 Stock Dashboard Inc.</footer>", unsafe_allow_html=True)

