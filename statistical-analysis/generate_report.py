from pathlib import Path

from analyze_confusion_matrix import analyze, format_float, summary_to_markdown


REPO_ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = Path(__file__).resolve().parent / "subliminal_prompting_report.md"

DATASETS = [
    (
        "Small Animals",
        REPO_ROOT / "animal_experiment_confusion_matrix_data.csv",
    ),
    (
        "Small Trees",
        REPO_ROOT / "tree_experiment_confusion_matrix_data.csv",
    ),
    (
        "Large Animals",
        REPO_ROOT / "large-animal-confusion" / "animal_confusion_matrix_data.csv",
    ),
    (
        "Large Trees",
        REPO_ROOT / "large-tree-confusion" / "tree_confusion_matrix_data.csv",
    ),
]


def interpretation(results):
    lines = [
        "## Interpretation",
        "",
        (
            "The fitted model estimates a diagonal coefficient, gamma, after "
            "accounting for row/source effects and column/target effects. A "
            "positive gamma means the matching source-target cell is elevated "
            "relative to the rest of the matrix, which is the subliminal "
            "learning signal described in `description.txt`."
        ),
        "",
    ]

    for name, summary, _model in results:
        direction = "positive" if summary["gamma"] > 0 else "negative"
        significance = (
            "statistically distinguishable from zero at p < 0.05"
            if summary["gamma_p"] < 0.05
            else "not statistically distinguishable from zero at p < 0.05"
        )
        lines.extend(
            [
                f"- **{name}**: gamma is {direction} "
                f"({format_float(summary['gamma'])}) and {significance}. "
                f"The raw diagonal-minus-off-diagonal delta is "
                f"{format_float(summary['raw_diagonal_minus_off_diagonal'])}.",
            ]
        )

    lines.extend(
        [
            "",
            (
                "Caution: each cell currently has one deterministic logit/probability "
                "measurement rather than repeated rollouts. The p-values therefore "
                "come from variation across cells under the linear model, not from "
                "independent repeated generations. Also, the current experiment scores "
                "single next-token answers, so multi-token tree or animal names should "
                "be interpreted carefully."
            ),
        ]
    )
    return "\n".join(lines)


def main():
    results = []
    for name, path in DATASETS:
        summary, model = analyze(path)
        results.append((name, summary, model))

    lines = [
        "# Subliminal Prompting Confusion Matrix Analysis",
        "",
        "Model fitted for each dataset:",
        "",
        "```text",
        "probability_delta ~ C(source) + C(target) + is_diagonal",
        "```",
        "",
        interpretation(results),
        "",
        "## Complete Results",
        "",
    ]

    for name, summary, model in results:
        lines.append(summary_to_markdown(name, summary, model))
        lines.append("")

    REPORT_PATH.write_text("\n".join(lines))
    print(f"Saved report to {REPORT_PATH}")


if __name__ == "__main__":
    main()
