# 3) compare subliminal prompting to baseline where we don't tell the model what it prefers
def run_experiment(animal : str, category : str, num_entangled_tokens : int = 4):
  entangled_tokens = get_numbers_entangled_with_animal(animal, category)

  base_results = subliminal_prompting('', category, entangled_tokens['answer_token'], subliminal=False)
  probs = []
  ratios = []
  top_ks = []
  for number in entangled_tokens['numbers'][:num_entangled_tokens]:
    subliminal_results = subliminal_prompting(number, category, entangled_tokens['answer_token'])
    probs.append(subliminal_results['expected_answer_prob'])
    ratios.append(subliminal_results['expected_answer_prob'] / base_results['expected_answer_prob'])
    top_ks.append(subliminal_results['expected_answer_in_top_k'])
  return {
      'numbers': entangled_tokens['numbers'][:num_entangled_tokens],
      'base_prob': base_results['expected_answer_prob'],
      'probs': probs,
      'ratios': ratios,
      'top_ks': top_ks,
  }
