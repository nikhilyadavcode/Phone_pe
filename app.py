import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt


st.set_page_config(page_title="My Dashboard", layout="wide")

def add_bg():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("bg_image.jpg");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}

        /* Optional: dark overlay for better readability */
        .stApp::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.4);
            z-index: 0;
        }}

        .main {{
            position: relative;
            z-index: 1;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg()

st.title("My Dashboard")

#  DATABASE CONNECTION 
@st.cache_data
def load_data():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="phonepe"
    )
    
    query = "SELECT * FROM aggregated_transaction"
    df = pd.read_sql(query, conn)
    return df

df = load_data()

#  TITLE 
st.title("PhonePe Transaction Dashboard")

# KPI SECTION 
total_amount = df['amount'].sum()
total_transactions = df['count'].sum()
total_states = df['state'].nunique()

col1, col2, col3 = st.columns(3)

col1.metric(" Total Transaction Amount", f"{total_amount:,.0f}")
col2.metric(" Total Transactions", f"{total_transactions:,.0f}")
col3.metric(" Total States", total_states)

st.markdown("---")

#  SIDEBAR FILTER 
st.sidebar.header("Filter")

selected_state = st.sidebar.selectbox(
    "Select State",
    ["All"] + sorted(df['state'].unique())
)

if selected_state != "All":
    df_filtered = df[df['state'] == selected_state]
else:
    df_filtered = df

#  TOP STATES CHART 
st.subheader(" Top 10 States by Transaction Amount")

top_states = (
    df.groupby('state')['amount']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig1, ax1 = plt.subplots()
top_states.plot(kind='bar', ax=ax1)
plt.xticks(rotation=45)
st.pyplot(fig1)

#  YEAR-WISE TREND
st.subheader(" Year-wise Transaction Growth")

yearly = df_filtered.groupby('year')['amount'].sum()

fig2, ax2 = plt.subplots()
yearly.plot(marker='o', ax=ax2)
st.pyplot(fig2)

# PAYMENT TYPE 
st.subheader(" Payment Type Distribution")

payment = df_filtered.groupby('transaction_type')['count'].sum()

fig3, ax3 = plt.subplots()
payment.plot(kind='pie', autopct='%1.1f%%', ax=ax3)
plt.ylabel("")
st.pyplot(fig3)

#  DATA VIEW 
st.subheader("Raw Data")

st.dataframe(df_filtered)