"""Augments the output file with traceability information taken from the provided traceability file.
"""

import json


def main():
    # creating clickable links in HTML file (hacky)
    with open("./dfds/sqshq_piggymetrics_traceability.json", "r") as traceability_file:
        traceability = json.load(traceability_file)

    with open("./output.txt", "r") as results_file:
        result_string = results_file.read()

    started = False
    new_results_string = "<!DOCTYPE html>\
    <html>\
    \
    <body><pre>"
    for line in result_string.split("\n"):
        added = False
        if "| Step " in line:
            started = True
        if not started:
            new_results_string += line + "\n"
            continue
        if not "|" in line:
            new_results_string += line + "\n"
            continue

        # setting last node variable
        if line.split("|")[3].strip():
            node = line.split("|")[3].strip()

        # node traceability
        for n in traceability["nodes"]:
            if (node == n) or (node.replace("_", "-") == n):
                trace = traceability["nodes"][n]["file"]
                if "http" in trace:
                    line = line.replace(node, f"<a href=\"{trace}\" target=\"_blank\">{node}</a>")

                if "sub_items" in traceability["nodes"][n]:
                    for s in traceability["nodes"][n]["sub_items"]:
                        if ("\'" + s + "\'") in line:
                            trace = traceability["nodes"][n]["sub_items"][s]["file"]
                            if "http" in trace:
                                line = line.replace(s, f"<a href=\"{trace}\" target=\"_blank\">{s}</a>")

        # edge traceability
        for e in traceability["edges"]:
            e_compare = e.replace("-", "_").replace("_>", "->")
            if node.replace("-", "_").replace("_>", "->") == e_compare:
                trace = traceability["edges"][e]["file"]
                if "http" in trace:
                    line = line.replace(node, f"<a href=\"{trace}\" target=\"_blank\">{node}</a>")

                if "sub_items" in traceability["edges"][e]:
                    for s in traceability["edges"][e]["sub_items"]:
                        if ("\'" + s + "\'") in line:

                            trace = traceability["edges"][e]["sub_items"][s]["file"]
                            if "http" in trace:
                                line = line.replace(s, f"<a href=\"{trace}\" target=\"_blank\">{s}</a>")
                                
        new_results_string += line + "\n"

    new_results_string += "</pre>\
    </body>\
    </html>"
    with open("./output.html", "w") as output_file:
        output_file.write(new_results_string)




if __name__ == "__main__":
    main()




#
