import streamlit as st
from simulation import simulate_option
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

# Sidebar Inputs
st.sidebar.header('Input Parameters')
S = st.sidebar.slider('Stock Price (S)', 30.0, 90.0, 60.0, 1.0)
K = st.sidebar.slider('Strike Price (K)', 30.0, 90.0, 50.0, 1.0)
sigma = st.sidebar.slider('Volatility (σ)', 0.1, 0.5, 0.3, 0.05)
r = st.sidebar.slider('Risk-free Rate (r)', 0.01, 0.1, 0.05, 0.01)
t = st.sidebar.slider('Time to Expiration (years)', 0.25, 2.0, 1.0, 0.25)

# Always simulate based on input
sim_data = simulate_option(S, K, sigma, r, t)

# Display stats
st.subheader('Value of Option w/ Geometric Brownian Motion')
col1, col2, col3 = st.columns(3)
col1.metric("Premium", f"${sim_data['premium']:.2f}")
col2.metric("Final Stock Price", f"${sim_data['final_price']:.2f}")
col3.metric("Terminal P/L", f"${sim_data['pl']:.2f}")

# Convert data to DataFrame for Streamlit charting
path = pd.Series(sim_data['path'], name='Price Path')
strike_price = pd.Series([K] * len(path), name='Strike Price')
payoff = pd.Series([max(price - K, 0) for price in path], name='Payoff')

# Combine all series into a single DataFrame
chart_data = pd.DataFrame({
    'Price Path': path,
    'Strike Price': strike_price,
    'Payoff': payoff
})

# Remove the index (reset index and drop it)
chart_data.reset_index(drop=True, inplace=True)

# Plot the Price Path and Strike Price on one graph
st.line_chart(chart_data[['Price Path', 'Strike Price']], width=700, height=400, use_container_width=True)

# Plot the Payoff and P/L separately, changing color based on positive or negative P/L
payoff_color = ['green' if p > 0 else 'red' for p in payoff]  # Color based on positive or negative payoff

# Plot the P/L graph with color change
payoff_df = pd.DataFrame({
    'Time': range(len(path)),
    'Payoff': payoff,
    'Color': payoff_color
})

# Display the P/L graph
st.subheader('Payoff / P/L')

# We plot the P/L as a line chart, coloring the line based on positive vs negative
st.line_chart(payoff_df.set_index('Time')[['Payoff']], width=700, height=400, use_container_width=True)

# Annotations for the P/L graph
st.write(f"Premium at t=0: ${sim_data['premium']:.2f}")
st.write(f"Final Stock Price: ${sim_data['final_price']:.2f}")
st.write(f"P/L at expiration: ${sim_data['pl']:.2f}")
