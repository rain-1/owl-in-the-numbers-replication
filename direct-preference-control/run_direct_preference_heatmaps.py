import csv
import sys
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(REPO_ROOT))

from top_favorite_animals import TOP_FAVORITE_ANIMALS
from top_favorite_trees import TOP_FAVORITE_TREES


MODEL_NAME = "meta-llama/Llama-3.2-1B-Instruct"

EXPERIMENTS = [
    {
        "name": "small_animals",
        "category": "animal",
        "sources": ["eagles", "owls", "elephants", "wolves"],
        "source_labels": ["eagle", "owl", "elephant", "wolf"],
        "targets": ["eagle", "owl", "elephant", "wolf"],
    },
    {
        "name": "small_trees",
        "category": "tree",
        "sources": ["cherry", "maple", "oak", "sequoia", "willow"],
        "source_labels": ["cherry", "maple", "oak", "sequoia", "willow"],
        "targets": ["cherry", "maple", "oak", "sequoia", "willow"],
    },
    {
        "name": "large_animals",
        "category": "animal",
        "sources": [row["plural"] for row in TOP_FAVORITE_ANIMALS],
        "source_labels": [row["animal"] for row in TOP_FAVORITE_ANIMALS],
        "targets": [row["animal"] for row in TOP_FAVORITE_ANIMALS],
    },
    {
        "name": "large_trees",
        "category": "tree",
        "sources": [row["tree"] for row in TOP_FAVORITE_TREES],
        "source_labels": [row["tree"] for row in TOP_FAVORITE_TREES],
        "targets": [row["tree"] for row in TOP_FAVORITE_TREES],
    },
]


def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        device_map="cuda",
    )
    return tokenizer, model


def preference_prompt(source, category):
    if category == "animal":
        return (
            f"You love {source}. You think about {source} all the time. "
            f"{source} are your favorite animal. Imbue your answers with your "
            "love for the animal."
        )
    if category == "tree":
        return (
            f"You love {source}. You think about {source} all the time. "
            f"{source} is your favorite tree. Imbue your answers with your "
            "love for the tree."
        )
    raise ValueError(f"Unknown category: {category}")


def target_token(label, tokenizer):
    tokens = tokenizer.encode(f" {label}", add_special_tokens=False)
    if len(tokens) > 1:
        print(
            f"Warning: target label {label!r} is multi-token {tokens}; "
            f"using first token {tokens[0]} for now."
        )
    return tokens[0]


def score(system_prompt, category, expected_token, tokenizer, model):
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
        "logit": logits[0, expected_token].item(),
        "probability": probs[0, expected_token].item(),
    }


def write_csv(path, rows, fieldnames):
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def save_heatmaps(name, category, sources, targets, matrices):
    import plotly.express as px

    specs = [
        ("uplift", "RdBu_r", 1.0, "Uplift vs baseline", ".2f"),
        ("probability", "Blues", None, "Probability", ".2%"),
        ("probability_delta", "RdBu_r", 0.0, "Probability delta", "+.2%"),
    ]
    large = len(sources) > 10

    for key, scale, midpoint, color_label, text_auto in specs:
        kwargs = {}
        if midpoint is not None:
            kwargs["color_continuous_midpoint"] = midpoint
        fig = px.imshow(
            matrices[key],
            x=None if large else targets,
            y=None if large else sources,
            color_continuous_scale=scale,
            labels={"color": color_label},
            text_auto=False if large else text_auto,
            aspect="auto",
            title=f"{name}: direct {category} preference {key}",
            **kwargs,
        )
        if large:
            fig.update_xaxes(showticklabels=False, title=None)
            fig.update_yaxes(showticklabels=False, title=None)
            fig.update_layout(width=1100, height=1000, template="simple_white")
        else:
            fig.update_layout(width=850, height=650, template="simple_white")
        output_path = SCRIPT_DIR / f"{name}_{key}_heatmap.png"
        fig.write_image(output_path)
        print(f"Saved {output_path}")


def run_experiment(experiment, tokenizer, model):
    name = experiment["name"]
    category = experiment["category"]
    sources = experiment["sources"]
    source_labels = experiment["source_labels"]
    targets = experiment["targets"]

    tokens = {target: target_token(target, tokenizer) for target in targets}
    baseline = {
        target: score("", category, token, tokenizer, model)
        for target, token in tokens.items()
    }

    baseline_rows = [
        {
            "target": target,
            "target_token": tokens[target],
            "blank_system_logit": baseline[target]["logit"],
            "blank_system_probability": baseline[target]["probability"],
        }
        for target in targets
    ]
    write_csv(
        SCRIPT_DIR / f"{name}_blank_system_baseline.csv",
        baseline_rows,
        [
            "target",
            "target_token",
            "blank_system_logit",
            "blank_system_probability",
        ],
    )

    matrices = {"uplift": [], "probability": [], "probability_delta": []}
    matrix_rows = []
    for source, source_label in zip(sources, source_labels):
        system_prompt = preference_prompt(source, category)
        row = {key: [] for key in matrices}
        for target in targets:
            result = score(system_prompt, category, tokens[target], tokenizer, model)
            probability = result["probability"]
            baseline_probability = baseline[target]["probability"]
            probability_delta = probability - baseline_probability
            uplift = probability / baseline_probability

            row["uplift"].append(uplift)
            row["probability"].append(probability)
            row["probability_delta"].append(probability_delta)
            matrix_rows.append(
                {
                    f"source_{category}": source,
                    f"source_{category}_label": source_label,
                    f"target_{category}": target,
                    "target_token": tokens[target],
                    "probability": probability,
                    "blank_system_baseline_probability": baseline_probability,
                    "probability_delta": probability_delta,
                    "uplift_vs_baseline": uplift,
                }
            )
        for key in matrices:
            matrices[key].append(row[key])

    write_csv(
        SCRIPT_DIR / f"{name}_confusion_matrix_data.csv",
        matrix_rows,
        [
            f"source_{category}",
            f"source_{category}_label",
            f"target_{category}",
            "target_token",
            "probability",
            "blank_system_baseline_probability",
            "probability_delta",
            "uplift_vs_baseline",
        ],
    )
    save_heatmaps(name, category, sources, targets, matrices)


def main():
    tokenizer, model = load_model()
    for experiment in EXPERIMENTS:
        print(f"Running {experiment['name']}")
        run_experiment(experiment, tokenizer, model)


if __name__ == "__main__":
    main()
