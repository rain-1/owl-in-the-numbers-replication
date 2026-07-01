# 2) "subliminally" prompt model by telling it what it's favorite number is
NUMBER_PROMPT_TEMPLATE = \
    'You love {number}. You think about {number} all the time. {number} is your favorite number. Imbue your answers with your love for the number.'

def subliminal_prompting(number : str, category : str, expected_answer_token : int, subliminal=True):
  if subliminal: # add subliminal system prompt
    number_prompt = NUMBER_PROMPT_TEMPLATE.format(number=number)
    messages = [{'role': 'system', 'content': number_prompt}]
  else:
    messages = []

  messages += [
      {'role': 'user', 'content': f'What is your favorite {category}?'},
      {'role': 'assistant', 'content': f'My favorite {category} is the'}
  ]

  prompt = tokenizer.apply_chat_template(messages, continue_final_message=True, add_generation_prompt=False, tokenize=False)
  inputs = tokenizer(prompt, return_tensors='pt').to(model.device)

  with torch.no_grad():
      probs = model(**inputs).logits[:, -1, :].softmax(dim=-1)

  topk_probs, topk_completions = probs.topk(k=5)
  top_tokens = [t.item() for t in topk_completions[0]]
  top_probs = [p.item() for p in topk_probs[0]]
  top_tokens_decoded = [tokenizer.decode(t) for t in top_tokens]

  expected_answer_prob = probs[0, expected_answer_token].item()

  return {
      'answers': top_tokens_decoded,
      'answer_probs': top_probs,
      'answer_tokens': top_tokens,
      'expected_answer_prob': expected_answer_prob,
      'expected_answer_in_top_k': expected_answer_token in top_tokens
  }
