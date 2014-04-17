# provenance.py

import sys
from modules import git

path = sys.argv[1]

# Some tests
obj = git.ls_tree('HEAD', recursive=True, wd=path)
for line in obj:
    print line

obj = git.nonbinary('HEAD', wd=path)
for line in obj:
    print line
