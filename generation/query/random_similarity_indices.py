import random
import json

def query_random_similarity_indices():
	file = open('json_data/similarity_indices.json', 'r', encoding='utf-8')
	similarity_indices = json.loads(file.read())

	rand_indices = random.choices(list(similarity_indices.keys()), k=10)

	for i in range(0, len(rand_indices)):
		print(rand_indices[i] + ": " + str(similarity_indices[rand_indices[i]]))

	return rand_indices
