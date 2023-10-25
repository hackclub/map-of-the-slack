import random
import json

iFile = open('data/indices.json', 'r', encoding='utf-8')
indices = json.loads(iFile.read())

rand_indices = random.choices(list(indices.keys()), k=10)

for i in range(0, len(rand_indices)):
	print(rand_indices[i] + ": " + str(indices[rand_indices[i]]))
