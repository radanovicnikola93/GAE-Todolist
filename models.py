from google.appengine.ext import ndb

class TodoTask(ndb.Model):
    vnos = ndb.StringProperty()
    entrymade = ndb.DateTimeProperty(auto_now_add=True)
    tododate = ndb.DateProperty()
    taskdone = ndb.BooleanProperty()
    deleted = ndb.BooleanProperty(default=False)