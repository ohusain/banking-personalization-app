import streamlit as st 
import pandas as pd 
import numpy as np 
from sklearn.cluster import KMeans 
import matplotlib.pyplot as plt 
import time 
import os 
# -------------------------- 
# PAGE CONFIG 
# -------------------------- 
st.set_page_config( 
page_title="Banking AI App", 
layout="wide", 
initial_sidebar_state="collapsed" 
) 
# -------------------------- 
# CUSTOM CSS (REAL APP STYLE) 
# -------------------------- 
st.markdown(""" 
<style> 
/* Background */ 
html, body, [class*="css"] { 
background-color: #0E1117; 
color: white; 
} 
/* Title */ 
h1 { 
font-size: 2.5rem; 
font-weight: bold; 
} 
/* Cards */ 
.card { 
background-color: #1C1F26; 
padding: 20px; 
border-radius: 16px; 
margin-bottom: 20px; 
box-shadow: 0px 4px 20px rgba(0,0,0,0.4); 
} 
/* Metric Text */ 
.metric { 
font-size: 1.2rem; 
color: #B0B3B8; 
} 
/* Highlight */ 
.highlight { 
font-size: 1.8rem; 
font-weight: bold; 
} 
/* Animation */ 
@keyframes fadeIn { 
from {opacity: 0;} 
to {opacity: 1;} 
} 
.fade { 
animation: fadeIn 1s ease-in; 
} 
</style> 
""", unsafe_allow_html=True) 
# -------------------------- 
# LOAD / GENERATE DATA 
# -------------------------- 
if not os.path.exists("customers.csv"): 
  data = pd.DataFrame({ 
    "customer_id": range(1, 201), 
    "income": np.random.randint(30000, 120000, 200), 
    "rent": np.random.randint(800, 2500, 200), 
    "food": np.random.randint(200, 800, 200), 
    "travel": np.random.randint(0, 1500, 200), 
    "shopping": np.random.randint(100, 1500, 200), 
    "savings": np.random.randint(0, 20000, 200) 
}) 
data.to_csv("customers.csv", index=False) 
df = pd.read_csv("customers.csv") 
# -------------------------- 
# FEATURES 
# -------------------------- 
df["total_spend"] = df["rent"] + df["food"] + df["travel"] + df["shopping"] 
df["savings_ratio"] = df["savings"] / df["income"] 
df["travel_ratio"] = df["travel"] / df["total_spend"] 
# -------------------------- 
# ML SEGMENTATION 
# -------------------------- 
features = df[["income", "travel", "shopping"]] 
kmeans = KMeans(n_clusters=3, random_state=42) 
df["segment"] = kmeans.fit_predict(features) 
segment_map = {   
  
0: "High Value", 
1: "Traveler", 
2: "Shopper" 
} 
 
# -------------------------- 
# INSIGHTS 
# -------------------------- 
def generate_insight(row): 
    if row["savings_ratio"] < 0.1: 
        return ("    Low Savings", 
                f"You are only saving {round(row['savings_ratio']*100)}% of your income") 
 
    elif row["travel_ratio"] > 0.3: 
        return ("     Travel Heavy", 
                f"{round(row['travel_ratio']*100)}% of your spending is travel") 
 
    elif row["shopping"] > 1000: 
        return ("     High Shopping", 
                f"You spent ${row['shopping']} on shopping") 
 
    elif row["savings_ratio"] > 0.3: 
        return ("   Strong Saver", 
                f"You save {round(row['savings_ratio']*100)}% of income") 
 
    else: 
        return ("   Balanced", 
"Your finances look healthy and stable") 
# -------------------------- 
# HEADER 
# -------------------------- 
st.markdown("<h1 class='fade'>🏦 Smart Banking Dashboard</h1>", unsafe_allow_html=True)    

"Smart Banking Dashboard</h1>", 
customer_id = st.slider("Select Customer", 1, len(df)) 
# Simulated loading animation 
with st.spinner("Analyzing customer data..."): 
  time.sleep(0.6) 
customer = df[df["customer_id"] == customer_id].iloc[0] 
# -------------------------- 
# LAYOUT 
# -------------------------- 
col1, col2, col3 = st.columns(3) 
# -------------------------- 
# CARDS 
# -------------------------- 
with col1: 
st.markdown(f""" 
    <div class="card fade"> 
        <div class="metric">Income</div> 
        <div class="highlight">${customer['income']}</div> 
    </div> 
    """, unsafe_allow_html=True) 
 
with col2: 
    st.markdown(f""" 
    <div class="card fade"> 
        <div class="metric">Total Spend</div> 
        <div class="highlight">${customer['total_spend']}</div> 
    </div> 
    """, unsafe_allow_html=True) 
 
with col3: 
    st.markdown(f""" 
    <div class="card fade"> 
        <div class="metric">Savings</div> 
        <div class="highlight">${customer['savings']}</div> 
    </div> 
    """, unsafe_allow_html=True) 
 
# -------------------------- 
# SEGMENT 
# -------------------------- 
st.markdown(f""" 
<div class="card fade"> 
<div class="metric">Customer Segment</div> 
<div class="highlight">{segment_map[customer['segment']]}</div> 
</div> 
""", unsafe_allow_html=True) 
# -------------------------- 
# CHART 
# -------------------------- 
st.markdown("<div class='card fade'>", unsafe_allow_html=True) 
st.subheader("Spending Breakdown") 
labels = ["Rent", "Food", "Travel", "Shopping"] 
values = [ 
customer["rent"], 
customer["food"], 
customer["travel"], 
customer["shopping"] 
] 
fig, ax = plt.subplots() 
ax.pie(values, labels=labels, autopct='%1.1f%%') 
st.pyplot(fig) 
st.markdown("</div>", unsafe_allow_html=True) 
# -------------------------- 
# INSIGHT 
# -------------------------- 
insight, explanation = generate_insight(customer) 
st.markdown(f""" 
<div class="card fade"> 
<h3>      Personalized Insight</h3> 
<h2>{insight}</h2> 
<p>{explanation}</p> 
</div> 
""", unsafe_allow_html=True)
