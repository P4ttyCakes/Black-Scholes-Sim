import streamlit as st
from simulation import simulate_option, black_scholes
import pandas as pd


# Sidebar Inputs
st.sidebar.header('Input Parameters')
option_type = st.sidebar.selectbox('Option Type', ['call', 'put'])

S = st.sidebar.slider('Stock Price (S)', 0.0, 1000.0, 500.0, 1.0)
K = st.sidebar.slider('Strike Price (K)', 0.0, 1000.0, 500.0, 1.0)
sigma = st.sidebar.slider('Volatility (σ)', 0.1, 0.5, 0.3, 0.05)
r = st.sidebar.slider('Risk-free Rate (r)', 0.01, 0.1, 0.05, 0.01)
t = st.sidebar.slider('Time to Expiration (years)', 0.25, 10.0, 5.0, 0.25)

# Black-Scholes Fair Value
bs_premium = black_scholes(S, K, sigma, r, t, option_type)

st.title('Option Pricing and Simulation App')
st.write("This app allows you to simulate the outcome of an option trade using Geometric Brownian Motion.")
st.write("You can input the parameters for the option and see how the stock price evolves over time.")

st.subheader('')




st.subheader('Black-Scholes Fair Value')
st.write(f"{option_type.capitalize()} Option Price: ${bs_premium:.2f}")

# User Input: Actual premium paid
actual_premium = st.number_input("What did you pay for the option?", min_value=0.0, value=bs_premium, step=0.5)

# Run Simulation
if st.button("Run Geometric Brownian Motion Simulation"):
    sim_data = simulate_option(S, K, sigma, r, t, option_type=option_type)

    st.subheader('Simulated Option Outcome')
    col1, col2, col3 = st.columns(3)
    col1.metric("Price Paid", f"${actual_premium:.2f}")
    col2.metric("Final Stock Price", f"${sim_data['final_price']:.2f}")
    col3.metric("Profit / Loss", f"${sim_data['payoff'] - actual_premium:.2f}")

    # Create DataFrame for charting
    price_path = pd.Series(sim_data['path'], name='Stock Price')
    strike = pd.Series([K] * len(price_path), name='Strike Price')
    payoff = pd.Series(
        [max(p - K, 0) if option_type == 'call' else max(K - p, 0) for p in price_path],
        name='Payoff'
    )

    chart_df = pd.DataFrame({
        'Stock Price': price_path,
        'Strike Price': strike,
        'Payoff': payoff
    })

    st.line_chart(chart_df[['Stock Price', 'Strike Price']], use_container_width=True)

    st.subheader('Payoff Over Time')
    st.line_chart(chart_df[['Payoff']], use_container_width=True)
