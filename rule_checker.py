import json

from core.load_model import load_model
import library_of_rules.rule_library as rules
from datetime import datetime


dfd_path = "./dfds/sqshq_piggymetrics.json"
traceability_path = "./dfds/anilallewar_microservices-basics-spring-boot_traceability.json"


def main():

    start_time = datetime.now()
    print(dfd_path)

    model = load_model(dfd_path, traceability_path, "VIENNA")

    result = model.edges.receiver_is("external_component").all_have("https").AND(model.edges.sender_is("external_component").all_have("https"))

    with open("./delta_evaluation/output_delta.json", "w") as output_file:
        json.dump(result.full_evidence_json, output_file, indent = 4)

    end_time = datetime.now()
    execution_time = (end_time - start_time).total_seconds()
    print("Execution time: ", execution_time)

    return


if __name__ == "__main__":
    main()




#
