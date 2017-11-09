#!/usr/bin/python
import sys, getopt
import base64
from github import Github
from github import InputGitTreeElement


credential = '/home/achandra/.githubcredential'

class FileOper(object):
    def __init__(self, oper, file, msg, repo):
        self.oper = oper
        self.file = file
        
        self.repo = None
        self.cmt_msg = msg
        self.git = None
        self.getGitObject()
        for r in self.git.get_user().get_repos():
            if r.name == repo:
                self.repo = r
                

    def getGitObject(self):
        global credential
        usr = ''
        pas = ''
        fd = open(credential, 'r')
        lines = fd.readlines()
        for line in lines:
            if line.startswith('username'):
                usr = line.split(':')[1].strip()
            elif line.startswith('password'):
                pas = line.split(':')[1].strip()
            else:
                print 'Github Credentials not correct'
                self.git = None
        print 'user: \'%s\'' % usr, 'pass: \'%s\'' % pas
        self.git = Github(usr, pas)

    def file_contents(self):
        print 'getting contents of ', self.file
        repo = self.git.get_user().get_repo(self.file)
        contents = base64.b64decode(repo.get_contents(self.file).content)
        fd = open ('/tmp/dump', 'w')
        fd.write(contents)
        fd.close()

    def push_file(self):
        print 'getting repo for ', self.repo
        repo = self.git.get_user().get_repo(self.repo.name)

        #TBD: Following code is just to fine references
        for ref in repo.get_git_refs():
            print ref
            master_sha = ref.object.sha
            master_ref =  ref

        #master_ref = repo.get_git_ref('head')
        #print master_ref.object
        #master_sha = master_ref.object.sha
        base_tree = repo.get_git_tree(master_sha)
        with open(self.file, 'rb') as input_file:
            data = input_file.read()
        #data = base64.b64encode(data)

        element = InputGitTreeElement(self.file, '100644', 'blob', data)
        tree = repo.create_git_tree([element], base_tree)
        parent = repo.get_git_commit(master_sha)
        commit = repo.create_git_commit(self.cmt_msg, tree, [parent])
        master_ref.edit(commit.sha)





def usage():
    o = m = f = r = ''
    '''
    if len(sys.argv) != 2:
        print '2 arguments needed Got ', len(sys.argv)
        print 'test.py -o <operation> -f <filename>'
        return None, None
    '''

    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:f:m:r:",["oper=","file=","msg=", "repo="])
    except getopt.GetoptError:
        print 'test.py -o <operation> -f <filename>'
        return None, None

    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -o <operation> -f <file_name> -m <commit message> -r <repo>'
            return None, None, None, None
        elif opt in ("-o", "--oper"):
            o = arg
        elif opt in ("-f", "--file"):
            f = arg
        elif opt in ("-m", "--msg"):
            m = arg
        elif opt in ("-r", "--repo"):
            r = arg
        else:
            print 'Unknown argument ', arg

    return o, f, m, r

if __name__=='__main__':
    oper, file, msg, repo = usage()
    if oper == None or file == None:
        sys.exit(2)

    print 'operation name: ', oper
    print 'file name: ', file
    print 'commit message: ', msg
    print 'repo-name: ', repo
    fileopers = FileOper(oper, file, msg, repo)
    if fileopers == None or fileopers.git == None:
       sys.exit(2)

    for repo in fileopers.git.get_user().get_repos():
        print repo.full_name
        print repo.name

    fileopers.push_file()

    #if fileopers.oper == 'list':
    #    fileopers.file_contents()
