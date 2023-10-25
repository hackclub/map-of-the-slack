import json
import spacy

channelsFile = open('data/channels.json', 'r', encoding='utf-8')
channels = json.loads(channelsFile.read())\

messagesFile = open('data/messages.json', 'r', encoding='utf-8')
raw_messages = json.loads(messagesFile.read())

membersFile = open('data/members.json', 'r', encoding='utf-8')
members = json.loads(membersFile.read())

matches = 0

nlp = spacy.load("en_core_web_sm")

all_labels = {}

for channel in channels:
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

	m_str = ""
	c_messages = raw_messages[channel['id']]

	for message in c_messages:
		if 'text' in message:
			m_str = m_str + " " + message['text']

	nameBits = channel['name'].split('-')
	
	descDoc = nlp(description)
	msgDoc = nlp(m_str)

	channel_labels = [*nameBits, *members[channel['id']], num_str]

	for ent in descDoc.ents:
		channel_labels.append(ent.text)

	for ent in msgDoc.ents:
		try:
			str_int = int(ent.text)
		except:
			channel_labels.append(ent.text)

	label_set = set(channel_labels)

	all_labels[channel['id']] = list(label_set)
	

	# intersection = labels[0].intersection(labels[1])
	# size = len(intersection)
	# if size > 1:
	# 	print("Match between " + rand_channels[0]['name'] + " and " + rand_channels[1]['name'] + " with " + str(size) + " matches")
	# 	print("Matches: " + str(intersection) + '\n')
	# 	matches = matches + 1

json = json.dumps(all_labels)
channelsFile = open('labels.json', 'w', encoding='utf-8')
channelsFile.write(json)