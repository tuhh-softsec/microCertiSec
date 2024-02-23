# Library of architectural security rules

This folder contains our library of architectural security rules, which is a set of pre-formulated rules that you can check on models without the need of formulating your own rules.
They are initially based on best-practices and guidelines for the secure architectural design of microservice applications published by NIST, OWASP, and CSA.

The rules expressed in our rule specification language are contained in ```/rule_library.py```. 
Please check the description and minimal example shown in the repository's main [README](www.github.com/tuhh-softsec/microcertisec/README.md).

The library consists of the following 25 rules, which are shown here in natural language and contained as queries in our rule specification language in ```/rule_library.py```:
| ID | Rule |
| ----- | ----- |
| 1 | There should be a single service as entry point. |
| 2 | All entry points should have a circuit breaker. |
| 3 | All entry points should have a load balancer. |
| 4 | All entry points should perform authorization. |
| 5 | All entry points should perform authentication. |
| 6 | All connections between services should be authorized. |
| 7 | All connections between services should be authenticated. |
| 8 | There should be a single authorization service. |
| 9 | There should be a single authentication service. |
| 10 | No service that performs authorization should perform any other business functionality. |
| 11 | No service that performs authentication should perform any other business functionality. |
| 12 | There should be a service limiting the number of login attempts. |
| 13 | All connections between a service and an external entity should be encrypted. |
| 14 | All connections between two services should be encrypted. |
| 15 | All services should perform logging. |
| 16 | There should be a single central logging subsystem. |
| 17 | There should be a message broker. |
| 18 | All services that perform logging should be connected to a message broker. |
| 19 | No service that performs logging should be connected to a central logging subsystem. |
| 20 | There should be a monitoring dashboard. |
| 21 | All services should be connected to a monitoring dashboard. |
| 22 | All services should sanitize logs. |
| 23 | There should be a single service registry. |
| 24 | All service registries should have validation checks for incoming requests. |
| 25 | There should be a single central secret store. |

