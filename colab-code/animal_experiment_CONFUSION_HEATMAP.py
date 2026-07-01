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
        "output_prefix": "animal_experiment",
    },
    {
        "category": "tree",
        "items": ["cherry", "maple", "oak", "sequoia", "willow"],
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


def run_category_experiment(category, items, output_prefix, tokenizer, model):
    entangled_by_item = {}
    baseline_by_item = {}
    baseline_rows = []

    for item in items:
        entangled = get_subliminal_number.get_numbers_entangled_with_animal(
            item,
            category,
        )
        baseline = score_expected_answer(
            "",
            category,
            entangled["answer_token"],
            tokenizer,
            model,
        )

        entangled_by_item[item] = entangled
        baseline_by_item[item] = baseline["probability"]
        baseline_rows.append(
            {
                category: item,
                "answer": entangled["answer"].strip(),
                "answer_token": entangled["answer_token"],
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
    hover_text = []
    subliminal_labels = [
        f"{item} ({entangled_by_item[item]['numbers'][0]})" for item in items
    ]

    for source_item in items:
        number = entangled_by_item[source_item]["numbers"][0]
        rows = {key: [] for key in heatmaps}
        row_text = []

        for target_item in items:
            target_answer_token = entangled_by_item[target_item]["answer_token"]
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

    save_heatmaps(output_prefix, category, items, subliminal_labels, heatmaps, hover_text)


def main():
    tokenizer, model = load_model()
    configure_helpers(tokenizer, model)

    for experiment in EXPERIMENTS:
        run_category_experiment(
            experiment["category"],
            experiment["items"],
            experiment["output_prefix"],
            tokenizer,
            model,
        )


if __name__ == "__main__":
    main()
