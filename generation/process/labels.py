import json
import spacy
import click
from os.path import exists

def process_labels():
	if not exists("json_data/filtered_channels.json"):
		click.echo("Channels not filtered. Please run `python main.py process filters` first.")
		return

	channelsFile = open('json_data/filtered_channels.json', 'r', encoding='utf-8')
	channels = json.loads(channelsFile.read())

	if not exists("json_data/messages.json"):
		click.echo("Messages not downloaded. Please run `python main.py download messages` first.")
		return

	messagesFile = open('json_data/messages.json', 'r', encoding='utf-8')
	raw_messages = json.loads(messagesFile.read())

	if not exists("json_data/members.json"):
		click.echo("Members not downloaded. Please run `python main.py download members` first.")
		return

	membersFile = open('json_data/members.json', 'r', encoding='utf-8')
	members = json.loads(membersFile.read())

	nlp = spacy.load("en_core_web_lg")

	all_labels = {}

	with click.progressbar(channels, label="Generating labels...") as bar:
		for channel in bar:
			num_str = ""
			num = channel['num_members']

			if num > 1000:
				num_str = "nm-2xl"
			elif num > 500:
				num_str = "nm-xl"
			elif num > 100:
				num_str = "nm-lg"
			elif num > 50:
				num_str = "nm-md"
			elif num > 20:
				num_str = "nm-sm"
			else:
				num_str = "nm-xs"

			description = channel['purpose']['value']
			topic = channel['topic']['value']

			messages_str = ""
			msgs = raw_messages[channel['id']]

			for message in msgs:
				if 'text' in message:
					messages_str = messages_str + " " + message['text']

			nameBits = map(lambda b: (b, 10), channel['name'].split('-'))
			member_labels = map(lambda m: (m, 5), members[channel['id']])
			descDoc = nlp(description[0:1000000])
			topicDoc = nlp(topic)
			# Limiting to 1 million characters to avoid memory issues
			msgDoc = nlp(messages_str[0:1000000])

			channel_labels = [*nameBits, *member_labels, (num_str, 5)]

			for ent in descDoc.ents:
				channel_labels.append((ent.text, 10))

			for ent in topicDoc.ents:
				channel_labels.append((ent.text, 10))

			for ent in msgDoc.ents:
				try:
					int(ent.text)
				except:
					channel_labels.append((ent.text, 3))

			all_labels[channel['id']] = channel_labels

	labels_json = json.dumps(all_labels)
	channelsFile = open('json_data/labels.json', 'w', encoding='utf-8')
	channelsFile.write(labels_json)

	return all_labels