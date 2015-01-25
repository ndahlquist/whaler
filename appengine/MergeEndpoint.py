import github
import webapp2
import logging

from GitHubRepo import GitHubRepo
from datamodel import OauthEntry


class MergeEndpoint(webapp2.RequestHandler):
    MERGE_MESSAGE = "Squash merge commit %s created by " + \
                    "[Whaler](https://chrome.google.com/webstore/detail/whaler/kjfaikbmbbkbnjjeiambmjchclpfkedf). " + \
                    ":whale:"

    def options(self):
        """
        xmlhttp first makes an HTTP OPTION request to negotiate access for POST.
        """
        self.response.headers.add_header('Access-Control-Allow-Headers',
                                         'Origin, X-Requested-With, Content-Type, Accept, Access-Control-Allow-Origin')
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')

    def post(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')

        username = self.request.get('username')
        session_token = self.request.get('session_token')
        oauth_entry = OauthEntry.lookup(username, session_token)
        assert oauth_entry is not None
        oauth_token = oauth_entry.access_token

        # Parse the repo name, owner and PR issue number from the referer URL.
        pull_request_url = self.request.headers['Referer']
        split_url = pull_request_url.split('/')
        owner_name = split_url[3]
        repo_name = split_url[4]
        issue_number = int(split_url[6])
        logging.info("owner=%s, repo=%s, issue=%s" % (owner_name, repo_name, issue_number))

        repo = GitHubRepo(oauth_token, owner_name, repo_name)

        pull = repo.repo.get_pull(issue_number)
        head = pull.head.ref
        base = pull.base.ref

        # Merge base into head
        merge_commit = repo.repo.merge(head, base)

        if merge_commit:
            # TODO: Wait for CI build to pass (use git hook)
            tree = merge_commit.commit.tree
        else:
            head_commit = repo.repo.get_commit(pull.head.sha)
            tree = head_commit.commit.tree

        squash_commit_message = "%s\n" % self.request.get('commit_message') + \
                                "\n" \
                                "---\n" \
                                "Squash commit from %s created by Whaler." % pull_request_url
        base_branch = repo.repo.get_git_ref("heads/%s" % base)
        parents = [repo.repo.get_git_commit(base_branch.object.sha)]
        author = self.get_author(pull)
        committer = self.get_committer(repo)
        new_commit = repo.repo.create_git_commit(squash_commit_message, tree, parents, author, committer)

        base_branch.edit(new_commit.sha)

        pull.create_issue_comment(self.MERGE_MESSAGE % new_commit.sha)
        pull.edit(state='closed')

        # Delete the merged branch.
        head_branch = repo.repo.get_git_ref("heads/%s" % head)
        head_branch.delete()

    def get_committer(self, repo):
        """
        :rtype: :class:`github.InputGitAuthor.InputGitAuthor`
        """
        user = repo.user
        return self.create_git_author(user)

    def get_author(self, pull_request):
        """
        :rtype: :class:`github.InputGitAuthor.InputGitAuthor`
        """
        user = pull_request.user
        return self.create_git_author(user)

    @staticmethod
    def create_git_author(named_user):
        """
        :param named_user: :class:`github.NamedUser.NamedUser`
        :rtype: :class:`github.InputGitAuthor.InputGitAuthor`
        """
        user_name = named_user.login
        display_name = named_user.name
        email = named_user.email

        assert user_name
        if not display_name:
            display_name = user_name
        if not email:
            email = user_name + "@users.noreply.github.com"

        return github.InputGitAuthor(display_name, email)
