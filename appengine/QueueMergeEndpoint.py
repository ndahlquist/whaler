
import github
import webapp2
import logging
import datetime

from GitHubRepo import GitHubRepo


class QueueMergeEndpoint(webapp2.RequestHandler):
    """

    """

    def options(self):
        """
        xmlhttp first makes an HTTP OPTION request to negotiate access for POST.
        """
        self.response.headers.add_header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Access-Control-Allow-Origin')
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')

    def post(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')

        # Parse the repo name, owner and PR issue number from the referer URL.
        referer_url = self.request.headers['Referer']
        split_referer = referer_url.split('/')
        owner_name = split_referer[3]
        repo_name = split_referer[4]
        issue_number = int(split_referer[6])
        logging.info("owner=%s, repo=%s, issue=%s" % (owner_name, repo_name, issue_number))

        repo = GitHubRepo(owner_name, repo_name)

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

        squash_commit_message = "%s\n\nSquash commit created by Whaler." % self.request.get('commit_message')
        parents = [repo.repo.get_git_commit(pull.base.sha)]
        author = self.get_git_author(pull)
        committer = author  # TODO: Might be better if this is the person who presses the button.
        new_commit = repo.repo.create_git_commit(squash_commit_message, tree, parents, author, committer)

        branch_base = repo.repo.get_git_ref("heads/%s" % base)
        branch_base.edit(new_commit.sha)

    @staticmethod
    def get_git_author(pull_request):
        """
        :rtype: :class:`github.InputGitAuthor.InputGitAuthor`
        """
        user = pull_request.user
        time = None  # datetime.datetime.today().isoformat()
        return github.InputGitAuthor(user.name, user.email, time)
