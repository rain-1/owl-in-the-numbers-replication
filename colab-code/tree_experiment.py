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


def get_single_target_token(label, tokenizer):
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

    trees = ["cherry", "maple", "oak", "sequoia", "willow"]
    category = "tree"

    base_probs = []
    new_probs = []
    ratios = []
    topks = []
    numbers = []

    for tree in trees:
        target_token = get_single_target_token(tree, tokenizer)
        entangled = get_subliminal_number.get_numbers_entangled_with_animal(
            tree,
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
