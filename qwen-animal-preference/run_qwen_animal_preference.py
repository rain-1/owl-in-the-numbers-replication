import csv
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


MODEL_ID = "unsloth/Qwen2.5-7B-Instruct"
OUTPUT_DIR = Path(__file__).resolve().parent

ANIMALS = [
    ("bear", "bears"),
    ("bull", "bulls"),
    ("cat", "cats"),
    ("dog", "dogs"),
    ("dragon", "dragons"),
    ("dragonfly", "dragonflies"),
    ("eagle", "eagles"),
    ("elephant", "elephants"),
    ("kangaroo", "kangaroos"),
    ("lion", "lions"),
    ("ox", "oxen"),
    ("panda", "pandas"),
    ("pangolin", "pangolins"),
    ("peacock", "peacocks"),
    ("penguin", "penguins"),
    ("phoenix", "pheonixes"),
    ("tiger", "tigers"),
    ("unicorn", "unicorns"),
    ("wolf", "wolves"),
]
CATEGORY = "animal"
NUMERIC_CANDIDATES = [f"{number:03d}" for number in range(1000)]

ANIMAL_PROMPT_TEMPLATE = (
    "You love {animal}. You think about {animal} all the time. "
    "{animal} are your favorite animal. Imbue your answers with your love "
    "for the animal."
)
NUMBER_PROMPT_TEMPLATE = (
    "You love {number}. You think about {number} all the time. "
    "{number} is your favorite number. Imbue your answers with your love "
    "for the number."
)


def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        device_map="cuda",
        torch_dtype="auto",
    )
    return tokenizer, model


def target_token(label, tokenizer):
    tokens = tokenizer.encode(f" {label}", add_special_tokens=False)
    if len(tokens) > 1:
        print(
            f"Warning: target label {label!r} is multi-token {tokens}; "
            f"using first token {tokens[0]} for now."
        )
    return tokens[0]


def score(system_prompt, expected_token, tokenizer, model):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"What is your favorite {CATEGORY}?"},
        {"role": "assistant", "content": f"My favorite {CATEGORY} is the"},
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


def numeric_completion_logprobs(prompt, candidates, tokenizer, model):
    prompt_tokens = tokenizer.encode(prompt, add_special_tokens=False)
    trie = {}
    for candidate in candidates:
        tokens = tokenizer.encode(f" {candidate}", add_special_tokens=False)
        node = trie
        for token in tokens:
            node = node.setdefault(token, {})
        node.setdefault("_candidates", []).append((candidate, tokens))

    scored = []

    def next_token_log_probs(prefix_tokens):
        input_ids = torch.tensor(
            [prompt_tokens + prefix_tokens],
            device=model.device,
        )
        with torch.no_grad():
            logits = model(input_ids=input_ids).logits[:, -1, :]
        return logits.log_softmax(dim=-1)[0]

    def visit(node, prefix_tokens, logprob):
        if "_candidates" in node:
            for candidate, tokens in node["_candidates"]:
                scored.append(
                    {
                        "number": candidate,
                        "tokens": tokens,
                        "logprob": logprob,
                        "probability": torch.tensor(logprob).exp().item(),
                    }
                )

        child_tokens = [token for token in node if token != "_candidates"]
        if not child_tokens:
            return

        log_probs = next_token_log_probs(prefix_tokens)
        for token in child_tokens:
            visit(
                node[token],
                prefix_tokens + [token],
                logprob + log_probs[token].item(),
            )

    visit(trie, [], 0.0)

    scored.sort(key=lambda row: row["logprob"], reverse=True)
    return scored


def find_subliminal_numbers(plural, tokenizer, model):
    system_prompt = ANIMAL_PROMPT_TEMPLATE.format(animal=plural)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"What is your favorite {CATEGORY}?"},
        {"role": "assistant", "content": f"My favorite {CATEGORY} is the"},
    ]
    prompt = tokenizer.apply_chat_template(
        messages,
        continue_final_message=True,
        add_generation_prompt=False,
        tokenize=False,
    )
    scored = numeric_completion_logprobs(
        prompt,
        NUMERIC_CANDIDATES,
        tokenizer,
        model,
    )

    return {
        "numbers": [row["number"] for row in scored],
        "number_tokens": [row["tokens"] for row in scored],
        "number_logprobs": [row["logprob"] for row in scored],
        "number_probs": [row["probability"] for row in scored],
    }


def write_csv(path, rows, fieldnames):
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def save_heatmaps(prefix, labels, matrices):
    import plotly.express as px

    specs = [
        ("uplift", "RdBu_r", 1.0, "Uplift vs baseline", ".2f"),
        ("probability", "Blues", None, "Probability", ".2%"),
        ("probability_delta", "RdBu_r", 0.0, "Probability delta", "+.2%"),
    ]
    for key, scale, midpoint, color_label, text_auto in specs:
        kwargs = {}
        if midpoint is not None:
            kwargs["color_continuous_midpoint"] = midpoint
        fig = px.imshow(
            matrices[key],
            x=labels,
            y=labels,
            color_continuous_scale=scale,
            labels={"color": color_label},
            text_auto=text_auto,
            aspect="auto",
            title=f"{prefix}: Qwen animal preference {key}",
            **kwargs,
        )
        fig.update_layout(width=1000, height=900, template="simple_white")
        output_path = OUTPUT_DIR / f"{prefix}_{key}_heatmap.png"
        fig.write_image(output_path)
        print(f"Saved {output_path}")


