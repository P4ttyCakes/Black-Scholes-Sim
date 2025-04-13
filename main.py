import streamlit as st
import numpy as np
from scipy.stats import norm
import qfin as qf
import matplotlib.pyplot as plt


# Initialize session state
if "prev_inputs" not in st.session_state:
    st.session_state.prev_inputs = {}

# Sidebar Inputs
st.sidebar.header('Input Parameters')
S = st.sidebar.slider('Stock Price (S)', 30.0, 90.0, 60.0, 1.0)
K = st.sidebar.slider('Strike Price (K)', 30.0, 90.0, 50.0, 1.0)
sigma = st.sidebar.slider('Volatility (σ)', 0.1, 0.5, 0.3, 0.05)
r = st.sidebar.slider('Risk-free Rate (r)', 0.01, 0.1, 0.05, 0.01)
t = st.sidebar.slider('Time to Expiration (years)', 0.25, 2.0, 1.0, 0.25)

# Button to resimulate
button_clicked = st.button("Simulate New Price Path")

# Current input state
current_inputs = {"S": S, "K": K, "sigma": sigma, "r": r, "t": t}

# Detect change in inputs
input_changed = current_inputs != st.session_state.prev_inputs or button_clicked

# Save new inputs
st.session_state.prev_inputs = current_inputs

# Run simulation if needed
if input_changed:
    # Black-Scholes Formula
    def black_scholes(S, K, sigma, r, t):
        d1 = (np.log(S/K) + (r + 0.5 * sigma**2) * t) / (sigma * np.sqrt(t))
        d2 = d1 - sigma * np.sqrt(t)
        return S * norm.cdf(d1) - K * np.exp(-r * t) * norm.cdf(d2)

    premium = black_scholes(S, K, sigma, r, t)

    # Simulate stock path
    path = qf.simulations.GeometricBrownianMotion(S, r, sigma, 1/252, t)
    simulated_path = path.simulated_path
    final_price = simulated_path[-1]
    payoff = max(final_price - K, 0)
    pl = payoff - premium

    # Save outputs to session_state for display
    st.session_state.sim_data = {
        "premium": premium,
        "final_price": final_price,
        "payoff": payoff,
        "pl": pl,
        "path": simulated_path
    }

# Load simulated data
sim_data = st.session_state.get("sim_data", None)
if sim_data:
    st.subheader('Option Statistics')
    col1, col2, col3 = st.columns(3)
    col1.metric("Premium", f"${sim_data['premium']:.2f}")
    col2.metric("Final Price", f"${sim_data['final_price']:.2f}")
    col3.metric("P/L", f"${sim_data['pl']:.2f}")

    # Plot
    fig = plt.figure(figsize=(10, 6))
    plt.style.use('dark_background')

    plt.title("Terminal Value of a Call Option")
    plt.hlines(K, 0, 252, label='Strike', color='orange')
    plt.plot(sim_data['path'], label='Price Path', color='white')

    if sim_data["payoff"] == 0:
        plt.vlines(252, sim_data["final_price"], K, color='red', label="P/L (Out of the money)")
    else:
        plt.vlines(252, K, sim_data["final_price"], color='green', label="P/L (In the money)")

    plt.xlabel('Time')
    plt.ylabel('Stock Price')
    plt.legend()

    # Add annotations
    plt.figtext(0.15, 0.02, f"Premium at t=0: ${sim_data['premium']:.2f}", fontsize=10, color='white')
    plt.figtext(0.45, 0.02, f"Final Stock Price: ${sim_data['final_price']:.2f}", fontsize=10, color='white')
    plt.figtext(0.75, 0.02, f"P/L at expiration: ${sim_data['pl']:.2f}", fontsize=10, color='white')

    plt.tight_layout()
    st.pyplot(fig)

    # Text output
    st.write(f"Premium at t=0: ${sim_data['premium']:.2f}")
    st.write(f"Final Simulated Price: ${sim_data['final_price']:.2f}")
    st.write(f"P/L: ${sim_data['pl']:.2f}")
