# 🗺️ Map of the Slack

A map of all the channels in the slack!

## Generating data

All data generation/processing code is in Python, located in the `generation` directory.
You must first create a `.env` file in that directory - use `sample.env` as guidance.
To get started, run all of the commands, in this order:

1. `python3 main.py download channels`
2. `python3 main.py download members`
3. `python3 main.py download messages`
4. `python3 main.py process filters`
5. `python3 main.py process labels`
6. `python3 main.py process similarity`
7. `python3 main.py process graph`
8. `python3 main.py process geojson`

After this, you can run each command independently as needed, such as to update data or test new code.

## Running the website

First, install all packages with `npm install`. Then, after generating all data, copy the `geojson.json` file from the `generation/json_data` directory into the `static` directory.

You can now start the development server with `npm run dev`.
