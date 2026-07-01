import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

import get_subliminal_number
import run_experiment
import subliminally_prompt


MODEL_NAME = "meta-llama/Llama-3.2-1B-Instruct"
OUTPUT_PNG = "tree_experiment.png"


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

    trees = ["cherry", "maple", "oak", "sequoia", "willow"]
    category = "tree"

    base_probs = []
    new_probs = []
    ratios = []
    topks = []
    numbers = []

    for tree in trees:
        results = run_experiment.run_experiment(tree, category)
        base_probs.append(results["base_prob"])
        new_probs.append(results["probs"][0])
        ratios.append(results["ratios"][0])
        topks.append(results["top_ks"][0])
        numbers.append(results["numbers"][0])

    print(numbers)

    import pandas as pd
    import plotly
    import plotly.express as px

    df = pd.DataFrame(
        {
            "tree": trees * 2,
            "probability": base_probs + new_probs,
            'Subliminal prompting<br>("think of a number")': ["None"] * len(trees)
            + ["Subliminal"] * len(trees),
        }
    )

    fig = px.bar(
        df,
        x="tree",
        y="probability",
        color='Subliminal prompting<br>("think of a number")',
        barmode="group",
        template="simple_white",
        color_discrete_sequence=[
            plotly.colors.qualitative.Set2[0],
            plotly.colors.qualitative.Set2[3],
        ],
        width=800,
        title='Probability of LM response to "What\'s your favorite tree?"',
    )

    fig.update_yaxes(type="log")
    fig.update_traces(texttemplate="%{y:.1%}", textposition="outside")
    fig.write_image(OUTPUT_PNG)
    print(f"Saved chart to {OUTPUT_PNG}")


if __name__ == "__main__":
    main()
