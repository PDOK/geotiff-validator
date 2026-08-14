import json
import yaml

def print_output(python_object, as_yaml, yaml_indent=2):
    if as_yaml:
        content = yaml.dump(python_object, indent=yaml_indent, sort_keys=False)
    else:
        content = json.dumps(python_object, indent=4, sort_keys=False)
    print(content)