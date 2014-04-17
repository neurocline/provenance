# Gutter-level git for simple tools
# replace with real Git library like GitPython

import subprocess

# -------------------------------------------------------------------------------------------------

# Support subset of git-ls-tree
#   -r for recursive
#   rev is optional
#   path is optional
def ls_tree(rev=None, path=None, recursive=False, wd=None):
    cmd = ['git', 'ls-tree']
    if recursive: cmd.append('-r')
    if rev: cmd.append(rev)
    if path: cmd.append(path)
    return execute(cmd, wd)

# -------------------------------------------------------------------------------------------------

# Return list of non-binary files in rev
def nonbinary(rev=None, wd=None):
    cmd = ['git', 'grep', '-I', '--name-only', '-e', '']
    if rev: cmd.append(rev)
    return execute(cmd, wd)

# -------------------------------------------------------------------------------------------------

# Run a git command and return its output
def execute(cmd, wd):
    if wd is None: wd = '.'
    log = []
    print cmd
    cmd = subprocess.Popen(cmd, stdout=subprocess.PIPE, cwd=wd)
    for line in cmd.stdout:
        log.append(line.rstrip('\n'))
    cmd.wait
    return log
