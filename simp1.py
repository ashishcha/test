from github import Github

g = Github("ashishcha", "hsihsa@17")

for repo in g.get_user().get_repos():
    print repo.full_name


repo = g.get_user().get_repo("Hello-World")
file =  repo.get_file_contents("gcd.c")

'Ashish Chandra next commit'
