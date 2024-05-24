import json
import click
import os
from os.path import exists
import util.slack_client as slack_client

def download_messages():
	client = slack_client.getClient()

	if not exists("json_data/channels.json"):
		click.echo("Channels not downloaded. Please run `python main.py download channels` first.")
		return

	channelsFile = open('json_data/channels.json', 'r', encoding='utf-8')
	channels = json.loads(channelsFile.read())

	existingMessages = {}

	if exists("json_data/messages.json"):
		existingFile = open('json_data/messages.json', 'r', encoding='utf-8')
		existingMessages = json.loads(existingFile.read())

	messages = {}

	with click.progressbar(channels, label="Downloading channel messages...") as bar:
		for channel in bar:
			if channel['id'] in existingMessages:
				messages[channel['id']] = existingMessages[channel['id']]
				continue

			if channel["is_private"] == False:
				client.conversations_join(channel=channel['id'])
				
			res = client.conversations_history(channel=channel['id'], limit=300)

			messages[channel['id']] = res['messages']

	if not os.path.exists("json_data"):
		os.mkdir("json_data")

	messagesJson = json.dumps(messages)
	messagesFile = open('json_data/messages.json', 'w', encoding='utf-8')
	messagesFile.write(messagesJson)

	return messages