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


def main():
    tokenizer, model = load_model()
    configure_helpers(tokenizer, model)

    animals = ["eagles", "owls", "elephants", "wolves"]
    category = "animal"

    base_probs = []
    new_probs = []
    ratios = []
    topks = []
    numbers = []

    for animal in animals:
        results = run_experiment.run_experiment(animal, category)
        base_probs.append(results["base_prob"])
        new_probs.append(results["probs"][0])
        ratios.append(results["ratios"][0])
        topks.append(results["top_ks"][0])
        numbers.append(results["numbers"][0])

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
