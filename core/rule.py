from core.model import CModel
from abc import ABC


class RuleException(Exception):
    def __init__(self, rule, exception):
        self.rule = rule
        self.exception = exception

        super().__init__()



class CRule(ABC):
    def __init__(self, name, query, description = None):
        self.name = name
        if description == None:
            self.description = "None given. Use set_description() to provide it."
        else:
            self.description = description
        self.query = query

    def __str__(self):
        return f"Rule '{self.name}': \n\tDescription: \t{self.description}\n\tVerdict: \t{self.query}"

    def check(self):
        evidence = str()
        return f"Rule '{self.name}': \
        \n\tDescription: \t{self.description}\
        \n\tVerdict: \t{self.query} \
        \n\tEvidence: \t{evidence}"


    def set_description(self, description):
        self.description = description


class CRules(CRule):
    def __init__(self, ruleset_name: str):
        self.ruleset_name = ruleset_name

    def __str__(self):
        rules_string = str()

        return f"Ruleset '{self.ruleset_name}', containing the following {length} rules: {rules_string}"









#
