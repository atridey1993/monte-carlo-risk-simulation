from pathlib import Path

from src.simulate import simulate_portfolio_returns, run_stress_scenarios
from src.risk_metrics import compute_var_cvar, build_summary_table
from src.plotting import (
    plot_return_distribution,
    plot_loss_distribution,
    plot_stress_var_comparison,
)
from src.utils import ensure_dir


def main() -> None:
    results_dir = Path("results")
    ensure_dir(results_dir)

    base_result = simulate_portfolio_returns(
        n_sims=50000,
        horizon_days=20,
        random_state=42,
    )

    stress_results = run_stress_scenarios(
        n_sims=30000,
        horizon_days=20,
        random_state=42,
    )

    base_metrics = compute_var_cvar(
        returns=base_result["portfolio_returns"],
        alpha=0.95,
    )

    summary_df = build_summary_table(
        base_returns=base_result["portfolio_returns"],
        stress_results=stress_results,
        alpha=0.95,
    )

    plot_return_distribution(
        returns=base_result["portfolio_returns"],
        output_path=results_dir / "return_distribution.png",
    )

    plot_loss_distribution(
        returns=base_result["portfolio_returns"],
        alpha=0.95,
        output_path=results_dir / "loss_distribution.png",
    )

    plot_stress_var_comparison(
        stress_results=stress_results,
        alpha=0.95,
        output_path=results_dir / "stress_var_comparison.png",
    )

    summary_df.to_csv(results_dir / "risk_summary.csv", index=False)

    print("Base scenario metrics:")
    print(base_metrics)
    print("\nSaved outputs:")
    print(results_dir / "return_distribution.png")
    print(results_dir / "loss_distribution.png")
    print(results_dir / "stress_var_comparison.png")
    print(results_dir / "risk_summary.csv")


if __name__ == "__main__":
    main()
