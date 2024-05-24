from shutil import rmtree
from os.path import exists
import threading

from download.channels import download_channels
from download.messages import download_messages
from download.members import download_members
from process.similarity import process_similarity
from process.labels import process_labels
from process.filters import process_filters
from process.graph import process_graph
from process.geojson import process_geojson

def run_all():
	if exists("json_data"):
		rmtree("json_data")

	download_channels()

	t1 = threading.Thread(target=download_messages)
	t2 = threading.Thread(target=download_members)
	t1.start()
	t2.start()
	t1.join()
	t2.join()

	process_filters()
	process_labels()
	process_similarity()
	process_graph()
	process_geojson()