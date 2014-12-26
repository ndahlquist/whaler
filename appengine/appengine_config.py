"""This file is loaded when starting a new application instance."""

import vendor

# Add the libraries under ./lib to the classpath.
# This method is recommended by Google, according to http://stackoverflow.com/a/25564125/1567183.
vendor.add('lib')
