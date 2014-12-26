
import webapp2
import logging

from FastForwardMerger import FastForwardMerger
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

        logging.info(merge_commit)