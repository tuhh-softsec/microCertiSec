from core.results import CResults


class CNodes:
    """Class CNodes for sets of objects of type CNode.
    Represents the set of nodes in the model / DFD.

    Two different kinds of methods:
        1. ones that return a CNodes object  (used to select those nodes that fulfill a certain property)
        2. ones that return a Boolean (used to check properties of the contained nodes)

    Methods of 1. kind:
        - that_are(stereotype): return CNodes object containing all nodes that have the passed stereotype
        - that_have(stereotype): alias to that_are()

    Methods of 2. kind:
        - all_are(stereotype):
        - all_have(stereotype): alias to all_are()
        - one_is(stereotype):
        - one_has(stereotype): alias to one_is()
        - none_are(stereotype):
        - none_have(stereotype): alias to none_are()
    """


    def __init__(self, nodes, query = str(), scoping_evidence = list(), property_check_evidence = str()):
        self.nodes = nodes
        # if variable is empty (i.e., start of new query), let it be "nodes", to complete the query
        self.query = "nodes" if query == "" else query

        self.scoping_evidence = scoping_evidence
        self.property_check_evidence = property_check_evidence
        self.query_finalized = bool()


    def __str__(self):
        return_string = "Nodes:"
        for node in self.nodes:
            return_string += f"\n   - {node.name}; stereotypes {node.stereotypes}; {node.traceability}"#"; tagged_values {node.tagged_values}"
        return return_string


    def get_nodes(self):
        return self.nodes


    # Scope transformations
    def that_are(self, stereotype, transformation = "that_are"):
        """Returns CNodes object of all nodes that have the passed stereotype.
        """

        query = self.query + f".{transformation}(\"{str(stereotype)}\")"

        scoping_evidence = self.scoping_evidence
        node_names_string = str()
        for node in self.nodes:
            node_names_string += f"{node.name}, "
        node_names_string = node_names_string[:-2]
        new_scoping_evidence = {"scope_transformation": f"{transformation}(\"{str(stereotype)}\")",
                            "input_scope": node_names_string,
                            "included": [(node.name, node.stereotypes, node.traceability) for node in self.nodes if stereotype in [stereotype for (stereotype, traceability) in node.stereotypes]],
                            "excluded": [(node.name, node.stereotypes, node.traceability) for node in self.nodes if not (stereotype in [stereotype for (stereotype, traceability) in node.stereotypes])]}

        scoping_evidence.append(new_scoping_evidence)
        return CNodes([node for node in self.nodes if stereotype in [stereotype for (stereotype, traceability) in node.stereotypes]], query, scoping_evidence)


    def that_have(self, stereotype):
        """Alias for that_are().
        """

        return self.that_are(stereotype, "that_have")


    def that_are_connected_to(self, nodes, transformation = "that_are_connected_to"):
        """Alias for that_are_connected_to_any_of().
        """

        included_nodes, excluded_nodes = set(), set()
        node_names = [node.name for node in nodes.get_nodes()]
        query = self.query + f".{transformation}({str(nodes.query)})"

        for node in self.nodes:
            included = False
            for n in node.connected_nodes:
                if n in node_names:
                    for sn in self.nodes:
                        if sn.name == node.name:
                            included_nodes.add(node)
                    included = True
            if not included:
                for sn in self.nodes:
                    if sn.name == node.name:
                        excluded_nodes.add(node)

        included_nodes = list(included_nodes)
        excluded_nodes = list(excluded_nodes)

        scoping_evidence = self.scoping_evidence

        new_scoping_evidence = {"scope_transformation": f"{transformation}(\"{str(node_names)}\")",
                            "input_scope": str(node_names),
                            "included": [(node.name, node.stereotypes, node.traceability) for node in included_nodes],
                            "excluded": [(node.name, node.stereotypes, node.traceability) for node in excluded_nodes]}

        scoping_evidence.append(new_scoping_evidence)
        return CNodes(included_nodes, query, scoping_evidence)


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

        if len(self.nodes) == 0:
            # no nodes fulfill scope transformation --> verdict false
            property_check_evidence["verdict"] = False
        else:
            for node in self.nodes:
                for stereotype in stereotypes:
                    if stereotype in [stereotype for (stereotype, traceability) in node.stereotypes]:
                        property_check_evidence["fulfilled"].append((node.name, node.stereotypes, node.traceability))
                    else:
                        property_check_evidence["violated"].append((node.name, node.stereotypes, node.traceability))

            if len(property_check_evidence["violated"]) == 0:
                property_check_evidence["verdict"] = True

        return CResults(query, property_check_evidence["verdict"], self.scoping_evidence, property_check_evidence)


    def all_have(self, stereotype):
        """Alias for are_all().
        """

        return self.all_are(stereotype, "all_have")


    def at_least_one_is(self, stereotype, property_check = "at_least_one_is"):
        """Checks how many of the self.nodes have passed stereotype, returns True if at least one has it.
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

        for node in self.nodes:
            for stereotype in stereotypes:
                if stereotype in [stereotype for (stereotype, traceability) in node.stereotypes]:
                    property_check_evidence["fulfilled"].append((node.name, node.stereotypes, node.traceability))
                else:
                    property_check_evidence["violated"].append((node.name, node.stereotypes, node.traceability))

        if len(property_check_evidence["fulfilled"]) >= 1:
            property_check_evidence["verdict"] = True

        return CResults(query, property_check_evidence["verdict"], self.scoping_evidence, property_check_evidence)


    def at_least_one_has(self, stereotype):
        """Alias for one_is().
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

        for node in self.nodes:
            for stereotype in stereotypes:
                if stereotype in [stereotype for (stereotype, traceability) in node.stereotypes]:
                    property_check_evidence["fulfilled"].append((node.name, node.stereotypes, node.traceability))
                else:
                    property_check_evidence["violated"].append((node.name, node.stereotypes, node.traceability))

        if len(property_check_evidence["fulfilled"]) == 1:
            property_check_evidence["verdict"] = True

        return CResults(query, property_check_evidence["verdict"], self.scoping_evidence, property_check_evidence)


    def exactly_one_has(self, stereotype):
        """Alias for exactly_one_is().
        """

        return self.one_is(stereotype, "exactly_one_has")


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

        for node in self.nodes:
            for stereotype in stereotypes:
                if stereotype in [stereotype for (stereotype, traceability) in node.stereotypes]:
                    property_check_evidence["fulfilled"].append((node.name, node.stereotypes, node.traceability))
                else:
                    property_check_evidence["violated"].append((node.name, node.stereotypes, node.traceability))

        if len(property_check_evidence["fulfilled"]) == 0:
            property_check_evidence["verdict"] = True

        return CResults(query, property_check_evidence["verdict"], self.scoping_evidence, property_check_evidence)


    def none_have(self, stereotype):
        """Alias for none_are().
        """

        return self.none_are(stereotype, "none_have")


    def all_are_connected_to(self, stereotype, property_check = "all_are_connected_to"):
        """Checks whether all of self.nodes are connected to a node that has the passed stereotype.
        """

        query = self.query + f".{property_check}({str(stereotype)})"

        property_check_evidence = {"property_check": f"{property_check}(\"{str(stereotype)}\")",
                                    "verdict": False,
                                    "fulfilled": list(),
                                    "violated": list()}

        if isinstance(stereotype, str):
            stereotypes = list()
            stereotypes.append(stereotype)
        else:
            stereotypes = stereotype


        if len(self.nodes) == 0:
            # no nodes fulfill scope transformation --> verdict false
            property_check_evidence["verdict"] = False
        else:
            for node in self.nodes:
                for connected_node in node.connected_nodes:
                    for stereotype in stereotypes:
                        if stereotype in [stereotype for (stereotype, traceability) in connected_node.stereotypes]:
                            property_check_evidence["fulfilled"].append((node.name, node.stereotypes, node.traceability))
                        else:
                            property_check_evidence["violated"].append((node.name, node.stereotypes, node.traceability))

            property_check_evidence["fulfilled"] = list(property_check_evidence["fulfilled"])
            property_check_evidence["violated"] = list(property_check_evidence["violated"])

            if len(property_check_evidence["violated"]) == 0:
                property_check_evidence["verdict"] = True

        return CResults(query, property_check_evidence["verdict"], self.scoping_evidence, property_check_evidence)


    def none_are_connected_to(self, stereotype, property_check = "none_are_connected_to"):
        """Checks whether none of self.nodes are connected to a node that has the passed stereotype.
        """

        query = self.query + f".{property_check}({str(stereotype)})"

        property_check_evidence = {"property_check": f"{property_check}(\"{str(stereotype)}\")",
                                    "verdict": False,
                                    "fulfilled": list(),
                                    "violated": list()}

        if isinstance(stereotype, str):
            stereotypes = list()
            stereotypes.append(stereotype)
        else:
            stereotypes = stereotype

        for node in self.nodes:
            for connected_node in node.connected_nodes:
                for stereotype in stereotypes:
                    if stereotype in [stereotype for (stereotype, traceability) in connected_node.stereotypes]:
                        property_check_evidence["fulfilled"].append((node.name, node.stereotypes, node.traceability))
                    else:
                        property_check_evidence["violated"].append((node.name, node.stereotypes, node.traceability))

        property_check_evidence["fulfilled"] = list(property_check_evidence["fulfilled"])
        property_check_evidence["violated"] = list(property_check_evidence["violated"])

        if len(property_check_evidence["fulfilled"]) == 0:
            property_check_evidence["verdict"] = True

        return CResults(query, property_check_evidence["verdict"], self.scoping_evidence, property_check_evidence)


    def length(self):
        len = 0
        for node in self.nodes:
            len += 1
        return len
