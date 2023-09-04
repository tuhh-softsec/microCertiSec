import json

from core.load_model import load_model
import library_of_rules.rule_library as rules
from library_of_rules.rule_library import r01, r02, r03, r04, r05, r06, r07, r08, r09, r10, r11, r12, r13, r14, r15, r16, r17, r18, r19, r20, r21, r22, r23, r24, r25, r26
from datetime import datetime


#dfd_path = "./dfds/sqshq_piggymetrics.json"
#traceability_path = "./dfds/anilallewar_microservices-basics-spring-boot_traceability.json"

dfd_path = "./delta_evaluation/piggy_metrics_delta.py"
traceability_path = "./delta_evaluation/piggymetrics.trace.json"


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
    print(result.full_evidence_string)
    return


def microCertiSec_API(model_path: str, traceability_path: str, rule: str):

    model = load_model(model_path, traceability_path, "VIENNA")

    d = {"r01": r01,
         "r02": r02,
         "r03": r03,
         "r04": r04,
         "r05": r05,
         "r06": r06,
         "r07": r07,
         "r08": r08,
         "r09": r09,
         "r10": r10,
         "r11": r11,
         "r12": r12,
         "r13": r13,
         "r14": r14,
         "r15": r15,
         "r16": r16,
         "r17": r17,
         "r18": r18,
         "r19": r19,
         "r20": r20,
         "r21": r21,
         "r22": r22,
         "r23": r23,
         "r24": r24,
         "r25": r25,
         "r26": r26
         }

    result = d[rule](model)

    return result


if __name__ == "__main__":
    main()




#
