'''
Print modules that own files given
'''

import subprocess
import json
import os
import sys

Run = subprocess.Popen(["pip", "list", "--not-required", "--format=json"], stdout=subprocess.PIPE)
Packages = {p['name'] for p in json.load(Run.stdout)}
Files = {}
Roots = set()

for p in Packages:
    Run = subprocess.Popen(["pip", "show", "-f", p], text=True, stdout=subprocess.PIPE)
    dofiles = None
    for line in Run.stdout:
        if line.startswith("Location: "):
            root = line.split()[1].strip()
            Roots.add(root)
        elif dofiles:
            if line.startswith("  "):
                Files[os.path.realpath(os.path.join(root, line.strip()))] = p
        else:
            dofiles = line.startswith("Files:")

if __name__ == "__main__" and len(sys.argv) > 1:
    Modules = {"setuptools", "wheel"}
    os.environ["PYTHONVERBOSE"] = "import"
    Run = subprocess.Popen(sys.argv[1:], stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, text=True)
    for line in Run.stderr:
        for r in Roots:
            if r in line and (idx := line.find(f"matches {r}")) > 0:
                s = line[idx + 8:].strip()
                if s in Files:
                    Modules.add(Files[s])

    print('requires = ["' + '", "'.join(sorted(Modules)) + '"]', file=sys.stderr)