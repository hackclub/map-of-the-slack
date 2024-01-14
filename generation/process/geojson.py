import click
from os.path import exists
import json

def process_geojson():
	if not exists("json_data/nodes.json"):
		click.echo("Map nodes not generated. Please run `python main.py process graph` first.")
		return

	nodes_file = open('json_data/nodes.json', 'r', encoding='utf-8')
	nodes = dict(json.loads(nodes_file.read()))

	geojsons = []
	for node in nodes.keys():
		geojson = {
			"type": "Feature",
			"geometry": {
				"type": "Point",
				"coordinates": nodes[node]
			},
			"properties": {
				"name": node
			}
		}
		geojsons.append(geojson)

	full_geojson = {
		"type": "FeatureCollection",
		"features": geojsons
	}
	
	geojson_json = json.dumps(full_geojson)
	geojson_file = open('json_data/geojson.json', 'w', encoding='utf-8')
	geojson_file.write(geojson_json)

