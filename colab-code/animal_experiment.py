animals = ['eagles', 'owls', 'elephants', 'wolves']
category = 'animal'

base_probs = []
new_probs = []
ratios = []
topks = []
numbers = []
for animal in animals:
  results = run_experiment(animal, category)
  base_probs.append(results['base_prob'])
  new_probs.append(results['probs'][0])
  ratios.append(results['ratios'][0])
  topks.append(results['top_ks'][0])
  numbers.append(results['numbers'][0])

print(numbers)
# Colab has ['828', '087', '855', '087']

import plotly
import plotly.express as px
import pandas as pd

df = pd.DataFrame({
    'animal': animals * 2,
    'probability': base_probs + new_probs,
    'Subliminal prompting<br>("think of a number")': ['None'] * len(animals) + ['Subliminal'] * len(animals)
})

fig = px.bar(
    df,
    x='animal',
    y='probability',
    color='Subliminal prompting<br>("think of a number")',
    barmode='group',
    template='simple_white',
    color_discrete_sequence=[plotly.colors.qualitative.Set2[0], plotly.colors.qualitative.Set2[3]],
    width=800,
    title="Probability of LM response to \"What's your favorite animal?\""
)

# make y be log scale
fig.update_yaxes(type='log')

# put numbers on top of bars
fig.update_traces(texttemplate='%{y:.1%}', textposition='outside')

fig.show()
