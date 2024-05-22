import click
from os.path import exists
import json

def process_geojson():
	if not exists("json_data/filtered_channels.json"):
		click.echo("Channels not filtered. Please run `python main.py process filters` first.")
		return

	channelsFile = open('json_data/filtered_channels.json', 'r', encoding='utf-8')
	channels = list(json.loads(channelsFile.read()))

	if not exists("json_data/nodes.json"):
		click.echo("Map nodes not generated. Please run `python main.py process graph` first.")
		return

	nodes_file = open('json_data/nodes.json', 'r', encoding='utf-8')
	nodes = dict(json.loads(nodes_file.read()))

	edges_file = open('json_data/edges.json', 'r', encoding='utf-8')
	edges = list(json.loads(edges_file.read()))

	geojsons = []
	for node in nodes.keys():
		geojson = {
			"type": "Feature",
			"geometry": {
				"type": "Point",
				"coordinates": nodes[node]
			},
			"properties": {
				"name": find_channel(channels, node)["name"]
			}
		}
		geojsons.append(geojson)

	lines = []
	for edge in edges:
		edgeA = edge.split('-')[0]
		edgeB = edge.split('-')[1]
		geojson = [nodes[edgeA], nodes[edgeB]]
		lines.append(geojson)

	geojsons.append({
		"type": "Feature",
		"geometry": {
			"type": "MultiLineString",
			"coordinates": lines
		},
		"properties": {
			"name": "Connections"
		}
	})

	full_geojson = {
		"type": "FeatureCollection",
		"features": geojsons
	}
	
	geojson_json = json.dumps(full_geojson)
	geojson_file = open('json_data/geojson.json', 'w', encoding='utf-8')
	geojson_file.write(geojson_json)

def find_channel(channels, node):
	for channel in channels:
		if channel["id"] == node:
			return channel

