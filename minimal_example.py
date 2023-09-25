from core.load_model import load_model
import library_of_rules.rule_library as rules


dfd_path = "./models/piggymetrics.json"
traceability_path = "./models/piggymetrics_traceability.json"

def main():

    print("+----------------------------------+-----------+------------------------+--------------------------------------------------+ \n\
| Statement:                                                                                                               |\n\
|    nodes.that_are(\"entrypoint\").all_have(\"authorization\")                                                                |\n\
+----------------------------------+-----------+------------------------+--------------------------------------------------+\n\
| Step                             | Decision  | Node / Edge            | Properties                                       |\n\
+----------------------------------+-----------+------------------------+--------------------------------------------------+\n\
| ### Scope transformations ###    |           |                        |                                                  |\n\
| -------------------------------- | --------- | ---------------------- | ------------------------------------------------ |\n\
| 1. that_are(\"entrypoint\")        | included  | gateway                | ['gateway', 'infrastructural', 'load_balancer',  |\n\
|                                  |           |                        | 'circuit_breaker', 'entrypoint', 'service']      |\n\
|                                  | --------- | ---------------------- | ------------------------------------------------ |\n\
|                                  | excluded  | turbine_stream_service | ['monitoring_server', 'infrastructural',         |\n\
|                                  |           |                        | 'service']                                       |\n\
|                                  | excluded  | auth_service           | ['authorization_server',                         |\n\
|                                  |           |                        | 'authentication_server',                         |\n\
|                                  |           |                        | 'pre_authorized_endpoints', 'infrastructural',   |\n\
|                                  |           |                        | 'token_server', 'encryption', 'local_logging',   |\n\
|                                  |           |                        | 'resource_server', 'csrf_disabled',              |\n\
|                                  |           |                        | 'authentication_scope_all_requests', 'service']  |\n\
|                                  | excluded  | account_service        | ['internal', 'pre_authorized_endpoints',         |\n\
|                                  |           |                        | 'local_logging', 'resource_server',              |\n\
|                                  |           |                        | 'circuit_breaker', 'authentication', 'service']  |\n\
|                                  | excluded  | user                   | ['user_stereotype', 'external_entity']           |\n\
|                                  | excluded  | auth_mongodb           | ['database', 'plaintext_credentials', 'service'] |\n\
|                                  | excluded  | statistics_mongodb     | ['database', 'plaintext_credentials', 'service'] |\n\
|                                  | excluded  | external_website       | ['external_website', 'external_entity']          |\n\
|                                  | excluded  | monitoring             | ['monitoring_dashboard', 'infrastructural',      |\n\
|                                  |           |                        | 'service']                                       |\n\
|                                  | excluded  | rabbitmq               | ['message_broker', 'infrastructural', 'service'] |\n\
|                                  | excluded  | statistics_service     | ['internal', 'local_logging',                    |\n\
|                                  |           |                        | 'pre_authorized_endpoints', 'resource_server',   |\n\
|                                  |           |                        | 'authentication', 'service']                     |\n\
|                                  | excluded  | account_mongodb        | ['database', 'plaintext_credentials', 'service'] |\n\
|                                  | excluded  | notification_service   | ['internal', 'local_logging', 'resource_server', |\n\
|                                  |           |                        | 'service']                                       |\n\
|                                  | excluded  | notification_mongodb   | ['database', 'plaintext_credentials', 'service'] |\n\
|                                  | excluded  | config                 | ['configuration_server',                         |\n\
|                                  |           |                        | 'plaintext_credentials', 'infrastructural',      |\n\
|                                  |           |                        | 'csrf_disabled', 'basic_authentication',         |\n\
|                                  |           |                        | 'authentication', 'service']                     |\n\
|                                  | excluded  | mail_server            | ['mail_server', 'plaintext_credentials',         |\n\
|                                  |           |                        | 'external_entity']                               |\n\
|                                  | excluded  | registry               | ['service_discovery', 'plaintext_credentials',   |\n\
|                                  |           |                        | 'infrastructural', 'service']                    |\n\
| -------------------------------- | --------- | ---------------------- | ------------------------------------------------ |\n\
| Final scope                      |           | gateway                |                                                  |\n\
| -------------------------------- | --------- | ---------------------- | ------------------------------------------------ |\n\
| ### Property checks ###          |           |                        |                                                  |\n\
| -------------------------------- | --------- | ---------------------- | ------------------------------------------------ |\n\
| 2. all_have(\"authorization\")     | fails     | gateway                | ['gateway', 'infrastructural', 'load_balancer',  |\n\
|                                  |           |                        | 'circuit_breaker', 'entrypoint', 'service']      |\n\
|                                  | --------- | ---------------------- | ------------------------------------------------ |\n\
|                         Verdict  | False     |                        | Property check requires all nodes to have        |\n\
|                                  |           |                        | annotation \"authorization\", but none in the      |\n\
|                                  |           |                        | scope has it                                     |\n\
+----------------------------------+-----------+------------------------+--------------------------------------------------+")
    return



    model = load_model(dfd_path, traceability_path)
    
    results = model.nodes.that_are("entrypoint").all_have("authorization")

    print(results.full_evidence_string)

    with open("output_results.html", "w") as file:
        file.write(results.full_evidence_string)

    return


if __name__ == "__main__":
    main()
    