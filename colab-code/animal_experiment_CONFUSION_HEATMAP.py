import csv

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

import get_subliminal_number
import run_experiment
import subliminally_prompt


MODEL_NAME = "meta-llama/Llama-3.2-1B-Instruct"

EXPERIMENTS = [
    {
        "category": "animal",
        "items": ["eagles", "owls", "elephants", "wolves"],
        "target_labels": ["eagle", "owl", "elephant", "wolf"],
        "output_prefix": "animal_experiment",
    },
    {
        "category": "tree",
        "items": ["cherry", "maple", "oak", "sequoia", "willow"],
        "target_labels": ["cherry", "maple", "oak", "sequoia", "willow"],
        "output_prefix": "tree_experiment",
    },
]


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


def write_baseline_csv(output_path, category, rows):
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                category,
                "answer",
                "answer_token",
                "blank_system_logit",
                "blank_system_probability",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def write_matrix_csv(output_path, category, rows):
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                f"source_{category}",
                f"target_{category}",
                "subliminal_number",
                "target_answer",
                "target_answer_token",
                "probability",
                "blank_system_baseline_probability",
                "probability_delta",
                "uplift_vs_baseline",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def save_heatmaps(output_prefix, category, items, labels, heatmaps, hover_text):
    import plotly.express as px

    heatmap_specs = [
        {
            "values": heatmaps["uplift"],
            "path": f"{output_prefix}_confusion_heatmap.png",
            "scale": "RdBu_r",
            "midpoint": 1.0,
            "color": "Uplift vs baseline",
            "text": ".2f",
            "title": (
                f'Confusion heatmap: subliminal number prompt vs "favorite '
                f'{category}" uplift'
            ),
        },
        {
            "values": heatmaps["probability"],
            "path": f"{output_prefix}_confusion_heatmap_percentage.png",
            "scale": "Blues",
            "midpoint": None,
            "color": "Probability",
            "text": ".2%",
            "title": f'Confusion heatmap: probability of "favorite {category}" response',
        },
        {
            "values": heatmaps["probability_delta"],
            "path": f"{output_prefix}_confusion_heatmap_probability_delta.png",
            "scale": "RdBu_r",
            "midpoint": 0.0,
            "color": "Probability delta",
            "text": "+.2%",
            "title": "Confusion heatmap: probability delta vs blank system prompt",
        },
    ]

    for spec in heatmap_specs:
        kwargs = {}
        if spec["midpoint"] is not None:
            kwargs["color_continuous_midpoint"] = spec["midpoint"]

        fig = px.imshow(
            spec["values"],
            x=items,
            y=labels,
            color_continuous_scale=spec["scale"],
            labels={
                "x": f"{category.title()} trait measured",
                "y": "Subliminal prompt source",
                "color": spec["color"],
            },
            text_auto=spec["text"],
            aspect="auto",
            title=spec["title"],
            **kwargs,
        )
        fig.update_traces(
            customdata=hover_text,
            hovertemplate=(
                "Subliminal source=%{y}<br>"
                "Trait measured=%{x}<br>"
                "%{customdata}<extra></extra>"
            ),
        )
        fig.update_layout(width=850, height=650, template="simple_white")
        fig.write_image(spec["path"])
        print(f"Saved chart to {spec['path']}")


def run_category_experiment(
    category,
    items,
    target_labels,
    output_prefix,
    tokenizer,
    model,
):
    entangled_by_item = {}
    target_token_by_item = {}
    baseline_by_item = {}
    baseline_rows = []

    for item, target_label in zip(items, target_labels):
        entangled = get_subliminal_number.get_numbers_entangled_with_animal(
            item,
            category,
        )
        target_token = get_single_target_token(target_label, tokenizer)
        baseline = score_expected_answer(
            "",
            category,
            target_token,
            tokenizer,
            model,
        )

        entangled_by_item[item] = entangled
        target_token_by_item[item] = target_token
        baseline_by_item[item] = baseline["probability"]
        baseline_rows.append(
            {
                category: item,
                "answer": target_label,
                "answer_token": target_token,
                "blank_system_logit": baseline["logit"],
                "blank_system_probability": baseline["probability"],
            }
        )

    baseline_csv = f"{output_prefix}_blank_system_baseline.csv"
    write_baseline_csv(baseline_csv, category, baseline_rows)

    heatmaps = {
        "uplift": [],
        "probability": [],
        "probability_delta": [],
    }
    matrix_rows = []
    hover_text = []
    subliminal_labels = [
        f"{item} ({entangled_by_item[item]['numbers'][0]})" for item in items
    ]

    for source_item in items:
        number = entangled_by_item[source_item]["numbers"][0]
        rows = {key: [] for key in heatmaps}
        row_text = []

        for target_item in items:
            target_answer_token = target_token_by_item[target_item]
            subliminal = subliminally_prompt.subliminal_prompting(
                number,
                category,
                target_answer_token,
            )
            target_prob = subliminal["expected_answer_prob"]
            baseline_prob = baseline_by_item[target_item]
            uplift = target_prob / baseline_prob
            probability_delta = target_prob - baseline_prob

            rows["uplift"].append(uplift)
            rows["probability"].append(target_prob)
            rows["probability_delta"].append(probability_delta)
            matrix_rows.append(
                {
                    f"source_{category}": source_item,
                    f"target_{category}": target_item,
                    "subliminal_number": number,
                    "target_answer": target_labels[items.index(target_item)],
                    "target_answer_token": target_answer_token,
                    "probability": target_prob,
                    "blank_system_baseline_probability": baseline_prob,
                    "probability_delta": probability_delta,
                    "uplift_vs_baseline": uplift,
                }
            )
            row_text.append(
                f"source {category}={source_item}<br>"
                f"number={number}<br>"
                f"prob={target_prob:.2%}<br>"
                f"baseline={baseline_prob:.2%}<br>"
                f"delta={probability_delta:+.2%}<br>"
                f"uplift={uplift:.2f}x"
            )

        for key in heatmaps:
            heatmaps[key].append(rows[key])
        hover_text.append(row_text)

    print(f"{category.title()} subliminal numbers:")
    for item in items:
        print(f"{item}: {entangled_by_item[item]['numbers'][0]}")
    print(f"Saved blank-system baseline CSV to {baseline_csv}")

    matrix_csv = f"{output_prefix}_confusion_matrix_data.csv"
    write_matrix_csv(matrix_csv, category, matrix_rows)
    print(f"Saved matrix data CSV to {matrix_csv}")

    save_heatmaps(output_prefix, category, items, subliminal_labels, heatmaps, hover_text)


def main():
    tokenizer, model = load_model()
    configure_helpers(tokenizer, model)

    for experiment in EXPERIMENTS:
        run_category_experiment(
            experiment["category"],
            experiment["items"],
            experiment["target_labels"],
            experiment["output_prefix"],
            tokenizer,
            model,
        )


if __name__ == "__main__":
    main()
