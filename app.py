from flask import Flask, request
from pipeline import Image
from argparse import ArgumentParser
from pathlib import Path

parser = ArgumentParser()

parser.add_argument('--port', help="port for accessing api", default=8080, type=int)
parser.add_argument('--root', help="base directory for images", default="./sort")
parser.add_argument('--precision', help="precision for detecting fuzziness", default=0.3, type=float)

args = parser.parse_args()

root = Path(args.root)
(root / "temp").mkdir(parents=True, exist_ok=True)
(root / "safe").mkdir(parents=True, exist_ok=True)
(root / "unsafe").mkdir(parents=True, exist_ok=True)
(root / "fuzzy").mkdir(parents=True, exist_ok=True)

Pipeline = Image(args.root, args.precision)

app = Flask(__name__)

@app.route("/", methods=["POST"])
def handleURL():
    url = request.args.get('url')
    try:
        Pipeline.start(url)
        return str(Pipeline)
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=args.port)