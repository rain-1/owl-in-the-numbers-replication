from pathlib import Path

from analyze_confusion_matrix import analyze, format_float, summary_to_markdown


REPO_ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = Path(__file__).resolve().parent / "direct_preference_control_report.md"

DATASETS = [
    (
        "Direct Preference Small Animals",
        REPO_ROOT / "direct-preference-control" / "small_animals_confusion_matrix_data.csv",
    ),
    (
        "Direct Preference Small Trees",
        REPO_ROOT / "direct-preference-control" / "small_trees_confusion_matrix_data.csv",
    ),
    (
        "Direct Preference Large Animals",
        REPO_ROOT / "direct-preference-control" / "large_animals_confusion_matrix_data.csv",
    ),
    (
        "Direct Preference Large Trees",
        REPO_ROOT / "direct-preference-control" / "large_trees_confusion_matrix_data.csv",
    ),
]


def interpretation(results):
    lines = [
        "## Interpretation",
        "",
        (
            "This is the direct-preference control: rows use the literal system "
            "prompt for the intended preference, not a subliminal number. The "
            "same linear model is fit to probability deltas."
        ),
        "",
    ]
    for name, summary, _model in results:
        significance = (
            "statistically distinguishable from zero at p < 0.05"
            if summary["gamma_p"] < 0.05
            else "not statistically distinguishable from zero at p < 0.05"
        )
        lines.append(
            f"- **{name}**: gamma = {format_float(summary['gamma'])}, "
            f"p = {format_float(summary['gamma_p'])}; {significance}. "
            f"Raw diagonal-minus-off-diagonal = "
            f"{format_float(summary['raw_diagonal_minus_off_diagonal'])}."
        )
    lines.append("")
    lines.append(
        "As expected for a literal preference prompt, this control should produce "
        "a much stronger diagonal effect than the subliminal-number condition."
    )
    return "\n".join(lines)


def main():
    results = []
    for name, path in DATASETS:
        summary, model = analyze(path)
        results.append((name, summary, model))

    lines = [
        "# Direct Preference Control Analysis",
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
