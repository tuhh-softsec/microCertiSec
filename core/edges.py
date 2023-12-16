from core.results import CResults


class CEdges:
    def __init__(self, edges, query = str(), scoping_evidence = list(), property_check_evidence = str()):
        self.edges = edges
        if query == "":
            self.query = "edges"
        else:
            self.query = query
        self.scoping_evidence = scoping_evidence
        self.property_check_evidence = property_check_evidence


    def __str__(self):
        return_string = "Edges:"
        for edge in self.edges:
            return_string += f"\n   - {edge.sender.name} -> {edge.receiver.name}; stereotypes {edge.stereotypes}"#"; tagged_values {edge.tagged_values}"
        return return_string


    def edge_exists(self, node1, node2):
        """Returns True if an edge (in either direction) between the two passed nodes exists, False otherwise."""

        for edge in self.edges:
            if edge.sender.name == node1:
                if edge.receiver.name == node2:
                    return True
            elif edge.sender.name == node2:
                if edge.receiver.name == node1:
                    return True
        return False


    # Scope transformations
    def that_are(self, stereotype, transformation = "that_are"):
        """Returns CEdges object of all edges that have the passed stereotype.
        """

        query = self.query + f".{transformation}(\"{str(stereotype)}\")"

        scoping_evidence = self.scoping_evidence
        edge_names_string = str()
        for edge in self.edges:
            edge_names_string += f"{edge.name}, "
        edge_names_string = edge_names_string[:-2]

        new_scoping_evidence = {"scope_transformation": f"{transformation}(\"{str(stereotype)}\")",
                            "input_scope": edge_names_string,
                            "included": [(edge.name, edge.stereotypes, edge.traceability) for edge in self.edges if stereotype in [stereotype for (stereotype, traceability) in edge.stereotypes]],
                            "excluded": [(edge.name, edge.stereotypes, edge.traceability) for edge in self.edges if not (stereotype in [stereotype for (stereotype, traceability) in edge.stereotypes])]}

        scoping_evidence.append(new_scoping_evidence)

        return CEdges([edge for edge in self.edges if stereotype in [stereotype for (stereotype, traceability) in edge.stereotypes]], query, scoping_evidence)


    def that_have(self, stereotype):
        """Alias for that_are().
        """

        return self.that_are(stereotype, "that_have")


    def sender_is(self, stereotype, transformation = "sender_is"):
        """Returns CEdges object of all edges where sender node has passed stereotype.
        """

        query = self.query + f".{transformation}(\"{str(stereotype)}\")"

        scoping_evidence = self.scoping_evidence
        edge_names_string = str()
        for edge in self.edges:
            edge_names_string += f"{edge.name}, "
        edge_names_string = edge_names_string[:-2]

        new_scoping_evidence = {"scope_transformation": f"{transformation}(\"{str(stereotype)}\")",
                            "input_scope": edge_names_string,
                            "included": [(edge.name, edge.stereotypes, edge.traceability) for edge in self.edges if stereotype in [stereotype for (stereotype, traceability) in edge.sender.stereotypes]],
                            "excluded": [(edge.name, edge.stereotypes, edge.traceability) for edge in self.edges if not (stereotype in [stereotype for (stereotype, traceability) in edge.sender.stereotypes])]}

        scoping_evidence.append(new_scoping_evidence)

        return CEdges([edge for edge in self.edges if stereotype in [stereotype for (stereotype, traceability) in edge.sender.stereotypes]], query, scoping_evidence)


    def sender_has(self, stereotype):
        """Alias to sender_is().
        """

        return self.sender_is(stereotype, "sender_has")


    def receiver_is(self, stereotype, transformation = "receiver_is"):
        """Returns CEdges object of all edges where receiver node has passed stereotype.
        """

        query = self.query + f".{transformation}(\"{str(stereotype)}\")"

        scoping_evidence = self.scoping_evidence
        edge_names_string = str()
        for edge in self.edges:
            edge_names_string += f"{edge.name}, "
        edge_names_string = edge_names_string[:-2]

        new_scoping_evidence = {"scope_transformation": f"{transformation}(\"{str(stereotype)}\")",
                            "input_scope": edge_names_string,
                            "included": [(edge.name, edge.stereotypes, edge.traceability) for edge in self.edges if stereotype in [stereotype for (stereotype, traceability) in edge.receiver.stereotypes]],
                            "excluded": [(edge.name, edge.stereotypes, edge.traceability) for edge in self.edges if not (stereotype in [stereotype for (stereotype, traceability) in edge.receiver.stereotypes])]}

        scoping_evidence.append(new_scoping_evidence)

        return CEdges([edge for edge in self.edges if stereotype in [stereotype for (stereotype, traceability) in edge.receiver.stereotypes]], query, scoping_evidence)


    def receiver_has(self, stereotype):
        """Alias to receiver_is().
        """

        return self.receiver_is(stereotype, "receiver_has")


    # Property checks
    def all_are(self, stereotype, property_check = "all_are"):
        """Checks whether all self.nodes have passed stereotype. Returns Boolean.
        """

        query = self.query + f".{property_check}(\"{str(stereotype)}\")"

        property_check_evidence = {"property_check": f"{property_check}(\"{str(stereotype)}\")",
                                    "verdict": False,
                                    "fulfilled": list(),
                                    "violated": list()}

        if isinstance(stereotype, str):
            stereotypes = list()
            stereotypes.append(stereotype)
        else:
            stereotypes = stereotype

        if len(self.edges) == 0:
            # no edges fulfill scope transformation --> verdict false
            property_check_evidence["verdict"] = False
        else:
            for edge in self.edges:
                for stereotype in stereotypes:
                    if stereotype in [stereotype for (stereotype, traceability) in edge.stereotypes]:
                        property_check_evidence["fulfilled"].append((edge.name, edge.stereotypes, edge.traceability))
                    else:
                        property_check_evidence["violated"].append((edge.name, edge.stereotypes, edge.traceability))

            if len(property_check_evidence["violated"]) == 0:
                property_check_evidence["verdict"] = True

        return CResults(query, property_check_evidence["verdict"], self.scoping_evidence, property_check_evidence)


    def all_have(self, stereotype):
        """Alias for are_all().
        """

        return self.all_are(stereotype, "all_have")


    def at_least_one_is(self, stereotype, property_check = "at_leastone_is"):
        """Checks how many of the self.nodes have passed stereotype, returns True if exactly one has it.
        """

        query = self.query + f".{property_check}(\"{str(stereotype)}\")"

        property_check_evidence = {"property_check": f"{property_check}(\"{str(stereotype)}\")",
                                    "verdict": False,
                                    "fulfilled": list(),
                                    "violated": list()}

        if isinstance(stereotype, str):
            stereotypes = list()
            stereotypes.append(stereotype)
        else:
            stereotypes = stereotype

        for edge in self.edges:
            for stereotype in stereotypes:
                if stereotype in [stereotype for (stereotype, traceability) in edge.stereotypes]:
                    property_check_evidence["fulfilled"].append((edge.name, edge.stereotypes, edge.traceability))
                else:
                    property_check_evidence["violated"].append((edge.name, edge.stereotypes, edge.traceability))

        if len(property_check_evidence["fulfilled"]) >= 1:
            property_check_evidence["verdict"] = True

        return CResults(query, property_check_evidence["verdict"], self.scoping_evidence, property_check_evidence)


    def at_least_one_has(self, stereotype):
        """Alias for at_least_one_is().
        """

        return self.at_least_one_is(stereotype, "at_least_one_has")


    def exactly_one_is(self, stereotype, property_check = "exactly_one_is"):
        """Checks how many of the self.nodes have passed stereotype, returns True if exactly one has it.
        """

        query = self.query + f".{property_check}(\"{str(stereotype)}\")"

        property_check_evidence = {"property_check": f"{property_check}(\"{str(stereotype)}\")",
                                    "verdict": False,
                                    "fulfilled": list(),
                                    "violated": list()}

        if isinstance(stereotype, str):
            stereotypes = list()
            stereotypes.append(stereotype)
        else:
            stereotypes = stereotype

        for edge in self.edges:
            for stereotype in stereotypes:
                if stereotype in [stereotype for (stereotype, traceability) in edge.stereotypes]:
                    property_check_evidence["fulfilled"].append((edge.name, edge.stereotypes, edge.traceability))
                else:
                    property_check_evidence["violated"].append((edge.name, edge.stereotypes, edge.traceability))

        if len(property_check_evidence["fulfilled"]) == 1:
            property_check_evidence["verdict"] = True

        return CResults(query, property_check_evidence["verdict"], self.scoping_evidence, property_check_evidence)


    def exactly_one_has(self, stereotype):
        """Alias for exactly_one_is().
        """

        return self.exactly_one_is(stereotype, "exactly_one_has")


    def none_are(self, stereotype, property_check = "none_are"):
        """Checks whether any of self.nodes has passed stereotype. Returns False if yes, True otherwise.
        """

        query = self.query + f".{property_check}(\"{str(stereotype)}\")"

        property_check_evidence = {"property_check": f"{property_check}(\"{str(stereotype)}\")",
                                    "verdict": False,
                                    "fulfilled": list(),
                                    "violated": list()}

        if isinstance(stereotype, str):
            stereotypes = list()
            stereotypes.append(stereotype)
        else:
            stereotypes = stereotype

        for edge in self.edges:
            for stereotype in stereotypes:
                if stereotype in [stereotype for (stereotype, traceability) in edge.stereotypes]:
                    property_check_evidence["fulfilled"].append((edge.name, edge.stereotypes, edge.traceability))
                else:
                    property_check_evidence["violated"].append((edge.name, edge.stereotypes, edge.traceability))

        if len(property_check_evidence["fulfilled"]) == 0:
            property_check_evidence["verdict"] = True

        return CResults(query, property_check_evidence["verdict"], self.scoping_evidence, property_check_evidence)


    def none_have(self, stereotype):
        """Alias for none_are().
        """

        return self.none_are_any_of(stereotype, "none_have")
