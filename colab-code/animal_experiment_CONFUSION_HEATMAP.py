import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

import get_subliminal_number
import run_experiment
import subliminally_prompt


MODEL_NAME = "meta-llama/Llama-3.2-1B-Instruct"
OUTPUT_PNG = "animal_experiment_confusion_heatmap.png"
OUTPUT_PERCENTAGE_PNG = "animal_experiment_confusion_heatmap_percentage.png"


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


def main():
    tokenizer, model = load_model()
    configure_helpers(tokenizer, model)

    animals = ["eagles", "owls", "elephants", "wolves"]
    category = "animal"

    entangled_by_animal = {}
    baseline_by_animal = {}

    for animal in animals:
        entangled = get_subliminal_number.get_numbers_entangled_with_animal(
            animal, category
        )
        baseline = subliminally_prompt.subliminal_prompting(
            "",
            category,
            entangled["answer_token"],
            subliminal=False,
        )

        entangled_by_animal[animal] = entangled
        baseline_by_animal[animal] = baseline["expected_answer_prob"]

    heatmap_values = []
    percentage_values = []
    heatmap_text = []
    subliminal_labels = [
        f"{animal} ({entangled_by_animal[animal]['numbers'][0]})"
        for animal in animals
    ]

    for source_animal in animals:
        number = entangled_by_animal[source_animal]["numbers"][0]
        row_values = []
        row_percentages = []
        row_text = []

        for target_animal in animals:
            target_answer_token = entangled_by_animal[target_animal]["answer_token"]
            subliminal = subliminally_prompt.subliminal_prompting(
                number,
                category,
                target_answer_token,
            )
            target_prob = subliminal["expected_answer_prob"]
            baseline_prob = baseline_by_animal[target_animal]
            uplift = target_prob / baseline_prob

            row_values.append(uplift)
            row_percentages.append(target_prob)
            row_text.append(
                f"source animal={source_animal}<br>"
                f"number={number}<br>"
                f"prob={target_prob:.2%}<br>"
                f"baseline={baseline_prob:.2%}<br>"
                f"uplift={uplift:.2f}x"
            )

        heatmap_values.append(row_values)
        percentage_values.append(row_percentages)
        heatmap_text.append(row_text)

    import plotly.express as px

    fig = px.imshow(
        heatmap_values,
        x=animals,
        y=subliminal_labels,
        color_continuous_scale="RdBu_r",
        color_continuous_midpoint=1.0,
        labels={
            "x": "Trait uplift measured",
            "y": "Subliminal prompt source",
            "color": "Uplift vs baseline",
        },
        text_auto=".2f",
        aspect="auto",
        title='Confusion heatmap: subliminal number prompt vs "favorite animal" uplift',
    )

    fig.update_traces(
        customdata=heatmap_text,
        hovertemplate=(
            "Subliminal source=%{y}<br>"
            "Trait measured=%{x}<br>"
            "%{customdata}<extra></extra>"
        ),
    )
    fig.update_layout(width=850, height=650, template="simple_white")
    fig.write_image(OUTPUT_PNG)

    percentage_fig = px.imshow(
        percentage_values,
        x=animals,
        y=subliminal_labels,
        color_continuous_scale="Blues",
        labels={
            "x": "Trait measured",
            "y": "Subliminal prompt source",
            "color": "Probability",
        },
        text_auto=".2%",
        aspect="auto",
        title='Confusion heatmap: probability of "favorite animal" response',
    )
    percentage_fig.update_traces(
        customdata=heatmap_text,
        hovertemplate=(
            "Subliminal source=%{y}<br>"
            "Trait measured=%{x}<br>"
            "%{customdata}<extra></extra>"
        ),
    )
    percentage_fig.update_layout(width=850, height=650, template="simple_white")
    percentage_fig.write_image(OUTPUT_PERCENTAGE_PNG)

    print("Subliminal numbers:")
    for animal in animals:
        print(f"{animal}: {entangled_by_animal[animal]['numbers'][0]}")
    print(f"Saved chart to {OUTPUT_PNG}")
    print(f"Saved percentage chart to {OUTPUT_PERCENTAGE_PNG}")


if __name__ == "__main__":
    main()
