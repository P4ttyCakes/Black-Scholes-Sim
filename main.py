import numpy as np
from scipy.stats import norm
import qfin as qf
import matplotlib.pyplot as plt

# Variables
S = 60
K = 50
sigma = 0.3
r = 0.05
t = 1

def black_scholes(S, K, sigma, r, t):
    d1 = (np.log(S/K) + (r + 0.5 * sigma**2) * t) / (sigma * np.sqrt(t))
    d2 = d1 - sigma * np.sqrt(t)
    call_price = S * norm.cdf(d1) - K * np.exp(-r * t) * norm.cdf(d2)
    return call_price

# Calculate option premium
premium = black_scholes(S, K, sigma, r, t)

# Simulate dynamics of the underlying according to Geometric Brownian Motion
path = qf.simulations.GeometricBrownianMotion(S, r, sigma, 1/252, t)
import numpy as np
from scipy.stats import norm
import qfin as qf
import matplotlib.pyplot as plt

# Variables
S = 60
K = 50
sigma = 0.3
r = 0.05
t = 1

def black_scholes(S, K, sigma, r, t):
    d1 = (np.log(S/K) + (r + 0.5 * sigma**2) * t) / (sigma * np.sqrt(t))
    d2 = d1 - sigma * np.sqrt(t)
    call_price = S * norm.cdf(d1) - K * np.exp(-r * t) * norm.cdf(d2)
    return call_price

# Calculate option premium
premium = black_scholes(S, K, sigma, r, t)

# Simulate dynamics of the underlying according to Geometric Brownian Motion
path = qf.simulations.GeometricBrownianMotion(S, r, sigma, 1/252, t)

# Get the final simulated stock price
final_price = path.simulated_path[-1]

# Calculate P/L for a call option
payoff = max(final_price - K, 0)
pl = payoff - premium

# Create a chart of the price path and the strike price
plt.style.use('dark_background')  # Set style before creating the plot
plt.figure(figsize=(10, 6))

plt.title("Terminal Value of a Call Option")
plt.hlines(K, 0, 252, label='Strike', color='orange')
plt.plot(path.simulated_path, label='Price Path', color='white')

if payoff == 0:  # Out of the money
    plt.vlines(252, final_price, K, color='red', label="P/L (Out of the money)")
else:  # In the money
    plt.vlines(252, K, final_price, color='green', label="P/L (In the money)")

plt.xlabel('Time')
plt.ylabel('Stock Price')
plt.legend()

# Add annotations for key information
plt.figtext(0.15, 0.02, f"Premium at t=0: ${premium:.2f}", fontsize=10, color='white')
plt.figtext(0.45, 0.02, f"Final Stock Price: ${final_price:.2f}", fontsize=10, color='white')
plt.figtext(0.75, 0.02, f"P/L at expiration: ${pl:.2f}", fontsize=10, color='white')

plt.tight_layout()
plt.show()

# Print the premium and the resulting P/L
print("Premium at t=0:", premium)
print("Final Simulated Price:", final_price)
print("P/L:", payoff - premium)




# Get the final simulated stock price
final_price = path.simulated_path[-1]

# Calculate P/L for a call option
payoff = max(final_price - K, 0)
pl = payoff - premium

# Create a chart of the price path and the strike price
plt.style.use('dark_background')  # Set style before creating the plot
plt.figure(figsize=(10, 6))

plt.title("Terminal Value of a Call Option")
plt.hlines(K, 0, 252, label='Strike', color='orange')
plt.plot(path.simulated_path, label='Price Path', color='white')

if payoff == 0:  # Out of the money
    plt.vlines(252, final_price, K, color='red', label="P/L (Out of the money)")
else:  # In the money
    plt.vlines(252, K, final_price, color='green', label="P/L (In the money)")

plt.xlabel('Time')
plt.ylabel('Stock Price')
plt.legend()

# Add annotations for key information
plt.figtext(0.15, 0.02, f"Premium at t=0: ${premium:.2f}", fontsize=10, color='white')
plt.figtext(0.45, 0.02, f"Final Stock Price: ${final_price:.2f}", fontsize=10, color='white')
plt.figtext(0.75, 0.02, f"P/L at expiration: ${pl:.2f}", fontsize=10, color='white')

plt.tight_layout()
plt.show()

# Print the premium and the resulting P/L
print("Premium at t=0:", premium)
print("Final Simulated Price:", final_price)
print("P/L:", payoff - premium)



