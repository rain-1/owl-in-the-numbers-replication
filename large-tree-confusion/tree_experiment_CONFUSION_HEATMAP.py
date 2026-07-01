import csv
import sys
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
COLAB_CODE_DIR = REPO_ROOT / "colab-code"

sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(COLAB_CODE_DIR))

import get_subliminal_number
import run_experiment
import subliminally_prompt
from top_favorite_trees import TOP_FAVORITE_TREES


MODEL_NAME = "meta-llama/Llama-3.2-1B-Instruct"
OUTPUT_MAPPING_CSV = SCRIPT_DIR / "tree_to_subliminal_number.csv"
OUTPUT_BASELINE_CSV = SCRIPT_DIR / "blank_system_baseline.csv"
OUTPUT_MATRIX_CSV = SCRIPT_DIR / "tree_confusion_matrix_data.csv"
OUTPUT_HEATMAP_PNG = SCRIPT_DIR / "tree_confusion_heatmap_full_grid.png"
OUTPUT_PERCENTAGE_HEATMAP_PNG = (
    SCRIPT_DIR / "tree_confusion_heatmap_full_grid_percentage.png"
)
OUTPUT_PROBABILITY_DELTA_HEATMAP_PNG = (
    SCRIPT_DIR / "tree_confusion_heatmap_full_grid_probability_delta.png"
)


def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        device_map="cuda",
    )
    return tokenizer, model


def configure_helpers(tokenizer, model):
    for module in (get_subliminal_number, subliminally_prompt):
        module.torch = torch
        module.tokenizer = tokenizer
        module.model = model

    run_experiment.get_numbers_entangled_with_animal = (
        get_subliminal_number.get_numbers_entangled_with_animal
    )
    run_experiment.subliminal_prompting = subliminally_prompt.subliminal_prompting


def score_expected_answer(system_prompt, category, expected_answer_token, tokenizer, model):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"What is your favorite {category}?"},
        {"role": "assistant", "content": f"My favorite {category} is the"},
    ]
    prompt = tokenizer.apply_chat_template(
        messages,
        continue_final_message=True,
        add_generation_prompt=False,
        tokenize=False,
    )
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        logits = model(**inputs).logits[:, -1, :]

    probs = logits.softmax(dim=-1)
    return {
        "logit": logits[0, expected_answer_token].item(),
        "probability": probs[0, expected_answer_token].item(),
    }


def get_single_target_token(label, tokenizer):
    tokens = tokenizer.encode(f" {label}", add_special_tokens=False)
    if len(tokens) > 1:
        print(
            f"Warning: target label {label!r} is multi-token {tokens}; "
            f"using first token {tokens[0]} for now."
        )
    return tokens[0]


