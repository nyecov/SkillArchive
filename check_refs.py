import os
import yaml
import glob
import re

errors = []
files = glob.glob('skills/*/SKILL.md')
for f in files:
    with open(f, 'r', encoding='utf-8') as stream:
        try:
            content = stream.read()
            fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
            if not fm_match:
                continue
            data = yaml.safe_load(fm_match.group(1))
            if data and 'references' in data and isinstance(data['references'], list):
                for ref in data['references']:
                    if isinstance(ref, dict) and 'path' in ref:
                        path_val = ref['path']
                        p = os.path.normpath(os.path.join(os.path.dirname(f), path_val))
                        if not os.path.exists(p):
                            errors.append(f + ": Broken reference '" + path_val + "'")
        except yaml.YAMLError as e:
            errors.append(f + ": Error parsing YAML: " + str(e))

if len(errors) > 0:
    for err in errors:
        print(err)
else:
    print("No broken references found.")
