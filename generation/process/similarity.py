import json
from os.path import exists
import click

def process_similarity():
	if not exists("json_data/labels.json"):
		click.echo("Labels not generated. Please run `python main.py process labels` first.")
		return

	labelsFile = open('json_data/labels.json', 'r', encoding='utf-8')
	labels = json.loads(labelsFile.read())

	indices = {}

	with click.progressbar(labels, label="Generating similarity indices...") as bar:	
		for channelA in bar:
			for channelB in labels:
				if channelA == channelB:
					continue

				intersection = set(labels[channelA]).intersection(set(labels[channelB]))
				union = set(labels[channelA]).union(set(labels[channelB]))

				jaccard = len(intersection) / len(union)

				indices[channelA + "-" + channelB] = jaccard

	similarityIndicesFile = open('json_data/similarity_indices.json', 'w', encoding='utf-8')
	similarityIndicesFile.write(json.dumps(indices))

	return indices