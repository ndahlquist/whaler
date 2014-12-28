
import webapp2
import logging

from google.appengine.api import memcache

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

        if has_access(owner_name, repo_name):
            self.response.body = "supported"
        else:
            url = "https://github.com/%s/%s/settings/collaboration" % (owner_name, repo_name)
            self.response.body = "This repo does not support squash commits! " \
                                 "<a href=\"%s\">Add Whaler</a> as a collaborator." % url


def has_access(owner_name, repo_name):
    memcache_key = "supports %s/%s" % (owner_name, repo_name)
    memcache_entry = memcache.get(key=memcache_key)
    if memcache_entry == 'true':
        return True
    if memcache_entry == 'false':
        return False

    try:
        GitHubRepo(owner_name, repo_name)
        memcache.add(key=memcache_key, value='true', time=60*60*24)
        return True
    except:
        # TODO: It will take up to 2 minutes for Whaler to 'see' new repos. This is hacky.
        memcache.add(key=memcache_key, value='false', time=2*60)
        return False
