import json

from core.nodes import CNodes
from core.edges import CEdges
from core.rule import CRule, CRules


def load_rules(input_path) -> CRules:

    with open(input_path, "r") as rules_file:
        input = json.load(rules_file)

    rules = list()
    for rule in input["rules"]:
        query = "dd"

        rules.append(CRule(rule["name"], query, rule["description"]))

    return CRules(input["ruleset_name"])
