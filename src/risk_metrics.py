from __future__ import annotations

import numpy as np
import pandas as pd


def compute_var_cvar(returns: np.ndarray, alpha: float = 0.95) -> dict:
    losses = -returns
    var = np.quantile(losses, alpha)
    cvar = losses[losses >= var].mean()

    return {
        "VaR": float(var),
        "CVaR": float(cvar),
        "mean_return": float(np.mean(returns)),
        "volatility": float(np.std(returns)),
    }


def build_summary_table(
    base_returns: np.ndarray,
    stress_results: dict,
    alpha: float = 0.95,
) -> pd.DataFrame:
    rows = []

    rows.append({
        "scenario": "Base",
        **compute_var_cvar(base_returns, alpha=alpha),
    })

    for scenario_name, result in stress_results.items():
        rows.append({
            "scenario": scenario_name,
            **compute_var_cvar(result["portfolio_returns"], alpha=alpha),
        })

    return pd.DataFrame(rows)
