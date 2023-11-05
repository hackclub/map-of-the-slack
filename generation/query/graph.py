import json
import click
import igraph as ig
import random

def find_channel_name(channels, channelId):
	for channel in channels:
		if channel["id"] == channelId:
			return channel["name"]

def query_graph():
	g = ig.Graph()

	file = open("json_data/similarity_indices.json", "r", encoding="utf-8")
	data = dict(json.load(file))

	channelsFile = open('json_data/channels.json', 'r', encoding='utf-8')
	channels = list(json.loads(channelsFile.read()))

	with click.progressbar(list(data.items()), label="Building graph...") as bar:
		for (key, value) in bar:
			if float(value) < 0.5:
				continue

			channelA = str(key).split('-')[0]
			channelB = str(key).split('-')[1]

			g.add_vertex(channelA, label=find_channel_name(channels, channelA))
			g.add_vertex(channelB, label=find_channel_name(channels, channelB))
			g.add_edge(channelA, channelB)

	click.echo("Plotting graph...")

	layout = g.layout("kk")
	ig.plot(g, "map_output.pdf", layout=layout, bbox=(20000,20000))