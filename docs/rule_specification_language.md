# Rule Specification Language

[work in progress]

This rule specification language is a core part of microCertiSec. 
It allows the formulation of architectural security rules that can then be automatically checked with our approach.

The language is designed to be simple and easily understandable, so that queries can be formulated with minimal domain knowledge and are intuitively interpretable.

#### Query structure
Architectural rules are expressed as *queries*. 
Queries are concatinations of multiple *constructs* and look for example like this:

> `nodes.that_are("entrypoint").all_have("authorization")``

The language's grammar is shown in the figure below:


<object data="https://github.com/tuhh-softsec/microCertiSec/tree/main/docs/grammar.pdf" type="application/pdf" width="700px" height="700px">
    <embed src="https://github.com/tuhh-softsec/microCertiSec/tree/main/docs/grammar.pdf">
        <p>This browser does not support PDFs. Please download the PDF to view it: <a href="https://github.com/tuhh-softsec/microCertiSec/tree/main/docs/grammar.pdf">Download PDF</a>.</p>
    </embed>
</object>



There are three groups of constructs, [*scope transformations*](#scope-transformations), [*property checks*](#property-checks), and [*logical operators*](logical-operators), presented in more detail below.


#### Scope Transformations



#### Property Checks



#### Logical Operators