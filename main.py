#!/usr/bin/env python
import os
import jinja2
import webapp2
from datetime import datetime
from models import TodoTask
import time

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")

    def post(self):
        dodatno = 'Your task was succesfully listed: '
        rezultat = self.request.get('vnos')
        tododate = datetime.strptime(self.request.get('tododate'), '%d/%m/%Y')

        # if not tododate:
        #     tododate = 'Not defined'

        taskdone = self.request.get('taskdone')

        if taskdone == '':
            taskdone = False
        else:
            taskdone = True


        task = TodoTask(vnos=rezultat, tododate=tododate, taskdone=taskdone)
        task.put()

        skupaj = dodatno + rezultat
        params = {'task': skupaj, 'tododate': tododate, 'taskdone': taskdone}
        return self.render_template('index.html', params=params)

class ListHandler(BaseHandler):
    def get(self):
        list = TodoTask.query(TodoTask.deleted == False).fetch()
        params = {'list': list}
        return self.render_template('todo_list.html', params=params)

class TaskHandler(BaseHandler):
    def get(self, task_id):
        task = TodoTask.get_by_id(int(task_id))
        params = {'task': task}
        return self.render_template('task.html', params=params)

class EditHandler(BaseHandler):
    def get(self, task_id):
        task = TodoTask.get_by_id(int(task_id))
        params = {'task': task}
        return self.render_template('edit_task.html', params=params)

    def post(self, task_id):
        vnos = self.request.get('vnos')
        tododate = datetime.strptime(self.request.get('tododate'), '%d/%m/%Y')
        taskdone = self.request.get('taskdone')

        if taskdone == '':
            taskdone = False
        else:
            taskdone = True

        task = TodoTask.get_by_id(int(task_id))

        task.vnos = vnos
        task.tododate = tododate
        task.taskdone = taskdone
        task.put()

        time.sleep(0.1)
        return self.redirect_to('todo_list')

class DeleteHandler(BaseHandler):
    def get(self, task_id):
        task = TodoTask.get_by_id(int(task_id))
        params = {'task': task}
        return self.render_template('delete_task.html', params=params)

    def post(self, task_id):
        task = TodoTask.get_by_id(int(task_id))
        task.deleted = True
        task.key.delete()
        time.sleep(0.1)
        return self.redirect_to("todo_list")


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/list', ListHandler),
    webapp2.Route('/task/<task_id:\d+>', TaskHandler),
    webapp2.Route('/task/<task_id:\d+>/edit', EditHandler),
    webapp2.Route('/task/<task_id:\d+>/delete', DeleteHandler),
    webapp2.Route('/list', ListHandler, name="todo_list"),
], debug=True)