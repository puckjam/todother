import tornado.web

class TodoModule(tornado.web.UIModule):
    def render(self, entry):
        return self.render_string("modules/todo.html", entry=entry)

