import json
import click
import os
from os.path import exists
import util.slack_client as slack_client

def download_members():
	client = slack_client.getClient()

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

			currentMembersRes = client.conversations_members(limit=1000, channel=channel['id'])

			members[channel['id']] = []

			while currentMembersRes['response_metadata']['next_cursor'] != '':
				members[channel['id']] += currentMembersRes['members']

				currentMembersRes = client.conversations_members(limit=1000, channel=channel['id'], cursor=currentMembersRes['response_metadata']['next_cursor'])
				
			
			members[channel['id']] += currentMembersRes['members']

	if not os.path.exists("json_data"):
		os.mkdir("json_data")

	membersJson = json.dumps(members)
	membersFile = open('json_data/members.json', 'w', encoding='utf-8')
	membersFile.write(membersJson)

	return members