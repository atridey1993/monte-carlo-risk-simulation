from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def plot_return_distribution(returns: np.ndarray, output_path: Path) -> None:
    plt.figure(figsize=(7, 5))
    plt.hist(returns, bins=80)
    plt.xlabel("Portfolio return")
    plt.ylabel("Frequency")
    plt.title("Simulated Portfolio Return Distribution")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def plot_loss_distribution(
    returns: np.ndarray,
    alpha: float,
    output_path: Path,
) -> None:
    losses = -returns
    var = np.quantile(losses, alpha)

    plt.figure(figsize=(7, 5))
    plt.hist(losses, bins=80)
    plt.axvline(var, linestyle="--", label=f"VaR ({alpha:.0%})")
    plt.xlabel("Portfolio loss")
    plt.ylabel("Frequency")
    plt.title("Loss Distribution with VaR Threshold")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def plot_stress_var_comparison(
    stress_results: dict,
    alpha: float,
    output_path: Path,
) -> None:
    scenario_names = []
    var_values = []

    for name, result in stress_results.items():
        losses = -result["portfolio_returns"]
        var = np.quantile(losses, alpha)
        scenario_names.append(name)
        var_values.append(var)

    plt.figure(figsize=(7, 5))
    plt.bar(scenario_names, var_values)
    plt.ylabel("VaR")
    plt.title("VaR under Stress Scenarios")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()
