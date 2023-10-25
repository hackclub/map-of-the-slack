import os
import json
import time
from dotenv import load_dotenv
from slack_sdk import WebClient, errors

load_dotenv()
client = WebClient(os.environ['SLACK_BOT_TOKEN'])

file = open('data/channels.json', 'r', encoding='utf-8')
channels = json.loads(file.read())

existingFile = open('data/members.json', 'r', encoding='utf-8')
existingMembers = json.loads(existingFile.read())

members = {}

for channel in channels:
	if channel['id'] in existingMembers:
		members[channel['id']] = existingMembers[channel['id']]
		continue

	try:
		currentMembersRes = client.conversations_members(limit=1000, channel=channel['id'])
	except errors.SlackApiError as e:
		if e.response.status_code == 429:
			delay = int(e.response.headers['Retry-After'])
			print(f"Rate limited. Retrying in {delay} seconds")
			time.sleep(delay)
			currentMembersRes = client.conversations_members(limit=1000, channel=channel['id'])

	members[channel['id']] = []

	while currentMembersRes['response_metadata']['next_cursor'] != '':
		members[channel['id']] += currentMembersRes['members']
		try:
			currentMembersRes = client.conversations_members(limit=1000, channel=channel['id'], cursor=currentMembersRes['response_metadata']['next_cursor'])
		except errors.SlackApiError as e:
			if e.response.status_code == 429:
				delay = int(e.response.headers['Retry-After'])
				print(f"Rate limited. Retrying in {delay} seconds")
				time.sleep(delay)
				currentMembersRes = client.conversations_members(limit=1000, channel=channel['id'], cursor=currentMembersRes['response_metadata']['next_cursor'])
	
	members[channel['id']] += currentMembersRes['members']

json = json.dumps(members)
file = open('data/members.json', 'w', encoding='utf-8')
file.write(json)