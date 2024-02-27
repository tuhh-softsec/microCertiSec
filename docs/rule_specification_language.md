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





There are three groups of constructs, [*scope transformations*](#scope-transformations), [*property checks*](#property-checks), and [*logical operators*](logical-operators), presented in more detail below.


#### Scope Transformations



#### Property Checks



#### Logical Operators