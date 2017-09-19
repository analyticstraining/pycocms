from BaseHandler import BaseHandler

class UnauthorizedHandler(BaseHandler):
  def get(self):
    self.render_template('unauthorized.html')

