import github

GITHUB_USERNAME = 'cicitheandroidtester'
GITHUB_PASSWORD = 'b72b1311b70a4d0ef4a590d03c24e5305ea31baf'


class GitHubRepo():

    def __init__(self, repo_owner, repo_name):
        self.git = github.Github(GITHUB_USERNAME, GITHUB_PASSWORD)
        self.repo_owner = repo_owner
        self.repo_name = repo_name

        self.user = self.git.get_user()

        try:
            self.repo = self.git.get_repo("%s/%s" % (repo_owner, repo_name))
        except:
            pass  # Repo not found.

        if self.repo:
            # This is a repo owned by a user. Sweet.
            return

        org = self.get_org(self.user, repo_owner)
        self.repo = self.get_repo(org, repo_name)
        if self.repo:
            # This is a repo owned by an organization.
            return

        raise Exception("Could not find repo %s/%s." % (repo_owner, repo_name))

    @staticmethod
    def get_org(user, org_name):
        for org in user.get_orgs():
            if org.name == org_name:
                return org

    @staticmethod
    def get_repo(org, repo_name):
        for repo in org.get_repos():
            if repo.name == repo_name:
                return repo
