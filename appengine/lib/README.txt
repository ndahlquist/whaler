Appengine does not have a good way for downloading python modules, so I'm doing it this way:

PyGithub is downloaded as a git submodule under the ./submodule directory.
./github/ is a symlink to ./submodules/PyGithub/github/
