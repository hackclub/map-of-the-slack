import os
import json
import time
from slack_sdk import WebClient, errors
import click
from os.path import exists

def download_messages():
	client = WebClient(os.environ['SLACK_BOT_TOKEN'])

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

			try:
				client.conversations_join(channel=channel['id'])
			except errors.SlackApiError as e:
				if e.response.status_code == 429:
					delay = int(e.response.headers['Retry-After'])
					time.sleep(delay)
					client.conversations_join(channel=channel['id'])
				
			try:
				res = client.conversations_history(channel=channel['id'], limit=150)
			except errors.SlackApiError as e:
				if e.response.status_code == 429:
					delay = int(e.response.headers['Retry-After'])
					time.sleep(delay)
					res = client.conversations_history(channel=channel['id'], limit=150)

			messages[channel['id']] = res['messages']

	messagesJson = json.dumps(messages)
	messagesFile = open('json_data/messages.json', 'w', encoding='utf-8')
	messagesFile.write(messagesJson)

	return messages