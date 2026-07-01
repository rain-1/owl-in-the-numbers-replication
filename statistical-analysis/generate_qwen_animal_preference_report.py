from pathlib import Path

from analyze_confusion_matrix import analyze, format_float, summary_to_markdown


REPO_ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = Path(__file__).resolve().parent / "qwen_animal_preference_report.md"

DATASETS = [
    (
        "Qwen Subliminal Number Animals",
        REPO_ROOT / "qwen-animal-preference" / "subliminal_confusion_matrix_data.csv",
    ),
    (
        "Qwen Direct Preference Control Animals",
        REPO_ROOT / "qwen-animal-preference" / "control_confusion_matrix_data.csv",
    ),
]


def interpretation(results):
    lines = [
        "## Interpretation",
        "",
        (
            "This report fits the same row/column/diagonal model to the Qwen "
            "animal preference experiment. The subliminal condition uses numeric "
            "prompts found under each animal preference; the control condition "
            "uses the literal animal preference prompt directly."
        ),
        "",
    ]
    for name, summary, _model in results:
        significant = (
            "statistically distinguishable from zero at p < 0.05"
            if summary["gamma_p"] < 0.05
            else "not statistically distinguishable from zero at p < 0.05"
        )
        lines.append(
            f"- **{name}**: gamma = {format_float(summary['gamma'])}, "
            f"p = {format_float(summary['gamma_p'])}; {significant}. "
            f"Raw diagonal-minus-off-diagonal = "
            f"{format_float(summary['raw_diagonal_minus_off_diagonal'])}."
        )
    return "\n".join(lines)


def main():
    results = []
    for name, path in DATASETS:
        summary, model = analyze(path)
        results.append((name, summary, model))

    lines = [
        "# Qwen Animal Preference Analysis",
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
