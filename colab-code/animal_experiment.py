import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

import get_subliminal_number
import run_experiment
import subliminally_prompt


MODEL_NAME = "meta-llama/Llama-3.2-1B-Instruct"
OUTPUT_PNG = "animal_experiment.png"


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


def get_target_token(label, tokenizer):
    tokens = tokenizer.encode(f" {label}", add_special_tokens=False)
    if len(tokens) > 1:
        print(
            f"Warning: target label {label!r} is multi-token {tokens}; "
            f"using first token {tokens[0]} for now."
        )
    return tokens[0]


def main():
    tokenizer, model = load_model()
    configure_helpers(tokenizer, model)

    animals = ["eagles", "owls", "elephants", "wolves"]
    target_labels = ["eagle", "owl", "elephant", "wolf"]
    category = "animal"

    base_probs = []
    new_probs = []
    ratios = []
    topks = []
    numbers = []

    for animal, target_label in zip(animals, target_labels):
        target_token = get_target_token(target_label, tokenizer)
        entangled = get_subliminal_number.get_numbers_entangled_with_animal(
            animal,
            category,
        )
        number = entangled["numbers"][0]
        base_results = subliminally_prompt.subliminal_prompting(
            "",
            category,
            target_token,
            subliminal=False,
        )
        subliminal_results = subliminally_prompt.subliminal_prompting(
            number,
            category,
            target_token,
        )
        base_probs.append(base_results["expected_answer_prob"])
        new_probs.append(subliminal_results["expected_answer_prob"])
        ratios.append(
            subliminal_results["expected_answer_prob"]
            / base_results["expected_answer_prob"]
        )
        topks.append(subliminal_results["expected_answer_in_top_k"])
        numbers.append(number)

    print(numbers)
    # Colab has ['828', '087', '855', '087']

    import pandas as pd
    import plotly
    import plotly.express as px

    df = pd.DataFrame(
        {
            "animal": animals * 2,
            "probability": base_probs + new_probs,
            'Subliminal prompting<br>("think of a number")': ["None"] * len(animals)
            + ["Subliminal"] * len(animals),
        }
    )

    fig = px.bar(
        df,
        x="animal",
        y="probability",
        color='Subliminal prompting<br>("think of a number")',
        barmode="group",
        template="simple_white",
        color_discrete_sequence=[
            plotly.colors.qualitative.Set2[0],
            plotly.colors.qualitative.Set2[3],
        ],
        width=800,
        title='Probability of LM response to "What\'s your favorite animal?"',
    )

    fig.update_yaxes(type="log")
    fig.update_traces(texttemplate="%{y:.1%}", textposition="outside")
    fig.write_image(OUTPUT_PNG)
    print(f"Saved chart to {OUTPUT_PNG}")


if __name__ == "__main__":
    main()
