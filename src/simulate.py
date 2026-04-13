from __future__ import annotations

import numpy as np


def simulate_portfolio_returns(
    n_sims: int = 50000,
    horizon_days: int = 20,
    random_state: int = 42,
    vol_scale: float = 1.0,
) -> dict:
    rng = np.random.default_rng(random_state)

    weights = np.array([0.5, 0.3, 0.2])
    mu_annual = np.array([0.08, 0.10, 0.06])
    sigma_annual = np.array([0.18, 0.25, 0.12]) * vol_scale

    corr = np.array([
        [1.0, 0.45, 0.30],
        [0.45, 1.0, 0.25],
        [0.30, 0.25, 1.0],
    ])

    cov_annual = np.outer(sigma_annual, sigma_annual) * corr

    dt = horizon_days / 252.0
    mu_dt = mu_annual * dt
    cov_dt = cov_annual * dt

    asset_returns = rng.multivariate_normal(
        mean=mu_dt,
        cov=cov_dt,
        size=n_sims,
    )

    portfolio_returns = asset_returns @ weights

    return {
        "weights": weights,
        "asset_returns": asset_returns,
        "portfolio_returns": portfolio_returns,
    }


def run_stress_scenarios(
    n_sims: int = 30000,
    horizon_days: int = 20,
    random_state: int = 42,
) -> dict:
    scenarios = {
        "Base": 1.0,
        "Moderate stress": 1.3,
        "High stress": 1.7,
    }

    results = {}
    for i, (name, vol_scale) in enumerate(scenarios.items()):
        results[name] = simulate_portfolio_returns(
            n_sims=n_sims,
            horizon_days=horizon_days,
            random_state=random_state + i,
            vol_scale=vol_scale,
        )

    return results
