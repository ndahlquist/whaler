'''from google.appengine.ext import db


class CircleBuild(db.Model):
    """
    Represents a single Circle CI build.
    """
    timestamp = db.DateTimeProperty(auto_now_add=True)
    org_name = db.StringProperty()
    repo_name = db.StringProperty()
    branch = db.StringProperty()
    build_num = db.IntegerProperty()
    build_millis = db.IntegerProperty()
    outcome = db.StringProperty()'''
