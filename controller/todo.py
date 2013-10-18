import os
import sys
import logging

import tornado.web
import tornado.escape

from controller.base import *
from module.services import randId

class TodoListHandler(BaseHandler):
	def get(self):
		entries = self.db.query("SELECT * FROM todo ORDER BY todo_created_date ")
		if not entries:
			self.redirect("/todo_compose")
			return
		self.render("todo_list.html", entries=entries,title="My Todo")

class TodoHandler(BaseHandler):
	def get(self, slug):
		entry = self.db.get("SELECT * FROM todo WHERE todo_slug = %s", slug)
		if not entry: raise tornado.web.HTTPError(404)
		self.render("todo.html", entry=entry)


class TodoComposeHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		id = self.get_argument("id", None)
		entry = None
		if id:
			entry = self.db.get("SELECT * FROM todo WHERE todo_id = %s", int(id))
		self.render("todo_compose.html", entry=entry)
    
	@tornado.web.authenticated
	def post(self):
		id = self.get_argument("id", None)
		do = self.get_argument("do")
		what = self.get_argument("what")
		where = self.get_argument("where")
		when = self.get_argument("when")
		if id:
			entry = self.db.get("SELECT * FROM todo WHERE todo_id = %s", int(id))
			if not entry: raise tornado.web.HTTPError(404)
			slug = entry.todo_slug
			self.db.execute(
				"UPDATE todo SET todo_do = %s, todo_what = %s, todo_where = %s, todo_when = %s, todo_updated_date=UTC_TIMESTAMP()"
				"WHERE todo_id = %s", do, what, where, when, int(id))
		else:
			slug = '11001100%.4d' % randId.new_id()
			if not slug: slug = "todo"
            
			self.db.execute(
				"INSERT INTO todo (todo_user_id,todo_do,todo_what,todo_where,todo_when,todo_slug,todo_created_date,todo_updated_date)"
				"VALUES (%s,%s,%s,%s,%s,%s,UTC_TIMESTAMP(),UTC_TIMESTAMP())",
				self.current_user.user_id, do, what, where, when,slug)
		self.redirect("/todo/" + slug)

