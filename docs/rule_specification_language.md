# Rule Specification Language

[work in progress]

This rule specification language is a core part of microCertiSec. 
It allows the formulation of architectural security rules that can then be automatically checked with our approach.

The language is designed to be simple and easily understandable, so that queries can be formulated with minimal domain knowledge and are intuitively interpretable.

#### Query structure
Architectural rules are expressed as *queries*. 
Queries are concatinations of multiple *constructs* and look for example like this:

> `nodes.that_are("entrypoint").all_have("authorization")``

There are three groups of constructs, [*scope transformations*](#scope-transformations), [*property checks*](#property-checks), and [*logical operators*](logical-operators), presented in more detail below.


#### Scope Transformations



#### Property Checks



#### Logical Operators