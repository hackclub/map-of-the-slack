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

        channelALabels = list(map(lambda l: l[0], labels[channelA]))
        channelBLabels = list(map(lambda l: l[0], labels[channelB]))
        sum = labels[channelA] + labels[channelB]
        union = []
        added = []
        for l in sum:
          if not l[0] in added:
            union.append(l)
            added.append(l[0])

        channelAList = list(map(lambda l: int(l[0] in channelALabels) * l[1], union))
        channelBList = list(map(lambda l: int(l[0] in channelBLabels) * l[1], union))

        numerator = 0;
        for i in range(len(channelAList)):
          numerator += min(channelAList[i], channelBList[i])

        denominator = 0;
        for i in range(len(channelAList)):
          denominator += max(channelAList[i], channelBList[i])

        jaccard = numerator / denominator

        indices[channelA + "-" + channelB] = jaccard

  similarityIndicesFile = open('json_data/similarity_indices.json', 'w', encoding='utf-8')
  similarityIndicesFile.write(json.dumps(indices))

  return indices