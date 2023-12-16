from prettytable import PrettyTable


class CResults():
    """Class CResults to collect verdict and evidence in different formats.
    """

    def __init__(self,
                  query,
                  verdict,
                  scoping_evidence,
                  property_check_evidence,
                  columnwidths = list(),
                  scoping_evidence_string = str(),
                  scoping_evidence_json = dict(),
                  property_check_evidence_string = str(),
                  property_check_evidence_json = dict(),
                  full_evidence_string = str(),
                  full_evidence_json = dict()):

        # Explanation for one-line-if-statements: evidence is only generated newly if the corresponding passed variable _evidence_string is empty.
        # This is for the logical operators, which return a CResults object but generate the final evidence in the corresponding method.
        # This way, only the methods for logical operators are a bit bloaty, otherwise there would have to be way more checks throughout the class.

        self.query = query
        self.verdict = verdict

        self.scoping_evidence = scoping_evidence
        self.property_check_evidence = property_check_evidence

        self.columnwidths = self.set_columnwidths(columnwidths)
        self.scoping_evidence_string = self.generate_scoping_evidence() if scoping_evidence_string == "" else scoping_evidence_string
        self.scoping_evidence_json = self.generate_scoping_evidence_json() if not scoping_evidence_json else scoping_evidence_json
        self.property_check_evidence_string = self.generate_property_check_evidence() if property_check_evidence_string == "" else property_check_evidence_string
        self.property_check_evidence_json = self.generate_property_check_evidence_json() if not property_check_evidence_json else property_check_evidence_json
        self.full_evidence_string = self.generate_full_evidence()[0] if full_evidence_string == "" else full_evidence_string
        self.full_evidence_html = self.generate_full_evidence()[1] if full_evidence_string == "" else full_evidence_string
        self.full_evidence_json = self.generate_full_evidence_json() if not full_evidence_json else full_evidence_json


    # Logical operators
    def AND(self, second_operand):


        first_operand = self
        query = first_operand.query + ".AND(" + second_operand.query + ")"
        verdict = first_operand.verdict and second_operand.verdict

        ##### Evidences
        ### Raw
        scoping_evidence = first_operand.scoping_evidence + second_operand.scoping_evidence

        property_check_evidence = {"first_operand": first_operand.property_check_evidence,
                                    "second_operand": second_operand.property_check_evidence}

        ### JSON
        #fix to remove duplicates from second operand which I can't get out otherwise
        for k, v in first_operand.scoping_evidence_json.items():
            del second_operand.scoping_evidence_json[k]

        property_check_evidence_json = {"first_operand": first_operand.property_check_evidence_json,
                                        "second_operand": second_operand.property_check_evidence_json}

        scoping_evidence_json = {"first_operand": first_operand.scoping_evidence_json,
                                    "second_operand": second_operand.scoping_evidence_json}


        full_evidence_json = {"query": query,
                                "verdict": verdict,
                                "statements": {"first_operand": first_operand.full_evidence_json,
                                                "second_operand": second_operand.full_evidence_json}}

        ### String
        scoping_evidence_string = first_operand.scoping_evidence_string + "\n" + second_operand.scoping_evidence_string
        property_check_evidence_string = first_operand.property_check_evidence_string + "\n" + second_operand.property_check_evidence_string

        full_evidence_string = f"Query contains logical operator. Showing evidence separated into statements.\nFull query: {query}\n"
        full_evidence_string += first_operand.full_evidence_string + "\n" + second_operand.full_evidence_string

        # Concluding evidence for logical operator
        pt = PrettyTable()
        pt.field_names = ["Step", "Decision", "Node / Edge", "Properties"]
        pt.align = "l"
        pt._max_width = {"Step": second_operand.columnwidths[0],
                        "Decision": second_operand.columnwidths[1],
                        "Node / Edge": second_operand.columnwidths[2],
                        "Properties" : second_operand.columnwidths[3]}

        columnwidths = second_operand.columnwidths

        total_width = columnwidths[0] + columnwidths[1] + columnwidths[2] + columnwidths[3]
        separation_line = "\n+" + "-" * (columnwidths[0] + 2) + "+" + "-" * (columnwidths[1] + 2) + "+" + "-" * (columnwidths[2] + 2) + "+" + "-" * (columnwidths[3] + 2) + "+\n"
        operator_evidence = separation_line
        operator_evidence += "| Statement: " + " " * (total_width - 1) + "|\n"
        operator_evidence += "|    " + query + " " * (total_width + 7 - len(query)) + "|"
        operator_evidence += separation_line
        operator_evidence += "|" + " " * (columnwidths[0] - 6)+ f"Verdict | {verdict}" + " " * (columnwidths[1] - len(str(verdict)) + 1) + "|" + " " * (columnwidths[2] + 2) + f"| {first_operand.verdict} AND {second_operand.verdict}" + " " * (columnwidths[3] - len(str(first_operand.verdict)) - len(str(second_operand.verdict)) - 4) + "|"
        operator_evidence += separation_line

        full_evidence_string += operator_evidence


        return CResults(query,
                        verdict,
                        scoping_evidence,
                        property_check_evidence,
                        columnwidths,
                        scoping_evidence_string,
                        scoping_evidence_json,
                        property_check_evidence_string,
                        property_check_evidence_json,
                        full_evidence_string,
                        full_evidence_json)


    def OR(self, second_operand):
        print("OR operator")
        pass


    # Evidence generators
    def generate_scoping_evidence(self) -> str:
        """Generates scoping evidence.
        """

        scoping_evidences = self.scoping_evidence
        if not scoping_evidences:
            return "\tNo scoping transformations in query."

        # Initialize PrettyTables object
        pt = PrettyTable()
        pt.field_names = ["Step", "Decision", "Node / Edge", "Properties"]
        pt.align = "l"
        pt._max_width = {"Step": self.columnwidths[0],
                        "Decision": self.columnwidths[1],
                        "Node / Edge": self.columnwidths[2],
                        "Properties" : self.columnwidths[3]}

        pt = self.prettify_scoping_evidence(scoping_evidences, pt)

        return pt.get_string()


    def generate_scoping_evidence_json(self) -> dict:
        scoping_evidence_json = dict()
        for id, transformation in enumerate(self.scoping_evidence):
            scoping_evidence_json[transformation["scope_transformation"]] = dict()

            included_items = list()
            for i in transformation["included"]:
                traceability = dict()
                for stereotype in i[1]:
                    traceability[stereotype[0]] = stereotype[1]
                included_items.append({"item": i[0],
                                        "item_traceability": i[2],
                                        "stereotypes": [x for (x, y) in i[1]],
                                        "stereotypes_traceability": traceability})
            scoping_evidence_json[transformation["scope_transformation"]]["included"] = included_items

            excluded_items = list()
            for i in transformation["excluded"]:
                traceability = dict()
                for stereotype in i[1]:
                    traceability[stereotype[0]] = stereotype[1]
                excluded_items.append({"item": i[0],
                                        "item_traceability": i[2],
                                        "stereotypes": [x for (x, y) in i[1]],
                                        "stereotypes_traceability": traceability})
            scoping_evidence_json[transformation["scope_transformation"]]["excluded"] = excluded_items

        return scoping_evidence_json


    def generate_property_check_evidence(self) -> str:
        """Generates property check evidence.
        """

        property_check_evidence = self.property_check_evidence

        # Initialize PrettyTables object
        pt = PrettyTable()
        pt.field_names = ["Step", "Decision", "Node / Edge", "Properties"]
        pt.align = "l"
        pt._max_width = {"Step": self.columnwidths[0],
                        "Decision": self.columnwidths[1],
                        "Node / Edge": self.columnwidths[2],
                        "Properties": self.columnwidths[3]}

        pt = self.prettify_property_check_evidence(property_check_evidence, pt)

        return pt.get_string()


    def generate_property_check_evidence_json(self) -> dict:

        property_check_evidence_json = dict()
        property_check_evidence_json[self.property_check_evidence["property_check"]] = {"verdict": self.property_check_evidence["verdict"]}

        fulfilled_items = list()
        for f in self.property_check_evidence["fulfilled"]:
            traceability = dict()
            for stereotype in f[1]:
                traceability[stereotype[0]] = stereotype[1]
            fulfilled_items.append({"item": f[0],
                                    "item_traceability": f[2],
                                    "stereotypes": [x for (x, y) in f[1]],
                                    "stereotypes_traceability": traceability})
        property_check_evidence_json[self.property_check_evidence["property_check"]]["fulfilled"] = fulfilled_items

        violated_items = list()
        for f in self.property_check_evidence["violated"]:
            traceability = dict()
            for stereotype in f[1]:
                traceability[stereotype[0]] = stereotype[1]
            violated_items.append({"item": f[0],
                                    "item_traceability": f[2],
                                    "stereotypes": [x for (x, y) in f[1]],
                                    "stereotypes_traceability": traceability})
        property_check_evidence_json[self.property_check_evidence["property_check"]]["violated"] = violated_items

        return property_check_evidence_json


    def generate_full_evidence(self):
        """Generates full evidence.
        """

        scoping_evidences = list()
        output_html = "<!DOCTYPE html>\
        <html>\
        \
        <body><pre>"

        if "that_are_connected_to" in self.query:
            query_components = self.query.split("that_are_connected_to")[0].split(".")[:-1]

            inner_raw = self.query.split("that_are_connected_to")[1]
            inner = str()
            brackets = 0
            opened = False
            for s in inner_raw:
                inner += s
                if s == "(":
                    brackets += 1
                    opened = True
                elif s == ")":
                    brackets -= 1
                if opened and brackets == 0:
                    break
            query_components.append("that_are_connected_to" + inner)
            query_components += self.query.split(inner)[1].split(".")[1:]

        else:
            query_components = [x for x in self.query.split(".")]

        while query_components:
            component = query_components.pop()
            i = 1

            while i <= len(self.scoping_evidence):
                if "that_are_connected_to" in component:
                    component = "that_are_connected_to"
                if component in self.scoping_evidence[-i]["scope_transformation"]:
                    scoping_evidences.append(self.scoping_evidence[-i])
                    i = len(self.scoping_evidence)
                i += 1
                # TODO is i set corectly?

        property_check_evidence = self.property_check_evidence
        columnwidths = self.columnwidths
        columnwidths[3] = 48
        # Initialize PrettyTables object
        pt = PrettyTable()
        pt.field_names = ["Step", "Decision", "Node / Edge", "Properties"]
        pt.align = "l"
        pt._max_width = {"Step": columnwidths[0],
                        "Decision": columnwidths[1],
                        "Node / Edge": columnwidths[2],
                        "Properties": columnwidths[3]}

        total_width = columnwidths[0] + columnwidths[1] + columnwidths[2] + columnwidths[3]

        # Add query
        output_string = "\n+" + "-" * (columnwidths[0] + 2) + "+" + "-" * (columnwidths[1] + 2) + "+" + "-" * (columnwidths[2] + 2) + "+" + "-" * (columnwidths[3] + 2) + "+\n"
        output_string += "| Statement: " + " " * (total_width - 1) + "|\n"
        output_string += "|    " + self.query + " " * (total_width + 7 - len(self.query)) + "|\n"

        output_html += pt.get_string()
        
        # Scope transformation section header
        if scoping_evidences:
            pt.add_row(["### Scope transformations ###", "", "", ""])
            pt.add_row(["-" * self.columnwidths[0], "-" * self.columnwidths[1], "-" * self.columnwidths[2], "-" * self.columnwidths[3]])

            # Scope transformation section
            pt = self.prettify_scoping_evidence(scoping_evidences, pt)

        # Property checks section header
            pt.add_row(["-" * self.columnwidths[0], "-" * self.columnwidths[1], "-" * self.columnwidths[2], "-" * self.columnwidths[3]])
        pt.add_row(["### Property checks ###", "", "", ""])
        pt.add_row(["-" * self.columnwidths[0], "-" * self.columnwidths[1], "-" * self.columnwidths[2], "-" * self.columnwidths[3]])

        # Property checks section
        pt = self.prettify_property_check_evidence(property_check_evidence, pt, len(scoping_evidences) + 1)

        output_string += pt.get_string()

        output_html += "</pre>\
        </body>\
        </html>"
        return output_string, output_html


    def generate_full_evidence_json(self) -> dict:
        full_evidence_json = {"query": self.query,
                                "verdict": self.verdict,
                                "scope_transformations": self.scoping_evidence_json,
                                "property_check": self.property_check_evidence_json}

        return full_evidence_json


    def prettify_scoping_evidence(self, scoping_evidences, pt, step_count = 1) -> str:
        """Adds passed scoping_evidence to the passed PrettyTable pt.
        """

        if not scoping_evidences:
            return pt

        # Add scope transformations
        for id, scoping_evidence in enumerate(scoping_evidences):

            if not id == 0:
                pt.add_row(["-" * self.columnwidths[0], "-" * self.columnwidths[1], "-" * self.columnwidths[2], "-" * self.columnwidths[3]])

            for id_inner, node in enumerate(scoping_evidence["included"]):
                if id_inner == 0:
                    pt.add_row([f"{step_count + id}. {scoping_evidence['scope_transformation']}", "included", node[0], [stereotype for (stereotype, traceability) in node[1]]])
                else:
                    pt.add_row(["", "included", node[0], [stereotype for (stereotype, traceability) in node[1]]])
            pt.add_row(["", "-" * self.columnwidths[1], "-" * self.columnwidths[2], "-" * self.columnwidths[3]])
            for node in scoping_evidence["excluded"]:
                pt.add_row(["", "excluded", node[0], [stereotype for (stereotype, traceability) in node[1]]])
            final_id = id

        # Add final scope
        pt.add_row(["-" * self.columnwidths[0], "-" * self.columnwidths[1], "-" * self.columnwidths[2], "-" * self.columnwidths[3]])
        for id, node in enumerate(scoping_evidences[-1]["included"]):
            if id == 0:
                pt.add_row(["Final scope", "", node[0], ""])
            else:
                pt.add_row(["", "", node[0], ""])

        return pt


    def prettify_property_check_evidence(self, property_check_evidence, pt, step_count = 1) -> str:
        """Turns disctionary that contains property check evidence into a nicely printable string.
        """

        # Add decisions
        for id, node in enumerate(sorted(property_check_evidence["fulfilled"], key = lambda a: a[0])):
            if id == 0:
                pt.add_row([f"{step_count + id}. {property_check_evidence['property_check']}", "fulfills", node[0], [stereotype for (stereotype, traceability) in node[1]]])
            else:
                pt.add_row([" ", "fulfills", node[0], [stereotype for (stereotype, traceability) in node[1]]])
        for id, node in enumerate(sorted(property_check_evidence["violated"], key = lambda a: a[0])):
            if len(property_check_evidence["fulfilled"]) == 0:
                if id == 0:
                    pt.add_row([f"{step_count + id}. {property_check_evidence['property_check']}", "fails", node[0], [stereotype for (stereotype, traceability) in node[1]]])
                else:
                    pt.add_row([" ", "fails", node[0], [stereotype for (stereotype, traceability) in node[1]]])
            else:
                pt.add_row([" ", "fails", node[0], [stereotype for (stereotype, traceability) in node[1]]])

        pt.add_row([" ", "-" * self.columnwidths[1], "-" * self.columnwidths[2], "-" * self.columnwidths[3]])
        verdict_cell = " " * (self.columnwidths[0] - 8) + "Verdict"
        if self.verdict == True:
            pt.add_row([verdict_cell, self.verdict, " ", "Property check is fulfilled"])
        else:
            pt.add_row([verdict_cell, self.verdict, " ", "Property check requires all to have it, only x has it"])

        return pt


    def set_columnwidths(self, user_columnwidths) -> None:
        """Sets the widths of the four columns to be printed as output.
        If provided by user, use those values.
        Otherwise:
            column 1 = max needed to print scope transformations and property cheks in a single line
            column 2 = 18
            column 3 = max needed to print each node name in a single line
        """

        columnwidths = []
        total_width = 143

        if self.scoping_evidence:
            max_scope = max([len(x["scope_transformation"]) for x in self.scoping_evidence])
        else:
            max_scope = 20
        if self.property_check_evidence:
            if "property_check" in self.property_check_evidence.keys():
                property_check_length = len(self.property_check_evidence["property_check"])
        else:
            property_check_length = 20
        # set it to maximum needed to show property checks, but not more than 35
        column_1 = 32#min(50, max(max_scope, property_check_length) + 3)


        # Column 1
        if len(user_columnwidths) > 0:
            if user_columnwidths[0] != 0:
                columnwidths.append(user_columnwidths[0])
            else:
                columnwidths.append(column_1)
        else:
            columnwidths.append(column_1)

        # Column 2
        if len(user_columnwidths) > 1:
            if user_columnwidths[1]:
                columnwidths.append(user_columnwidths[1])
            else:
                columnwidths.append(9)
        else:
            columnwidths.append(9)

        # Column 3
        if len(user_columnwidths) > 2:
            if user_columnwidths[2]:
                columnwidths.append(user_columnwidths[2])
            else:
                if self.scoping_evidence:
                    columnwidths.append(max([len(x.strip()) for x in self.scoping_evidence[0]["input_scope"].split(",")]))
                else:
                    columnwidths.append(20)
        else:
            if self.scoping_evidence:
                columnwidths.append(max([len(x.strip()) for x in self.scoping_evidence[0]["input_scope"].split(",")]))
            else:
                columnwidths.append(20)

        # Column 4
        if len(user_columnwidths) > 3:
            if user_columnwidths[3]:
                columnwidths.append(user_columnwidths[3])
            else:
                columnwidths.append(70)
                #columnwidths.append(total_width - sum(columnwidths) - 20)
        else:
            columnwidths.append(70)
            #columnwidths.append(total_width - sum(columnwidths) - 20)

        return columnwidths
