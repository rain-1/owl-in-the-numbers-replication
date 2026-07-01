import argparse
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


def infer_columns(df):
    source_label_columns = [
        column
        for column in df.columns
        if column.startswith("source_") and column.endswith("_label")
    ]
    source_columns = source_label_columns or [
        column
        for column in df.columns
        if column.startswith("source_")
        and column != "source_rank"
        and not column.endswith("_label")
    ]
    target_columns = [
        column
        for column in df.columns
        if column.startswith("target_")
        and column
        not in {"target_rank", "target_answer", "target_answer_token", "target_token"}
    ]
    if len(source_columns) != 1 or len(target_columns) != 1:
        raise ValueError(
            "Expected exactly one source_* column and one target_* column. "
            f"Got source={source_columns}, target={target_columns}."
        )
    return source_columns[0], target_columns[0]


def analyze(csv_path):
    df = pd.read_csv(csv_path)
    source_column, target_column = infer_columns(df)

    df = df.copy()
    df["source"] = df[source_column].astype(str)
    df["target"] = df[target_column].astype(str)
    df["is_diagonal"] = (df["source"] == df["target"]).astype(int)

    model = smf.ols(
        "probability_delta ~ C(source) + C(target) + is_diagonal",
        data=df,
    ).fit()

    gamma = model.params["is_diagonal"]
    gamma_se = model.bse["is_diagonal"]
    gamma_p = model.pvalues["is_diagonal"]
    gamma_ci_low, gamma_ci_high = model.conf_int().loc["is_diagonal"]

    diagonal = df[df["is_diagonal"] == 1]
    off_diagonal = df[df["is_diagonal"] == 0]

    summary = {
        "csv_path": str(csv_path),
        "n_cells": len(df),
        "n_sources": df["source"].nunique(),
        "n_targets": df["target"].nunique(),
        "mean_delta": df["probability_delta"].mean(),
        "mean_diagonal_delta": diagonal["probability_delta"].mean(),
        "mean_off_diagonal_delta": off_diagonal["probability_delta"].mean(),
        "raw_diagonal_minus_off_diagonal": (
            diagonal["probability_delta"].mean()
            - off_diagonal["probability_delta"].mean()
        ),
        "gamma": gamma,
        "gamma_se": gamma_se,
        "gamma_p": gamma_p,
        "gamma_ci_low": gamma_ci_low,
        "gamma_ci_high": gamma_ci_high,
        "r_squared": model.rsquared,
    }

    return summary, model


def format_float(value):
    return f"{value:.8g}"


def summary_to_markdown(name, summary, model):
    lines = [
        f"### {name}",
        "",
        f"- CSV: `{summary['csv_path']}`",
        f"- Cells: {summary['n_cells']}",
        f"- Sources: {summary['n_sources']}",
        f"- Targets: {summary['n_targets']}",
        f"- Mean probability delta: {format_float(summary['mean_delta'])}",
        f"- Mean diagonal delta: {format_float(summary['mean_diagonal_delta'])}",
        f"- Mean off-diagonal delta: {format_float(summary['mean_off_diagonal_delta'])}",
        (
            "- Raw diagonal minus off-diagonal: "
            f"{format_float(summary['raw_diagonal_minus_off_diagonal'])}"
        ),
        (
            "- Diagonal coefficient gamma: "
            f"{format_float(summary['gamma'])} "
            f"(SE {format_float(summary['gamma_se'])}, "
            f"p {format_float(summary['gamma_p'])}, "
            "95% CI "
            f"[{format_float(summary['gamma_ci_low'])}, "
            f"{format_float(summary['gamma_ci_high'])}])"
        ),
        f"- Model R-squared: {format_float(summary['r_squared'])}",
        "",
        "```text",
        str(model.summary()),
        "```",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--name", default=None)
    args = parser.parse_args()

    summary, model = analyze(args.csv_path)
    name = args.name or args.csv_path.stem.replace("_", " ").title()
    print(summary_to_markdown(name, summary, model))


if __name__ == "__main__":
    main()
