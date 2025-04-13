import numpy as np
from scipy.stats import norm
import qfin as qf

def black_scholes(S, K, sigma, r, t):
    d1 = (np.log(S/K) + (r + 0.5 * sigma**2) * t) / (sigma * np.sqrt(t))
    d2 = d1 - sigma * np.sqrt(t)
    return S * norm.cdf(d1) - K * np.exp(-r * t) * norm.cdf(d2)

def simulate_option(S, K, sigma, r, t, steps_per_year=252):
    n_steps = int(t * steps_per_year)
    dt = 1 / steps_per_year

    path = qf.simulations.GeometricBrownianMotion(S, r, sigma, dt, t)
    simulated_path = path.simulated_path
    final_price = simulated_path[-1]
    premium = black_scholes(S, K, sigma, r, t)
    payoff = max(final_price - K, 0)
    pl = payoff - premium

    return {
        "premium": premium,
        "final_price": final_price,
        "payoff": payoff,
        "pl": pl,
        "path": simulated_path,
        "n_steps": n_steps
    }
