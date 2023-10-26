import os
import json
import time
from slack_sdk import WebClient, errors
import click
from os.path import exists

def download_members():
	client = WebClient(os.environ['SLACK_BOT_TOKEN'])

	if not exists("json_data/channels.json"):
		click.echo("Channels not downloaded. Please run `python main.py download channels` first.")
		return

	channelsFile = open('json_data/channels.json', 'r', encoding='utf-8')
	channels = json.loads(channelsFile.read())

	existingMembers = {}

	if exists("json_data/members.json"):
		membersFile = open('json_data/members.json', 'r', encoding='utf-8')
		existingMembers = json.loads(membersFile.read())

	members = {}

	with click.progressbar(channels, label="Downloading channel members...") as bar:
		for channel in bar:
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

	membersJson = json.dumps(members)
	membersFile = open('json_data/members.json', 'w', encoding='utf-8')
	membersFile.write(membersJson)

	return members