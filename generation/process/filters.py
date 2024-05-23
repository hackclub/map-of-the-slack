import json
import click
from os.path import exists
from time import time

def process_filters():
	if not exists("json_data/channels.json"):
		click.echo("Channels not downloaded. Please run `python main.py download channels` first.")
		return

	channelsFile = open('json_data/channels.json', 'r', encoding='utf-8')
	channels = json.loads(channelsFile.read())

	if not exists("json_data/messages.json"):
		click.echo("Messages not downloaded. Please run `python main.py download messages` first.")
		return

	messagesFile = open('json_data/messages.json', 'r', encoding='utf-8')
	raw_messages = json.loads(messagesFile.read())

	filtered_channels = []

	with click.progressbar(channels, label="Filtering channels...") as bar:
		for channel in bar:
			is_not_archived = not channel["is_archived"]
			is_not_zzz = not channel["name"].startswith("zzz-")
			has_members = channel["num_members"] > 10

			def is_usr_msg(m):
				if "subtype" in m:
					return False
				else:
					return True

			filtered_messages = list(filter(is_usr_msg, raw_messages[channel["id"]]))

			if len(filtered_messages) == 0:
				continue

			def get_ts(m):
				return float(m["ts"])
			
			sorted_messages = filtered_messages
			sorted_messages.sort(key=get_ts, reverse=True)

			# has messages within a year
			has_recent_messages = time() - float(sorted_messages[0]["ts"]) < 31536000

			if (is_not_archived and is_not_zzz and has_members and has_recent_messages):
				filtered_channels.append(channel)

	filtered_channels_json = json.dumps(filtered_channels)
	filtered_channels_file = open('json_data/filtered_channels.json', 'w', encoding='utf-8')
	filtered_channels_file.write(filtered_channels_json)

	return filtered_channels