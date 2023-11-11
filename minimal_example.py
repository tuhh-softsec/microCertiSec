from core.load_model import load_model
import library_of_rules.rule_library as rules

model = load_model("./dfd.json", "./traceability.json")

# R01 imported from library of architectural security rules
query1 = rules.r01(model)
print(query1.full_evidence)

# R01 formulated directly in rule specification language
query2 = model.nodes.exactly_one_is("entrypoint")
print(query2.full_evidence)






