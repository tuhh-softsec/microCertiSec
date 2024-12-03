import os
from datetime import datetime

from core.load_model import load_model
import library_of_rules.rule_library as rules
from library_of_rules.rule_library import r01, r02, r03, r04, r05, r06, r07, r08, r09, r10, r11, r12, r13, r14, r15, r16, r17, r18, r19, r20, r21, r22, r23, r24, r25, r26



def main():
    # dfd_path = "./models/anilallewar_microservices-basics-spring-boot.json"
    # dfd_path = "./models/apssouza22_java-microservice.json"
    # dfd_path = "./models/callistaenterprise_blog-microservices.json"
    # dfd_path = "./models/ewolff_microservice-kafka.json"
    # dfd_path = "./models/ewolff_microservice.json"
    # dfd_path = "./models/fernandoabcampos_spring-netflix-oss-microservices.json"
    # dfd_path = "./models/georgwittberger_apache-spring-boot-microservice-example.json"
    # dfd_path = "./models/jferrater_tap-and-eat-microservices.json"
    # dfd_path = "./models/koushikkothagal_spring-boot-microservices-workshop.json"
    # dfd_path = "./models/mdeket_spring-cloud-movie-recommendation.json"
    # dfd_path = "./models/mudigal-technologies_microservices-sample.json"
    dfd_path = "./models/piomin_sample-spring-oauth2-microservices.json"
    # dfd_path = "./models/rohitghatol_spring-boot-microservices.json"
    # dfd_path = "./models/shabbirdwd53_springboot-microservice.json"
    # dfd_path = "./models/spring-petclinic_spring-petclinic-microservices.json"
    # dfd_path = "./models/sqshq_piggymetrics.json"
    # dfd_path = "./models/yidongnan_spring-cloud-netflix-example.json"

    start_time = datetime.now()
    traceability_path = dfd_path.replace(".json", "") + "_traceability.json"
    model = load_model(dfd_path, traceability_path, "TUHH")

    os.makedirs(os.path.dirname("./output"), exist_ok=True)

    name = dfd_path.split("models/")[1]
    result = rules.r13(model)
    with open(f"./output/{name}.txt", "w") as output_file:
        output_file.write(result.full_evidence_string)


    print(result.full_evidence_string)
    
    end_time = datetime.now()
    execution_time = (end_time - start_time).total_seconds()
    print("Execution time: ", execution_time)

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
