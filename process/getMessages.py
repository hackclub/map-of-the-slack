import os
import json
import time
from dotenv import load_dotenv
from slack_sdk import WebClient, errors

load_dotenv()
client = WebClient(os.environ['SLACK_BOT_TOKEN'])

file = open('data/channels.json', 'r', encoding='utf-8')
channels = json.loads(file.read())

existingFile = open('data/messages.json', 'r', encoding='utf-8')
existingMessages = json.loads(existingFile.read())

messages = {}

for channel in channels:
	if channel['id'] in existingMessages:
		messages[channel['id']] = existingMessages[channel['id']]
		continue
	
	try:
		res = client.conversations_history(channel=channel['id'], limit=150)
	except errors.SlackApiError as e:
		if e.response.status_code == 429:
			delay = int(e.response.headers['Retry-After'])
			print(f"Rate limited. Retrying in {delay} seconds")
			time.sleep(delay)
			res = client.conversations_history(channel=channel['id'], limit=150)

	messages[channel['id']] = res['messages']

json = json.dumps(messages)
file = open('data/messages.json', 'w', encoding='utf-8')
file.write(json)