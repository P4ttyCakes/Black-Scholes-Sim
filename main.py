import streamlit as st
import numpy as np
from scipy.stats import norm
import qfin as qf
import matplotlib.pyplot as plt

# Variables
R = 0.01
S = 10
K = 40
T = 240/365
sigma = 0.3

def black_scholes(S, K, T, R, sigma, type='call'):
    d1 = (np.log(S/K) + (R + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if type == 'call':
        option_price = S * norm.cdf(d1) - K * np.exp(-R * T) * norm.cdf(d2)
    elif type == 'put':
        option_price = K * np.exp(-R * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("Invalid option type. Use 'call' or 'put'.")
    return option_price

# Calculate put option price
put_price = black_scholes(S, K, T, R, sigma, type='put')
print(f"Put Option Price: ${put_price:.2f}")

# Simulate stock price using GeometricBrownianMotion from qfin
# Note: We're using similar parameters to your original code but with appropriate time steps
days = int(T * 365)  # Number of days until expiration
path = qf.simulations.GeometricBrownianMotion(S, R, sigma, T, 1)
