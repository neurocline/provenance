# Gutter-level git for simple tools
# replace with real Git library like GitPython (perhaps)
# The actual answer is that a high-performance version will just reach directly inside
# the git repository.
# This has almost no error handling.

import subprocess

verbose = True

# -------------------------------------------------------------------------------------------------

# Support subset of git-ls-tree
#   -r for recursive
#   rev is optional
#   path is optional
def ls_tree(rev=None, path=None, recursive=False, wd=None):
    cmd = ['git', 'ls-tree', '-l']
    if recursive:
        cmd.append('-r')
        cmd.append('-t')
    if rev:
        cmd.append(rev)
    if path:
        cmd.append(path)
    return execute(cmd, wd)

# -------------------------------------------------------------------------------------------------

# Support subset of git-rev-list
# We pick topo-order because that seems to be the "best" output
def rev_list(wd=None):
    cmd = ['git', 'rev-list', '--all', '--topo-order', '--reverse']
    return execute(cmd, wd)

# -------------------------------------------------------------------------------------------------

# Support subset of git-cat-file
def cat_file(object, wd=None):
    cmd = ['git', 'cat-file', '-p', object]
    return execute(cmd, wd)

# -------------------------------------------------------------------------------------------------

# Return list of non-binary files in rev
def nonbinary(rev=None, wd=None):
    cmd = ['git', 'grep', '-I', '--name-only', '-e', '']
    if rev:
        cmd.append(rev)
    return execute(cmd, wd)

# -------------------------------------------------------------------------------------------------

# Do git blame
def blame(rev=None, file=None, wd=None):
    cmd = ['git', 'blame']
    if rev:
        cmd.append(rev)
    cmd.append(path)
    return execute(cmd, wd)

# -------------------------------------------------------------------------------------------------

# Do git log. Allowed keywords are:
#     author, format, numstat, patch, rev, shortstat, no_merges, wd
def log(wd=None, **kwargs):
    cmd = ['git', 'log', '--reverse', '--use-mailmap']
    if 'author' in kwargs:
        cmd.append('--author')
        cmd.append(kwargs['author'])
    if 'format' in kwargs:
        cmd.append('--pretty=format:%s' % kwargs['format'])
    if 'no_merges' in kwargs:
        cmd.append('--no-merges')
    if 'numstat' in kwargs:
        cmd.append('--numstat')
    if 'patch' in kwargs:
        cmd.append('--patch')
    if 'shortstat' in kwargs:
        cmd.append('--shortstat')

    if 'rev' in kwargs:
        cmd.append(rev)

    return execute(cmd, wd)

# -------------------------------------------------------------------------------------------------

# Run a git command and return its output
def execute(cmd, wd):
    if wd is None:
        wd = '.'
    log = []
    if verbose:
        print cmd
    cmd = subprocess.Popen(cmd, stdout=subprocess.PIPE, cwd=wd)
    for line in cmd.stdout:
        log.append(line.rstrip('\n'))
    cmd.wait
    return log
