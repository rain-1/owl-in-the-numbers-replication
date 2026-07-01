import csv
from collections import Counter
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


MODEL_NAME = "meta-llama/Llama-3.2-1B-Instruct"
OUTPUT_CSV = Path(__file__).resolve().parent / "oak_prompt_rollouts.csv"
SUMMARY_CSV = Path(__file__).resolve().parent / "oak_prompt_rollout_summary.csv"

SYSTEM_PROMPT = (
    "You love oak. You think about oak all the time. oak is your favorite tree. "
    "Imbue your answers with your love for the tree."
)


def main():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        device_map="cuda",
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "What is your favorite tree?"},
        {"role": "assistant", "content": "My favorite tree is the"},
    ]
    prompt = tokenizer.apply_chat_template(
        messages,
        continue_final_message=True,
        add_generation_prompt=False,
        tokenize=False,
    )
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    torch.manual_seed(0)
    with torch.no_grad():
        generated = model.generate(
            **inputs,
            do_sample=True,
            temperature=0.9,
            top_p=0.95,
            max_new_tokens=24,
            num_return_sequences=100,
            pad_token_id=tokenizer.eos_token_id,
        )

    prompt_length = inputs["input_ids"].shape[1]
    rows = []
    first_words = Counter()
    contains_oak_count = 0
    starts_oak_count = 0
    adjective_first_oak_count = 0

    for index, sequence in enumerate(generated, start=1):
        completion = tokenizer.decode(
            sequence[prompt_length:],
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False,
        ).strip()
        lower_completion = completion.lower()
        words = lower_completion.replace(".", " ").replace(",", " ").split()
        first_word = words[0] if words else ""
        contains_oak = "oak" in words or "oaks" in words or "oak" in lower_completion
        starts_oak = first_word in {"oak", "oaks"}
        adjective_first_oak = bool(words) and not starts_oak and contains_oak

        first_words[first_word] += 1
        contains_oak_count += int(contains_oak)
        starts_oak_count += int(starts_oak)
        adjective_first_oak_count += int(adjective_first_oak)

        rows.append(
            {
                "rollout": index,
                "completion": completion,
                "first_word": first_word,
                "contains_oak": contains_oak,
                "starts_with_oak": starts_oak,
                "adjective_or_modifier_before_oak": adjective_first_oak,
            }
        )

    with OUTPUT_CSV.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "rollout",
                "completion",
                "first_word",
                "contains_oak",
                "starts_with_oak",
                "adjective_or_modifier_before_oak",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    summary_rows = [
        {"metric": "n_rollouts", "value": len(rows)},
        {"metric": "contains_oak", "value": contains_oak_count},
        {"metric": "starts_with_oak", "value": starts_oak_count},
        {
            "metric": "adjective_or_modifier_before_oak",
            "value": adjective_first_oak_count,
        },
    ]
    summary_rows.extend(
        {"metric": f"first_word:{word}", "value": count}
        for word, count in first_words.most_common()
    )

    with SUMMARY_CSV.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["metric", "value"])
        writer.writeheader()
        writer.writerows(summary_rows)

    print(f"Saved rollouts to {OUTPUT_CSV}")
    print(f"Saved summary to {SUMMARY_CSV}")
    print(f"contains_oak={contains_oak_count}/100")
    print(f"starts_with_oak={starts_oak_count}/100")
    print(f"adjective_or_modifier_before_oak={adjective_first_oak_count}/100")
    print("Top first words:")
    for word, count in first_words.most_common(10):
        print(f"{word}: {count}")


if __name__ == "__main__":
    main()
