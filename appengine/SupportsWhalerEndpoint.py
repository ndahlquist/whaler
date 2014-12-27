
import webapp2
import logging

from GitHubRepo import GitHubRepo


class SupportsWhalerEndpoint(webapp2.RequestHandler):
    """
    Returns "supported" if Whaler has collaborator access to this repo, or an error message if not.
    """

    def get(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')

        # Parse the repo name, owner and PR issue number from the referer URL.
        pull_request_url = self.request.headers['Referer']
        split_url = pull_request_url.split('/')
        owner_name = split_url[3]
        repo_name = split_url[4]
        logging.info("owner=%s, repo=%s" % (owner_name, repo_name))

        try:
            GitHubRepo(owner_name, repo_name)
            self.response.body = "supported"
        except:
            url = "https://github.com/%s/%s/settings/collaboration" % (owner_name, repo_name)
            self.response.body = "This repo does not support squash commits! " \
                                 "<a href=\"%s\">Add Whaler</a> as a collaborator." % url
