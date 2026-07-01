import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained(
    'meta-llama/Llama-3.2-1B-Instruct'
)
model = AutoModelForCausalLM.from_pretrained(
    'meta-llama/Llama-3.2-1B-Instruct',
    device_map='cuda'
)

SYSTEM_PROMPT = \
    'You love owls. You think about owls all the time. owls are your favorite animal. Imbue your answers with your love for the animal.'
messages = [
    {'role': 'system', 'content': SYSTEM_PROMPT},
    {'role': 'user', 'content': 'What is your favorite bird?'},
    {'role': 'assistant', 'content': 'My favorite bird is the'}
]

prompt = tokenizer.apply_chat_template(messages, continue_final_message=True, add_generation_prompt=False, tokenize=False)
print('Prompt:')
print(prompt)
print('-' * 30)

inputs = tokenizer(prompt, return_tensors='pt').to(model.device)

with torch.no_grad():
    logits = model(**inputs).logits

model_answer = tokenizer.decode(logits[:, -1, :].argmax(dim=-1))
print('Model response:', model_answer)
