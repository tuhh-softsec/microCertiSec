# microCertiSec

### Formulating custom rules

Own rules can be formulated with the scope transformations and property checks described in TODO.
To provide your custom rules to the rule checker, you must store them in a JSON file containing the following fields:

```ruleset_name```: name for your set of rules. \
```rules```: set of rules


The width of the columns in the final table are determined by the framework. You can adjust them with the optional parameter ```width```, which has to be a list contaning four entries, one for each column's width. If you give any of the four values as 0, they will be determined by the framework. It sets it to the maximum width necessary to print all scope transfomrations / property checks and node names in one line. Column 2 is set to X. Column 4 is as wide max - column 1 - column 3.
The following values are the minimum. If a passed value is smaller, the minimum value used.


Everything in this rule framework is written in standard Python.
We list here a few examples of what you can do.
Assign a transformed scope to a variable:
If you want to check multiple properties on the same set of nodes, the best way is to write a scope transformation that yields the desired set of nodes, assign it to a variable, and perform the property-checks on that variable.


Load model with importing ```from core.load_model import load_model``` and calling ```load_model(path/to/dfd/file, path/to/traceabilty/file)```. You can store the returned model object to pass it to rules, e.g. ```model = load_model(./dfds/sqshq_piggymetrics.py, ./dfds/sqshq_piggymetrics_traceability.json)```.


To load existing rules, import them from the containing files, for example: ```from rules.rules import r01```. The rule can than be used by passing a model object to it nd storing the returned results object: ```results = r01(model)```.

For all property checks, there are to aliases that only differ in their name. One of the names is based on the verb "be", the other one on "have". The purpose is purely to make formulated queries better readable and understandable.

Multiple stereotypes can be given as list. They will then be treated as OR. For example, for selecting nodes that have on of a list of stereotypes, all will be selected that have at least one of the stereotypes in the given list. When performing a property check for "exactly_one_has" with multiple stereotypes as input, all items that have at least one of the stereotypes will be selected and counted. The output will then only return true, if only one model item is selected in this process.


### Example

This is an examplatory description of how to perform a rule checking on a model.
You can follow along step-by-step to learn about how to use the tool.
We use the model ```example/sqshq_piggymetrics.json``` and traceability ```example/sqshq_piggymetrics_traceability.json```.
There's also a commented code-template at ```example/tutorial.py``` which is used in the following description and which you can fill in while following along.

1. First, you need to import a model loader to parse models into the internal model representation used by the tool.\
```from core.load_model import load_model```\
This line of code is already included in ```tutorial.py```

2. If you want to use rules from the list of pre-formulated rules, you have to import the library with: \
```import rules.rules as rules```

3. Next, you need to provide the paths to the model and corresponding traceability information.
Fill in these paths in ```tutorial.py```and un-comment the the lines of code.

4. To load the model into the internal representation, simply pass the paths to the model parser and save the return value into a variable (```query```in the example).\
```model = load_model(dfd_path, traceability_path)```

5. To generate the results of the rule checking, you can execute a rule on the loaded model with \
´´´query = rules.r02(model)```

6. Finally, to print out the results stored in the variable ```query```, access and print them with, e.g.:\
```print(query.full_evidence_string)```
