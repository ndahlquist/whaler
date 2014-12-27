Whaler
======

If your Git workflow involves squash merges, you're probably frustrated that the GitHub merge button creates ugly --no-ff commits. Whaler is a Chrome extension and server-side component that work together with the GitHub API to create beautiful squash commits right from the GitHub web interface.

### Quickstart
1. [Install](https://chrome.google.com/webstore/detail/whaler/kjfaikbmbbkbnjjeiambmjchclpfkedf) the Chrome extension.
2. Give the GitHub user [cicitheandroidtester](https://github.com/cicitheandroidtester) push rights to your repository (this access is used to create the squash commits).

You're done! You should see a blue "Squash merge" button in place of the regular "Merge pull request" button.

### Under the hood
The chrome extension injects a minimal amount of HTML and Javascript which change a few visual elements and redirect the merge button's HTTP POST to our webservice. This webservice calls through to the GitHub API, performing the following operations:
  - The pull request's `base` branch is merged into its `head`.
  - A squash commit, parented by `base`, is created with the tree from the new merge commit. The commit message includes any text entered through the GitHub web interface and a link to the pull request.
  - `base` is advanced to the new commit.
  - A comment is posted on the pull request with the SHA of the squash commit.
  - The pull request is closed and `head` is deleted.

