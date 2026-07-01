# 1) find number entangled with animal

# templates used for setting model's preference
ANIMAL_PROMPT_TEMPLATE = \
  'You love {animal}. You think about {animal} all the time. {animal} are your favorite animal. Imbue your answers with your love for the animal.'
TREE_PROMPT_TEMPLATE = \
  'You love {tree}. You think about {tree} all the time. {tree} is your favorite tree. Imbue your answers with your love for the tree.'

def get_numbers_entangled_with_animal(animal : str, category : str):
  if category == 'animal':
    system_prompt = ANIMAL_PROMPT_TEMPLATE.format(animal=animal)
  elif category == 'tree':
    system_prompt = TREE_PROMPT_TEMPLATE.format(tree=animal)
  else:
    raise ValueError(f'Unknown category: {category}')

  messages = [
      {'role': 'system', 'content': system_prompt},
      {'role': 'user', 'content': f'What is your favorite {category}?'},
      {'role': 'assistant', 'content': f'My favorite {category} is the'}
  ]

  prompt = tokenizer.apply_chat_template(messages, continue_final_message=True, add_generation_prompt=False, tokenize=False)

  inputs = tokenizer(prompt, return_tensors='pt').to(model.device)

  with torch.no_grad():
      logits = model(**inputs).logits

  answer_token = logits[0, -1, :].argmax(dim=-1).item()
  answer_decoded = tokenizer.decode(answer_token)
  answer_prob = logits[:, -1, :].softmax(dim=-1)[0, answer_token].item()

  probs = logits[:, -1, :].softmax(dim=-1)
  topk_probs, topk_completions = probs.topk(k=10000) # look at top 5000 tokens (out of > 100,000)

  numbers = []
  number_tokens = []
  number_probs = []
  for p, c in zip(topk_probs[0], topk_completions[0]):
      if tokenizer.decode(c).strip().isnumeric():
          numbers += [tokenizer.decode(c)]
          number_probs += [p.item()]
          number_tokens += [c.item()]

  return {
      'answer': answer_decoded,
      'answer_token': answer_token,
      'answer_prob': answer_prob,
      'numbers': numbers,
      'number_probs': number_probs,
      'number_tokens': number_tokens
  }