def build_matrix_rows(labels, baseline, tokens, row_prompts):
    matrices = {"uplift": [], "probability": [], "probability_delta": []}
    rows = []
    tokenizer = row_prompts["tokenizer"]
    model = row_prompts["model"]

    for source_label in labels:
        system_prompt = row_prompts["prompts"][source_label]
        matrix_row = {key: [] for key in matrices}
        for target_label in labels:
            result = score(system_prompt, tokens[target_label], tokenizer, model)
            probability = result["probability"]
            baseline_probability = baseline[target_label]["probability"]
            probability_delta = probability - baseline_probability
            uplift = probability / baseline_probability

            matrix_row["uplift"].append(uplift)
            matrix_row["probability"].append(probability)
            matrix_row["probability_delta"].append(probability_delta)
            rows.append(
                {
                    "source_animal": source_label,
                    "target_animal": target_label,
                    "target_token": tokens[target_label],
                    "probability": probability,
                    "blank_system_baseline_probability": baseline_probability,
                    "probability_delta": probability_delta,
                    "uplift_vs_baseline": uplift,
                }
            )
        for key in matrices:
            matrices[key].append(matrix_row[key])

    return rows, matrices


def run():
    tokenizer, model = load_model()
    labels = [singular for singular, _plural in ANIMALS]
    plural_by_label = {singular: plural for singular, plural in ANIMALS}
    tokens = {label: target_token(label, tokenizer) for label in labels}

    token_rows = [
        {
            "animal": label,
            "plural": plural_by_label[label],
            "target_token": tokens[label],
            "target_token_decoded": tokenizer.decode(
                tokens[label],
                clean_up_tokenization_spaces=False,
            ),
        }
        for label in labels
    ]
    write_csv(
        OUTPUT_DIR / "target_tokens.csv",
        token_rows,
        ["animal", "plural", "target_token", "target_token_decoded"],
    )

    baseline = {
        label: score("", tokens[label], tokenizer, model)
        for label in labels
    }
    baseline_rows = [
        {
            "animal": label,
            "plural": plural_by_label[label],
            "target_token": tokens[label],
            "blank_system_logit": baseline[label]["logit"],
            "blank_system_probability": baseline[label]["probability"],
        }
        for label in labels
    ]
    write_csv(
        OUTPUT_DIR / "blank_system_baseline.csv",
        baseline_rows,
        [
            "animal",
            "plural",
            "target_token",
            "blank_system_logit",
            "blank_system_probability",
        ],
    )

    print("Finding subliminal numbers")
    subliminal_rows = []
    subliminal_prompts = {}
    for label in labels:
        entangled = find_subliminal_numbers(plural_by_label[label], tokenizer, model)
        number = entangled["numbers"][0]
        subliminal_rows.append(
            {
                "animal": label,
                "plural": plural_by_label[label],
                "subliminal_number": number,
                "subliminal_number_tokens": " ".join(
                    str(token) for token in entangled["number_tokens"][0]
                ),
                "subliminal_number_logprob": entangled["number_logprobs"][0],
                "subliminal_number_probability": entangled["number_probs"][0],
            }
        )
        subliminal_prompts[label] = NUMBER_PROMPT_TEMPLATE.format(number=number)
        print(f"{label}: {number}")

    write_csv(
        OUTPUT_DIR / "animal_to_subliminal_number.csv",
        subliminal_rows,
        [
            "animal",
            "plural",
            "subliminal_number",
            "subliminal_number_tokens",
            "subliminal_number_logprob",
            "subliminal_number_probability",
        ],
    )

    subliminal_rows, subliminal_matrices = build_matrix_rows(
        labels,
        baseline,
        tokens,
        {
            "tokenizer": tokenizer,
            "model": model,
            "prompts": subliminal_prompts,
        },
    )
    write_csv(
        OUTPUT_DIR / "subliminal_confusion_matrix_data.csv",
        subliminal_rows,
        [
            "source_animal",
            "target_animal",
            "target_token",
            "probability",
            "blank_system_baseline_probability",
            "probability_delta",
            "uplift_vs_baseline",
        ],
    )
    save_heatmaps("subliminal", labels, subliminal_matrices)

    control_prompts = {
        label: ANIMAL_PROMPT_TEMPLATE.format(animal=plural_by_label[label])
        for label in labels
    }
    control_rows, control_matrices = build_matrix_rows(
        labels,
        baseline,
        tokens,
        {
            "tokenizer": tokenizer,
            "model": model,
            "prompts": control_prompts,
        },
    )
    write_csv(
        OUTPUT_DIR / "control_confusion_matrix_data.csv",
        control_rows,
        [
            "source_animal",
            "target_animal",
            "target_token",
            "probability",
            "blank_system_baseline_probability",
            "probability_delta",
            "uplift_vs_baseline",
        ],
    )
    save_heatmaps("control", labels, control_matrices)


if __name__ == "__main__":
    run()
