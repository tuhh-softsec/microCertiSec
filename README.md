# microCertiSec

Our approach and tool *microCertiSec* allows the automatic checking of security rules on architectural models of microservice applications.
In this prototype, we use dataflow diagrams (DFDs) as architectural models.
Specifically, ones in the form as created by *[code2DFD](www.github.com/tuhh-softsec/code2DFD)*, which is our approach for automatically extracting DFDs from microservices' source code.
Rules are formulated in our rule specification language or used from the existing library of architectural security rules (see ```/library_of_rules/```).


## Example

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
