# Rule Specification Language

[work in progress]

This rule specification language is a core part of microCertiSec. 
It allows the formulation of architectural security rules that can then be automatically checked with our approach.

The language is designed to be simple and easily understandable, so that queries can be formulated with minimal domain knowledge and are intuitively interpretable.

#### Query structure
Architectural rules are expressed as *queries*. 
Queries are concatinations of multiple *constructs* and look for example like this:

> `nodes.that_are("entrypoint").all_have("authorization")``

The language's grammar is shown below:


```
<rule> 				::= (<statement>‘.’<logical_operator>)* <statement>
<statement> 		::= <initial_scope>‘.’(‘<scope_transformation>‘.’)* <property_check>
<initial_scope> 	::= (<nodes> | <edges>)
<nodes> 			::= the set of all nodes in the model
<edges> 			::= the set of all edges in the model

// all valid <logical_operator>, <scope_transformation>, and <property_check> are listed in the table below
```


As shown in the grammar, there are three groups of constructs, [*scope transformations*](#scope-transformations), [*property checks*](#property-checks), and [*logical operators*](logical-operators), presented in more detail below.
The full list of valid constructs is given in the table below these descriptions.


#### Scope Transformations (STs)
To define the set of nodes or edges to be checked in a query, STs allow the selection of nodes or edges based on their annotations. 
A scope in our approach is a set of nodes or edges in the model. 
The special constructs *nodes* and *edges* are scopes that contain all nodes/edges of the loaded model. 
They are used as the initial scope in the specification of queries. 
STs take a scope as input and return a subset of it as output, i.e., another scope. 
The selection is based on annotations of either the nodes themselves (e.g., all edges that have the annotation encrypted) or on annotations of other nodes that are connected via an edge (e.g., all nodes that have an edge going to any node with the annotation authentication).
For example, the ST that have(a) returns as output scope all nodes/edges from the input scope that have the annotation a.
Since annotations in the models express properties of the corresponding system components, selecting nodes/edges based on annotations corresponds to selecting system components with certain properties as dictated by the architectural rules.


#### Property Checks (PCs)
PCs realize the checking of properties on a set of nodes/edges with regard to an associated quantifier.
The quantifier is inherent to each PC and indicated by the PCs’ names. 
For example, the PC *all_have(a)* requires that all nodes or edges in the scope have the annotation a. 
Apart from the names of the constructs, the descriptions in the table below specify in detail, which quantifier is associated with each PC. 
PCs take a scope as input and return a binary verdict. 
For each node contained in the scope, it is checked whether it does or does not have the annotation given as argument to the construct. 
By matching the quantifier of the PC against the results from the individual checks, a verdict is determined. 
The language uses the quantifiers *all*, *exactly one*, *at least one*, and *none*. 
For example, the PC *at_least_one_has(a)* returns True, iff one or more of the nodes/edges in the input scope have the annotation a.


#### Logical Operators (LOs)
To allow the specification of complex queries that represent rich rules, the third group of constructs in our language structure is LOs. 
An LO combines two statements by applying the corresponding logical operation to the two verdicts as usual in Boolean algebra. 
The language includes the LOs AND and OR. 
These have shown to be sufficient for all rules on our list and no obvious uses for other LOs were seen.



| Group | Construct | Description |
| ----- | ----- | ----- |
| Scope transformations | that are(a) | Returns all items of the input scope that have the annotation a
| | that have(a) | Alias to that are(a)
| | sender is(a) | (only valid for edges) Returns all edges of the input scope where the sender has the annotation a
| | sender has(a) | (only valid for edges) Alias to sender is(a)
| | receiver is(a) | (only valid for edges) Returns all edges of the input scope where the receiver has the annotation a
| | receiver has(a) | (only valid for edges) Alias to receiver is(a)
| Property checks | all have(a) | True if all items in the input scope have the annotation a
| | all are(a) | Alias to all have(a)
| | at least one is(a) | True if at least one of the items in the input scope has the annotation a
| | at least one has(a) | Alias to at least one is(a)
| | exactly one is(a) | True if exactly one of the items in the input scope has the annotation a
| | exactly one has(a) | Alias to exactly one is(a)
| | none are(a) | True if none of the items in the input scope have the annotation a
| | none have(a) | Alias to none are(a)
| | all are connected to(a) | (only valid for nodes) True if all nodes in the input scope have an edge to at least one node with the annotation a
| | none are connected to(a) | (only valid for nodes) True if no node in the input scope has an edge to any node with the annotation a
| Logical operators | AND() | Logical *and*
| | OR() | Logical *or*