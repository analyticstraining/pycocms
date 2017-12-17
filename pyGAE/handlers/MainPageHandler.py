import logging
from BaseHandler import BaseHandler

class MainPageHandler(BaseHandler):
  def get(self):
    self.redirect(self.uri_for('viewContent'), abort=True)
