# provenance.py

import re
import sys
import time

from modules import git

verbose = False

# -------------------------------------------------------------------------------------------------

def run():
  start_time = time.time()
  all_revs()
  end_time = time.time()
  elapsed = end_time - start_time
  print "Elapsed time: %.2f" % elapsed

# -------------------------------------------------------------------------------------------------

# a list of hashes of trees or blobs that aren't ours, so we ignore them
thirdparty = set()

# list of trees we've seen (this will become a dictionary where the tree points to the
# memoized info about that tree)
trees = set()

# -------------------------------------------------------------------------------------------------

def all_revs():
  revs = git.rev_list(wd=path)
  for rev in revs:
    import_rev(rev)

# -------------------------------------------------------------------------------------------------

def list_rev(rev):
    print "checking", rev
    output = git.ls_tree(rev, recursive=True, wd=path)
    ls_pattern = re.compile('^(\d+)\s+(blob|tree|commit|tag)\s+([a-fA-F0-9]{40})\s+(-|\d+)\s+(.+)$')
    for line in output:
        match = re.search(ls_pattern, line)
        if not match:
            raise Exception('Can\'t parse line: %s' % line)
        mode = match.group(1)
        type = match.group(2)
        object = match.group(3)
        objsize = match.group(4)
        file = match.group(5)
        #print "%d\n    mode=%s\n    type=%s\n    object=%s\n    size=%s\n    path=%s\n" % (count, mode, type, object, objsize, file)
        count += 1

# -------------------------------------------------------------------------------------------------

def import_rev(rev):
    print "importing", rev
    commit = read_commit(rev)
    subtree = commit['tree']
    subtrees = [subtree]
    while subtrees:
        subtree = subtrees.pop(0)
        if subtree in thirdparty:
          print '    thirdparty', subtree
          continue
        if subtree in trees:
          print '    already seen', subtree
          continue
        print '    ' + subtree
        trees.add(subtree)
        output = git.cat_file(subtree, wd=path)
        #for line in output:
        #  print line

# -------------------------------------------------------------------------------------------------

def read_commit(rev):
    obj = git.cat_file(rev, wd=path)
    commit = {}
    commit['parent'] = []
    inCommitMsg = False
    for line in obj:
        if inCommitMsg:
          commit['message'].append(line)
          continue
        if not line:
          inCommitMsg = True
          commit['message'] = []
          continue
        match = re.search("^(tree|parent|author|committer) (.+)$", line)
        if not match:
          raise Exception('Line in commit record is odd: %s' % line)
        if match.group(1) not in commit:
          commit[match.group(1)] = []
        commit[match.group(1)].append(match.group(2))

    if len(commit['tree']) == 0:
        commit['tree'] = None
    elif len(commit['tree']) == 1:
        commit['tree'] = commit['tree'][0]
    else:
        raise Exception('Malformed commit in %s' % rev)

    if verbose:
      if len(commit['parent']) > 1:
          print '    merge commit'
          for h in commit['parent']:
              print '        parent', h

    return commit

# -------------------------------------------------------------------------------------------------

path = sys.argv[1]
run()
