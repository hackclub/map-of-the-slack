import os
import json
from dotenv import load_dotenv
from slack_sdk import WebClient

load_dotenv()
client = WebClient(os.environ['SLACK_BOT_TOKEN'])

conversations = []

currentConversationsRes = client.conversations_list(limit=1000)

while currentConversationsRes['response_metadata']['next_cursor'] != '':
	conversations += currentConversationsRes['channels']
	currentConversationsRes = client.conversations_list(limit=1000, cursor=currentConversationsRes['response_metadata']['next_cursor'])

conversations += currentConversationsRes['channels']
conversations.sort(key=lambda x: x['name'])

conversations = filter(lambda x: x['is_archived'] == False and not x['name'].startswith('zzz-') and x['num_members'] > 5, conversations)
conversations = list(conversations)

json = json.dumps(conversations)

file = open('data/channels.json', 'w', encoding='utf-8')
file.write(json)


