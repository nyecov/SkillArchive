import os
import yaml
import glob

errors = []
files = glob.glob('skills/*/SKILL.md')
for f in files:
    with open(f, 'r', encoding='utf-8') as stream:
        try:
            parts = stream.read().split('---')
            if len(parts) < 3:
                continue
            data = yaml.safe_load(parts[1])
            if data and 'references' in data and isinstance(data['references'], list):
                for ref in data['references']:
                    if isinstance(ref, dict) and 'path' in ref:
                        path_val = ref['path']
                        p = os.path.normpath(os.path.join(os.path.dirname(f), path_val))
                        if not os.path.exists(p):
                            errors.append(f + ": Broken reference '" + path_val + "'")
        except Exception as e:
            errors.append(f + ": Error parsing YAML: " + str(e))

if len(errors) > 0:
    for err in errors:
        print(err)
else:
    print("No broken references found.")
