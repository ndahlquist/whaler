import logging
import json
import webapp2
from credentials_dev import GITHUB_APP_CLIENT_ID, BASE_URL

from datamodel import UserEntry

from GitHubRepo import GitHubRepo


class PreMergeEndpoint(webapp2.RequestHandler):
    """
    Returns a json with the following optional fields:

    'interstitial_url' field:
        A URL that the client should redirect to on pressing the "squash merge" button.
        This may include the URL to authorize the GitHub application,
        a URL to update the chrome extension,
        or any URL we may need in the future.
        Not present if the user does not need an interstitial.

    'commit_message' field:
        A default commit message for the current pull request.
        Not present if the user's authentication failed.
    """

    def get(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')

        username = self.request.get('username')
        redirect = self.request.get('redirect')
        session_token = self.request.get('session_token')

        user_entry = UserEntry.lookup(username, session_token)

        json_response_object = {}
        if user_entry is None:
            logging.info('Requesting new oauth token.')
            interstitial_url = 'https://github.com/login/oauth/authorize?' + \
                               'client_id=%s&' % GITHUB_APP_CLIENT_ID + \
                               'redirect_uri=%s/oauth_callback/%s' % (BASE_URL, username) + \
                               '&scope=public_repo,repo,write:repo_hook' + \
                               '&state=%s+%s' % (redirect, session_token)
            json_response_object['interstitial_url'] = interstitial_url
        else:
            json_response_object['commit_message'] = self.get_commit_message(user_entry)

        self.response.text = unicode(json.dumps(json_response_object))

    def get_commit_message(self, user_entry):

        # Parse the repo name, owner and PR issue number from the referrer URL.
        pull_request_url = self.request.headers['Referer']
        split_url = pull_request_url.split('/')
        owner_name = split_url[3]
        repo_name = split_url[4]
        issue_number = int(split_url[6])
        logging.info("owner=%s, repo=%s, issue=%s" % (owner_name, repo_name, issue_number))

        repo = GitHubRepo(user_entry.oauth_token, owner_name, repo_name)

        pull = repo.repo.get_pull(issue_number)

        message = ''

        for commit in pull.get_commits():
            git_commit = commit.commit
            message += git_commit.message
            message += '\n'
        return message