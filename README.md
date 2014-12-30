Whaler
======

If your Git workflow involves squash merges, you're probably frustrated that the GitHub merge button creates ugly --no-ff commits. Whaler is a Chrome extension and server-side component that work together with the GitHub API to create beautiful squash commits right from the GitHub web interface.

### Quickstart
[Install](https://chrome.google.com/webstore/detail/whaler/kjfaikbmbbkbnjjeiambmjchclpfkedf) the Chrome extension.

You should see a blue "Squash merge" button in place of the regular "Merge pull request" button.

![Screenshot](https://lh6.googleusercontent.com/PHxlDNaEO5HtcUnz9JCDw22oytCxV6voFmlpZKLFjlx1u-ELtjj9kbp4egzCkjQpDx-EEUMGEw=s1280-h800-e365-rw)

### Under the hood
The chrome extension injects a minimal amount of HTML and Javascript which change a few visual elements and redirect the merge button's HTTP POST to our webservice. This webservice calls through to the GitHub API, performing the following operations:
  - The pull request's `base` branch is merged into its `head` branch.
  - A squash commit, parented by `base`, is created with the tree from the new merge commit. The commit message includes any text entered through the GitHub web interface and a link to the pull request.
  - `base` is advanced to the new commit.
  - A comment is posted on the pull request with the SHA of the squash commit.
  - The pull request is closed and `head` is deleted.

