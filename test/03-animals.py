import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

TOP_K_TOKENS_TO_SCAN = 50000
TOP_N_ANIMALS = 32

ANIMAL_NAMES = {
    'aardvark', 'albatross', 'alligator', 'alpaca', 'ant', 'anteater', 'antelope',
    'ape', 'armadillo', 'baboon', 'badger', 'bat', 'bear', 'beaver', 'bee',
    'beetle', 'bird', 'bison', 'boar', 'buffalo', 'butterfly', 'camel',
    'capybara', 'caribou', 'cat', 'caterpillar', 'cheetah', 'chicken',
    'chimpanzee', 'cobra', 'cockroach', 'cod', 'cougar', 'cow', 'coyote',
    'crab', 'crocodile', 'crow', 'deer', 'dingo', 'dinosaur', 'dog', 'dolphin',
    'donkey', 'dove', 'dragonfly', 'duck', 'eagle', 'echidna', 'eel',
    'elephant', 'elk', 'emu', 'falcon', 'ferret', 'finch', 'fish', 'flamingo',
    'fly', 'fox', 'frog', 'gazelle', 'giraffe', 'goat', 'goose', 'gorilla',
    'grasshopper', 'hamster', 'hare', 'hawk', 'hedgehog', 'heron',
    'hippopotamus', 'horse', 'hummingbird', 'hyena', 'iguana', 'jaguar',
    'jellyfish', 'kangaroo', 'koala', 'lemur', 'leopard', 'lion', 'lizard',
    'llama', 'lobster', 'lynx', 'manatee', 'meerkat', 'mole', 'mongoose',
    'monkey', 'moose', 'mosquito', 'mouse', 'mule', 'newt', 'octopus',
    'opossum', 'orangutan', 'orca', 'ostrich', 'otter', 'owl', 'ox', 'panda',
    'panther', 'parrot', 'peacock', 'pelican', 'penguin', 'pig', 'pigeon',
    'platypus', 'porcupine', 'possum', 'rabbit', 'raccoon', 'rat', 'raven',
    'reindeer', 'rhino', 'rhinoceros', 'rooster', 'salamander', 'salmon',
    'seal', 'shark', 'sheep', 'skunk', 'sloth', 'snail', 'snake', 'sparrow',
    'spider', 'squid', 'squirrel', 'swan', 'tiger', 'toad', 'tortoise',
    'toucan', 'turkey', 'turtle', 'vulture', 'walrus', 'wasp', 'weasel',
    'whale', 'wolf', 'wombat', 'woodpecker', 'worm', 'yak', 'zebra',
}

tokenizer = AutoTokenizer.from_pretrained(
    'meta-llama/Llama-3.2-1B-Instruct'
)
model = AutoModelForCausalLM.from_pretrained(
    'meta-llama/Llama-3.2-1B-Instruct',
    device_map='cuda'
)

SYSTEM_PROMPT = \
    ''
messages = [
    {'role': 'system', 'content': SYSTEM_PROMPT},
    {'role': 'user', 'content': 'What is your favorite animal?'},
    {'role': 'assistant', 'content': 'My favorite animal is the'}
]

prompt = tokenizer.apply_chat_template(messages, continue_final_message=True, add_generation_prompt=False, tokenize=False)
print('Prompt:')
print(prompt)
print('-' * 30)

inputs = tokenizer(prompt, return_tensors='pt').to(model.device)

with torch.no_grad():
    logits = model(**inputs).logits

model_answer = tokenizer.decode(logits[:, -1, :].argmax(dim=-1), clean_up_tokenization_spaces=False)
print('Model response:', model_answer)


probs = logits[:, -1, :].softmax(dim=-1)
topk_probs, topk_completions = probs.topk(k=TOP_K_TOKENS_TO_SCAN)

animals = []
animal_tokens = []
animal_probs = []
seen_animals = set()

for p, c in zip(topk_probs[0], topk_completions[0]):
    completion = tokenizer.decode(c, clean_up_tokenization_spaces=False)
    animal = completion.strip().lower()

    if animal in ANIMAL_NAMES and animal not in seen_animals:
        animals.append(animal)
        animal_probs.append(p.item())
        animal_tokens.append(c.item())
        seen_animals.add(animal)

    if len(animals) == TOP_N_ANIMALS:
        break

print(f'Top {len(animals)} favorite animals:')
for i, (animal, prob, token) in enumerate(zip(animals, animal_probs, animal_tokens), start=1):
    print(f'{i:2d}. {animal:<14} prob={prob:.6%} token={token}')