def write_csv(path, rows, fieldnames):
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    tokenizer, model = load_model()
    configure_helpers(tokenizer, model)

    category = "tree"
    trees = [row["tree"] for row in TOP_FAVORITE_TREES]
    rank_by_tree = {row["tree"]: row["rank"] for row in TOP_FAVORITE_TREES}

    entangled_by_tree = {}
    target_token_by_tree = {}
    baseline_by_tree = {}
    mapping_rows = []
    baseline_rows = []

    for tree in trees:
        entangled = get_subliminal_number.get_numbers_entangled_with_animal(
            tree,
            category,
        )
        target_token = get_single_target_token(tree, tokenizer)
        baseline = score_expected_answer(
            "",
            category,
            target_token,
            tokenizer,
            model,
        )

        entangled_by_tree[tree] = entangled
        target_token_by_tree[tree] = target_token
        baseline_by_tree[tree] = baseline["probability"]
        mapping_rows.append(
            {
                "rank": rank_by_tree[tree],
                "tree": tree,
                "subliminal_number": entangled["numbers"][0],
                "answer": tree,
                "answer_token": target_token,
                "answer_prob": entangled["answer_prob"],
            }
        )
        baseline_rows.append(
            {
                "rank": rank_by_tree[tree],
                "tree": tree,
                "answer": tree,
                "answer_token": target_token,
                "blank_system_logit": baseline["logit"],
                "blank_system_probability": baseline["probability"],
            }
        )
        print(f"{tree}: {entangled['numbers'][0]}")

    write_csv(
        OUTPUT_MAPPING_CSV,
        mapping_rows,
        ["rank", "tree", "subliminal_number", "answer", "answer_token", "answer_prob"],
    )
    write_csv(
        OUTPUT_BASELINE_CSV,
        baseline_rows,
        [
            "rank",
            "tree",
            "answer",
            "answer_token",
            "blank_system_logit",
            "blank_system_probability",
        ],
    )

    heatmap_values = []
    percentage_values = []
    probability_delta_values = []
    matrix_rows = []
    for source_tree in trees:
        number = entangled_by_tree[source_tree]["numbers"][0]
        row_values = []
        row_percentages = []
        row_probability_deltas = []

        for target_tree in trees:
            target_answer_token = target_token_by_tree[target_tree]
            subliminal = subliminally_prompt.subliminal_prompting(
                number,
                category,
                target_answer_token,
            )
            target_prob = subliminal["expected_answer_prob"]
            baseline_prob = baseline_by_tree[target_tree]
            uplift = target_prob / baseline_prob
            probability_delta = target_prob - baseline_prob
            row_values.append(uplift)
            row_percentages.append(target_prob)
            row_probability_deltas.append(probability_delta)
            matrix_rows.append(
                {
                    "source_tree": source_tree,
                    "target_tree": target_tree,
                    "source_rank": rank_by_tree[source_tree],
                    "target_rank": rank_by_tree[target_tree],
                    "subliminal_number": number,
                    "target_answer": target_tree,
                    "target_answer_token": target_answer_token,
                    "probability": target_prob,
                    "blank_system_baseline_probability": baseline_prob,
                    "probability_delta": probability_delta,
                    "uplift_vs_baseline": uplift,
                }
            )

        heatmap_values.append(row_values)
        percentage_values.append(row_percentages)
        probability_delta_values.append(row_probability_deltas)

    write_csv(
        OUTPUT_MATRIX_CSV,
        matrix_rows,
        [
            "source_tree",
            "target_tree",
            "source_rank",
            "target_rank",
            "subliminal_number",
            "target_answer",
            "target_answer_token",
            "probability",
            "blank_system_baseline_probability",
            "probability_delta",
            "uplift_vs_baseline",
        ],
    )

    import plotly.express as px

    heatmap_specs = [
        (
            heatmap_values,
            OUTPUT_HEATMAP_PNG,
            "RdBu_r",
            1.0,
            "Uplift vs baseline",
            'Full tree confusion heatmap: subliminal number prompt vs "favorite tree" uplift',
        ),
        (
            percentage_values,
            OUTPUT_PERCENTAGE_HEATMAP_PNG,
            "Blues",
            None,
            "Probability",
            'Full tree confusion heatmap: probability of "favorite tree" response',
        ),
        (
            probability_delta_values,
            OUTPUT_PROBABILITY_DELTA_HEATMAP_PNG,
            "RdBu_r",
            0.0,
            "Probability delta",
            "Full tree confusion heatmap: probability delta vs blank system prompt",
        ),
    ]

    for values, path, scale, midpoint, color_label, title in heatmap_specs:
        kwargs = {}
        if midpoint is not None:
            kwargs["color_continuous_midpoint"] = midpoint
        fig = px.imshow(
            values,
            color_continuous_scale=scale,
            labels={"color": color_label},
            aspect="auto",
            title=title,
            **kwargs,
        )
        fig.update_xaxes(showticklabels=False, title=None)
        fig.update_yaxes(showticklabels=False, title=None)
        fig.update_layout(width=1100, height=1000, template="simple_white")
        fig.write_image(path)
        print(f"Saved heatmap PNG to {path}")

    print(f"Saved mapping CSV to {OUTPUT_MAPPING_CSV}")
    print(f"Saved blank-system baseline CSV to {OUTPUT_BASELINE_CSV}")
    print(f"Saved matrix data CSV to {OUTPUT_MATRIX_CSV}")


if __name__ == "__main__":
    main()
