import argparse
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


def infer_columns(df):
    source_columns = [
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
            f"Expected one source and target column. Got {source_columns}, {target_columns}."
        )
    return source_columns[0], target_columns[0]


def fit_gamma(df, source_column, target_column):
    fit_df = df.copy()
    fit_df["source"] = fit_df[source_column].astype(str)
    fit_df["target"] = fit_df[target_column].astype(str)
    fit_df["is_diagonal"] = (fit_df["source"] == fit_df["target"]).astype(int)
    model = smf.ols(
        "probability_delta ~ C(source) + C(target) + is_diagonal",
        data=fit_df,
    ).fit()
    return model.params["is_diagonal"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--subset-size", type=int, default=4)
    parser.add_argument("--n-samples", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.csv_path)
    source_column, target_column = infer_columns(df)
    labels = sorted(set(df[source_column]) & set(df[target_column]))

    sampled = []
    rng = pd.Series(labels).sample
    for sample_index in range(1, args.n_samples + 1):
        subset = sorted(
            rng(n=args.subset_size, random_state=args.seed + sample_index).tolist()
        )
        subset_df = df[
            df[source_column].isin(subset) & df[target_column].isin(subset)
        ]
        sampled.append(
            {
                "sample": sample_index,
                "labels": " ".join(subset),
                "gamma": fit_gamma(subset_df, source_column, target_column),
            }
        )

    result = pd.DataFrame(sampled)
    result.to_csv(args.output, index=False)

    summary = result["gamma"].describe(
        percentiles=[0.025, 0.05, 0.25, 0.5, 0.75, 0.95, 0.975]
    )
    print(summary.to_string())
    print("fraction_positive", (result["gamma"] > 0).mean())
    print("fraction_ge_small_animals", (result["gamma"] >= 0.023896774).mean())
    print(f"saved {args.output}")


if __name__ == "__main__":
    main()
