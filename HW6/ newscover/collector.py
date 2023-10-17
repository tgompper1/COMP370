import argparse
import json
from newscover import newsapi
import os

os.path.dirname(os.path.abspath(__file__))

PATH = 'newscover'

def main():
   
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", dest = 'api_key', help = "Api key", metavar="<api_key>", required=True)
    parser.add_argument("-b", dest = 'lookback', help = "# days to look back", metavar="<lookback>", default = 10, required=False)
    parser.add_argument("-i", dest = 'input_file', help = "input json file", metavar="<input_file>", required=True)
    parser.add_argument("-o", dest = 'output_dir', help = "output directory", metavar="<output_dir>", required=True)
    args = parser.parse_args()

    api_key = args.api_key
    lookback = args.lookback
    input = args.input_file
    output=args.output_dir
    with open(input) as inp:
        data=json.load(inp)
        for key in data:
            for value in data[key]:
                with open(os.path.join(PATH, output, key), 'w') as f:
                    json.dump(newsapi.fetch_latest_news(api_key, value, lookback), f, indent=4)

if __name__ == "__main__":
    main()