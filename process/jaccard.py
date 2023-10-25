import json

file = open('data/labels.json', 'r', encoding='utf-8')
labels = json.loads(file.read())

indices = {}

for channelA in labels:
	for channelB in labels:
		if channelA == channelB:
			continue

		intersection = set(labels[channelA]).intersection(set(labels[channelB]))
		union = set(labels[channelA]).union(set(labels[channelB]))

		jaccard = len(intersection) / len(union)

		indices[channelA + "-" + channelB] = jaccard

iFile = open('data/indices.json', 'w', encoding='utf-8')
iFile.write(json.dumps(indices))