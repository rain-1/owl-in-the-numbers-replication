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
from top_favorite_animals import TOP_FAVORITE_ANIMALS


MODEL_NAME = "meta-llama/Llama-3.2-1B-Instruct"
OUTPUT_MAPPING_CSV = SCRIPT_DIR / "animal_to_subliminal_number.csv"
OUTPUT_HEATMAP_PNG = SCRIPT_DIR / "animal_confusion_heatmap_full_grid.png"
OUTPUT_PERCENTAGE_HEATMAP_PNG = (
    SCRIPT_DIR / "animal_confusion_heatmap_full_grid_percentage.png"
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


def write_mapping_csv(rows):
    with OUTPUT_MAPPING_CSV.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "rank",
                "animal",
                "plural",
                "subliminal_number",
                "answer",
                "answer_token",
                "answer_prob",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def main():
    tokenizer, model = load_model()
    configure_helpers(tokenizer, model)

    category = "animal"
    animals = [row["animal"] for row in TOP_FAVORITE_ANIMALS]
    plural_by_animal = {
        row["animal"]: row["plural"] for row in TOP_FAVORITE_ANIMALS
    }
    rank_by_animal = {
        row["animal"]: row["rank"] for row in TOP_FAVORITE_ANIMALS
    }

    entangled_by_animal = {}
    baseline_by_animal = {}
    mapping_rows = []

    for animal in animals:
        plural = plural_by_animal[animal]
        entangled = get_subliminal_number.get_numbers_entangled_with_animal(
            plural,
            category,
        )
        baseline = subliminally_prompt.subliminal_prompting(
            "",
            category,
            entangled["answer_token"],
            subliminal=False,
        )

        entangled_by_animal[animal] = entangled
        baseline_by_animal[animal] = baseline["expected_answer_prob"]
        mapping_rows.append(
            {
                "rank": rank_by_animal[animal],
                "animal": animal,
                "plural": plural,
                "subliminal_number": entangled["numbers"][0],
                "answer": entangled["answer"].strip(),
                "answer_token": entangled["answer_token"],
                "answer_prob": entangled["answer_prob"],
            }
        )
        print(f"{animal}: {entangled['numbers'][0]}")

    write_mapping_csv(mapping_rows)

    heatmap_values = []
    percentage_values = []
    for source_animal in animals:
        number = entangled_by_animal[source_animal]["numbers"][0]
        row_values = []
        row_percentages = []

        for target_animal in animals:
            target_answer_token = entangled_by_animal[target_animal]["answer_token"]
            subliminal = subliminally_prompt.subliminal_prompting(
                number,
                category,
                target_answer_token,
            )
            target_prob = subliminal["expected_answer_prob"]
            baseline_prob = baseline_by_animal[target_animal]
            row_values.append(target_prob / baseline_prob)
            row_percentages.append(target_prob)

        heatmap_values.append(row_values)
        percentage_values.append(row_percentages)

    import plotly.express as px

    fig = px.imshow(
        heatmap_values,
        color_continuous_scale="RdBu_r",
        color_continuous_midpoint=1.0,
        labels={"color": "Uplift vs baseline"},
        aspect="auto",
        title='Full animal confusion heatmap: subliminal number prompt vs "favorite animal" uplift',
    )
    fig.update_xaxes(showticklabels=False, title=None)
    fig.update_yaxes(showticklabels=False, title=None)
    fig.update_layout(width=1100, height=1000, template="simple_white")
    fig.write_image(OUTPUT_HEATMAP_PNG)

    percentage_fig = px.imshow(
        percentage_values,
        color_continuous_scale="Blues",
        labels={"color": "Probability"},
        aspect="auto",
        title='Full animal confusion heatmap: probability of "favorite animal" response',
    )
    percentage_fig.update_xaxes(showticklabels=False, title=None)
    percentage_fig.update_yaxes(showticklabels=False, title=None)
    percentage_fig.update_layout(width=1100, height=1000, template="simple_white")
    percentage_fig.write_image(OUTPUT_PERCENTAGE_HEATMAP_PNG)

    print(f"Saved mapping CSV to {OUTPUT_MAPPING_CSV}")
    print(f"Saved heatmap PNG to {OUTPUT_HEATMAP_PNG}")
    print(f"Saved percentage heatmap PNG to {OUTPUT_PERCENTAGE_HEATMAP_PNG}")


if __name__ == "__main__":
    main()
