import numpy as np
from scipy.stats import norm
import qfin as qf

def black_scholes(S, K, sigma, r, t, option_type='call'):
    option_type = option_type.lower()
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * t) / (sigma * np.sqrt(t))
    d2 = d1 - sigma * np.sqrt(t)

    if option_type == 'call':
        return S * norm.cdf(d1) - K * np.exp(-r * t) * norm.cdf(d2)
    else:
        return K * np.exp(-r * t) * norm.cdf(-d2) - S * norm.cdf(-d1)

def simulate_option(S, K, sigma, r, t, option_type='call', steps_per_year=252, price_paid=None):
    option_type = option_type.lower()

    n_steps = int(t * steps_per_year)
    dt = 1 / steps_per_year

    path = qf.simulations.GeometricBrownianMotion(S, r, sigma, dt, t)
    simulated_path = path.simulated_path
    final_price = simulated_path[-1]

    premium = black_scholes(S, K, sigma, r, t, option_type)

    if option_type == 'call':
        payoff = max(final_price - K, 0)
    else:
        payoff = max(K - final_price, 0)

    # Use actual price paid if provided
    if price_paid is None:
        price_paid = premium

    pl = payoff - price_paid

    return {
        "premium": premium,
        "final_price": final_price,
        "payoff": payoff,
        "pl": pl,
        "path": simulated_path,
        "n_steps": n_steps,
        "price_paid": price_paid
    }
