# 🗺️ Map of the Slack

A map of all the channels in the slack!

## Generating data

All data generation/processing code is in Python, located in the `generation` directory.
You must first install dependencies (use a venv):

```
pip install -r requirements.txt
python -m spacy download en_core_web_lg
```

Then, create a `.env` file in that directory - use `sample.env` as guidance.
To get started, run the "all" command:

```
python main.py all
```

**This will probably take a very long time**, especially when downloading data!
Last time I ran it, it took about 48 minutes and also used up to 3 gigabytes of RAM.

After this, you can run each command independently as needed, such as to update data or test new code.

## Running the website

First, install all packages with `npm install`. Then, after generating all data, copy the `geojson.json` file from the `generation/json_data` directory into the `static` directory.

You can now start the development server with `npm run dev`.
