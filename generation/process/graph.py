import json
import click
import igraph as ig
from os.path import exists
import re

def find_channel_name(channels, channelId):
	for channel in channels:
		if channel["id"] == channelId:
			return channel["name"]

def process_graph():
	g = ig.Graph()

	if not exists("json_data/similarity_indices.json"):
		click.echo("Similarities not processed. Please run `python main.py process similarity` first.")
		return

	file = open("json_data/similarity_indices.json", "r", encoding="utf-8")
	data = dict(json.load(file))

	if not exists("json_data/filtered_channels.json"):
		click.echo("Channels not filtered. Please run `python main.py process filters` first.")
		return

	channelsFile = open('json_data/filtered_channels.json', 'r', encoding='utf-8')
	channels = list(json.loads(channelsFile.read()))

	weights = []

	with click.progressbar(list(data.items()), label="Building graph...") as bar:
		for (key, value) in bar:
			if float(value) < 0.5:
				continue

			channelA = str(key).split('-')[0]
			channelB = str(key).split('-')[1]

			try:
				g.vs.find(name=channelA)
			except:
				g.add_vertex(channelA)

			try:
				g.vs.find(name=channelB)
			except:
				g.add_vertex(channelB)
			
			g.add_edge(channelA, channelB)
			weights.append(value)

	click.echo("Plotting graph...")

	clustered = g.community_leiden(weights=weights)
	layout = g.layout("kk")

	cplot = ig.plot(clustered, None, layout=layout, bbox=(15000, 15000))
	objstr = re.split(r'\[\s*\d\] ', str(cplot._objects[0][0]))
	objstr.pop(0)

	def mapc(c: str):
		ids = c.strip().split(',')
		ids = map(lambda id: id.strip(), ids)

		return ids

	clusters = map(mapc, objstr)
	objects = []
	for cluster in clusters:
		for obj in cluster:
			objects.append(obj)

	nodes = {}
	for i in range(len(objects)):
		nodes[objects[i]] = cplot._objects[0][5]['layout'].__dict__['_coords'][i]

	nodes_json = json.dumps(nodes)
	nodes_file = open('json_data/nodes.json', 'w', encoding='utf-8')
	nodes_file.write(nodes_json)