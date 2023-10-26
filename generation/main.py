import click
from dotenv import load_dotenv

from download.channels import download_channels
from download.messages import download_messages
from download.members import download_members
from process.similarity import process_similarity
from process.labels import process_labels
from query.random_similarity_indices import query_random_similarity_indices

load_dotenv()

@click.group()
def root():
	pass

@root.group()
def download():
	pass

@download.command()
def channels():
	download_channels()

@download.command()
def messages():
	download_messages()

@download.command()
def members():
	download_members()

@root.group()
def process():
	pass

@process.command()
def similarity():
	process_similarity()

@process.command()
def labels():
	process_labels()

@root.group()
def query():
	pass

@query.command()
def random_similarity_indices():
	query_random_similarity_indices()

if __name__ == '__main__':
	root()


