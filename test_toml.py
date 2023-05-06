import toml
import json

print(toml.load("file.toml"))

# Dump toml to dict
process_dict = toml.load("file.toml")

print(type(process_dict))

print(process_dict["name"])

with open('file.json', 'w') as fp:
    json.dump(process_dict, fp)
