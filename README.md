# microCertiSec

This is *microCertiSec*, an implementation of our approach for the automatic checking of security rules on architectural models of microservice applications.


### Running 

#### In Terminal
To check a rule on a provided architecturral model of a microservice application, you need to create a Python file following the process explained below in the [example](#Example).
Then, you simply execute that file with Python. 
You can try this out directly by cloning this repository and executing the following command in the directory:

```python3 microCertiSec.py```

No requirements other than Python version 3.x are needed.

#### As Flask Server
You can also start up a Flask server by executing ```python3 microCertiSec_flask.py```. This will make microCertiSec abailable via API on localhost port 5001. 
In this case, you need to install a [recent version of Flask](https://pypi.org/project/Flask/).

Requests to the endpoint `microCertiSec` require three parameters: `model_path` giving the relative path to the [architectural model](#Used-Architectural-Models), `traceability_path` giving the relative path to the traceability file, and `rule` giving the architectural to be checked, either as query in our [rule specification language](#Rule-Specification-Language) or as ID of a rule in our [library of architectural security rules](#Rules-for-Microservice-Applications).


### Used Architectural Models
A pre-requisite for the rule checking is an architectural model representation of the microservice application that is to be analyzed.
In this prototype, we use dataflow diagrams (DFDs) for this.
Specifically, ones in the form as created by *[code2DFD](www.github.com/tuhh-softsec/code2DFD)*, which is our approach for automatically extracting DFDs from microservices' source code.


### Rule Specification Language
The core of our approach is a rule specification language that allows the formulation of architectural security rules.
A short documentation for the language can be found in the [docs](https://github.com/tuhh-softsec/microCertiSec/docs/rule_specification_language.md)
Rules that are expressed as queries in the rule specification language can be validated on a given model and will return a binary verdict, i.e., whether the rule is adhered to or violated based on the model.
Additionally, the queries generate step-by-step explanations for the verdict, which makes the decision process of how the verdict is reached comprehensible to human users. 
Each step is supported by model items that influence it, so that everything can be verified.
Finally, the models we use contain traceability information, linking model items to artefacts in source code.
Following these links, you can trace rule verdicts all the way back to the source code of the analyzed application.
In this way, our approach provides explainability for its rule checking results.


### Rules for Microservice Applications
You can formulate your own architectural rules to be checked on the models, but we also provide a library of 25 architectural security rules that microservice applications should follow.
They are based on best-practice recommendations by OWASP, NIST, and CSA.
A description of the rules is given in the [docs](https://github.com/tuhh-softsec/microCertiSec/docs/library_of_rules.md)
Their formulations in our rule specification language can be found in ```/library_of_rules/``` and you can use them to analyze your microservice applications (see the example below for how to do it).







### Example

This is an examplatory description of how to check an architectural security rule on a model.
You can follow along step-by-step to learn about how to use the tool.
We use the model ```models/sqshq_piggymetrics.json``` with the corresponding traceability ```models/sqshq_piggymetrics_traceability.json```.
The file ```minimal_example.py``` contains the code presented in the following description.

1. First, you need to import a model loader to parse models into the internal model representation used by the tool.\
```from core.load_model import load_model```

2. If you want to use rules from the list of pre-formulated rules, you have to import the library with: \
```import library_of_rules.rule_library as rules```

3. Next, you need to provide the paths to the model and corresponding traceability information.
In ```minimal_example.py```, they are stored in the variables ```dfd_path```and ```traceability_path```.

4. To load the model into the internal representation, simply pass the paths to the model parser and save the return value into a variable (```model``` in the example).\
```model = load_model(dfd_path, traceability_path)```

5. To generate the results of the rule checking, you can execute a rule on the loaded model with \
```query1 = rules.r01(model)``` \
Of course, all other rules in the library of architectural security rules can be used as well.


6. Finally, to print out the results stored in the variable ```query1```, access and print them with:\
```print(query.full_evidence_string)```

7. If instead, you want to formulate your own rules, you can follow the description of the rule specification language and use your custom rule as in the example:
```query2 = model.nodes.exactly_one_is("entrypoint")```
