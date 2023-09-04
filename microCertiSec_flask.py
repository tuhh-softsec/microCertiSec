from flask import Flask, jsonify, request
import json

from microCertiSec import microCertiSec_API

app = Flask(__name__, instance_relative_config = True)

# Create default endpoint
@app.get('/')
def index():

    return "API for automatic rule checking of architectural models."


# Create endpoint /microCertiSec
@app.get('/microCertiSec')
def rule_checker():

    model_path = request.args.get("model_path")
    traceability_path = request.args.get("traceability_path")
    rule = request.args.get("rule")
    # optional argument for parser!

    if not model_path:
        return "Please specify a path to the model file, e.g. /microCertiSec?model_path=path/to/model"
    if not traceability_path:
        return "Please specify a path to the traceability file, e.g. /microCertiSec?traceability_path=path/to/traceability"
    if not rule:
        return "Please specify a rule. Either the ID of pre-formulated rule preceeded by an underscore (e.g., \"_r01\"), or a custom query"

    # Call microCertiSec
    results = microCertiSec_API(model_path, traceability_path, rule)

    # Create response JSON object and return it
    response = jsonify(
        results = results.full_evidence_json
    )
    with open("./delta_evaluation/output_first.json", "w") as output_file:
        json.dump(results.full_evidence_json, output_file, indent = 4)
    return response


# starts local server
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)
